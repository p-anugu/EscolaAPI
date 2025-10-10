# User Management API Guide for Admin

## Overview
Complete API documentation for managing users, students, and groups as an admin in the EscolaLMS system.

## Base URL
```
http://api.localhost
```

## Authentication Required
All endpoints require admin authentication:
```javascript
Headers: { "Authorization": "Bearer {admin_token}" }
```

---

# USER DATABASE SCHEMA

## Users Table Structure (PostgreSQL)
| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | bigint | NOT NULL | auto_increment | Primary key |
| `first_name` | varchar(255) | NOT NULL | - | User's first name |
| `last_name` | varchar(255) | NOT NULL | - | User's last name |
| `email` | varchar(120) | YES | - | Email address (unique) |
| `phone` | varchar(255) | YES | - | Phone number |
| `password` | varchar(60) | YES | - | Hashed password |
| `is_active` | boolean | NOT NULL | true | Account active status |
| `remember_token` | varchar(100) | YES | - | Remember me token |
| `password_reset_token` | varchar(32) | YES | - | Password reset token |
| `email_verified_at` | timestamp | YES | - | Email verification date |
| `path_avatar` | varchar(255) | YES | - | Avatar file path |
| `gender` | integer | YES | - | Gender (1=male, 2=female, etc) |
| `age` | integer | YES | - | User age |
| `country` | varchar(255) | YES | - | Country |
| `city` | varchar(255) | YES | - | City |
| `street` | varchar(255) | YES | - | Street address |
| `postcode` | varchar(255) | YES | - | Postal code |
| `created_at` | timestamp | YES | - | Account creation date |
| `updated_at` | timestamp | YES | - | Last update date |
| `points` | bigint | NOT NULL | 0 | Gamification points |
| `notification_channels` | json | YES | - | Preferred notification methods |
| `access_to_directories` | json | YES | - | Directory permissions |
| `current_timezone` | varchar(50) | YES | UTC | User timezone |
| `deleted_at` | timestamp | YES | - | Soft delete timestamp |
| `delete_user_token` | text | YES | - | Account deletion token |

---

# USER MANAGEMENT ENDPOINTS

## 1. LIST ALL USERS
**Endpoint:** `GET /api/admin/users`

### Query Parameters:
```javascript
{
  // Pagination
  page: 1,                    // Page number
  per_page: 15,               // Items per page

  // Filtering
  search: "john",             // Search by name/email
  role: "student",            // Filter by role
  is_active: true,            // Active/inactive users
  email_verified: true,       // Email verification status

  // Sorting
  order_by: "created_at",     // Sort field
  order: "desc"               // Sort direction (asc/desc)
}
```

### Response:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "is_active": true,
      "email_verified_at": "2024-01-15T10:00:00Z",
      "path_avatar": "avatars/user1.jpg",
      "url_avatar": "http://storage.localhost/avatars/user1.jpg",
      "gender": 1,
      "age": 25,
      "country": "USA",
      "city": "New York",
      "street": "123 Main St",
      "postcode": "10001",
      "points": 150,
      "current_timezone": "America/New_York",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-20T15:30:00Z",
      "roles": ["student"],
      "groups": [
        {"id": 1, "name": "Premium Students"}
      ]
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 15,
    "total": 250,
    "last_page": 17
  }
}
```

## 2. GET SINGLE USER
**Endpoint:** `GET /api/admin/users/{id}`

### Response includes all fields plus:
```json
{
  "success": true,
  "data": {
    // All fields from list plus:
    "notification_channels": {
      "email": true,
      "sms": false,
      "push": true
    },
    "access_to_directories": ["uploads", "documents"],
    "settings": {
      "language": "en",
      "notifications_enabled": true
    },
    "interests": [
      {"id": 1, "name": "Web Development"},
      {"id": 2, "name": "JavaScript"}
    ],
    "courses": [
      {"id": 1, "title": "Introduction to Programming", "progress": 75}
    ],
    "permissions": ["view_courses", "purchase_courses"]
  }
}
```

## 3. CREATE NEW USER
**Endpoint:** `POST /api/admin/users`

### Request Body:
```json
{
  // REQUIRED
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@example.com",
  "password": "securePassword123",

  // OPTIONAL
  "phone": "+1234567890",
  "is_active": true,
  "gender": 2,
  "age": 28,
  "country": "Canada",
  "city": "Toronto",
  "street": "456 Queen St",
  "postcode": "M5V 3A8",
  "current_timezone": "America/Toronto",

  // Role assignment
  "roles": ["student"],

  // Group assignment
  "groups": [1, 2],

  // Settings
  "settings": {
    "language": "en",
    "notifications_enabled": true
  },

  // Send verification email
  "verify_email": true
}
```

### Response:
```json
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "id": 251,
    // ... all user fields
  }
}
```

## 4. UPDATE USER (Full Update)
**Endpoint:** `PUT /api/admin/users/{id}`

### Request Body:
```json
{
  // All fields from create (except password requires special handling)
  "first_name": "Jane Updated",
  "is_active": false,
  "roles": ["student", "tutor"]
}
```

## 5. PARTIAL UPDATE USER
**Endpoint:** `PATCH /api/admin/users/{id}`

### Request Body (only fields to update):
```json
{
  "is_active": false,
  "city": "Vancouver"
}
```

## 6. DELETE USER
**Endpoint:** `DELETE /api/admin/users/{id}`

### Query Parameters:
```javascript
{
  force: false  // true for hard delete, false for soft delete
}
```

### Response:
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

---

# USER AVATAR MANAGEMENT

## 7. UPLOAD AVATAR
**Endpoint:** `POST /api/admin/users/{id}/avatar`

### Request (FormData):
```javascript
const formData = new FormData();
formData.append('avatar', fileInput.files[0]);

fetch(`/api/admin/users/${userId}/avatar`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData
});
```

### Response:
```json
{
  "success": true,
  "data": {
    "path_avatar": "avatars/user1_new.jpg",
    "url_avatar": "http://storage.localhost/avatars/user1_new.jpg"
  }
}
```

## 8. DELETE AVATAR
**Endpoint:** `DELETE /api/admin/users/{id}/avatar`

---

# USER SETTINGS

## 9. GET USER SETTINGS
**Endpoint:** `GET /api/admin/users/{id}/settings`

### Response:
```json
{
  "success": true,
  "data": {
    "language": "en",
    "notifications_enabled": true,
    "email_frequency": "daily",
    "timezone": "UTC",
    "theme": "light"
  }
}
```

## 10. UPDATE USER SETTINGS
**Endpoint:** `PUT /api/admin/users/{id}/settings`

### Request Body:
```json
{
  "language": "es",
  "notifications_enabled": false,
  "theme": "dark"
}
```

## 11. PATCH USER SETTINGS
**Endpoint:** `PATCH /api/admin/users/{id}/settings`

---

# USER INTERESTS

## 12. GET USER INTERESTS
**Endpoint:** `GET /api/admin/users/{id}/interests`

### Response:
```json
{
  "success": true,
  "data": [
    {"id": 1, "name": "Programming"},
    {"id": 2, "name": "Web Development"}
  ]
}
```

## 13. UPDATE USER INTERESTS (Replace All)
**Endpoint:** `PUT /api/admin/users/{id}/interests`

### Request Body:
```json
{
  "interests": [1, 3, 5]  // Array of interest IDs
}
```

## 14. ADD SINGLE INTEREST
**Endpoint:** `POST /api/admin/users/{id}/interests`

### Request Body:
```json
{
  "interest_id": 4
}
```

## 15. REMOVE SINGLE INTEREST
**Endpoint:** `DELETE /api/admin/users/{id}/interests/{interest_id}`

---

# USER GROUPS MANAGEMENT

## 16. LIST ALL GROUPS
**Endpoint:** `GET /api/admin/user-groups`

### Response:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Premium Students",
      "parent_id": null,
      "is_registerable": true,
      "users_count": 45,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

## 17. GET GROUPS TREE (Hierarchical)
**Endpoint:** `GET /api/admin/user-groups/tree`

### Response:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "All Students",
      "parent_id": null,
      "children": [
        {
          "id": 2,
          "name": "Premium Students",
          "parent_id": 1,
          "children": []
        }
      ]
    }
  ]
}
```

## 18. LIST GROUPS WITH USERS
**Endpoint:** `GET /api/admin/user-groups/users`

### Response includes users in each group:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Premium Students",
      "users": [
        {"id": 5, "name": "John Doe", "email": "john@example.com"},
        {"id": 7, "name": "Jane Smith", "email": "jane@example.com"}
      ]
    }
  ]
}
```

## 19. CREATE GROUP
**Endpoint:** `POST /api/admin/user-groups`

### Request Body:
```json
{
  "name": "Advanced Learners",
  "parent_id": 1,
  "is_registerable": true
}
```

## 20. UPDATE GROUP
**Endpoint:** `PUT /api/admin/user-groups/{id}`

## 21. DELETE GROUP
**Endpoint:** `DELETE /api/admin/user-groups/{id}`

## 22. ADD USER TO GROUP
**Endpoint:** `POST /api/admin/user-groups/{group_id}/members`

### Request Body:
```json
{
  "user_id": 10
}
```

## 23. REMOVE USER FROM GROUP
**Endpoint:** `DELETE /api/admin/user-groups/{group_id}/members/{user_id}`

---

# ADVANCED ADMIN FEATURES

## 24. IMPERSONATE USER
**Endpoint:** `POST /api/admin/auth/impersonate`

### Request Body:
```json
{
  "user_id": 5
}
```

### Response:
```json
{
  "success": true,
  "data": {
    "token": "impersonation_token_here",
    "original_token": "admin_token_to_return"
  }
}
```

---

# IMPLEMENTATION EXAMPLES

## Complete User Management Class
```javascript
class UserManagementAPI {
  constructor(baseURL = 'http://api.localhost', token) {
    this.baseURL = baseURL;
    this.token = token;
  }

  async request(endpoint, options = {}) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.token}`,
        ...options.headers
      }
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || 'API Error');
    }
    return data;
  }

  // User CRUD
  async getUsers(page = 1, filters = {}) {
    const params = new URLSearchParams({
      page,
      per_page: 20,
      ...filters
    });
    return this.request(`/api/admin/users?${params}`);
  }

  async getUser(userId) {
    return this.request(`/api/admin/users/${userId}`);
  }

  async createUser(userData) {
    return this.request('/api/admin/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
  }

  async updateUser(userId, updates) {
    return this.request(`/api/admin/users/${userId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    });
  }

  async deleteUser(userId, hardDelete = false) {
    const params = hardDelete ? '?force=true' : '';
    return this.request(`/api/admin/users/${userId}${params}`, {
      method: 'DELETE'
    });
  }

  // Avatar
  async uploadAvatar(userId, file) {
    const formData = new FormData();
    formData.append('avatar', file);

    return this.request(`/api/admin/users/${userId}/avatar`, {
      method: 'POST',
      body: formData,
      headers: {} // Let browser set Content-Type for FormData
    });
  }

  // Groups
  async addToGroup(groupId, userId) {
    return this.request(`/api/admin/user-groups/${groupId}/members`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId })
    });
  }

  // Search
  async searchUsers(query) {
    return this.getUsers(1, { search: query });
  }

  // Bulk operations
  async bulkUpdateUsers(userIds, updates) {
    const promises = userIds.map(id =>
      this.updateUser(id, updates)
    );
    return Promise.all(promises);
  }

  // Role management
  async assignRole(userId, roles) {
    return this.updateUser(userId, { roles });
  }

  // Activation
  async activateUser(userId) {
    return this.updateUser(userId, { is_active: true });
  }

  async deactivateUser(userId) {
    return this.updateUser(userId, { is_active: false });
  }
}

// Usage
const userAPI = new UserManagementAPI('http://api.localhost', adminToken);

// Get paginated users
const users = await userAPI.getUsers(1, {
  role: 'student',
  is_active: true
});

// Create new user
const newUser = await userAPI.createUser({
  first_name: 'John',
  last_name: 'Doe',
  email: 'john@example.com',
  password: 'secure123',
  roles: ['student']
});

// Update user
await userAPI.updateUser(newUser.data.id, {
  city: 'Los Angeles',
  is_active: true
});

// Add to group
await userAPI.addToGroup(1, newUser.data.id);
```

## Search and Filter Implementation
```javascript
// Advanced search with multiple filters
async function searchUsers(filters) {
  const queryParams = new URLSearchParams();

  // Text search
  if (filters.search) {
    queryParams.append('search', filters.search);
  }

  // Role filter
  if (filters.role) {
    queryParams.append('role', filters.role);
  }

  // Date range
  if (filters.createdFrom) {
    queryParams.append('created_from', filters.createdFrom);
  }
  if (filters.createdTo) {
    queryParams.append('created_to', filters.createdTo);
  }

  // Status filters
  if (filters.isActive !== undefined) {
    queryParams.append('is_active', filters.isActive);
  }
  if (filters.emailVerified !== undefined) {
    queryParams.append('email_verified', filters.emailVerified);
  }

  // Sorting
  queryParams.append('order_by', filters.orderBy || 'created_at');
  queryParams.append('order', filters.order || 'desc');

  const response = await fetch(
    `/api/admin/users?${queryParams}`,
    { headers: { 'Authorization': `Bearer ${token}` }}
  );

  return response.json();
}

// Usage
const results = await searchUsers({
  search: 'john',
  role: 'student',
  isActive: true,
  createdFrom: '2024-01-01',
  orderBy: 'last_name',
  order: 'asc'
});
```

## Pagination Component
```javascript
class UserPagination {
  constructor(apiClient) {
    this.api = apiClient;
    this.currentPage = 1;
    this.totalPages = 1;
    this.perPage = 20;
    this.filters = {};
  }

  async loadPage(page = 1) {
    const response = await this.api.getUsers(page, {
      ...this.filters,
      per_page: this.perPage
    });

    this.currentPage = response.meta.current_page;
    this.totalPages = response.meta.last_page;

    return response.data;
  }

  async nextPage() {
    if (this.currentPage < this.totalPages) {
      return this.loadPage(this.currentPage + 1);
    }
    return [];
  }

  async previousPage() {
    if (this.currentPage > 1) {
      return this.loadPage(this.currentPage - 1);
    }
    return [];
  }

  setFilter(key, value) {
    this.filters[key] = value;
    return this.loadPage(1); // Reset to first page
  }

  clearFilters() {
    this.filters = {};
    return this.loadPage(1);
  }
}
```

---

# ERROR HANDLING

## Common Error Responses

### Validation Error (422)
```json
{
  "message": "The given data was invalid.",
  "errors": {
    "email": ["The email has already been taken."],
    "password": ["The password must be at least 8 characters."]
  }
}
```

### Not Found (404)
```json
{
  "success": false,
  "message": "User not found"
}
```

### Unauthorized (401)
```json
{
  "message": "Unauthenticated."
}
```

### Forbidden (403)
```json
{
  "message": "You do not have permission to perform this action."
}
```

---

# ROLES AND PERMISSIONS

## Common User Roles
- `admin` - Full system access
- `tutor` - Can create and manage courses
- `student` - Can enroll and take courses
- `guest` - Limited access

## Role Assignment
```javascript
// Assign single role
await updateUser(userId, { roles: ['student'] });

// Assign multiple roles
await updateUser(userId, { roles: ['student', 'tutor'] });

// Get users by role
const students = await getUsers(1, { role: 'student' });
```

---

# BEST PRACTICES

1. **Pagination**: Always paginate when listing users (default 20 per page)
2. **Soft Delete**: Use soft delete by default to preserve data integrity
3. **Validation**: Validate email uniqueness before creating users
4. **Password Security**: Never send plain passwords in responses
5. **Avatar Upload**: Limit file size (max 5MB) and validate image types
6. **Bulk Operations**: Use batch endpoints for multiple updates
7. **Caching**: Cache user lists with appropriate TTL
8. **Search**: Implement debouncing for search inputs
9. **Error Handling**: Always handle 401/403/404/422 errors gracefully
10. **Timezone**: Store and display times in user's timezone

---

# TEST DATA

```javascript
// Test admin credentials
const ADMIN = {
  email: 'admin2@escolalms.com',
  password: 'secret'
};

// Test student
const STUDENT = {
  email: 'student@escolalms.com',
  password: 'secret'
};
```