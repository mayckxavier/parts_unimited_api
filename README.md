# Parts Unlimited API

A REST API for Parts Unlimited product catalog that allows for CRUD operations on parts.

## Setup

1. This project is using Python 3.11.7
2. Clone this repository
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Set up environment variables (copy `.env.example` to `.env` and adjust values)
7. Run database migrations: `alembic upgrade head`. (This will create the SQLite Database and add some data)
8. Start the application: `uvicorn main:app --reload`
9. To access documentation just add `/docs` at the end of the URL. Example: `http://127.0.0.1:8000/docs`

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
