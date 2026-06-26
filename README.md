# PageWise

A full-stack product browser for 200,000 products, built with FastAPI, PostgreSQL, SQLAlchemy 2.x, Alembic, React, Vite, TypeScript, and Tailwind CSS.

The app exposes a cursor-paginated `/products` API and a minimal frontend for browsing products by newest update time, with optional category filtering.

## Features

- Browse products ordered by newest update time
- Cursor/keyset pagination, no `OFFSET`
- Optional category filtering
- Stable pagination ordering: `updated_at DESC, id DESC`
- FastAPI Swagger/OpenAPI documentation
- PostgreSQL schema managed by Alembic migrations
- Faker-based seed script for 200,000 products
- Docker Compose setup for database, backend, frontend, and seed job
- Minimal React UI with loading and error states

## Tech Stack

Backend:

- Python 3.12
- FastAPI
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- psycopg 3
- Pydantic Settings
- Faker

Frontend:

- React
- Vite
- TypeScript
- Tailwind CSS
- lucide-react

Infrastructure:

- Docker Compose
- PostgreSQL 16 Alpine
- Nginx for frontend container serving

## Project Structure

```text
.
├── backend/
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 202606250001_create_products.py
│   ├── app/
│   │   ├── api/
│   │   │   └── products.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   └── product.py
│   │   ├── repositories/
│   │   │   └── products.py
│   │   ├── schemas/
│   │   │   └── product.py
│   │   ├── services/
│   │   │   └── cursor.py
│   │   └── main.py
│   ├── scripts/
│   │   └── seed_products.py
│   ├── alembic.ini
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── styles.css
│   │   └── vite-env.d.ts
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
├── docker-compose.yml
├── .env.example
└── README.md
```

## Prerequisites

For Docker-based setup:

- Docker Desktop
- Docker Compose

For local setup without Docker:

- Python 3.12
- Node.js
- npm
- PostgreSQL
- A PostgreSQL database matching `DATABASE_URL`

## Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Current `.env.example`:

```env
POSTGRES_DB=products
POSTGRES_USER=products
POSTGRES_PASSWORD=products
DATABASE_URL=postgresql+psycopg://products:products@localhost:5432/products
BACKEND_CORS_ORIGINS=http://localhost:5173
VITE_API_URL=http://localhost:8000
```

Variables:

| Variable | Used by | Description |
|---|---|---|
| `POSTGRES_DB` | Docker Compose | PostgreSQL database name |
| `POSTGRES_USER` | Docker Compose | PostgreSQL username |
| `POSTGRES_PASSWORD` | Docker Compose | PostgreSQL password |
| `DATABASE_URL` | Backend, Alembic, seed script | SQLAlchemy database URL |
| `BACKEND_CORS_ORIGINS` | Backend | Comma-separated allowed frontend origins |
| `VITE_API_URL` | Frontend | Backend API base URL used by Vite |

Important Docker note:

Inside Docker Compose, the backend and seed services override `DATABASE_URL` to use the Docker service hostname:

```text
postgresql+psycopg://products:products@db:5432/products
```

This is required because `localhost` inside a container refers to that container, not the PostgreSQL service.

## Running With Docker Compose

Start the database and backend:

```bash
docker compose up -d backend
```

The backend service runs Alembic before starting Uvicorn:

```bash
python -m alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Start the frontend:

```bash
docker compose up -d frontend
```

Run the seed job:

```bash
docker compose --profile seed run --rm seed
```

The seed service runs migrations before seeding:

```bash
python -m alembic upgrade head && python -m scripts.seed_products
```

Useful checks:

```bash
docker compose ps
docker compose logs backend
docker compose logs db
```

Backend:

```text
http://localhost:8000
```

Frontend:

```text
http://localhost:5173
```

Health check:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## Database Migrations

Alembic configuration lives in:

```text
backend/alembic.ini
backend/alembic/env.py
backend/alembic/versions/
```

The current migration is:

```text
backend/alembic/versions/202606250001_create_products.py
```

It creates the `products` table and indexes.

Run migrations with Docker Compose:

```bash
docker compose run --rm backend python -m alembic upgrade head
```

Run migrations locally from the backend directory:

```bash
cd backend
python -m alembic upgrade head
```

Render migration SQL without applying it:

```bash
cd backend
python -m alembic upgrade head --sql
```

## Seed Script

Seed script path:

```text
backend/scripts/seed_products.py
```

The seed script:

- Deletes existing products
- Inserts `200,000` generated products
- Uses batches of `10,000`
- Uses SQLAlchemy Core bulk insert
- Uses Faker with deterministic seeding

Run with Docker Compose:

```bash
docker compose --profile seed run --rm seed
```

Run locally from the backend directory after migrations:

```bash
cd backend
python -m scripts.seed_products
```

The script prints progress:

```text
Inserted 10,000/200,000 products
...
Inserted 200,000/200,000 products
```

## Running Without Docker

### Backend

Create and activate a virtual environment:

```bash
cd backend
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure PostgreSQL is running and `DATABASE_URL` points to it.

Run migrations:

```bash
python -m alembic upgrade head
```

Seed data:

```bash
python -m scripts.seed_products
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

### Frontend

Install dependencies:

```bash
cd frontend
npm install
```

Start the Vite dev server:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

Build frontend for production:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

## API Documentation

FastAPI provides Swagger/OpenAPI docs automatically.

Swagger UI:

```text
http://localhost:8000/docs
```

OpenAPI JSON:

```text
http://localhost:8000/openapi.json
```

## API Endpoints

### `GET /health`

Returns backend health status.

Example:

```bash
curl http://localhost:8000/health
```

Response:

```json
{"status":"ok"}
```

### `GET /products`

Returns cursor-paginated products.

Query parameters:

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `limit` | integer | `50` | Minimum `1`, maximum `100` |
| `cursor` | string | none | Opaque cursor from previous response |
| `category` | string | none | Optional category filter |

Example:

```bash
curl "http://localhost:8000/products?limit=50"
```

With category:

```bash
curl "http://localhost:8000/products?limit=50&category=Books"
```

With cursor:

```bash
curl "http://localhost:8000/products?limit=50&cursor=<next_cursor>"
```

Response shape:

```json
{
  "products": [
    {
      "id": 1,
      "name": "Example Product",
      "category": "Books",
      "price": "12.99",
      "created_at": "2026-06-25T10:00:00Z",
      "updated_at": "2026-06-25T10:00:00Z"
    }
  ],
  "next_cursor": "opaque-cursor-or-null"
}
```

## Cursor / Keyset Pagination Design

The API does not use `OFFSET`.

Products are ordered by:

```sql
ORDER BY updated_at DESC, id DESC
```

This ordering is stable because `id` is used as a tie-breaker when multiple products have the same `updated_at`.

On the first request, the backend captures a high-water fence:

```text
(fence_updated_at, fence_id)
```

The cursor stores:

- Last item from the current page: `(last_updated_at, last_id)`
- First-page high-water fence: `(fence_updated_at, fence_id)`
- Category filter used for the query

Follow-up pages apply:

```sql
(updated_at, id) <= (:fence_updated_at, :fence_id)
AND (updated_at, id) < (:last_updated_at, :last_id)
```

This keeps pagination stable during a browsing session. Newer inserts or updates do not jump into later pages and cause duplicates. To see newer data, start a fresh browse or use the frontend refresh button.

If a cursor is reused with a different category filter, the API returns `400`.

## Database Schema

Table: `products`

| Column | Type | Notes |
|---|---|---|
| `id` | `BIGINT` | Primary key, autoincrement |
| `name` | `VARCHAR(240)` | Required |
| `category` | `VARCHAR(80)` | Required |
| `price` | `NUMERIC(10, 2)` | Required |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | Defaults to `now()` |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | Defaults to `now()` |

SQLAlchemy model:

```text
backend/app/models/product.py
```

Alembic migration:

```text
backend/alembic/versions/202606250001_create_products.py
```

## Database Indexes

The migration creates these indexes:

```sql
CREATE INDEX ix_products_updated_at_id_desc
ON products (updated_at DESC, id DESC);
```

Used for newest-first product browsing.

```sql
CREATE INDEX ix_products_category_updated_at_id_desc
ON products (category, updated_at DESC, id DESC);
```

Used for category-filtered newest-first browsing.

## Frontend

The frontend is intentionally minimal.

It includes:

- Product table
- Category dropdown
- Refresh button
- Next page button
- Loading state
- Error state
- Empty state

Frontend source:

```text
frontend/src/main.tsx
```

The frontend calls:

```text
GET {VITE_API_URL}/products
```

Default API URL:

```text
http://localhost:8000
```

## Deployment: Render + Supabase/Neon

This project can be deployed with:

- Render for backend and frontend services
- Supabase or Neon for managed PostgreSQL

### PostgreSQL on Supabase or Neon

Create a PostgreSQL database and copy the connection string.

Use the SQLAlchemy psycopg format:

```text
postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
```

Set this as:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
```

### Backend on Render

Create a Render Web Service from the `backend/` directory.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
python -m alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Environment variables:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
BACKEND_CORS_ORIGINS=https://your-frontend-domain
```

Run the seed script once after deployment if demo data is needed:

```bash
python -m alembic upgrade head && python -m scripts.seed_products
```

Do not run the seed script repeatedly in production unless replacing all product data is intended. The current seed script deletes existing products before inserting generated data.

### Frontend on Render

Create a Render Static Site from the `frontend/` directory.

Build command:

```bash
npm install && npm run build
```

Publish directory:

```text
dist
```

Environment variable:

```env
VITE_API_URL=https://your-backend-domain
```

## Troubleshooting

### `relation "products" does not exist`

Run Alembic migrations before querying or seeding:

```bash
docker compose run --rm backend python -m alembic upgrade head
```

Or locally:

```bash
cd backend
python -m alembic upgrade head
```

The Docker backend service already runs migrations before Uvicorn starts.

### `connection to server at "127.0.0.1", port 5432 failed`

Inside Docker, the backend must connect to PostgreSQL using the Compose service name:

```text
db
```

The Docker Compose backend uses:

```text
postgresql+psycopg://products:products@db:5432/products
```

For local non-Docker execution, `localhost:5432` is valid only if PostgreSQL is running on the host.

### `Bind for 0.0.0.0:8000 failed: port is already allocated`

Another process or container is using port `8000`.

Check Docker containers:

```bash
docker ps
```

Stop the conflicting container if appropriate:

```bash
docker stop <container-name>
```

Or change the backend port mapping in `docker-compose.yml`.

### `BACKEND_CORS_ORIGINS` parsing error

The settings model supports comma-separated values.

Example:

```env
BACKEND_CORS_ORIGINS=http://localhost:5173
```

For multiple origins:

```env
BACKEND_CORS_ORIGINS=http://localhost:5173,https://example.com
```

### Frontend cannot reach backend

Check `VITE_API_URL`.

Local default:

```env
VITE_API_URL=http://localhost:8000
```

Also confirm the backend is running:

```bash
curl http://localhost:8000/health
```

### Seed script takes time

The seed script inserts 200,000 products in batches of 10,000. Progress is printed after each batch.

## Future Improvements

- Add automated backend tests for pagination edge cases
- Add frontend tests for loading, error, and pagination states
- Add CI for linting, type-checking, and builds
- Add a dedicated migration job for production deployments
- Add optional category discovery endpoint instead of hardcoded frontend categories
- Add structured logging and request IDs
- Add health checks that verify database connectivity
- Add configurable seed size for faster local smoke tests

## License

No license file is currently included in this repository.

Add a license file before distributing or open-sourcing the project.
```
