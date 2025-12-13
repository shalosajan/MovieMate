// DetailsModal.jsx
import React, { useEffect, useState } from "react";
import Modal from "./Modal";
import { getMovieDetails, getTVDetails } from "../api/tmdbProxy";

export default function DetailsModal({ item, open, onClose }) {
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!open || !item) return;

    setLoading(true);
    setDetails(null); // reset every time modal opens

    const fetchDetails = async () => {
      try {
        const data =
          item.media_type === "tv"
            ? await getTVDetails(item.id)
            : await getMovieDetails(item.id);

        setDetails(data);
      } catch (err) {
        console.error("Failed to load details", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDetails();
  }, [open, item]);

  // ⛔ DO NOT BLOCK MODAL RENDER
  return (
    <Modal open={open} onClose={onClose}>
      {loading && (
        <p className="text-gray-400 text-center">
          Loading details...
        </p>
      )}

      {!loading && details && (
        <div className="flex gap-6">
          <img
            className="w-40 rounded"
            src={
              details.poster_path
                ? `https://image.tmdb.org/t/p/w300${details.poster_path}`
                : ""
            }
            alt={details.title || details.name}
          />

          <div>
            <h2 className="text-2xl font-bold mb-2">
              {details.title || details.name}
            </h2>

            <p className="text-sm text-gray-400 mb-2">
              ⭐ {details.vote_average?.toFixed(1)}
            </p>

            <p className="text-gray-300 text-sm">
              {details.overview}
            </p>
          </div>
        </div>
      )}
    </Modal>
  );
}


