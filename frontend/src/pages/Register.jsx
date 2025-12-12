import React, {useState} from 'react'
import api from '../api/axios'
import { useNavigate } from 'react-router-dom'


export default function Register(){
const [form, setForm] = useState({username:'',password:'',password2:'',email:''})
const nav = useNavigate()


const submit = async (e)=>{
e.preventDefault()
try{
await api.post('/accounts/register/', form)
alert('Registered — please login')
nav('/login')
}catch(e){
alert('Registration failed')
}
}


return (
<div className="max-w-md mx-auto p-4">
<h2 className="text-xl font-semibold mb-4">Register</h2>
<form onSubmit={submit} className="space-y-3">
<input placeholder="username" className="w-full p-2 border rounded" onChange={e=>setForm({...form,username:e.target.value})} />
<input placeholder="email" className="w-full p-2 border rounded" onChange={e=>setForm({...form,email:e.target.value})} />
<input placeholder="password" type="password" className="w-full p-2 border rounded" onChange={e=>setForm({...form,password:e.target.value})} />
<input placeholder="password2" type="password" className="w-full p-2 border rounded" onChange={e=>setForm({...form,password2:e.target.value})} />
<button className="w-full py-2 bg-green-600 text-white rounded">Register</button>
</form>
</div>
)
}