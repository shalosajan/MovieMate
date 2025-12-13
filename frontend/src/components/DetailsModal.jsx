// DetailsModal.jsx
import React, { useEffect, useState } from "react";
import Modal from "./Modal";
import { getMovieDetails, getTVDetails } from "../api/tmdbProxy";
import { addToWishlist } from "../api/wishlist";
import { useNavigate } from "react-router-dom";
import { importFromTMDB } from "../api/catalog";



export default function DetailsModal({ item, open, onClose }) {
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem("access_token");

  const handleWishlist = async () => {
    if (!isAuthenticated) {
      navigate("/login");
      return;
    }

    try {
      await addToWishlist({
        ...details,
        media_type: item.media_type,
      });
      alert("Added to wishlist ❤️");
    } catch {
      alert("Already in wishlist");
    }
  };


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

            
            <button
              onClick={handleWishlist}
              className="mt-4 px-4 py-2 bg-red-600 hover:bg-red-700 rounded"
            >
              ❤️ Add to Wishlist
            </button>
           
<button
  onClick={async () => {
    try {
      // 🔥 AUTO IMPORT
      await importFromTMDB(item.id);

      // ➜ Go to watch page
      navigate(`/watch/${item.media_type}/${item.id}`);
      onClose();
    } catch (err) {
      console.error("Import failed", err);
      alert("Failed to import title");
    }
  }}
  className="mt-4 px-4 py-2 bg-indigo-600 rounded hover:bg-indigo-700"
>
  Watch Now
</button>


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