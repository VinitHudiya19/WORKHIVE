# 🐝 WorkHive Workspace Collaboration Platform

Welcome to the **WorkHive Monorepo**. This repository houses both the frontend client and the backend API service for the WorkHive application.

---

## 📂 Project Structure

```
├── WorkHive-Backend/   # FastAPI (Python) backend service
└── WorkHive-Frontend/  # React (Vite) frontend application
```

For detailed local setup instructions, prerequisites, and developer documentation, please refer to the respective project README files:
* 🐍 **Backend Setup**: [WorkHive-Backend/README.md](WorkHive-Backend/README.md)
* 🕸️ **Frontend Setup**: [WorkHive-Frontend/README.md](WorkHive-Frontend/README.md)

---

## 🚀 Deployment Guide

This monorepo is designed to be easily deployed to **Vercel** (Frontend) and **Render** (Backend).

### 1. Frontend Deployment (Vercel)

1. Sign in to your [Vercel Dashboard](https://vercel.com).
2. Click **Add New** > **Project** and select this repository.
3. In the project configuration:
   * **Framework Preset**: Select **Vite** (or let Vercel auto-detect it).
   * **Root Directory**: Click *Edit* and select **`WorkHive-Frontend`**.
4. Under **Environment Variables**, add:
   * `VITE_API_BASE`: Set this to your live Render backend URL (e.g., `https://workhive-backend.onrender.com`).
   * `VITE_GOOGLE_CLIENT_ID`: Your Google OAuth Client ID.
5. Click **Deploy**.

---

### 2. Backend Deployment (Render)

1. Sign in to your [Render Dashboard](https://render.com).
2. Click **New +** > **Web Service**.
3. Connect your GitHub repository.
4. In the configuration settings:
   * **Name**: `workhive-backend`
   * **Language**: `Python`
   * **Root Directory**: **`WorkHive-Backend`**
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Under **Advanced** > **Environment Variables**, add the variables defined in `WorkHive-Backend/.env.example`:
   * `DATABASE_URL`: Your live database URL (e.g., a managed MySQL instance on Render, Aiven, or PlanetScale).
   * `SECRET_KEY`: A secure random secret key.
   * `ALGORITHM`: `HS256`
   * `FRONTEND_URL`: Your live Vercel URL (e.g., `https://workhive.vercel.app`).
   * `GOOGLE_CLIENT_ID`: Your Google OAuth Client ID.
   * `GOOGLE_CLIENT_SECRET`: Your Google OAuth Client Secret.
   * `GOOGLE_REDIRECT_URI`: `https://workhive.vercel.app/auth/google/callback`
6. Click **Create Web Service**.
