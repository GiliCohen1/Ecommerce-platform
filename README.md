# Mini E-Commerce Platform

A full-stack mini e-commerce application for digital products (e-books, software licenses, online courses)..

**Stack:** Vue 3 + TypeScript + Pinia + Tailwind CSS + PrimeVue | Python FastAPI + Redis

---

## Quick Start (Docker — recommended)

> Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) to be running.

```bash
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:8081 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

---

## Manual Setup (without Docker)

### Prerequisites

| Tool | Min version |
|---|---|
| Node.js | 18+ |
| Python | 3.12+ |
| Redis | 7+ (optional — app works without it) |

---

### 1. Backend

```bash
cd backend

# Copy env file (edit REDIS_URL if you have Redis running)
cp .env.example .env          # Mac / Linux
copy .env.example .env        # Windows

# Install dependencies
pip install -r requirements.txt       # Mac / Linux
py -m pip install -r requirements.txt # Windows

# Start the server
uvicorn app.main:app --reload         # Mac / Linux
py -m uvicorn app.main:app --reload   # Windows
```

API runs at **http://localhost:8000**  
Interactive API docs at **http://localhost:8000/docs**

---

### 2. Frontend

Open a new terminal:

```bash
cd frontend

# Copy env file
cp .env.example .env          # Mac / Linux
copy .env.example .env        # Windows

# Install dependencies
npm install

# Start the dev server
npm run dev
```

App runs at **http://localhost:8081**

---

### 3. Redis (optional)

If you have Docker available but don't want to run the full compose stack:

```bash
docker run -p 6379:6379 redis:7-alpine
```

Without Redis the app works fine — product responses are served directly from memory and a 30-second reconnect cooldown prevents any extra latency.

---

## Running Tests

### Backend

```bash
cd backend
pytest app/tests/ -v                  # Mac / Linux
py -m pytest app/tests/ -v           # Windows
```

### Frontend

```bash
cd frontend
npm run test
```

---

## API Documentation

### GET /products

Returns a filtered and sorted list of product summaries.

| Query param | Type | Default | Description |
|---|---|---|---|
| `name` | string | — | Case-insensitive substring match on product name |
| `category` | `online-course` \| `ebook` \| `software-license` | — | Exact category filter |
| `sort_by` | `name` \| `price` | `name` | Sort field |
| `order` | `asc` \| `desc` | `asc` | Sort direction |

**Response 200:**
```json
{
  "data": [
    {
      "id": "prod-001",
      "name": "Python Mastery Course",
      "price": 49.99,
      "shortDescription": "Go from beginner to advanced Python developer in 40 hours.",
      "thumbnailUrl": "https://picsum.photos/seed/prod001/400/300",
      "category": "online-course"
    }
  ],
  "total": 1,
  "filters": { "name": "python", "category": null, "sort_by": "price", "order": "asc" }
}
```

### GET /products/{id}

Returns full product details including long description and reviews.

**Response 200:**
```json
{
  "id": "prod-001",
  "name": "Python Mastery Course",
  "price": 49.99,
  "shortDescription": "...",
  "thumbnailUrl": "...",
  "category": "online-course",
  "longDescription": "A comprehensive 40-hour video course...",
  "reviews": [
    { "id": "rev-001", "author": "Alice K.", "rating": 5, "comment": "Best Python course!", "date": "2025-11-15" }
  ]
}
```

**Response 404:**
```json
{ "detail": "Product with id 'xyz' not found." }
```

### GET /health

```json
{ "status": "ok", "redis": "connected" }
```

---

## Architecture Decisions

### Cart: client-side only (Pinia)

The shopping cart is managed entirely in the Vue frontend via a Pinia store. No server-side cart endpoints exist because:

- The spec involves digital products with no user accounts or session persistence requirements
- The assignment explicitly permits this: *"handle cart client-side via Pinia if cart is not meant to persist server-side"*
- It keeps the backend focused on product data and makes the cart store trivially unit-testable with Vitest

### Redis caching

Product list and detail responses are cached in Redis with TTL values:
- Filtered product lists: 120–300 seconds
- Single product details: 600 seconds

If Redis is unavailable, a 30-second circuit breaker prevents repeated reconnect attempts on every request. All responses continue to be served from the in-memory JSON store with no extra latency.

### FastAPI over Flask

FastAPI was chosen for its auto-generated Swagger UI (`/docs`), built-in request validation via Pydantic, and native async support.

---

## Project Structure

```
ecommerce-platform/
├── docker-compose.yml
├── frontend/               # Vue 3 + TypeScript (port 8081)
│   └── src/
│       ├── types/          # TypeScript interfaces (Product, CartItem, etc.)
│       ├── api/            # Axios HTTP layer
│       ├── stores/         # Pinia cart store
│       ├── router/         # Vue Router routes
│       ├── components/     # Reusable UI components
│       ├── views/          # Page-level components
│       └── tests/          # Vitest unit tests
└── backend/                # Python FastAPI (port 8000)
    └── app/
        ├── data/           # products.json mock database
        ├── models/         # Pydantic response models
        ├── services/       # Business logic + Redis cache
        ├── routers/        # HTTP route handlers
        └── tests/          # pytest unit tests
```
