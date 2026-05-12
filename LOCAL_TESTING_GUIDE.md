# Beginner's Guide: Running and Testing the Flask API

Welcome to your new Flask Auth + Notes API! This guide will walk you through every step of running this backend on your local machine and testing the endpoints.

---

## 🛠️ Part 1: Project Setup

Before you start, make sure you have **Python 3** and **PostgreSQL** installed on your computer.

### Step 1: Open the Terminal
Open your terminal (PowerShell or Command Prompt) and navigate to the project directory:
```powershell
cd d:\projects\flask-auth-notes
```

### Step 2: Create a Virtual Environment
A virtual environment keeps your project's Python packages isolated from other projects.
```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment
You must activate the virtual environment every time you work on this project in a new terminal.
```powershell
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# (If it fails due to execution policies, run this first: Set-ExecutionPolicy Unrestricted -Scope CurrentUser)
```
*You will know it worked if you see `(venv)` at the beginning of your terminal prompt.*

### Step 4: Install Dependencies
Now install all the required libraries (Flask, SQLAlchemy, etc.):
```powershell
pip install -r requirements.txt
```

---

## 🗄️ Part 2: Database & Environment Setup

### Step 5: Configure the Database
Open PostgreSQL (using pgAdmin, `psql`, or a DB viewer) and create an empty database specifically for this app.
```sql
CREATE DATABASE flask_auth_notes;
```

### Step 6: Configure your `.env` File
Ensure your `.env` file looks like this. Make sure the username and password match your PostgreSQL setup (usually `postgres` / `postgres`).

```env
# d:\projects\flask-auth-notes\.env
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=super-secret-flask-key

# FORMAT: postgresql://USERNAME:PASSWORD@localhost:5432/DATABASE_NAME
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/flask_auth_notes
JWT_SECRET_KEY=super-secret-jwt-key
```

### Step 7: Run Database Migrations
Migrations automatically create the necessary tables (`users` and `notes`) in your PostgreSQL database based on our Python code.
```powershell
# Initialize the migrations folder (run only once per project)
flask db init

# Create a migration script based on your models
flask db migrate -m "Initial migration"

# Apply the script to actually create the tables in PostgreSQL
flask db upgrade
```

### Step 8: Start the Server
Run the Flask development server:
```powershell
python run.py
```
You should see output saying the server is running on `http://127.0.0.1:5000/`. Leave this terminal window open!

---

## 🧪 Part 3: Testing with Postman (or Thunder Client)

Now that the server is running, we will act as the "Frontend" making requests to our Backend.

### 1. Register a User
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/api/auth/register`
- **Body (Raw -> JSON):**
  ```json
  {
      "username": "ayush",
      "email": "ayush@example.com",
      "password": "mysecurepassword"
  }
  ```
- **Click Send.** You should receive a `201 Created` status with a success message.

### 2. Login to get a JWT Token
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/api/auth/login`
- **Body (Raw -> JSON):**
  ```json
  {
      "username": "ayush",
      "password": "mysecurepassword"
  }
  ```
- **Click Send.**
- **Important:** Look at the response! You will see an `access_token` string. **Copy this string.**

### 3. Understanding Authorization Headers
For any protected route (like viewing notes), the API needs to know *who* you are. We don't send the username/password every time. Instead, we send the `access_token` in the **Headers**.
In Postman:
1. Go to the **Headers** tab (or **Auth** tab -> Bearer Token).
2. Key: `Authorization`
3. Value: `Bearer <paste_your_copied_token_here>` *(Note the space after the word Bearer)*

### 4. Create a Note
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/api/notes/`
- **Headers:** Add the `Authorization: Bearer <token>`
- **Body (Raw -> JSON):**
  ```json
  {
      "title": "Learn Flask",
      "content": "Flask with JWT is awesome!"
  }
  ```

### 5. Get All Notes (with sorting)
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/api/notes/?sort_by=created_at&sort_order=desc`
- **Headers:** Add the `Authorization: Bearer <token>`
- **Click Send.** You'll see your notes listed inside the JSON response. Grab the `id` of your note to use in the next step.

### 6. Update/Pin a Note
- **Method:** `PUT`
- **URL:** `http://127.0.0.1:5000/api/notes/<NOTE_ID_HERE>`
- **Headers:** Add the `Authorization: Bearer <token>`
- **Body (Raw -> JSON):**
  ```json
  {
      "is_pinned": true
  }
  ```

---

## 🧠 Part 4: How It All Works

### 1. Database Data Flow
When you create a note:
1. The request hits `app/routes/note_routes.py`.
2. Flask extracts the `user_id` from your JWT token.
3. The route passes data to `app/services/note_service.py`.
4. The service creates a `Note` object via SQLAlchemy and links it to your `user_id`.
5. `db.session.commit()` translates this into an `INSERT INTO notes ...` SQL command in PostgreSQL.

### 2. Token Usage (JWT)
JSON Web Tokens (JWT) are secure strings generated by the server. 
- When you login, the server verifies your password using `bcrypt`, generates a JWT that essentially says *"This is user ID #1"*, signs it cryptographically with the `JWT_SECRET_KEY`, and hands it to you.
- Every time you send the token back in the `Authorization` header, the `@jwt_required()` decorator in Flask intercepts the request, verifies the signature mathematically, and allows the request through. No database lookup is needed just to verify who you are!

### 3. Common Errors You Might See

| HTTP Status | What it means | Common Cause |
| :--- | :--- | :--- |
| **401 Unauthorized** | Missing or Invalid Token | You forgot the `Authorization` header, misspelled `Bearer`, or your token expired. |
| **400 Bad Request** | Validation Error | You forgot to include a required field like `title` in your JSON body. |
| **404 Not Found** | Resource Missing | You tried to update a note ID that doesn't exist, or a URL that is misspelled. |
| **500 Internal Error** | Server Crashed | Usually caused by a database connection error (is PostgreSQL running?) or a bug in the code. Check the Python terminal for the stack trace! |
