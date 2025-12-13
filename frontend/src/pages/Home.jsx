import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/axios'
import ContentCard from '../components/ContentCard'

export default function Home() {
  const [items, setItems] = useState([])
  const isAuthenticated = !!localStorage.getItem("access_token")

  useEffect(() => {
    // Only fetch user collection if logged in
    if (!isAuthenticated) return

    (async () => {
      try {
        const res = await api.get('/catalog/contents/')
        setItems(res.data.results || res.data)
      } catch (e) {
        console.warn("User not authenticated or error loading collection")
      }
    })()
  }, [isAuthenticated])

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">
          {isAuthenticated ? "My Collection" : "Welcome to MovieMate"}
        </h1>

        {isAuthenticated && (
          <Link
            to="/search"
            className="py-1 px-3 bg-blue-600 text-white rounded"
          >
            Search & Import
          </Link>
        )}
      </div>

      {!isAuthenticated && (
        <p className="text-gray-400 mt-2">
          Discover movies & TV shows. Sign in to track your watchlist.
        </p>
      )}

      {isAuthenticated && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
          {items.map(it => (
            <ContentCard key={it.id} item={it} />
          ))}
        </div>
      )}
    </div>
  )
}
