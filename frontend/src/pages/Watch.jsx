import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  getMovieDetails,
  getTVDetails,
} from "../api/tmdbProxy";

export default function Watch() {
  const { type, id } = useParams();
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(true);

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
