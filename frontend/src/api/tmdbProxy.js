// frontend/src/api/tmdbProxy.js
import api from "./axios";

/*
  These endpoints are PUBLIC.
  No auth header required.
*/

export const getTrendingMovies = () =>
  api.get("/catalog/tmdb/trending/movies/").then(res => res.data);

export const getTrendingTV = () =>
  api.get("/catalog/tmdb/trending/tv/").then(res => res.data);

export const getPopularMovies = () =>
  api.get("/catalog/tmdb/popular/movies/").then(res => res.data);

export const getPopularTV = () =>
  api.get("/catalog/tmdb/popular/tv/").then(res => res.data);

export const getTopRatedMovies = () =>
  api.get("/catalog/tmdb/top-rated/movies/").then(res => res.data);

export const getTopRatedTV = () =>
  api.get("/catalog/tmdb/top-rated/tv/").then(res => res.data);

export const getNowPlayingMovies = () =>
  api.get("/catalog/tmdb/now-playing/").then(res => res.data);

export const getMovieGenres = () =>
  api.get("/catalog/tmdb/genres/movies/").then(res => res.data);

export const getTVGenres = () =>
  api.get("/catalog/tmdb/genres/tv/").then(res => res.data);
