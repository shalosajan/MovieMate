import React from "react";

export default function MovieCard({ item, onClick }) {
  return (
    <div
      onClick={() => onClick?.(item)}
      className="min-w-[150px] cursor-pointer hover:scale-105 transition-transform"
    >
      <img
        src={
          item.poster_path
            ? `https://image.tmdb.org/t/p/w300${item.poster_path}`
            : "/placeholder.png"
        }
        alt={item.title || item.name}
        className="rounded-lg"
      />
      <div className="mt-2 text-sm">
        <p className="font-semibold truncate">
          {item.title || item.name}
        </p>
        <p className="text-gray-400">
          ⭐ {item.vote_average?.toFixed(1)}
        </p>
      </div>
    </div>
  );
}
