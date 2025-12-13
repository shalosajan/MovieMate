import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { getMovieDetails, getTVDetails } from "../api/tmdbProxy";
import {
  getContentByTMDB,
  importFromTMDB,
  markMovieWatched,
  getContentSeasons,
  markSeasonWatched,
  toggleEpisode,
} from "../api/catalog";

export default function Watch() {
  const { type, id: tmdbId } = useParams();

  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(true);

  // backend content
  const [contentId, setContentId] = useState(null);

  // movie
  const [movieStatus, setMovieStatus] = useState("unwatched");

  // tv
  const [backendSeasons, setBackendSeasons] = useState([]);
  const [watchedSeasons, setWatchedSeasons] = useState([]);
  const [watchedEpisodes, setWatchedEpisodes] = useState([]);

  /* ================= LOAD TMDB DETAILS ================= */

  useEffect(() => {
    const loadTMDB = async () => {
      try {
        const data =
          type === "tv"
            ? await getTVDetails(tmdbId)
            : await getMovieDetails(tmdbId);
        setDetails(data);
      } catch (e) {
        console.error("Failed to load TMDB content", e);
      } finally {
        setLoading(false);
      }
    };
    loadTMDB();
  }, [type, tmdbId]);

  /* ================= ENSURE BACKEND CONTENT ================= */

  useEffect(() => {
    if (!details) return;

    const ensureContent = async () => {
      try {
        // 1️⃣ try fetching
        let content = await getContentByTMDB(tmdbId);

        // 2️⃣ auto-import if missing
        if (!content) {
          if (!contentId) {
          await importFromTMDB(tmdbId);
           }
          content = await getContentByTMDB(tmdbId);
        }

        setContentId(content.id);

        if (content.status === "completed") {
          setMovieStatus("completed");
        }
      } catch (err) {
        console.error("Failed to sync backend content", err);
      }
    };

    ensureContent();
  }, [details, tmdbId]);

  /* ================= LOAD BACKEND SEASONS ================= */

  useEffect(() => {
    if (!contentId || type !== "tv") return;

    getContentSeasons(contentId)
      .then((data) => {
        setBackendSeasons(data);
        setWatchedSeasons(
          data
            .filter(
              s =>
                s.episodes?.length &&
                s.episodes.every(e => e.watched)
            )
            .map(s => s.season_number)
        );
      })
      .catch(() => {});
  }, [contentId, type]);

  /* ================= STATES ================= */

  if (loading || !details) {
    return (
      <div className="p-10 text-center text-gray-400">
        Loading content...
      </div>
    );
  }

  /* ===================================================== */

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      <div className="flex gap-8">
        <img
          className="w-64 rounded"
          src={
            details.poster_path
              ? `https://image.tmdb.org/t/p/w500${details.poster_path}`
              : ""
          }
          alt={details.title || details.name}
        />

        <div className="flex-1">
          <h1 className="text-3xl font-bold mb-3">
            {details.title || details.name}
          </h1>

          <p className="text-gray-400 mb-2">
            ⭐ {details.vote_average?.toFixed(1)}
          </p>

          <p className="text-gray-300 mb-6">
            {details.overview}
          </p>

          {/* ================= MOVIE ================= */}

          {type === "movie" && contentId && (
            <button
              onClick={async () => {
                setMovieStatus("completed");
                try {
                  await markMovieWatched(contentId);
                } catch {
                  setMovieStatus("unwatched");
                }
              }}
              className={`px-4 py-2 rounded ${
                movieStatus === "completed"
                  ? "bg-green-600"
                  : "bg-indigo-600 hover:bg-indigo-700"
              }`}
            >
              {movieStatus === "completed"
                ? "Watched ✓"
                : "Mark as watched"}
            </button>
          )}

          {/* ================= TV ================= */}

          {type === "tv" && contentId && (
            <div className="mt-8">
              <h3 className="text-xl font-semibold mb-4">
                Seasons
              </h3>

              {details.seasons
                ?.filter(s => s.season_number !== 0)
                .map((season) => {
                  const isSeasonWatched =
                    watchedSeasons.includes(season.season_number);

                  return (
                    <div
                      key={season.season_number}
                      className="border border-gray-700 rounded p-4 mb-4"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="font-medium">
                          Season {season.season_number}
                        </h4>

                        <button
                          onClick={async () => {
                            setWatchedSeasons(prev => [
                              ...prev,
                              season.season_number,
                            ]);
                            try {
                              await markSeasonWatched(
                                contentId,
                                season.season_number
                              );
                            } catch {
                              setWatchedSeasons(prev =>
                                prev.filter(
                                  n => n !== season.season_number
                                )
                              );
                            }
                          }}
                          className={`text-sm px-3 py-1 rounded ${
                            isSeasonWatched
                              ? "bg-green-600"
                              : "bg-indigo-600 hover:bg-indigo-700"
                          }`}
                        >
                          {isSeasonWatched
                            ? "Watched ✓"
                            : "Mark season watched"}
                        </button>
                      </div>

                      {season.episode_count && (
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                          {Array.from(
                            { length: season.episode_count },
                            (_, i) => i + 1
                          ).map((epNum) => {
                            const key = `${season.season_number}-${epNum}`;
                            const watched = watchedEpisodes.includes(key);

                            return (
                              <button
                                key={epNum}
                                onClick={async () => {
                                  setWatchedEpisodes(prev => [...prev, key]);
                                  try {
                                    await toggleEpisode(
                                      contentId,
                                      season.season_number,
                                      epNum
                                    );
                                  } catch {
                                    setWatchedEpisodes(prev =>
                                      prev.filter(k => k !== key)
                                    );
                                  }
                                }}
                                className={`text-xs px-2 py-1 rounded ${
                                  watched
                                    ? "bg-green-700"
                                    : "bg-gray-700 hover:bg-gray-600"
                                }`}
                              >
                                Ep {epNum}
                              </button>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  );
                })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
