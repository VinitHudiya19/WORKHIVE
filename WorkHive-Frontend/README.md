# 🕸️ WorkHive Frontend

A modern, responsive, and compliance-hardened React client application built with **Vite**, **Zustand**, and **Vanilla CSS** to power the WorkHive project management client.

---

## 🚀 Key Features

* **Kanban Board & Workload Overviews**: Drag-and-drop workspace cards mapping task states and assignee workloads interactively.
* **Google Identity Services SSO**: Unified and aligned Google OAuth Login/Registration integration with auto-resize listeners.
* **Compliance Audit Logs Dashboard**: Interactive tracking interface featuring resource mapping, status indicators, and CSV export capabilities.
* **Private Tasks Panel**: Separated workspace view for private individual tasks with checklists and progress tracking.
* **Interactive Modals & Toast Alerts**: Modern sliding alerts and confirmation dialogs replacing default browser alert overlays.
* **Pulse Skeleton Loaders**: Premium loading screens styled to match actual UI components during server operations.
* **Admin Control Center**: Integrated pending registration views enabling organization admins to approve/reject workspace requests.

---

## 🛠️ Tech Stack

* **Build Tool**: Vite (ESBuild compiler)
* **Framework**: React 18+
* **Routing**: React Router DOM v6
* **State Management**: Zustand (persistent local storage caching)
* **Styling**: Vanilla CSS (CSS Variables based design system)
* **Icons**: Lucide React

---

## 📋 Prerequisites

Ensure your machine has the following tools installed:
* **Node.js** (v18.0 or higher)
* **npm** (included with Node.js installation)

---

## 💻 Getting Started (Step-by-Step)

### 1. Position into Frontend Directory
```bash
cd WorkHive-Frontend
```

### 2. Install Dependencies
Restore and install all npm package dependencies:
```bash
npm install
```

### 3. Setup Environment File
Copy the example environment file:
* **Windows (CMD/PowerShell):**
  ```powershell
  copy .env.example .env
  ```
* **macOS / Linux:**
  ```bash
  cp .env.example .env
  ```

Open the `.env` file and configure the target variables:
> [!NOTE]
> During local development, if your backend server runs on `http://localhost:8000`, the Vite configuration will automatically proxy requests.

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `VITE_API_BASE` | Base endpoint URL of the FastAPI Backend | `http://localhost:8000` |
| `VITE_GOOGLE_CLIENT_ID` | OAuth Client ID from Google Cloud Console | `your-id.apps.googleusercontent.com` |

### 4. Run Development Server
Launch the local Vite development server:
```bash
npm run dev
```
The application will start running at [http://localhost:5173](http://localhost:5173). Open the URL in your browser to view the client.

### 5. Compile Production Bundle
To compile optimized static assets ready for production hosting (Vercel, Netlify, etc.):
```bash
npm run build
```
The compiled artifacts will be outputted to the `dist` directory.
