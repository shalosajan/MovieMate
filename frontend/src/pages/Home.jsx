import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import { getTrendingMovies } from "../api/tmdbProxy";
import Carousel from "../components/Carousel";
import ContentCard from "../components/ContentCard";
import {
  getPopularMovies,
  getTopRatedMovies,
  getTrendingTV,
  getNowPlayingMovies
} from "../api/tmdbProxy";

export default function Home() {
  const [collection, setCollection] = useState([]);
  const [trendingMovies, setTrendingMovies] = useState([]);
  const [popularMovies, setPopularMovies] = useState([]);
  const [topRatedMovies, setTopRatedMovies] = useState([]);
  const [trendingTV, setTrendingTV] = useState([]);
  const [nowPlaying, setNowPlaying] = useState([]);

  const [query, setQuery] = useState("");

  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem("access_token");

  // 🔓 Public TMDB proxy data
  useEffect(() => {
    getTrendingMovies().then(d => setTrendingMovies(d.results));
    getPopularMovies().then(d => setPopularMovies(d.results));
    getTopRatedMovies().then(d => setTopRatedMovies(d.results));
    getTrendingTV().then(d => setTrendingTV(d.results));
    getNowPlayingMovies().then(d => setNowPlaying(d.results));
  }, []);

  // 🔐 User collection
  useEffect(() => {
    if (!isAuthenticated) return;

    api.get("/catalog/contents/")
      .then(res => setCollection(res.data.results || res.data))
      .catch(() => {});
  }, [isAuthenticated]);

  return (
    <div className="px-6 py-6 max-w-7xl mx-auto">

      {/* HERO */}
      <div className="mb-10 text-center">
        <h1 className="text-4xl font-bold mb-4">
          Track Movies & TV Shows
        </h1>

        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") navigate(`/search?q=${query}`);
          }}
          placeholder="Search movies or TV shows..."
          className="w-full max-w-xl px-4 py-3 rounded bg-gray-800 text-white outline-none"
        />
      </div>

      {/* PUBLIC */}
      <Carousel
        title="🔥 Trending Movies"
        items={trendingMovies}
      />
    <Carousel title="🎥 Popular Movies" items={popularMovies} />

    <Carousel title="⭐ Top Rated Movies" items={topRatedMovies} />

    <Carousel title="📺 Trending TV Shows" items={trendingTV} />

    <Carousel title="🆕 Latest Releases" items={nowPlaying} />

      {/* PRIVATE */}
      {isAuthenticated && (
        <>
          <h2 className="text-xl font-bold mt-10 mb-4">
            My Collection
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {collection.map(it => (
              <ContentCard key={it.id} item={it} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
