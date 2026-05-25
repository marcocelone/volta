# Lucky Call API - Example api 

A REST API built with **Flask**, **Flask-JWT-Extended**, and **Flask-SQLAlchemy**.

Keywords and results are stored in a **SQLite** database for convenience.

---

## How It Works

- The `/keyword` endpoints are **admin-only** — they require a valid JWT access token belonging to an admin user. The admin submits a keyword to the DB once it has been broadcast.
- Regular users must **register** (if new) or **login** to receive a JWT access token.
- The access token must be sent in the `Authorization` header to submit a result via `/results`.

> Full endpoint documentation on Swagger: [LuckyCall API Docs](https://app.swaggerhub.com/apis-docs/self7732/LuckyCall/1.0.0#/)

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/marcocelone/volta.git
cd volta
```

### 2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install requirements
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

The API will be available at: `http://127.0.0.1:5000`

---

## Endpoints

### Register — `POST /register`

Create a new user account.

```json
{
  "username": "marco",
  "password": "marco"
}
```

---

### Login — `POST /login`

Returns a JWT access token to use in subsequent requests.

```json
{
  "username": "marco",
  "password": "marco"
}
```

**Response:**
```json
{
  "access_token": "<your_jwt_token>"
}
```

---

### Submit Keyword *(admin only)* — `POST /keyword`

Requires `Authorization: Bearer <admin_token>` header.

```json
{
  "keyword": "my_keyword"
}
```

**Example curl:**
```bash
curl -X POST "http://127.0.0.1:5000/keyword" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <admin_token>" \
  -d '{"keyword": "my_keyword"}'
```

---

### List Keywords *(admin only)* — `GET /keywords`

Requires `Authorization: Bearer <admin_token>` header.

---

### Submit Result — `POST /results`

Requires `Authorization: Bearer <token>` header. Submit a keyword and a 3-digit number to check if you are a winner.

```json
{
  "keyword": "my_keyword",
  "number": 121
}
```

**Example curl:**
```bash
curl -X POST "http://127.0.0.1:5000/results" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token>" \
  -d '{"keyword": "my_keyword", "number": 121}'
```

---

## Possible Improvements

- **Admin access control** — Admin endpoints are now JWT-protected with an `is_admin` claim. ✅
  - When registering, pass `"is_admin": true` to create an admin user.
  - On login, the `is_admin` flag is embedded as a custom claim inside the JWT token.
  - The `/keyword` (POST, DELETE) and `/keywords` (GET) endpoints use an `@admin_required` decorator that validates the token **and** checks the `is_admin` claim — returning `403 Forbidden` if the claim is missing or false.
  - Regular users with a valid token will still be denied access to these endpoints.
- **Replace SQLite** — Use **Redis** as a fast in-memory store for active contest data and **MySQL** as a persistent store for user info and winners.
- **Better error handling** — More descriptive error messages and HTTP status codes across all endpoints.
- **Environment-based config** — Move secrets like `JWT_SECRET_KEY` to environment variables (e.g. via `python-dotenv`).

---

## Notes on Fairness & Testing

I feel that challenges like this are more naturally suited to developers. As a **QA Engineer**, my typical approach to an application like this would be to build a dedicated testing framework — using the **`requests`** library with **`pytest`** to drive the API, validate responses, and generate structured reports. Nonetheless, this was a lot of fun!
