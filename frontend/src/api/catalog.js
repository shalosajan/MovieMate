import api from "./axios";

/* ---------------- MOVIE ---------------- */

export const markMovieWatched = (contentId) =>
  api.patch(`/catalog/contents/${contentId}/`, {
    status: "completed",
  });

/* ---------------- TV ---------------- */

export const getContentSeasons = (contentId) =>
  api.get(`/catalog/contents/${contentId}/seasons/`)
    .then(res => res.data);

export const markSeasonWatched = (contentId, seasonNumber) =>
  api.post(`/catalog/contents/${contentId}/mark_season_watched/`, {
    season_number: seasonNumber,
  });

export const toggleEpisode = (contentId, seasonNumber, episodeNumber) =>
  api.post(`/catalog/contents/${contentId}/toggle_episode/`, {
    season_number: seasonNumber,
    episode_number: episodeNumber,
  });

export const getContentByTMDB = (tmdbId) =>
  api
    .get(`/catalog/contents/?tmdb_id=${tmdbId}`)
    .then(res => res.data.results?.[0]);

export const importFromTMDB = (tmdbId) =>
  api.post("/catalog/contents/import_tmdb/", {
    tmdb_id: tmdbId,
  }).then(res => res.data);

