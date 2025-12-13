import React, { useEffect, useState } from "react";
import { getWishlist, removeFromWishlist } from "../api/wishlist";
import DetailsModal from "../components/DetailsModal";

export default function Wishlist() {
  const [items, setItems] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);

  useEffect(() => {
    getWishlist().then(setItems);
  }, []);

  const removeItem = async (tmdb_id) => {
    await removeFromWishlist(tmdb_id);
    setItems(items.filter(i => i.tmdb_id !== tmdb_id));
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">
        My Wishlist
      </h1>

      {items.length === 0 && (
        <p className="text-gray-400">
          Your wishlist is empty.
        </p>
      )}

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {items.map(item => (
          <div
            key={item.id}
            className="bg-gray-800 rounded p-3 cursor-pointer"
            onClick={() =>
              setSelectedItem({
                id: item.tmdb_id,
                media_type: item.media_type,
                title: item.title,
                poster_path: item.poster_path
              })
            }
          >
            {item.poster_path && (
              <img
                src={`https://image.tmdb.org/t/p/w300${item.poster_path}`}
                className="rounded mb-2"
              />
            )}

            <h3 className="text-sm font-semibold">
              {item.title}
            </h3>

            <button
              onClick={(e) => {
                e.stopPropagation();
                removeItem(item.tmdb_id);
              }}
              className="text-red-500 text-xs mt-2"
            >
              Remove
            </button>
          </div>
        ))}
      </div>

      <DetailsModal
        item={selectedItem}
        open={!!selectedItem}
        onClose={() => setSelectedItem(null)}
      />
    </div>
  );
}
