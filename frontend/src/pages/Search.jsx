import React, {useState} from 'react'
import api from '../api/axios'


export default function Search(){
const [q, setQ] = useState('')
const [results, setResults] = useState([])


const search = async () => {
const res = await api.get('/catalog/contents/tmdb_search/', { params: { q } })
setResults(res.data.results)
}


const importItem = async (tmdb_id) => {
await api.post('/catalog/contents/import_tmdb/', { tmdb_id })
alert('Imported — refresh home to see it')
}


return (
<div className="max-w-3xl mx-auto p-4">
<h2 className="text-xl mb-2">Search TMDB</h2>
<div className="flex gap-2">
<input value={q} onChange={e=>setQ(e.target.value)} className="flex-1 p-2 border rounded" placeholder="Search title..." />
<button onClick={search} className="px-3 bg-blue-600 text-white rounded">Search</button>
</div>


<div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
{results.map(r => (
<div key={r.id} className="p-3 bg-white rounded shadow">
<h3 className="font-semibold">{r.title} <span className="text-xs text-gray-400">({r.media_type})</span></h3>
<p className="text-sm text-gray-500">{r.overview}</p>
<div className="mt-2 flex gap-2">
<button onClick={()=>importItem(r.id)} className="px-2 py-1 bg-green-600 text-white rounded">Import</button>
</div>
</div>
))}
</div>
</div>
)
}