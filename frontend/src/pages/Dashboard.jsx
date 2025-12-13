import React from "react";
import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">
        Dashboard
      </h1>

      <div className="grid md:grid-cols-2 gap-6">
        <Link
          to="/wishlist"
          className="bg-gray-800 hover:bg-gray-700 p-6 rounded"
        >
          ❤️ My Wishlist
        </Link>

        <Link
          to="/search"
          className="bg-gray-800 hover:bg-gray-700 p-6 rounded"
        >
          🔍 Search & Add
        </Link>
      </div>
    </div>
  );
}
