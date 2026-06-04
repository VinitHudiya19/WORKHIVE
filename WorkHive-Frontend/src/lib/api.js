/**
 * Central axios instance for WorkHive API calls.
 *
 * Features:
 * - Auto-injects Authorization header from localStorage
 * - On 401: tries to refresh tokens, retries original request
 * - On refresh failure: logs user out and redirects to /login
 */
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
})

// ── Request interceptor: attach access token ──────────────────────────────
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ── Response interceptor: handle 401 → refresh → retry ───────────────────
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

api.interceptors.response.use(
  response => response,
  async (error) => {
    // Normalize FastAPI validation errors (array of dicts) to a clean user-facing string
    if (error.response?.data?.detail && Array.isArray(error.response.data.detail)) {
      error.response.data.detail = error.response.data.detail
        .map(d => d.msg || d.message || JSON.stringify(d))
        .join(', ')
    }

    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Queue requests that come in while refresh is in flight
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then(token => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            return api(originalRequest)
          })
          .catch(err => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      const refreshToken = localStorage.getItem('refreshToken')
      if (!refreshToken) {
        await _forceLogout()
        return Promise.reject(error)
      }

      try {
        const res = await axios.post(`${API_BASE}/api/v1/auth/refresh`, {
          token: refreshToken,
        })
        const { access_token, refresh_token } = res.data

        localStorage.setItem('accessToken', access_token)
        localStorage.setItem('refreshToken', refresh_token)

        api.defaults.headers.Authorization = `Bearer ${access_token}`
        originalRequest.headers.Authorization = `Bearer ${access_token}`

        processQueue(null, access_token)
        return api(originalRequest)
      } catch (refreshError) {
        processQueue(refreshError, null)
        const status = refreshError.response?.status
        if (status === 400 || status === 401) {
          await _forceLogout()
        }
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

async function _forceLogout() {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  try {
    // Dynamic import to avoid circular dependency
    const { useAuthStore } = await import('../store/auth')
    useAuthStore.getState().logout()
  } catch (e) {
    // ignore
  }
  window.location.href = '/login'
}

export default api
