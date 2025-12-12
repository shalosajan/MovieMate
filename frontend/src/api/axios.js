import axios from 'axios'


const baseURL = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'
const api = axios.create({ baseURL })


api.interceptors.request.use((config) => {
const token = localStorage.getItem('access_token')
if (token) config.headers.Authorization = `Bearer ${token}`
return config
})


api.interceptors.response.use(
(res) => res,
async (err) => {
const originalReq = err.config
if (err.response && err.response.status === 401 && !originalReq._retry) {
originalReq._retry = true
const refresh = localStorage.getItem('refresh_token')
if (refresh) {
try {
const resp = await axios.post(`${baseURL}/accounts/token/refresh/`, { refresh })
localStorage.setItem('access_token', resp.data.access)
originalReq.headers.Authorization = `Bearer ${resp.data.access}`
return axios(originalReq)
} catch (e) {
localStorage.removeItem('access_token')
localStorage.removeItem('refresh_token')
}
}
}
return Promise.reject(err)
}
)


export default api