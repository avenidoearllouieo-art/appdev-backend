# Smart Locker System - Backend API Documentation

## Overview
The Smart Locker System backend is a Django REST Framework application that manages smart locker operations, user authentication, and locker status tracking for Mobile and Web UI integration.

## Technology Stack
- **Framework**: Django 6.0.3
- **API**: Django REST Framework
- **Database**: SQLite3
- **Authentication**: Token Authentication
- **CORS**: Enabled for frontend access

---

## API Endpoints

### Authentication Endpoints

#### 1. User Registration
**POST** `/api/register/`

Register a new user and receive authentication token.

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "",
    "last_name": ""
  },
  "token": "afe282cef51fc1047472df17e3af4fb462bf0726",
  "message": "User registered successfully"
}
```

**Possible Errors:**
- `400 Bad Request`: Username or email already exists
- `400 Bad Request`: Missing required fields

---

#### 2. User Login
**POST** `/api/login/`

Login with username and password, receive authentication token.

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "",
    "last_name": ""
  },
  "token": "afe282cef51fc1047472df17e3af4fb462bf0726",
  "message": "Login successful"
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid credentials

---

#### 3. User Logout
**POST** `/api/logout/`

Logout and invalidate authentication token.

**Headers:**
```
Authorization: Token afe282cef51fc1047472df17e3af4fb462bf0726
```

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

**Possible Errors:**
- `401 Unauthorized`: Not authenticated

---

### Locker Endpoints

#### 4. Get All Lockers
**GET** `/api/lockers/`

Retrieve all lockers with their current status.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "number": 1,
    "status": "Available",
    "owner": null,
    "time_left": 0
  },
  {
    "id": 2,
    "number": 2,
    "status": "In Use",
    "owner": "john_doe",
    "time_left": 45
  }
]
```

---

#### 5. Get Locker Details
**GET** `/api/lockers/{id}/`

Get details of a specific locker.

**Response (200 OK):**
```json
{
  "id": 1,
  "number": 1,
  "status": "Available",
  "owner": null,
  "time_left": 0
}
```

**Possible Errors:**
- `404 Not Found`: Locker does not exist

---

#### 6. Open Locker
**POST** `/api/lockers/{id}/open/`

Open a locker - assigns current user as owner and starts timer.

**Headers:**
```
Authorization: Token afe282cef51fc1047472df17e3af4fb462bf0726
```

**Response (200 OK):**
```json
{
  "id": 1,
  "number": 1,
  "status": "In Use",
  "owner": "john_doe",
  "time_left": 60
}
```

**Possible Errors:**
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: Locker does not exist
- `400 Bad Request`: Locker is not available

---

#### 7. Update Locker (Timer/Status)
**PUT/PATCH** `/api/lockers/{id}/`

Update locker status or timer. When `time_left` reaches 0, locker automatically resets.

**Headers:**
```
Authorization: Token afe282cef51fc1047472df17e3af4fb462bf0726
```

**Request Body (Update Timer):**
```json
{
  "time_left": 30
}
```

**Request Body (Timer Expiration - Reset):**
```json
{
  "time_left": 0
}
```

**Response (200 OK) - Timer Updated:**
```json
{
  "id": 1,
  "number": 1,
  "status": "In Use",
  "owner": "john_doe",
  "time_left": 30
}
```

**Response (200 OK) - Timer Expired (Auto-Reset):**
```json
{
  "id": 1,
  "number": 1,
  "status": "Available",
  "owner": null,
  "time_left": 0
}
```

**Possible Errors:**
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Only admin or locker owner can update
- `404 Not Found`: Locker does not exist

---

#### 8. Delete Locker
**DELETE** `/api/lockers/{id}/`

Delete a locker (admin only).

**Headers:**
```
Authorization: Token afe282cef51fc1047472df17e3af4fb462bf0726
```

**Response (204 No Content):**
```
(empty)
```

**Possible Errors:**
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Only admin can delete
- `404 Not Found`: Locker does not exist

---

## Locker Object Structure

```json
{
  "id": 1,
  "number": 1,
  "status": "Available",
  "owner": null,
  "time_left": 0
}
```

### Fields:
- **id** (integer): Unique locker identifier
- **number** (integer): Locker number/label (1-10, etc.)
- **status** (string): Current status - `"Available"` or `"In Use"`
- **owner** (string|null): Username of current owner, `null` if available
- **time_left** (integer): Seconds remaining on timer, `0` if not in use

---

## Locker Logic Flow

### 1. Default State
```
Status: Available
Owner: null
Time Left: 0
```

### 2. When User Opens Locker
```
Status: "Available" → "In Use"
Owner: null → "username"
Time Left: 0 → 60 (seconds)
```

### 3. Timer Counting Down
```
Frontend updates time_left via PATCH /api/lockers/{id}/
Time Left: 60 → 59 → 58 → ... → 1
```

### 4. Timer Expires (time_left reaches 0)
```
PATCH /api/lockers/{id}/ with {"time_left": 0}
Status: "In Use" → "Available"
Owner: "username" → null
Time Left: 1 → 0
```

---

## Authentication

### Token-Based Authentication
All protected endpoints require an `Authorization` header:

```
Authorization: Token <your_token_here>
```

**Example:**
```bash
curl -H "Authorization: Token afe282cef51fc1047472df17e3af4fb462bf0726" \
     http://127.0.0.1:8000/api/lockers/1/open/
```

### Obtaining a Token
1. **After Registration** - Token is returned in response
2. **After Login** - Token is returned in response
3. **Token Invalidation** - Logout endpoint invalidates token

---

## CORS Configuration

CORS is enabled for all origins in development:
```python
CORS_ALLOW_ALL_ORIGINS = True
```

> **Note**: For production, configure specific origins:
> ```python
> CORS_ALLOWED_ORIGINS = [
>     "https://yourdomain.com",
>     "https://app.yourdomain.com",
> ]
> ```

---

## Django Admin Panel

### Access
- **URL**: `http://127.0.0.1:8000/admin/`
- **Credentials**: Admin username/password (created via `python manage.py createsuperuser`)

### Manageable Models
1. **Users** - View all registered users
2. **Lockers** - Manage locker status, owner, timer
3. **User Profiles** - User bio and metadata
4. **Activity Logs** - Track all user actions

---

## Project Structure

```
backend/
├── backend/              # Main project settings
│   ├── settings.py       # Configuration (CORS, Database, Apps)
│   ├── urls.py           # Main URL router
│   ├── asgi.py           # ASGI config
│   └── wsgi.py           # WSGI config
├── lockers/              # Main app
│   ├── models.py         # Database models (User, Locker, etc.)
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # API endpoint handlers
│   ├── urls.py           # App URL routing
│   ├── admin.py          # Django Admin configuration
│   ├── migrations/       # Database migrations
│   └── tests.py          # Unit tests
├── manage.py             # Django management script
├── db.sqlite3            # SQLite database
├── test_api.py           # API test suite
├── setup_lockers.py      # Sample data initialization
└── README.md             # This file
```

---

## Models

### User (Django Built-in)
```python
id              - Auto-generated primary key
username        - Unique username
email           - User email
first_name      - First name (optional)
last_name       - Last name (optional)
is_staff        - Admin flag
is_active       - Active status
date_joined     - Account creation date
```

### Locker
```python
id              - Auto-generated primary key
number          - Locker number (e.g., 1-10)
status          - "Available" or "In Use"
owner           - ForeignKey to User (nullable)
time_left       - Remaining seconds (default: 0)
is_active       - Active status (default: True)
created_at      - Creation timestamp (auto)
updated_at      - Last update timestamp (auto)
```

### UserProfile
```python
user            - OneToOne relationship to User
bio             - User biography
created_at      - Creation timestamp
updated_at      - Last update timestamp
```

### ActivityLog
```python
user            - ForeignKey to User
action          - Action description
timestamp       - When action occurred
```

---

## Setup & Running

### 1. Install Dependencies
```bash
pip install django djangorestframework django-cors-headers
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Sample Lockers
```bash
python setup_lockers.py
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```

### 5. Start Development Server
```bash
python manage.py runserver
```

Server runs at: `http://127.0.0.1:8000/`

---

## Testing

### Run Comprehensive API Test Suite
```bash
python test_api.py
```

**Test Coverage:**
- ✓ User Registration
- ✓ User Login
- ✓ Get All Lockers
- ✓ Open Locker
- ✓ Update Locker (Timer)
- ✓ User Logout

---

## Frontend Integration Examples

### JavaScript (React/Vue/Flutter)

**Register**
```javascript
const response = await fetch('http://127.0.0.1:8000/api/register/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'john_doe',
    email: 'john@example.com',
    password: 'password123'
  })
});
const data = await response.json();
const token = data.token;
```

**Login**
```javascript
const response = await fetch('http://127.0.0.1:8000/api/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'john_doe',
    password: 'password123'
  })
});
const data = await response.json();
const token = data.token;
```

**Get Lockers**
```javascript
const response = await fetch('http://127.0.0.1:8000/api/lockers/');
const lockers = await response.json();
```

**Open Locker**
```javascript
const response = await fetch('http://127.0.0.1:8000/api/lockers/1/open/', {
  method: 'POST',
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  }
});
const locker = await response.json();
```

**Update Timer**
```javascript
const response = await fetch('http://127.0.0.1:8000/api/lockers/1/', {
  method: 'PATCH',
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ time_left: 30 })
});
const locker = await response.json();
```

**Logout**
```javascript
const response = await fetch('http://127.0.0.1:8000/api/logout/', {
  method: 'POST',
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  }
});
```

---

## Error Handling

All errors return appropriate HTTP status codes:

| Status Code | Meaning |
|---|---|
| `200 OK` | Successful GET, POST, or PATCH |
| `201 Created` | Successful resource creation |
| `204 No Content` | Successful deletion |
| `400 Bad Request` | Invalid data or validation error |
| `401 Unauthorized` | Authentication required or failed |
| `403 Forbidden` | Permission denied |
| `404 Not Found` | Resource does not exist |

**Error Response Format:**
```json
{
  "error": "Error message here",
  "message": "Additional details (if available)"
}
```

---

## Key Features

✓ **Token-Based Authentication** - Secure user sessions  
✓ **CORS Enabled** - Works with Web and Mobile UIs  
✓ **Activity Logging** - Track all user actions  
✓ **Admin Panel** - Manage users and lockers  
✓ **Clean JSON Responses** - Frontend-friendly data format  
✓ **Timer Management** - Automatic locker reset  
✓ **User Profiles** - Extensible user data  
✓ **Permission System** - Admin and user-level controls  

---

## Production Checklist

- [ ] Change `DEBUG = False` in settings.py
- [ ] Update `ALLOWED_HOSTS` with production domain
- [ ] Configure `CORS_ALLOWED_ORIGINS` for specific frontend URLs
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set `SECRET_KEY` from environment variable
- [ ] Enable HTTPS only
- [ ] Set up proper logging
- [ ] Configure static files serving
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Set up database backups

---

## Support & Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Errors
```bash
python manage.py migrate
python manage.py migrate --fake-initial
```

### Create New Admin
```bash
python manage.py createsuperuser
```

### Reset Database
```bash
rm db.sqlite3
python manage.py migrate
python setup_lockers.py
```

---

## Version Info
- Django: 6.0.3
- Django REST Framework: Latest
- Python: 3.9+
- Created: May 2026
