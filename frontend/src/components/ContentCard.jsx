import React from 'react'
import { Link } from 'react-router-dom'


export default function ContentCard({ item }){
return (
<div className="bg-white p-3 rounded shadow">
{item.poster_path ? <img src={item.poster_path} alt={item.title} className="w-full h-48 object-cover rounded" /> : <div className="h-48 bg-gray-200 flex items-center justify-center">No Image</div>}
<h3 className="mt-2 text-lg font-semibold">{item.title}</h3>
<div className="text-sm text-gray-500">{item.type}</div>
<div className="mt-2 flex justify-between items-center">
<div className="text-sm">{item.status}</div>
<Link to={`/content/${item.id}`} className="text-blue-600">Open</Link>
</div>
</div>
)
}