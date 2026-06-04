import { create } from 'zustand'
import api from '../lib/api'

export const useAuthStore = create((set, get) => ({
  user: null,
  accessToken: localStorage.getItem('accessToken'),
  refreshToken: localStorage.getItem('refreshToken'),
  isAuthenticated: !!localStorage.getItem('accessToken'),

  /**
   * Hydrate user object from /auth/me on app load.
   * Called once in App.jsx when a token exists.
   */
  fetchMe: async () => {
    try {
      const res = await api.get('/api/v1/auth/me')
      set({ user: res.data, isAuthenticated: true })
    } catch (error) {
      if (error.response?.status === 401) {
        get().logout()
      } else {
        // Prevent logging out on network errors
        set({ user: null })
      }
    }
  },

  login: async (email, password) => {
    try {
      const formData = new FormData()
      formData.append('username', email)
      formData.append('password', password)

      const response = await api.post('/api/v1/auth/login', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      const { access_token, refresh_token, user } = response.data

      localStorage.setItem('accessToken', access_token)
      localStorage.setItem('refreshToken', refresh_token)

      set({ user, accessToken: access_token, refreshToken: refresh_token, isAuthenticated: true })
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Login failed' }
    }
  },

  logout: () => {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false })
  },

  googleLogin: async (credential) => {
    try {
      const response = await api.post('/api/v1/auth/google', { credential })
      const { access_token, refresh_token, user } = response.data
      localStorage.setItem('accessToken', access_token)
      localStorage.setItem('refreshToken', refresh_token)
      set({ user, accessToken: access_token, refreshToken: refresh_token, isAuthenticated: true })
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Google login failed' }
    }
  },
}))
