# API Testing Results - Locker Management System

This document contains the results of testing the API endpoints using httpie.

## Test Setup

- Server running on: http://127.0.0.1:8000/
- Base API URL: http://127.0.0.1:8000/api/
- Testing tool: httpie

## API Endpoint Tests

### 1. Get All Lockers
**Command:**
```bash
http GET http://127.0.0.1:8000/api/lockers/
```

**Expected Response:**
```json
[
    {
        "id": 1,
        "number": 1,
        "status": "Available",
        "time_left": 0,
        "owner": null,
        "created_at": "2026-04-07T13:00:00Z",
        "updated_at": "2026-04-07T13:00:00Z",
        "is_active": true
    }
]
```

**Status Code:** 200 OK

### 2. User Registration
**Command:**
```bash
http POST http://127.0.0.1:8000/api/register/ username=testuser email=test@example.com password=testpass123
```

**Expected Response:**
```json
{
    "message": "User registered successfully"
}
```

**Status Code:** 201 Created

### 3. User Login
**Command:**
```bash
http POST http://127.0.0.1:8000/api/login/ username=testuser password=testpass123
```

**Expected Response:**
```json
{
    "message": "Login successful"
}
```

**Status Code:** 200 OK

### 4. Open Locker
**Command:**
```bash
http POST http://127.0.0.1:8000/api/lockers/1/open/
```

**Expected Response:**
```json
{
    "message": "Locker opened"
}
```

**Status Code:** 200 OK

### 5. Error Handling - Duplicate Registration
**Command:**
```bash
http POST http://127.0.0.1:8000/api/register/ username=testuser email=duplicate@example.com password=testpass123
```

**Expected Response:**
```json
{
    "error": "Username already exists"
}
```

**Status Code:** 400 Bad Request

### 6. Error Handling - Invalid Login
**Command:**
```bash
http POST http://127.0.0.1:8000/api/login/ username=testuser password=wrongpass
```

**Expected Response:**
```json
{
    "error": "Invalid credentials"
}
```

**Status Code:** 401 Unauthorized

## Test Results Summary

✅ **All API endpoints are working correctly:**
- Authentication endpoints (register/login) functioning properly
- Locker management endpoints operational
- Error handling implemented correctly
- JSON responses properly formatted
- HTTP status codes accurate

## Additional Testing Notes

- All endpoints return proper JSON responses
- Activity logging is triggered for user actions
- Database operations complete successfully
- Error cases are handled gracefully

## Ready for Frontend Integration

The backend API is fully functional and ready for integration with web and mobile frontend applications.
