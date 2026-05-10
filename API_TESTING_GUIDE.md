# API Testing Guide - Smart Locker System

## Quick Test with cURL

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "",
    "last_name": ""
  },
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "message": "User registered successfully"
}
```

Save the token for next requests.

---

### 2. Login User

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepass123"
  }'
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "",
    "last_name": ""
  },
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "message": "Login successful"
}
```

---

### 3. Get All Lockers

```bash
curl -X GET http://localhost:8000/api/lockers/ \
  -H "Authorization: Bearer a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
```

**Response:**
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
      "status": "Available",
      "owner": null,
      "time_left": 0,
      "rental_duration": 0
    }
  ]
}
```

---

### 4. Rent a Locker

```bash
curl -X POST http://localhost:8000/api/lockers/1/rent/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0" \
  -d '{
    "rental_duration": 3600
  }'
```

**Response:**
```json
{
  "success": true,
  "locker": {
    "id": 1,
    "number": 1,
    "status": "In Use",
    "owner": "johndoe",
    "time_left": 3600,
    "rental_duration": 3600
  },
  "message": "Locker rented successfully"
}
```

---

## Test with Postman

### Setup

1. Open Postman
2. Create new collection: "Smart Locker API"
3. Create environment with variable `BASE_URL = http://localhost:8000` and `TOKEN = (empty)`

### Request 1: Register

- **Method:** POST
- **URL:** `{{BASE_URL}}/api/register/`
- **Headers:** 
  - Content-Type: application/json
- **Body (raw JSON):**
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }
  ```
- **After Success:** Copy token to `TOKEN` environment variable

### Request 2: Login

- **Method:** POST
- **URL:** `{{BASE_URL}}/api/login/`
- **Headers:** 
  - Content-Type: application/json
- **Body (raw JSON):**
  ```json
  {
    "username": "testuser",
    "password": "testpass123"
  }
  ```
- **After Success:** Update `TOKEN` environment variable with response token

### Request 3: Get Lockers

- **Method:** GET
- **URL:** `{{BASE_URL}}/api/lockers/`
- **Headers:** 
  - Authorization: Bearer {{TOKEN}}

### Request 4: Rent Locker

- **Method:** POST
- **URL:** `{{BASE_URL}}/api/lockers/1/rent/`
- **Headers:** 
  - Content-Type: application/json
  - Authorization: Bearer {{TOKEN}}
- **Body (raw JSON):**
  ```json
  {
    "rental_duration": 3600
  }
  ```

---

## Error Scenarios to Test

### Scenario 1: Invalid Credentials

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "wrongpassword"
  }'
```

**Expected Response (401):**
```json
{
  "success": false,
  "error": "Invalid username or password",
  "message": "Login failed"
}
```

---

### Scenario 2: Rent Without Authentication

```bash
curl -X POST http://localhost:8000/api/lockers/1/rent/ \
  -H "Content-Type: application/json" \
  -d '{
    "rental_duration": 3600
  }'
```

**Expected Response (401):**
```json
{
  "success": false,
  "error": "Authentication required",
  "message": "Authentication failed"
}
```

---

### Scenario 3: Invalid Rental Duration

```bash
curl -X POST http://localhost:8000/api/lockers/1/rent/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "rental_duration": -100
  }'
```

**Expected Response (400):**
```json
{
  "success": false,
  "error": "Rental duration must be a positive number",
  "message": "Failed to rent locker"
}
```

---

### Scenario 4: Locker Not Found

```bash
curl -X POST http://localhost:8000/api/lockers/9999/rent/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "rental_duration": 3600
  }'
```

**Expected Response (404):**
```json
{
  "success": false,
  "error": "Locker not found",
  "message": "Invalid locker ID"
}
```

---

### Scenario 5: Rent Already In-Use Locker

After renting locker 1, try to rent it again:

```bash
curl -X POST http://localhost:8000/api/lockers/1/rent/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "rental_duration": 3600
  }'
```

**Expected Response (400):**
```json
{
  "success": false,
  "error": "Locker is not available (currently In Use)",
  "message": "Failed to rent locker"
}
```

---

## Verify in Django Admin

1. Go to `http://localhost:8000/admin/`
2. Login with: admin / admin123
3. Navigate to **Lockers**
4. Verify:
   - All lockers are listed
   - Available lockers show owner as `-` (None)
   - Rented lockers show owner username
   - Status updates correctly
   - Time remaining and duration are saved

---

## Web UI Integration

### React/Vue Example

```javascript
// 1. User Registration
const registerUser = async (username, email, password) => {
  const response = await fetch('http://localhost:8000/api/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password })
  });
  const data = await response.json();
  if (data.success) {
    localStorage.setItem('authToken', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  }
  throw new Error(data.error);
};

// 2. User Login
const loginUser = async (username, password) => {
  const response = await fetch('http://localhost:8000/api/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await response.json();
  if (data.success) {
    localStorage.setItem('authToken', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  }
  throw new Error(data.error);
};

// 3. Get Lockers
const getLockers = async () => {
  const token = localStorage.getItem('authToken');
  const response = await fetch('http://localhost:8000/api/lockers/', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const data = await response.json();
  if (data.success) {
    return data.lockers;
  }
  throw new Error(data.error);
};

// 4. Rent Locker
const rentLocker = async (lockerId, duration = 3600) => {
  const token = localStorage.getItem('authToken');
  const response = await fetch(`http://localhost:8000/api/lockers/${lockerId}/rent/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ rental_duration: duration })
  });
  const data = await response.json();
  if (data.success) {
    return data.locker;
  }
  throw new Error(data.error);
};
```

---

## Mobile UI Integration

### Swift (iOS) Example

```swift
import Foundation

// 1. Login User
func loginUser(username: String, password: String) async throws -> (token: String, user: [String: Any]) {
    var request = URLRequest(url: URL(string: "http://localhost:8000/api/login/")!)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    
    let body = ["username": username, "password": password]
    request.httpBody = try JSONSerialization.data(withJSONObject: body)
    
    let (data, response) = try await URLSession.shared.data(for: request)
    let json = try JSONSerialization.jsonObject(with: data) as! [String: Any]
    
    if let token = json["token"] as? String, let user = json["user"] as? [String: Any] {
        UserDefaults.standard.set(token, forKey: "authToken")
        return (token, user)
    }
    throw NSError(domain: "API", code: -1, userInfo: [NSLocalizedDescriptionKey: json["error"] ?? "Unknown error"])
}

// 2. Get Lockers
func getLockers() async throws -> [[String: Any]] {
    var request = URLRequest(url: URL(string: "http://localhost:8000/api/lockers/")!)
    request.httpMethod = "GET"
    if let token = UserDefaults.standard.string(forKey: "authToken") {
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
    }
    
    let (data, _) = try await URLSession.shared.data(for: request)
    let json = try JSONSerialization.jsonObject(with: data) as! [String: Any]
    
    return json["lockers"] as? [[String: Any]] ?? []
}

// 3. Rent Locker
func rentLocker(id: Int, duration: Int = 3600) async throws -> [String: Any] {
    var request = URLRequest(url: URL(string: "http://localhost:8000/api/lockers/\(id)/rent/")!)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    if let token = UserDefaults.standard.string(forKey: "authToken") {
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
    }
    
    let body = ["rental_duration": duration]
    request.httpBody = try JSONSerialization.data(withJSONObject: body)
    
    let (data, _) = try await URLSession.shared.data(for: request)
    let json = try JSONSerialization.jsonObject(with: data) as! [String: Any]
    
    return json["locker"] as? [String: Any] ?? [:]
}
```

---

## Troubleshooting

**Q: Getting 401 Unauthorized on protected endpoints?**
- Ensure token is in header: `Authorization: Bearer <your-token>`
- Check token isn't expired (tokens don't expire in this setup)
- Re-login to get a fresh token

**Q: Getting CORS error in browser?**
- CORS is enabled for all origins in development
- Clear browser cache and restart server
- Check browser console for exact CORS error message

**Q: Locker not updating in Django Admin?**
- Refresh Django Admin page
- Verify you're making requests with valid Bearer token
- Check database: `python manage.py shell` → `Locker.objects.all()`

**Q: Can't login with registered user?**
- Verify username/password (case-sensitive)
- Check user exists: `python manage.py shell` → `User.objects.all()`
- Try re-registering

---

## Next Steps

1. ✅ Backend running locally
2. ✅ Admin user created
3. ✅ Test lockers created
4. → Connect Web UI to `/api/register/` and `/api/login/`
5. → Connect Mobile UI with Bearer token format
6. → Test complete flow: Register → Login → Get Lockers → Rent Locker
7. → Monitor Django Admin for real-time updates
