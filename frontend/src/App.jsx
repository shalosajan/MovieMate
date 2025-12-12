import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Home from './pages/Home.jsx'
import Search from './pages/Search.jsx'
import ContentDetail from './pages/ContentDetail.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'


function PrivateRoute({ children }) {
const token = localStorage.getItem('access_token')
return token ? children : <Navigate to="/login" replace />
}


export default function App(){
return (
<BrowserRouter>
<div className="min-h-screen bg-gray-50 text-gray-900">
<Routes>
<Route path="/" element={<Home/>} />
<Route path="/search" element={<PrivateRoute><Search/></PrivateRoute>} />
<Route path="/content/:id" element={<PrivateRoute><ContentDetail/></PrivateRoute>} />
<Route path="/login" element={<Login/>} />
<Route path="/register" element={<Register/>} />
</Routes>
</div>
</BrowserRouter>
)
}