# Flask Auth  +  Notes API

A production-ready, scalable RESTful API built with Flask, SQLAlchemy, and PostgreSQL. It features robust JWT-based user authentication, a complete Notes CRUD system, advanced querying (search, filter, sort, pagination), and centralized error handling.

This project is built using a modular application factory and Blueprint architecture, making it highly maintainable and easily extensible for future enterprise-level features.

## 🚀 Key Features

- **Authentication System**: Secure user registration and login using `Flask-Bcrypt` for password hashing and `Flask-JWT-Extended` for token-based authentication.
- **Notes Management**: Full CRUD operations (Create, Read, Update, Delete) for user-specific notes.
- **Advanced Querying**: 
  - Search notes by title or content
  - Filter by pinned status
  - Sort by title, created_at, or updated_at
  - Pagination to handle large datasets efficiently
- **Robust Error Handling**: Centralized exception management ensuring consistent, unified JSON error responses (400, 401, 404, 500).
- **Unit Testing**: Comprehensive automated testing using `pytest` and an isolated in-memory SQLite database.
- **Database Architecture**: SQLAlchemy ORM integrated with PostgreSQL and Flask-Migrate for version-controlled database schemas.

## 🛠️ Technology Stack

- **Backend Framework**: Python 3.x, Flask 3.x
- **Database**: PostgreSQL
- **ORM & Migrations**: SQLAlchemy, Flask-Migrate
- **Security**: Flask-JWT-Extended, Flask-Bcrypt
- **Testing**: Pytest

## 📋 Prerequisites

To run this project, you will need:
- Python 3.8+
- PostgreSQL server running locally or via Docker

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/flask-auth-notes.git
   cd flask-auth-notes
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory and add the following:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-super-secret-key
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/flask_auth_notes
   JWT_SECRET_KEY=your-jwt-super-secret-key
   ```
   *(Ensure you create a database named `flask_auth_notes` in your PostgreSQL instance)*

5. **Run Database Migrations**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Start the Application**
   ```bash
   python run.py
   ```
   The API will be available at `http://127.0.0.1:5000`

## 🧪 Running Tests

This project includes a suite of unit tests utilizing an in-memory SQLite database to ensure the development database remains isolated.

```bash
pytest
```

## 📖 API Documentation Summary

### Auth Endpoints
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Authenticate and retrieve JWT
- `GET /api/auth/profile` - View protected user profile (Requires Auth)

### Notes Endpoints (Require Auth)
- `GET /api/notes/` - Retrieve all notes (Supports `?search=`, `?is_pinned=`, `?sort_by=`, `?page=`)
- `POST /api/notes/` - Create a new note
- `GET /api/notes/<id>` - Retrieve a specific note
- `PUT /api/notes/<id>` - Update/Pin a note
- `DELETE /api/notes/<id>` - Delete a note

> **Note on Authorization:** 
> All protected routes require a Bearer token in the request header:
> `Authorization: Bearer <your_access_token>`

## 📝 License

This project is open-source and available under the MIT License.
