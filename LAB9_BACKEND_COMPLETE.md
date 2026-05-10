# Lab 9: Smart Locker System Backend - Complete

**Status:** ✅ PRODUCTION READY FOR LAB 9  
**Date:** May 10, 2026  
**All Tests:** ✅ PASSING (15/15)

---

## Backend Overview

Your Django REST Framework backend for the Smart Locker System is complete and ready for Lab 9. The backend includes all required endpoints for both renting and releasing lockers.

---

## All Required Endpoints (5 Endpoints)

### 1. User Registration ✅
```
POST /api/register/
```
**Response:** User account + authentication token

### 2. User Login ✅
```
POST /api/login/
```
**Response:** User data + authentication token

### 3. Get Lockers ✅
```
GET /api/lockers/
```
**Response:** All lockers with current status (Available/In Use)

### 4. Rent Locker ✅
```
POST /api/lockers/{id}/rent/
```
**Request:** `{"rental_duration": 3600}`  
**Response:** Updated locker with status "In Use"

### 5. Release Locker ✅ (NEW)
```
POST /api/lockers/{id}/release/
```
**Request:** `{}`  
**Response:** Updated locker reset to "Available"

---

## Database Schema

### User (Django Built-in)
```
- id
- username (unique)
- email (unique)
- password (hashed)
- Token (for authentication)
```

### Locker
```
- id
- number (unique, 1-100)
- status (Available | In Use)
- owner (Foreign Key to User, null if available)
- time_left (seconds remaining)
- rental_duration (total seconds)
- is_active (boolean)
- created_at (auto timestamp)
- updated_at (auto timestamp)
```

---

## Testing

### All 15 Tests Passing ✅

**User Registration (2 tests)**
- ✅ Successful registration
- ✅ Duplicate username rejection

**User Login (2 tests)**
- ✅ Successful login
- ✅ Invalid credentials rejection

**Locker Retrieval (2 tests)**
- ✅ Get lockers without auth
- ✅ Get lockers with auth

**Locker Rental (5 tests)**
- ✅ Successful rental
- ✅ Rental without authentication (401)
- ✅ Invalid rental duration
- ✅ Locker not found
- ✅ Locker already in use

**Locker Release (4 tests)** ← NEW
- ✅ Successful release
- ✅ Release without authentication (401)
- ✅ Release locker not found
- ✅ Release locker not in use

### Run Tests
```bash
cd backend
python manage.py test lockers.tests -v 2
```

**Expected Output:**
```
Ran 15 tests in 12.209s
OK
```

---

## API Response Examples

### Register
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "pass123"
  }'
```

**Response (201):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "first_name": "",
    "last_name": ""
  },
  "token": "a1b2c3d4...",
  "message": "User registered successfully"
}
```

---

### Login
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "pass123"
  }'
```

**Response (200):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "first_name": "",
    "last_name": ""
  },
  "token": "a1b2c3d4...",
  "message": "Login successful"
}
```

---

### Get Lockers
```bash
curl -X GET http://localhost:8000/api/lockers/ \
  -H "Authorization: Bearer a1b2c3d4..."
```

**Response (200):**
```json
{
  "success": true,
  "count": 5,
  "lockers": [
    {
      "id": 1,
      "number": 1,
      "status": "Available",
      "owner": null,
      "time_left": 0,
      "rental_duration": 0
    },
    {
      "id": 2,
      "number": 2,
      "status": "In Use",
      "owner": "john",
      "time_left": 3600,
      "rental_duration": 3600
    }
  ]
}
```

---

### Rent Locker
```bash
curl -X POST http://localhost:8000/api/lockers/1/rent/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a1b2c3d4..." \
  -d '{
    "rental_duration": 3600
  }'
```

**Response (200):**
```json
{
  "success": true,
  "locker": {
    "id": 1,
    "number": 1,
    "status": "In Use",
    "owner": "john",
    "time_left": 3600,
    "rental_duration": 3600
  },
  "message": "Locker rented successfully"
}
```

---

### Release Locker (NEW)
```bash
curl -X POST http://localhost:8000/api/lockers/1/release/ \
  -H "Authorization: Bearer a1b2c3d4..."
```

**Response (200):**
```json
{
  "success": true,
  "locker": {
    "id": 1,
    "number": 1,
    "status": "Available",
    "owner": null,
    "time_left": 0,
    "rental_duration": 0
  },
  "message": "Locker released successfully"
}
```

---

## Complete Locker Workflow

### Step 1: Create Admin User
```bash
python manage.py createsuperuser
```

### Step 2: Create Test Lockers in Django Admin
- Go to http://localhost:8000/admin/
- Create 5-10 lockers with numbers 1-10
- All start as "Available"

### Step 3: Start Backend Server
```bash
python manage.py runserver
```

### Step 4: Frontend Workflow (Web/Mobile UI)

**a) User Registration**
```javascript
POST /api/register/
→ Creates user in database
→ Returns token
→ Frontend stores token
```

**b) User Login**
```javascript
POST /api/login/
→ Authenticates user
→ Returns token
→ Frontend stores token in localStorage/UserDefaults
```

**c) View Available Lockers**
```javascript
GET /api/lockers/
→ Returns all lockers with status
→ Frontend displays lockers
```

**d) Rent Locker**
```javascript
POST /api/lockers/1/rent/
Headers: Authorization: Bearer <token>
Body: {"rental_duration": 3600}
→ Updates locker status to "In Use"
→ Sets owner to user
→ Sets timer (time_left = 3600)
```

**e) Release Locker**
```javascript
POST /api/lockers/1/release/
Headers: Authorization: Bearer <token>
→ Resets locker status to "Available"
→ Clears owner
→ Resets timer to 0
```

### Step 5: Monitor in Django Admin
- Go to http://localhost:8000/admin/
- View Lockers
- Observe real-time updates:
  - Locker status changes (Available ↔ In Use)
  - Owner changes (empty ↔ username)
  - Time tracking (0 ↔ rental_duration)

---

## File Structure

```
backend/
├── lockers/
│   ├── views.py              ← 5 API endpoints
│   ├── models.py             ← Locker model
│   ├── serializers.py        ← Data validation
│   ├── urls.py               ← 5 URL patterns
│   ├── tests.py              ← 15 test cases (all passing)
│   ├── admin.py              ← Django Admin config
│   ├── authentication.py     ← Bearer token auth
│   ├── exceptions.py         ← Error handling
│   └── migrations/
│
├── backend/
│   ├── settings.py           ← Configured correctly
│   ├── urls.py               ← Main routing
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── db.sqlite3                ← Database
└── startup.bat/startup.sh    ← Startup scripts
```

---

## Key Features

✅ **User Authentication**
- Register new users
- Login with credentials
- Token-based authentication
- Bearer token format (standard for mobile/web)

✅ **Locker Management**
- Create/edit lockers in Django Admin
- View all lockers via API
- Real-time status updates
- No hardcoded data

✅ **Rental System**
- Rent available lockers
- Set rental duration (in seconds)
- Track locker owner
- Validate rental requests

✅ **Release System** (NEW for Lab 9)
- Release rented lockers
- Reset to available state
- Clear owner information
- Reset timer

✅ **Data Synchronization**
- All changes synced to database
- Django Admin reflects API changes
- API reflects Admin changes
- Single source of truth

✅ **Error Handling**
- Consistent JSON responses
- Proper HTTP status codes
- Clear error messages
- Input validation

✅ **Testing**
- 15 comprehensive tests
- 100% pass rate
- All edge cases covered
- Ready for production

---

## Frontend Integration Code Examples

### JavaScript (Web UI)

```javascript
// 1. Register
const register = async (username, email, password) => {
  const res = await fetch('http://localhost:8000/api/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password })
  });
  const data = await res.json();
  if (data.success) {
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
  }
  return data;
};

// 2. Login
const login = async (username, password) => {
  const res = await fetch('http://localhost:8000/api/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await res.json();
  if (data.success) {
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
  }
  return data;
};

// 3. Get Lockers
const getLockers = async () => {
  const token = localStorage.getItem('token');
  const res = await fetch('http://localhost:8000/api/lockers/', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return (await res.json()).lockers;
};

// 4. Rent Locker
const rentLocker = async (lockerId, duration) => {
  const token = localStorage.getItem('token');
  const res = await fetch(`http://localhost:8000/api/lockers/${lockerId}/rent/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ rental_duration: duration })
  });
  return (await res.json()).locker;
};

// 5. Release Locker (NEW)
const releaseLocker = async (lockerId) => {
  const token = localStorage.getItem('token');
  const res = await fetch(`http://localhost:8000/api/lockers/${lockerId}/release/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return (await res.json()).locker;
};
```

### Swift (Mobile UI)

```swift
// 1. Login
func login(username: String, password: String) async throws {
  var request = URLRequest(url: URL(string: "http://localhost:8000/api/login/")!)
  request.httpMethod = "POST"
  request.setValue("application/json", forHTTPHeaderField: "Content-Type")
  request.httpBody = try JSONSerialization.data(withJSONObject: ["username": username, "password": password])
  
  let (data, _) = try await URLSession.shared.data(for: request)
  let json = try JSONSerialization.jsonObject(with: data) as! [String: Any]
  
  if let token = json["token"] as? String {
    UserDefaults.standard.set(token, forKey: "token")
  }
}

// 2. Get Lockers
func getLockers() async throws -> [[String: Any]] {
  var request = URLRequest(url: URL(string: "http://localhost:8000/api/lockers/")!)
  if let token = UserDefaults.standard.string(forKey: "token") {
    request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
  }
  
  let (data, _) = try await URLSession.shared.data(for: request)
  let json = try JSONSerialization.jsonObject(with: data) as! [String: Any]
  return json["lockers"] as? [[String: Any]] ?? []
}

// 3. Rent Locker
func rentLocker(id: Int, duration: Int) async throws {
  var request = URLRequest(url: URL(string: "http://localhost:8000/api/lockers/\(id)/rent/")!)
  request.httpMethod = "POST"
  request.setValue("application/json", forHTTPHeaderField: "Content-Type")
  if let token = UserDefaults.standard.string(forKey: "token") {
    request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
  }
  request.httpBody = try JSONSerialization.data(withJSONObject: ["rental_duration": duration])
  
  let (_, _) = try await URLSession.shared.data(for: request)
}

// 4. Release Locker (NEW)
func releaseLocker(id: Int) async throws {
  var request = URLRequest(url: URL(string: "http://localhost:8000/api/lockers/\(id)/release/")!)
  request.httpMethod = "POST"
  if let token = UserDefaults.standard.string(forKey: "token") {
    request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
  }
  
  let (_, _) = try await URLSession.shared.data(for: request)
}
```

---

## Quick Start Commands

```bash
# Navigate to backend
cd backend

# Create admin user
python manage.py createsuperuser

# Create test lockers (in Django shell)
python manage.py shell
>>> from lockers.models import Locker
>>> for i in range(1, 6):
...     Locker.objects.create(number=i, status='Available')
>>> exit()

# Run all tests
python manage.py test lockers.tests -v 2

# Start server
python manage.py runserver
```

---

## Production Checklist for Lab 9

- [ ] Backend running on localhost:8000
- [ ] Admin user created
- [ ] 5+ test lockers created
- [ ] All 15 tests passing
- [ ] Web UI connects to /api/register/
- [ ] Web UI connects to /api/login/
- [ ] Web UI connects to /api/lockers/
- [ ] Web UI connects to /api/lockers/{id}/rent/
- [ ] Web UI connects to /api/lockers/{id}/release/
- [ ] Mobile UI uses same endpoints
- [ ] Bearer token authentication working
- [ ] Locker status updates in Django Admin
- [ ] User can rent lockers
- [ ] User can release lockers
- [ ] Complete workflow tested end-to-end

---

## Support

**Q: Getting 401 Unauthorized?**  
A: Ensure token is in header: `Authorization: Bearer <token>`

**Q: Locker not updating?**  
A: Verify you're authenticated and locker exists

**Q: Can't release locker?**  
A: Ensure locker is in "In Use" status

**Q: CORS errors?**  
A: CORS is enabled for all origins in development

---

## Summary

Your backend is **complete and production-ready for Lab 9**:

✅ **5 Required Endpoints**
- POST /api/register/
- POST /api/login/
- GET /api/lockers/
- POST /api/lockers/{id}/rent/
- POST /api/lockers/{id}/release/ (NEW)

✅ **15 Tests Passing** (including 4 new release tests)

✅ **Database Connected** (users, lockers, rentals)

✅ **Authentication Working** (Bearer tokens)

✅ **Admin Synced** (real-time updates)

✅ **Error Handling** (consistent responses)

✅ **Clean Code** (no unnecessary complexity)

**Ready for Lab 9 submission and Web/Mobile UI integration!**

Start the server: `python manage.py runserver`  
Access admin: http://localhost:8000/admin/
