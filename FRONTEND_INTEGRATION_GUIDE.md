# Frontend Integration Guide - Smart Locker System API

**Quick Reference for Web UI & Mobile UI Developers**

---

## Base URL
```
http://127.0.0.1:8000/api/
```

---

## Quick Start Code Examples

### 1. User Registration
```javascript
async function register(username, email, password) {
  const response = await fetch('http://127.0.0.1:8000/api/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password })
  });
  
  const data = await response.json();
  
  if (response.ok) {
    // Store token
    localStorage.setItem('token', data.token);
    console.log('Registered:', data.user);
    return data;
  } else {
    console.error('Registration failed:', data.error);
    throw new Error(data.error);
  }
}
```

### 2. User Login
```javascript
async function login(username, password) {
  const response = await fetch('http://127.0.0.1:8000/api/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  
  if (response.ok) {
    // Store token
    localStorage.setItem('token', data.token);
    console.log('Logged in:', data.user);
    return data;
  } else {
    console.error('Login failed:', data.error);
    throw new Error(data.error);
  }
}
```

### 3. Get All Lockers (Dashboard)
```javascript
async function getLockers() {
  const response = await fetch('http://127.0.0.1:8000/api/lockers/', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  });
  
  if (response.ok) {
    const lockers = await response.json();
    console.log('Lockers:', lockers);
    // Display lockers in UI
    return lockers;
  } else {
    console.error('Failed to fetch lockers');
    throw new Error('Failed to fetch lockers');
  }
}
```

### 4. Open Locker
```javascript
async function openLocker(lockerId, token) {
  const response = await fetch(`http://127.0.0.1:8000/api/lockers/${lockerId}/open/`, {
    method: 'POST',
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  const data = await response.json();
  
  if (response.ok) {
    console.log('Locker opened:', data);
    // data.status = "In Use"
    // data.owner = "username"
    // data.time_left = 60
    return data;
  } else {
    console.error('Failed to open locker:', data.error);
    throw new Error(data.error);
  }
}
```

### 5. Update Timer (Every Second)
```javascript
async function updateTimer(lockerId, timeLeft, token) {
  const response = await fetch(`http://127.0.0.1:8000/api/lockers/${lockerId}/`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ time_left: timeLeft })
  });
  
  if (response.ok) {
    const locker = await response.json();
    console.log('Timer updated:', locker.time_left);
    return locker;
  } else {
    console.error('Failed to update timer');
  }
}

// Timer loop example
function startTimerLoop(lockerId, initialTime, token) {
  let timeLeft = initialTime;
  
  const interval = setInterval(async () => {
    timeLeft--;
    console.log(`Time left: ${timeLeft}s`);
    
    // Update backend every 5 seconds (optional)
    if (timeLeft % 5 === 0) {
      await updateTimer(lockerId, timeLeft, token);
    }
    
    // When timer reaches 0
    if (timeLeft <= 0) {
      clearInterval(interval);
      await updateTimer(lockerId, 0, token);
      console.log('Locker auto-reset by backend');
    }
  }, 1000);
}
```

### 6. User Logout
```javascript
async function logout(token) {
  const response = await fetch('http://127.0.0.1:8000/api/logout/', {
    method: 'POST',
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  const data = await response.json();
  
  if (response.ok) {
    // Clear stored token
    localStorage.removeItem('token');
    console.log('Logged out');
    return data;
  } else {
    console.error('Logout failed');
  }
}
```

---

## API Endpoint Reference

### Authentication
| Method | Endpoint | Auth Required | Response |
|--------|----------|---------------|----------|
| POST | `/register/` | No | `{user, token}` |
| POST | `/login/` | No | `{user, token}` |
| POST | `/logout/` | Yes | `{message}` |

### Lockers
| Method | Endpoint | Auth Required | Response |
|--------|----------|---------------|----------|
| GET | `/lockers/` | No | `[locker, ...]` |
| POST | `/lockers/{id}/open/` | Yes | `{locker}` |
| PATCH | `/lockers/{id}/` | Yes | `{locker}` |
| DELETE | `/lockers/{id}/` | Yes (Admin) | 204 No Content |

---

## Locker Object Format

```javascript
{
  "id": 1,
  "number": 1,
  "status": "Available",  // or "In Use"
  "owner": null,          // or "username"
  "time_left": 0          // seconds remaining
}
```

---

## UI Flow Implementation

### 1. Authentication Screen
```
┌─────────────────────────┐
│  Sign Up / Login Form   │
│                         │
│  Username: [___]        │
│  Password: [___]        │
│  Email: [___] (signup)  │
│                         │
│  [Register] [Login]     │
└─────────────────────────┘
         ↓
   POST /login/ or /register/
         ↓
   Store token in localStorage
```

### 2. Dashboard Screen
```
┌─────────────────────────┐
│  Welcome, username!     │
│  [Logout]               │
│                         │
│  LOCKERS AVAILABLE      │
│                         │
│  [Locker 1] [Locker 2]  │
│  [Locker 3] [Locker 4]  │
│  ...                    │
└─────────────────────────┘
         ↓
   GET /lockers/
   (Fetch every 5-10 seconds)
```

### 3. Locker Detail Screen (When Opening)
```
┌─────────────────────────┐
│  LOCKER #1              │
│                         │
│  Status: In Use         │
│  Owner: john_doe        │
│                         │
│  Time Remaining:        │
│  ⏱ 00:59                │
│  ⏱ 00:58                │
│  ⏱ 00:57                │
│                         │
│  [Close Locker]         │
└─────────────────────────┘
         ↓
   POST /lockers/1/open/
         ↓
   Start timer loop
   PATCH /lockers/1/ every second
```

---

## Error Handling

### Common Errors

**401 Unauthorized**
```javascript
// Missing or invalid token
if (response.status === 401) {
  // Clear token and redirect to login
  localStorage.removeItem('token');
  window.location.href = '/login';
}
```

**400 Bad Request**
```javascript
// Invalid data or validation error
const error = data.error || 'Invalid request';
alert(error);
```

**404 Not Found**
```javascript
// Locker doesn't exist
if (response.status === 404) {
  alert('Locker not found');
}
```

**403 Forbidden**
```javascript
// Permission denied
if (response.status === 403) {
  alert('You do not have permission to perform this action');
}
```

---

## Token Management

### Storing Token
```javascript
// After login/register
localStorage.setItem('token', data.token);
```

### Retrieving Token
```javascript
// For authenticated requests
const token = localStorage.getItem('token');
const headers = {
  'Authorization': `Token ${token}`,
  'Content-Type': 'application/json'
};
```

### Clearing Token (Logout)
```javascript
localStorage.removeItem('token');
```

### Checking if Logged In
```javascript
function isLoggedIn() {
  return !!localStorage.getItem('token');
}
```

---

## Helper Functions (Reusable)

```javascript
// API Base URL
const API_BASE = 'http://127.0.0.1:8000/api';

// Generic fetch wrapper
async function apiCall(endpoint, method = 'GET', body = null) {
  const token = localStorage.getItem('token');
  
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    }
  };
  
  if (token) {
    options.headers['Authorization'] = `Token ${token}`;
  }
  
  if (body) {
    options.body = JSON.stringify(body);
  }
  
  const response = await fetch(`${API_BASE}${endpoint}`, options);
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.error || 'API Error');
  }
  
  return data;
}

// Usage examples
await apiCall('/lockers/', 'GET');
await apiCall('/login/', 'POST', { username, password });
await apiCall(`/lockers/${id}/open/`, 'POST');
await apiCall(`/lockers/${id}/`, 'PATCH', { time_left: 30 });
```

---

## Real-Time Updates Strategy

### Option 1: Polling (Recommended for MVP)
```javascript
// Fetch lockers every 10 seconds
setInterval(async () => {
  const lockers = await getLockers();
  updateUI(lockers);
}, 10000);
```

### Option 2: Frontend Timer
```javascript
// Run timer locally, update backend periodically
let timeLeft = 60;
setInterval(() => {
  timeLeft--;
  updateTimerDisplay(timeLeft);
  
  // Update backend every 5 seconds
  if (timeLeft % 5 === 0) {
    updateTimer(lockerId, timeLeft, token);
  }
}, 1000);
```

### Option 3: Polling + Timer Combined
```javascript
// Local timer for UI responsiveness
// Backend polling to sync status changes
```

---

## Mobile-Specific Considerations

### React Native Example
```javascript
// Similar fetch API, but use fetch() directly
fetch('http://YOUR_SERVER_IP:8000/api/lockers/', {
  method: 'GET',
  headers: { 'Content-Type': 'application/json' }
})
.then(res => res.json())
.then(data => setLockers(data));
```

### Flutter/Dart Example
```dart
// Use http package
import 'package:http/http.dart' as http;

Future<List<Locker>> getLockers() async {
  final response = await http.get(
    Uri.parse('http://YOUR_SERVER_IP:8000/api/lockers/'),
  );
  
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  }
  throw Exception('Failed to load lockers');
}
```

---

## Testing the API

### Using cURL
```bash
# Register
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123"}'

# Login
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'

# Get Lockers
curl http://127.0.0.1:8000/api/lockers/

# Open Locker (replace TOKEN and ID)
curl -X POST http://127.0.0.1:8000/api/lockers/1/open/ \
  -H "Authorization: Token TOKEN" \
  -H "Content-Type: application/json"
```

### Using Postman
1. Import collection from API_DOCUMENTATION.md
2. Set `{{base_url}}` to `http://127.0.0.1:8000/api`
3. Run requests in sequence
4. Save token in Postman environment variable

---

## Troubleshooting

### "Token is invalid"
- Token might have been deleted by logout
- Try logging in again

### "Locker is not available"
- Locker is already in use by another user
- Try a different locker

### "Permission denied"
- You're not the locker owner or admin
- Only admin can delete lockers

### "Connection refused"
- Backend server is not running
- Run `python manage.py runserver` in backend folder

### CORS Errors
- Should not happen - backend has CORS enabled
- Check that API URL is correct

---

## Performance Tips

1. **Cache lockers** - Don't fetch every render
2. **Debounce timer updates** - Update backend every 5s, not every 1s
3. **Lazy load** - Only fetch lockers when needed
4. **Minimize requests** - Combine multiple updates if possible
5. **Local state** - Manage timer locally for responsiveness

---

## Security Notes

1. **Always use HTTPS in production** - Not just HTTP
2. **Securely store token** - Not in global variables
3. **Don't expose token in logs** - Sanitize console output
4. **Validate user input** - Before sending to API
5. **Handle errors gracefully** - Don't expose backend details

---

## Support

**API Server Logs**: Check terminal running `python manage.py runserver`  
**Database Admin**: http://127.0.0.1:8000/admin/ (admin credentials required)  
**Full Documentation**: See `API_DOCUMENTATION.md`  
**Test Suite**: Run `python test_api.py` to verify all endpoints

---

**Ready to integrate! 🚀**
