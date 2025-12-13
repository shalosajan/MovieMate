import api from "./axios";

export const getWishlist = () =>
  api.get("/catalog/wishlist/").then(res => res.data);

export const addToWishlist = (item) =>
  api.post("/catalog/wishlist/add/", {
    tmdb_id: item.id,
    media_type: item.media_type || "movie",
    title: item.title || item.name,
    poster_path: item.poster_path || ""
  });

export const removeFromWishlist = (tmdb_id) =>
  api.delete(`/catalog/wishlist/remove/${tmdb_id}/`);
