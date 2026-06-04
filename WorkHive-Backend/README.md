# 🐝 WorkHive Backend

A secure, high-performance, and compliance-hardened REST API built with **FastAPI**, **SQLAlchemy**, and **MySQL** to power the WorkHive workspace collaboration client.

---

## 🚀 Key Features

* **Multi-Assignee Tasks**: Full relational junction tables mapping workspace tasks to multiple team members.
* **Google OAuth 2.0 Integration**: Direct backend authentication verifying ID tokens from Google Identity Services (SSO).
* **Compliance Audit Logs**: Automated system audit engine logging security, project, file, and task events with client IP/User-Agent tracking.
* **Personal Task Management**: Independent endpoints allowing users to maintain isolated, private task lists.
* **Google Drive File Storage**: Integrated OAuth tokens storage and automatic refresh caching on database records.
* **Admin Registration Controls**: Flow restricting new users to "Pending Approval" state until reviewed by an administrator.
* **Mail Notifications**: Multi-recipient system notifications using SMTP or a local mock log fallback.

---

## 🛠️ Tech Stack

* **Language**: Python 3.10+
* **Framework**: FastAPI (Pydantic v2 validation)
* **Database**: MySQL Server
* **ORM & Migrations**: SQLAlchemy & Alembic
* **Drivers**: PyMySQL + Cryptography
* **Authentication**: PyJWT + Passlib (bcrypt)

---

## 📋 Prerequisites

Ensure your machine has the following tools installed:
* **Python 3.10+** (with `pip`)
* **MySQL Server** (running locally on port 3306, or a remote cloud database)

---

## 💻 Getting Started (Step-by-Step)

### 1. Position into Backend Directory
```bash
cd WorkHive-Backend
```

### 2. Create Python Virtual Environment
Create a clean, isolated environment to install dependencies:
* **Windows (CMD/PowerShell):**
  ```powershell
  python -m venv venv
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  ```

### 3. Activate the Environment
* **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
* **Windows (CMD):**
  ```cmd
  .\venv\Scripts\activate.bat
  ```
* **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
Install all required libraries specified in the requirements file:
```bash
pip install -r requirements.txt
```

### 5. Setup Environment File
Copy the example environment file:
* **Windows (CMD/PowerShell):**
  ```powershell
  copy .env.example .env
  ```
* **macOS / Linux:**
  ```bash
  cp .env.example .env
  ```

Open `.env` and fill in the required parameters:
> [!IMPORTANT]
> Change the default credentials and set secure keys in production configurations.

| Variable | Description | Example / Default |
| :--- | :--- | :--- |
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://root:password@localhost:3306/workhive` |
| `SECRET_KEY` | Secret key for signing JWTs | *Long random string* |
| `ALGORITHM` | Algorithm used for JWT encryption | `HS256` |
| `FRONTEND_URL` | URL of the client frontend for CORS | `http://localhost:5173` |
| `GOOGLE_CLIENT_ID` | Client ID from Google Cloud Console | `your-id.apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | Client Secret from Google Cloud Console | `GOCSPX-secret` |
| `GOOGLE_REDIRECT_URI` | Redirect URI registered in Google Console | `http://localhost:5173/auth/google/callback` |
| `SMTP_HOST` | *(Optional)* Outgoing SMTP host for emails | `smtp.gmail.com` |

### 6. Run Database Migrations
Deploy the database schema mappings using Alembic:
```bash
alembic upgrade head
```

### 7. Seed Admin Credentials
Create the default Admin user in the workspace. An admin is required to approve pending employee registrations:
```bash
python seed_admin.py
```
> [!WARNING]
> Copy the randomly generated admin password printed to the terminal console! You will need it to perform the first login.

### 8. Run FastAPI Server
Start the development server with hot-reload enabled:
```bash
uvicorn app.main:app --reload
```

* **Interactive API Playground**: Once running, navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to access Swagger UI and try endpoints.
* **Alternative Redoc Playground**: Access API schemas at [http://localhost:8000/redoc](http://localhost:8000/redoc).
