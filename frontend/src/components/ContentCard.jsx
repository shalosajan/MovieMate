import React from "react";

export default function ContentCard({ item, onClick }) {
  return (
    <div
      onClick={() => onClick?.(item)}
      className="bg-gray-800 p-3 rounded shadow cursor-pointer hover:scale-105 transition"
    >
      {item.poster_path ? (
        <img
          src={item.poster_path}
          alt={item.title || item.name}
          className="w-full h-48 object-cover rounded"
        />
      ) : (
        <div className="h-48 bg-gray-700 flex items-center justify-center">
          No Image
        </div>
      )}

      <h3 className="mt-2 text-sm font-semibold">
        {item.title || item.name}
      </h3>

      {item.type && (
        <div className="text-xs text-gray-400">
          {item.type}
        </div>
      )}
    </div>
  );
}
