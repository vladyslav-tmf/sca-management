# 🐈‍⬛️ Spy Cat Agency Management System

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com/)

A full-stack CRUD application for managing spy cats, missions, and targets.

## 📋 Table of Contents

- [About The Project](#-about-the-project)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development Setup](#local-development-setup)
  - [Docker Setup](#docker-setup)
- [Environment Variables](#-environment-variables)
- [API Documentation](#-api-documentation)
- [Usage Examples](#-usage-examples)

## 🎯 About The Project

The Spy Cat Agency Management System is a comprehensive solution for managing spy operations. It provides:

- **Spy Cat Management**: Complete CRUD operations for managing spy cats with breed validation
- **Mission Management**: Create and manage missions with multiple targets
- **Target Tracking**: Track mission progress with notes and completion status
- **External API Integration**: Breed validation using TheCatAPI
- **Modern UI**: Responsive dashboard built with Next.js and Shadcn/UI

### Key Features

- **Spy Cats CRUD** - Create, read, update, delete spy cats, missions, and targets
- **Breed Validation** - Real-time validation using TheCatAPI
- **Mission Management** - Assign cats to missions with targets
- **Progress Tracking** - Update notes and mark targets complete
- **Responsive UI** - Modern dashboard for easy navigation
- **Docker Support** - Full containerization with auto-migrations

## 🚀 Getting Started

Choose your preferred setup method:

### Prerequisites

#### For Docker Setup (Recommended)
- **Docker** and **Docker Compose**
- **Git**

#### For Local Development Setup
- **Python** (3.12+)
- **Node.js** and **npm**
- **PostgreSQL**
- **Git**
- **uv** (Python package manager)

### Docker Setup

The easiest way to run the entire application:

1. **Clone the repository**
   ```bash
   git clone https://github.com/vladyslav-tmf/sca-management.git
   cd sca-management
   ```

2. **Environment configuration**
   ```bash
   # Copy environment template
   cp .env.example .env

   # Edit .env if needed (default values work for Docker)
   ```

3. **Start all services**
   ```bash
   # Build and start all containers
   docker-compose up --build

   # Or run in background
   docker-compose up --build -d
   ```

4. **Access the application**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000 (auto-redirects to `/docs`)
   - **API Docs**: http://localhost:8000/docs

The Docker setup automatically:
- Creates PostgreSQL database
- Runs database migrations
- Starts backend and frontend services

### Local Development Setup

For development with hot reload and debugging:

#### 1. Database Setup
Start PostgreSQL using Docker for convenience, or use your local PostgreSQL 

#### 2. Backend Setup
```bash
cd backend

# Install dependencies
uv sync

# Set up environment variables
# Edit DATABASE_URL to use localhost: postgresql+asyncpg://postgres:password@localhost:5432/sca_db

# Run database migrations
uv run alembic upgrade head

# Start development server
cd src
uv run uvicorn main:app --reload
```

Backend will be available at http://localhost:8000

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at http://localhost:3000

## ⚙️ Environment Variables

The application uses environment variables for configuration. Copy `.env.example` to `.env` and modify as needed.

### Core Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ENVIRONMENT` | Application environment | `development` | ✅ |

### Database Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `POSTGRES_DB` | PostgreSQL database name | `sca_db` | ✅ |
| `POSTGRES_USER` | PostgreSQL username | `postgres` | ✅ |
| `POSTGRES_PASSWORD` | PostgreSQL password | `password` | ✅ |
| `DATABASE_URL` | Full database connection string | `postgresql+asyncpg://postgres:password@localhost:5432/sca_db` | ✅ |

**Note**: For Docker, use `@db:5432` in DATABASE_URL. For local development, use `@localhost:5432`.

### External APIs

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `CAT_API_URL` | TheCatAPI endpoint for breed validation | `https://api.thecatapi.com/v1/breeds` | ✅ |

### Frontend Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL for frontend | `http://localhost:8000` | ✅ |

## 📚 API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

#### Spy Cats Management

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| `GET` | `/api/v1/cats/` | List all spy cats | - |
| `POST` | `/api/v1/cats/` | Create new spy cat | `CatCreate` |
| `GET` | `/api/v1/cats/{id}` | Get cat details | - |
| `PATCH` | `/api/v1/cats/{id}` | Update cat salary | `CatUpdate` |
| `DELETE` | `/api/v1/cats/{id}` | Delete spy cat | - |

#### Missions Management

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| `GET` | `/api/v1/missions/` | List all missions | - |
| `POST` | `/api/v1/missions/` | Create mission with targets | `MissionCreate` |
| `GET` | `/api/v1/missions/{id}` | Get mission details | - |
| `PATCH` | `/api/v1/missions/{id}/assign` | Assign cat to mission | `MissionAssign` |
| `DELETE` | `/api/v1/missions/{id}` | Delete mission | - |

#### Targets Management

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| `PATCH` | `/api/v1/targets/{id}` | Update target notes/status | `TargetUpdate` |

### Example Requests

#### Create Spy Cat
```bash
curl -X POST "http://localhost:8000/api/v1/cats/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Agent Whiskers",
    "years_of_experience": 3,
    "breed": "Siamese",
    "salary": 50000
  }'
```

#### Create Mission with Targets
```bash
curl -X POST "http://localhost:8000/api/v1/missions/" \
  -H "Content-Type: application/json" \
  -d '{
    "targets": [
      {
        "name": "Dr. Evil",
        "country": "Germany",
        "notes": "High priority target"
      }
    ]
  }'
```

## 💡 Usage Examples

### Frontend Dashboard

1. **View Spy Cats**: Browse all registered spy cats with their details
2. **Add New Cat**: Click "Add Spy Cat" and fill in the form
3. **Edit Cat**: Click "Edit" on any cat card to update salary
4. **View Details**: Click "Details" to see comprehensive cat information
5. **Delete Cat**: Remove cats from the system with confirmation

### API Usage

#### Error Handling
All endpoints return structured error responses:
```json
{
  "detail": "Cat with breed 'InvalidBreed' not found in TheCatAPI"
}
```

#### Pagination
List endpoints support pagination:
```bash
GET /api/v1/cats/?skip=0&limit=10
```

---

**Built with ❤️ for the Spy Cat Agency**
