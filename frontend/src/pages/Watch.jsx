import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  getMovieDetails,
  getTVDetails,
} from "../api/tmdbProxy";
import { markMovieWatched, markSeasonWatched } from "../api/catalog";

export default function Watch() {
  const { type, id } = useParams();
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [movieStatus, setMovieStatus] = useState("unwatched");
  const [watchedSeasons, setWatchedSeasons] = useState([]);
  const [backendSeasons, setBackendSeasons] = useState([]);

  useEffect(() => {
    const load = async () => {
      try {
        const data =
          type === "tv"
            ? await getTVDetails(id)
            : await getMovieDetails(id);
        setDetails(data);
      } catch (e) {
        console.error("Failed to load content", e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [type, id]);

  useEffect(() => {
  if (type === "movie") {
    setMovieStatus("unwatched"); // reset when navigating
  }
}, [type, id]);

useEffect(() => {
  if (type !== "tv") return;

  getContentSeasons(id)
    .then(setBackendSeasons)
    .catch(() => {});
}, [type, id]);

  if (loading) {
    return (
      <div className="p-10 text-center text-gray-400">
        Loading content...
      </div>
    );
  }

  if (!details) {
    return (
      <div className="p-10 text-center text-red-400">
        Content not found
      </div>
    );
  }

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

        <div>
          <h1 className="text-3xl font-bold mb-3">
            {details.title || details.name}
          </h1>

          <p className="text-gray-400 mb-2">
            ⭐ {details.vote_average?.toFixed(1)}
          </p>

          <p className="text-gray-300 mb-6">
            {details.overview}
          </p>
 {type === "movie" && (
  <button
onClick={async () => {
  setMovieStatus("completed"); // 👈 immediate UI change
  try {
    await markMovieWatched(details.id);
  } catch {
    setMovieStatus("unwatched"); // rollback on failure
  }
}}
    disabled={movieStatus === "completed"}
    className={`mt-4 px-4 py-2 rounded ${
      movieStatus === "completed"
        ? "bg-green-600 cursor-default"
        : "bg-indigo-600 hover:bg-indigo-700"
    }`}
  >
    {movieStatus === "completed" ? "Watched ✓" : "Mark as watched"}
  </button>
)}


{type === "tv" && (
  <div className="mt-6">
    <h3 className="text-lg font-semibold mb-3">Seasons</h3>

    {details.seasons
      ?.filter(s => s.season_number !== 0) // 🚫 ignore specials
      .map((tmdbSeason) => {
        const backendSeason = backendSeasons.find(
          s => s.season_number === tmdbSeason.season_number
        );

        if (!backendSeason) return null;

        const watched = watchedSeasons.includes(backendSeason.id);

        return (
          <div
            key={tmdbSeason.season_number}
            className="border border-gray-700 rounded p-3 mb-3"
          >
            <div className="flex items-center justify-between">
              <h4 className="font-medium">
                Season {tmdbSeason.season_number}
              </h4>

              <button
                onClick={async () => {
                  await markSeasonWatched(backendSeason.id);
                  setWatchedSeasons(prev => [...prev, backendSeason.id]);
                }}
                className={`text-sm px-3 py-1 rounded ${
                  watched
                    ? "bg-green-600"
                    : "bg-indigo-600 hover:bg-indigo-700"
                }`}
              >
                {watched ? "Watched ✓" : "Mark season watched"}
              </button>
            </div>
          </div>
        );
      })}
  </div>
)}



          {/* Placeholder for Phase 2 */}
          <div className="border-t border-gray-700 pt-4">
            <p className="text-sm text-gray-500">
              Progress tracking coming next
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
