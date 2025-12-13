// frontend/src/api/tmdbProxy.js
import api from "./axios";

/*
  These endpoints are PUBLIC.
  No auth header required.
*/

const safeGet = async (url) => {
  try {
    const res = await api.get(url);
    return res.data;
  } catch (err) {
    console.warn(
      "TMDB proxy unavailable:",
      url,
      err.response?.status
    );
    return null; // graceful fallback
  }
};

export const getTrendingMovies = () =>
  safeGet("/catalog/tmdb/trending/movies/");

export const getTrendingTV = () =>
  safeGet("/catalog/tmdb/trending/tv/");

export const getPopularMovies = () =>
  safeGet("/catalog/tmdb/popular/movies/");

export const getPopularTV = () =>
  safeGet("/catalog/tmdb/popular/tv/");

export const getTopRatedMovies = () =>
  safeGet("/catalog/tmdb/top-rated/movies/");

export const getTopRatedTV = () =>
  safeGet("/catalog/tmdb/top-rated/tv/");

export const getNowPlayingMovies = () =>
  safeGet("/catalog/tmdb/now-playing/");

export const getMovieGenres = () =>
  safeGet("/catalog/tmdb/genres/movies/");

export const getTVGenres = () =>
  safeGet("/catalog/tmdb/genres/tv/");

export const getMovieDetails = (id) =>
  safeGet(`/catalog/tmdb/movie/${id}/`);

export const getTVDetails = (id) =>
  safeGet(`/catalog/tmdb/tv/${id}/`);

export const searchTMDB = (query) =>
  api
    .get(`/catalog/tmdb/search/?q=${encodeURIComponent(query)}`)
    .then(res => res.data);
