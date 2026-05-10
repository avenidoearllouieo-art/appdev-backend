# Smart Locker System - API Usage Guide

## Quick Start

### 1. Start the Django Development Server

```bash
cd c:\Users\Avenido\appdev-backend\backend
python manage.py runserver
```

Server runs at: `http://127.0.0.1:8000`

---

## API Endpoints

### **1. POST /api/register/ - Create New User**

**Purpose:** Register a new user and get authentication token

**URL:** `http://127.0.0.1:8000/api/register/`

**Method:** POST

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "",
    "last_name": ""
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "User registered successfully"
}
```

**Error Response (400):**
```json
{
  "success": false,
  "errors": {
    "username": ["This username is already taken"]
  },
  "message": "Registration failed"
}
```

**Using cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

**Using Python:**
```python
import requests

url = "http://127.0.0.1:8000/api/register/"
data = {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123"
}
response = requests.post(url, json=data)
print(response.json())
```

**Using JavaScript/Fetch:**
```javascript
const url = "http://127.0.0.1:8000/api/register/";
const data = {
  username: "john_doe",
  email: "john@example.com",
  password: "securepass123"
};

fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### **2. POST /api/login/ - User Login**

**Purpose:** Authenticate user and get token

**URL:** `http://127.0.0.1:8000/api/login/`

**Method:** POST

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "securepass123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "",
    "last_name": ""
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "Login successful"
}
```

**Error Response (401):**
```json
{
  "success": false,
  "error": "Invalid username or password",
  "message": "Login failed"
}
```

**Using cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

---

### **3. GET /api/lockers/ - Get All Lockers**

**Purpose:** Retrieve all lockers from database

**URL:** `http://127.0.0.1:8000/api/lockers/`

**Method:** GET

**Authentication:** Optional (add token if needed)

**Request Headers (Optional):**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Success Response (200):**
```json
{
  "success": true,
  "count": 10,
  "lockers": [
    {
      "id": 1,
      "locker_number": 1,
      "status": "Available",
      "rented_by": null,
      "rental_hours": 0,
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "locker_number": 2,
      "status": "Occupied",
      "rented_by": "john_doe",
      "rental_hours": 2,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Using cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/lockers/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Using JavaScript:**
```javascript
const token = "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b";

fetch("http://127.0.0.1:8000/api/lockers/", {
  method: "GET",
  headers: {
    "Authorization": `Token ${token}`
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### **4. POST /api/lockers/{id}/rent/ - Rent a Locker**

**Purpose:** Rent (occupy) a locker for the authenticated user

**URL:** `http://127.0.0.1:8000/api/lockers/1/rent/`

**Method:** POST

**Authentication Required:** YES

**Request Headers:**
```
Content-Type: application/json
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Request Body:**
```json
{
  "rental_hours": 2
}
```

**Success Response (200):**
```json
{
  "success": true,
  "locker": {
    "id": 1,
    "locker_number": 1,
    "status": "Occupied",
    "rented_by": "john_doe",
    "rental_hours": 2,
    "created_at": "2024-01-15T10:30:00Z"
  },
  "message": "Locker rented successfully"
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Locker is not available (currently Occupied)",
  "message": "Failed to rent locker"
}
```

**Error Response (401):**
```json
{
  "success": false,
  "error": "Authentication required",
  "message": "Authentication failed"
}
```

**Error Response (404):**
```json
{
  "success": false,
  "error": "Locker not found",
  "message": "Invalid locker ID"
}
```

**Using cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/lockers/1/rent/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -d '{
    "rental_hours": 2
  }'
```

**Using JavaScript:**
```javascript
const token = "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b";
const lockerId = 1;

fetch(`http://127.0.0.1:8000/api/lockers/${lockerId}/rent/`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Token ${token}`
  },
  body: JSON.stringify({
    rental_hours: 2
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### **5. POST /api/lockers/{id}/release/ - Release a Locker**

**Purpose:** Release (return) a rented locker back to available

**URL:** `http://127.0.0.1:8000/api/lockers/1/release/`

**Method:** POST

**Authentication Required:** YES

**Request Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Request Body:** Empty
```json
{}
```

**Success Response (200):**
```json
{
  "success": true,
  "locker": {
    "id": 1,
    "locker_number": 1,
    "status": "Available",
    "rented_by": null,
    "rental_hours": 0,
    "created_at": "2024-01-15T10:30:00Z"
  },
  "message": "Locker released successfully"
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Locker is not in use (currently Available)",
  "message": "Failed to release locker"
}
```

**Using cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/lockers/1/release/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -d '{}'
```

**Using JavaScript:**
```javascript
const token = "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b";
const lockerId = 1;

fetch(`http://127.0.0.1:8000/api/lockers/${lockerId}/release/`, {
  method: "POST",
  headers: {
    "Authorization": `Token ${token}`
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### **6. /admin/ - Django Admin Interface**

**Purpose:** Manage lockers and users through web interface

**URL:** `http://127.0.0.1:8000/admin/`

**Method:** Access in browser

**Steps:**
1. Open browser: `http://127.0.0.1:8000/admin/`
2. Login with Django admin credentials:
   - Username: (create with `python manage.py createsuperuser`)
   - Password: (your password)
3. Browse and manage:
   - Lockers
   - Users
   - Tokens

---

## Complete Workflow Example

### Step-by-Step API Usage:

```bash
# 1. Register a new user
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "alice123456"
  }'

# Response includes token: "abc123def456..."

# 2. Get all lockers
curl -X GET http://127.0.0.1:8000/api/lockers/ \
  -H "Authorization: Token abc123def456..."

# 3. Rent locker 1 for 3 hours
curl -X POST http://127.0.0.1:8000/api/lockers/1/rent/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token abc123def456..." \
  -d '{"rental_hours": 3}'

# 4. Release locker 1
curl -X POST http://127.0.0.1:8000/api/lockers/1/release/ \
  -H "Authorization: Token abc123def456..." \
  -d '{}'

# 5. Login with credentials
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "alice123456"
  }'
```

---

## Testing Tools

### Using Postman:
1. Import requests (or create manually)
2. Set method (GET/POST)
3. Enter URL
4. Add headers
5. Add body (JSON)
6. Click Send

### Using Python requests:
```python
import requests

BASE_URL = "http://127.0.0.1:8000/api"

# Register
response = requests.post(f"{BASE_URL}/register/", json={
    "username": "bob",
    "email": "bob@example.com",
    "password": "bob123456"
})
token = response.json()["token"]

# Get lockers
response = requests.get(f"{BASE_URL}/lockers/", 
    headers={"Authorization": f"Token {token}"})
print(response.json())

# Rent locker
response = requests.post(f"{BASE_URL}/lockers/1/rent/",
    headers={"Authorization": f"Token {token}"},
    json={"rental_hours": 2})
print(response.json())
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Method not allowed" | Use correct HTTP method (POST/GET) |
| "Authentication failed" | Include `Authorization: Token <token>` header |
| "Locker not found" | Check locker ID exists (1-10) |
| "Locker not available" | Try a different locker with `status: Available` |
| "Invalid token" | Generate new token with login endpoint |

---

## Status Codes

- `200` - Success (GET, successful POST operations)
- `201` - Created (user registration)
- `400` - Bad request (validation error)
- `401` - Unauthorized (authentication required)
- `404` - Not found (locker doesn't exist)
- `500` - Server error

---

## Ready to Test?

1. Start server: `python manage.py runserver`
2. Try endpoints above
3. Check responses
4. Access admin: `http://127.0.0.1:8000/admin/`

Happy testing! 🚀
