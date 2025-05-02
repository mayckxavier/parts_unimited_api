# Parts Unlimited API

A REST API for Parts Unlimited product catalog that allows for CRUD operations on parts.

## Setup

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables (copy `.env.example` to `.env` and adjust values)
6. Run database migrations: `alembic upgrade head`
7. Start the application: `uvicorn main:app --reload`

## Features

- CRUD operations for parts catalog
- Analytics endpoint for most common words in part descriptions

## API Endpoints

- GET /api/v1/parts - List all parts
- GET /api/v1/parts/{id} - Get part by ID
- POST /api/v1/parts - Create new part
- PUT /api/v1/parts/{id} - Update part
- DELETE /api/v1/parts/{id} - Delete part
- GET /api/v1/parts/common-words - Get most common words in part descriptions
