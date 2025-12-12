import api from "../api/axios";
import React, {useEffect, useState} from 'react'
import { useParams } from "react-router-dom";
export default function ContentDetail(){
const { id } = useParams()
const [item, setItem] = useState(null)


useEffect(()=>{
(async ()=>{
const res = await api.get(`/catalog/contents/${id}/`)
setItem(res.data)
})()
}, [id])


if (!item) return <div className="p-4">Loading...</div>


return (
<div className="p-4 max-w-3xl mx-auto">
<h2 className="text-2xl font-bold">{item.title}</h2>
<p className="text-sm text-gray-600">{item.overview}</p>


{item.type === 'tv' && (
<div className="mt-4">
<h3 className="font-semibold">Seasons</h3>
<div className="space-y-3 mt-2">
{item.seasons.map(s => (
<div key={s.id} className="p-3 bg-white rounded shadow">
<div className="flex justify-between items-center">
<div>Season {s.season_number} ({s.episodes.length || s.episodes_count || '—'} eps)</div>
<button onClick={async ()=>{
await api.post(`/catalog/contents/${id}/mark_season_watched/`, { season_number: s.season_number })
const r = await api.get(`/catalog/contents/${id}/`)
setItem(r.data)
}} className="px-2 py-1 bg-indigo-600 text-white rounded">Mark season watched</button>
</div>
<div className="mt-2 grid grid-cols-6 gap-2">
{s.episodes.map(ep => (
<label key={ep.id} className="flex items-center gap-2 text-sm">
<input type="checkbox" checked={ep.watched} onChange={async ()=>{
await api.post(`/catalog/contents/${id}/toggle_episode/`, { season_number: s.season_number, episode_number: ep.episode_number })
const r = await api.get(`/catalog/contents/${id}/`)
setItem(r.data)
}} />
S{s.season_number}E{ep.episode_number}
</label>
))}
</div>
</div>
))}
</div>
</div>
)}


{item.type === 'movie' && (
<div className="mt-4">
<h3 className="font-semibold">Movie</h3>
<div className="mt-2">Rate & review UI here</div>
</div>
)}
</div>
)
}