import React, {useState} from 'react'
import api from '../api/axios'
import { useNavigate } from 'react-router-dom'


export default function Login(){
const [username,setUsername] = useState('')
const [password,setPassword] = useState('')
const nav = useNavigate()


const submit = async (e)=>{
e.preventDefault()
try {
const res = await api.post('/accounts/token/', { username, password })
localStorage.setItem('access_token', res.data.access)
localStorage.setItem('refresh_token', res.data.refresh)
nav('/')
} catch (err) {
alert('Login failed')
}
}


return (
<div className="max-w-md mx-auto p-4">
<h2 className="text-xl font-semibold mb-4">Login</h2>
<form onSubmit={submit} className="space-y-3">
<input value={username} onChange={e=>setUsername(e.target.value)} placeholder="username" className="w-full p-2 border rounded" />
<input value={password} onChange={e=>setPassword(e.target.value)} type="password" placeholder="password" className="w-full p-2 border rounded" />
<button className="w-full py-2 bg-blue-600 text-white rounded">Login</button>
</form>
</div>
)
}