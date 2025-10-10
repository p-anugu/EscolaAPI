# Answers for Frontend Team

## ✅ Quick Answers to Your Questions

### 1. **Admin Credentials - VALID**
```json
{
  "email": "admin2@escolalms.com",
  "password": "secret"
}
```

### 2. **Token Format - CORRECT**
```javascript
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

### 3. **Admin Courses Endpoint**
- Endpoint: `/api/admin/courses`
- Status: Returns "Unauthenticated" (backend bug)
- **Workaround**: Use `/api/courses` instead

### 4. **CORS Configuration**
- CORS is properly configured (`allowed_origins: ['*']`)
- Not a CORS issue

### 5. **Authorization Header**
- You're setting it correctly
- Backend isn't processing it (their bug)

### 6. **Login Response Format**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "eyJ0eXAiOiJKV1Q...",
    "expires_at": "2025-10-02T18:59:09.000000Z"
  }
}
```

### 7. **Alternative to Get All Courses**
```javascript
// This works without authentication:
fetch('http://api.localhost/api/courses')
```

### 8. **Session vs Token**
- API uses Bearer tokens only
- No session/cookie auth available

---

## 🎯 What Works Right Now

```javascript
// ✅ WORKING - Login
const response = await fetch('http://api.localhost/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'admin2@escolalms.com',
    password: 'secret'
  })
});

// ✅ WORKING - Get all courses (no auth needed)
const courses = await fetch('http://api.localhost/api/courses');

// ❌ BROKEN - All authenticated endpoints return "Unauthenticated"
// - /api/profile/me
// - /api/admin/courses
// - /api/courses/my
```

---

## 🔧 Recommended Implementation

```javascript
class EscolaAPI {
  constructor() {
    this.baseURL = 'http://api.localhost'; // Use this, not localhost:1000
  }

  async login(email, password) {
    const res = await fetch(`${this.baseURL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    if (data.success) {
      localStorage.setItem('token', data.data.token);
    }
    return data;
  }

  async getCourses() {
    // Use public endpoint (auth is broken)
    const res = await fetch(`${this.baseURL}/api/courses`);
    return res.json();
  }

  async getProfile() {
    // Mock it - endpoint is broken
    return {
      data: {
        id: 2,
        email: "admin2@escolalms.com",
        roles: [{name: "admin"}]
      }
    };
  }
}
```

---

## 📝 Test Commands

```bash
# Login (WORKS)
curl -X POST http://api.localhost/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin2@escolalms.com","password":"secret"}'

# Get courses (WORKS)
curl http://api.localhost/api/courses
```

---

## 🚨 Current Status

- **Authentication is broken** on the backend
- **Use public endpoints** that don't require auth
- **Mock user profiles** locally
- **Assume admin mode** based on login email

## Enrollment API

To enroll students (when auth is fixed):
```javascript
// POST /api/admin/courses/{courseId}/access/add
{
  "users": [5, 6, 7]  // User IDs to enroll
}
```