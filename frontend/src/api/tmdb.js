// src/api/tmdb.js

const TMDB_BASE = "https://api.themoviedb.org/3";

const API_KEY = import.meta.env.VITE_TMDB_KEY;  

if (!API_KEY) {
  console.warn("⚠️ Missing TMDB API Key. Add VITE_TMDB_KEY to your .env file.");
}

// Helper function
async function tmdbFetch(path, params = {}) {
  const url = new URL(`${TMDB_BASE}${path}`);

  params.api_key = API_KEY;
  params.language = "en-US";

  Object.keys(params).forEach((key) => url.searchParams.append(key, params[key]));

  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`TMDB Error: ${res.status}`);
  }

  return res.json();
}

/* ---------------------------------------------------
   PUBLIC TMDB FUNCTIONS
----------------------------------------------------*/

// Trending
export function getTrendingMovies() {
  return tmdbFetch("/trending/movie/week");
}

export function getTrendingTV() {
  return tmdbFetch("/trending/tv/week");
}

// Popular
export function getPopularMovies() {
  return tmdbFetch("/movie/popular");
}

export function getPopularTV() {
  return tmdbFetch("/tv/popular");
}

// Top Rated
export function getTopRatedMovies() {
  return tmdbFetch("/movie/top_rated");
}

export function getTopRatedTV() {
  return tmdbFetch("/tv/top_rated");
}

// Now Playing (Latest releases)
export function getNowPlayingMovies() {
  return tmdbFetch("/movie/now_playing");
}

// Genres
export function getMovieGenres() {
  return tmdbFetch("/genre/movie/list");
}

export function getTVGenres() {
  return tmdbFetch("/genre/tv/list");
}

// Shows within a genre
export function getMoviesByGenre(genreId) {
  return tmdbFetch("/discover/movie", { with_genres: genreId });
}

export function getTVByGenre(genreId) {
  return tmdbFetch("/discover/tv", { with_genres: genreId });
}

// Full details (modal)
export function getMovieDetails(id) {
  return tmdbFetch(`/movie/${id}`);
}

export function getTVDetails(id) {
  return tmdbFetch(`/tv/${id}`);
}

// Watch providers (optional)
export function getWatchProviders(id, type = "movie") {
  return tmdbFetch(`/${type}/${id}/watch/providers`);
}
