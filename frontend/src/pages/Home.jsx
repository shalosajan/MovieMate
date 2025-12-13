// Home.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import { getTrendingMovies } from "../api/tmdbProxy";
import Carousel from "../components/Carousel";
import ContentCard from "../components/ContentCard";
import { searchTMDB } from "../api/tmdbProxy";

import {
  getPopularMovies,
  getTopRatedMovies,
  getTrendingTV,
  getNowPlayingMovies
} from "../api/tmdbProxy";
import DetailsModal from "../components/DetailsModal";


export default function Home() {
  const [collection, setCollection] = useState([]);
  const [trendingMovies, setTrendingMovies] = useState([]);
  const [popularMovies, setPopularMovies] = useState([]);
  const [topRatedMovies, setTopRatedMovies] = useState([]);
  const [trendingTV, setTrendingTV] = useState([]);
  const [nowPlaying, setNowPlaying] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);
  const [searchResults, setSearchResults] = useState([]);
  const [searching, setSearching] = useState(false);

  const [query, setQuery] = useState("");

  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem("access_token");

  // 🔓 Public TMDB proxy data
useEffect(() => {
  getTrendingMovies().then(d => setTrendingMovies(d?.results || []));
  getPopularMovies().then(d => setPopularMovies(d?.results || []));
  getTopRatedMovies().then(d => setTopRatedMovies(d?.results || []));
  getTrendingTV().then(d => setTrendingTV(d?.results || []));
  getNowPlayingMovies().then(d => setNowPlaying(d?.results || []));
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
  onKeyDown={async (e) => {
    if (e.key === "Enter" && query.trim()) {
      setSearching(true);
      const data = await searchTMDB(query);
      setSearchResults(data.results || []);
      setSearching(false);
    }
  }}
  placeholder="Search movies or TV shows..."
  className="w-full max-w-xl px-4 py-3 rounded bg-gray-800 text-white outline-none"
/>
{searching && (
  <p className="text-gray-400 text-center mt-6">
    Searching...
  </p>
)}

{searchResults.length > 0 && (
  <div className="mt-10 grid grid-cols-2 md:grid-cols-4 gap-6">
    {searchResults.map(item => (
      <div
        key={item.id}
        onClick={() => setSelectedItem(item)}
        className="cursor-pointer"
      >
        <img
          src={
            item.poster_path
              ? `https://image.tmdb.org/t/p/w300${item.poster_path}`
              : ""
          }
          className="rounded mb-2"
        />
        <h3 className="text-sm font-semibold">
          {item.title || item.name}
        </h3>
        <p className="text-xs text-gray-400">
          ⭐ {item.vote_average?.toFixed(1)}
        </p>
      </div>
    ))}
  </div>
)}


      </div>

      {/* PUBLIC */}
      <Carousel
        title="🔥 Trending Movies"
        items={trendingMovies}
        onItemClick={(item) => setSelectedItem(item)}
      />
    <Carousel title="🎥 Popular Movies"
     items={popularMovies}
     onItemClick={(item) => setSelectedItem(item)}
    />

    <Carousel title="⭐ Top Rated Movies" 
    items={topRatedMovies}
    onItemClick={(item) => setSelectedItem(item)}
    />

    <Carousel title="📺 Trending TV Shows" 
    items={trendingTV}
    onItemClick={(item) => setSelectedItem(item)}
    />

    <Carousel title="🆕 Latest Releases"
     items={nowPlaying}
     onItemClick={(item) => setSelectedItem(item)}
    />

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
      <DetailsModal
  item={selectedItem}
  open={!!selectedItem}
  onClose={() => setSelectedItem(null)}
/>

    </div>
  );
}
