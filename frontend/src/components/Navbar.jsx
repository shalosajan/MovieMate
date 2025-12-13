import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem("access_token");

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    navigate("/login");
  };

  return (
    <nav className="sticky top-0 z-50 bg-gray-950/90 backdrop-blur border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        
        {/* Left: Logo */}
        <Link to="/" className="text-xl font-bold text-white tracking-wide">
          🎬 MovieMate
        </Link>

        {/* Right: Actions */}
        <div className="flex items-center gap-4 text-sm">
          <Link to="/" className="text-gray-300 hover:text-white">
            Home
          </Link>

          {isAuthenticated ? (
            <>

            <Link to="/dashboard"
            className="text-gray-300 hover:text-white"
            >Dashboard</Link>
            <Link to="/wishlist"
            className="text-gray-300 hover:text-white"
            >Wishlist</Link>

              <button
                onClick={handleLogout}
                className="px-3 py-1 rounded bg-red-600 hover:bg-red-700 text-white"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="px-3 py-1 rounded border border-gray-600 text-gray-200 hover:bg-gray-800"
              >
                Login
              </Link>

              <Link
                to="/register"
                className="px-3 py-1 rounded bg-indigo-600 hover:bg-indigo-700 text-white"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
