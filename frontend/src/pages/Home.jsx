import React, {useEffect, useState} from 'react'
import api from '../api/axios'
import { Link, useNavigate } from 'react-router-dom'
import ContentCard from '../components/ContentCard'


export default function Home(){
const [items, setItems] = useState([])
const nav = useNavigate()


useEffect(()=>{
(async ()=>{
try{
const res = await api.get('/catalog/contents/')
setItems(res.data.results || res.data)
} catch (e) {
nav('/login')
}
})()
}, [])


return (
<div className="container mx-auto p-4">
<div className="flex justify-between items-center">
<h1 className="text-2xl font-bold">My Collection</h1>
<Link to="/search" className="py-1 px-3 bg-blue-600 text-white rounded">Search & import</Link>
</div>


<div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
{items.map(it => <ContentCard key={it.id} item={it} />)}
</div>
</div>
)
}