import React from "react";
import MovieCard from "./MovieCard";

export default function Carousel({ title, items, onItemClick }) {
  if (!items?.length) return null;

  return (
    <section className="mb-8">
      <h2 className="text-xl font-bold mb-3">{title}</h2>
      <div className="flex gap-4 overflow-x-auto scrollbar-hide pb-2">
        {items.map((item) => (
          <MovieCard
            key={item.id}
            item={item}
            onClick={onItemClick}
          />
        ))}
      </div>
    </section>
  );
}
