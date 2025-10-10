# EscolaLMS Frontend API Integration Guide

## 🚨 IMPORTANT: Authentication Required
Most endpoints require a Bearer token. The token expires after 5 minutes, so handle token refresh appropriately.

## Base Configuration
```javascript
const API_BASE_URL = 'http://api.localhost';
const API_ENDPOINTS = {
  // Auth
  login: '/api/auth/login',
  profile: '/api/profile/me',

  // Public Course Endpoints
  coursesList: '/api/courses',
  courseDetail: '/api/courses/:id',
  courseProgram: '/api/courses/:id/program',

  // Admin Course Endpoints
  adminCourses: '/api/admin/courses',
  adminCourseDetail: '/api/admin/courses/:id',
  adminCourseDelete: '/api/admin/courses/:id',

  // Course Components
  lessons: '/api/admin/lessons',
  topics: '/api/admin/topics',

  // User Progress
  myCourseIds: '/api/courses/my',
  courseProgress: '/api/courses/progress/:courseId'
};
```

## 1. Authentication Flow

### Login and Get Token
```javascript
async function login(email, password) {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });

  const data = await response.json();
  if (data.success) {
    // Store token and expiry
    localStorage.setItem('auth_token', data.data.token);
    localStorage.setItem('token_expires', data.data.expires_at);
    return data.data.token;
  }
  throw new Error(data.message);
}

// Working Test Credentials
const TEST_USERS = {
  admin: {
    email: 'admin2@escolalms.com',
    password: 'secret',
    role: 'admin'
  },
  student: {
    email: 'student@escolalms.com',
    password: 'secret',
    role: 'student'
  }
};
```

### Get User Profile
After login, you MUST call `/api/profile/me` to get user details:
```javascript
async function getUserProfile(token) {
  const response = await fetch(`${API_BASE_URL}/api/profile/me`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });

  const data = await response.json();
  return data.data; // Contains user info, roles, permissions
}
```

## 2. Course CRUD Operations

### List All Courses
```javascript
// Public listing (shows only published courses)
async function getPublicCourses(page = 1, perPage = 15) {
  const response = await fetch(
    `${API_BASE_URL}/api/courses?page=${page}&per_page=${perPage}`
  );
  return await response.json();
}

// Admin listing (shows all courses including drafts)
async function getAdminCourses(token, page = 1) {
  const response = await fetch(
    `${API_BASE_URL}/api/admin/courses?page=${page}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    }
  );
  return await response.json();
}
```

### Create New Course
```javascript
async function createCourse(token, courseData) {
  const response = await fetch(`${API_BASE_URL}/api/admin/courses`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: courseData.title,               // Required
      summary: courseData.summary,           // Brief description
      description: courseData.description,   // Full HTML content
      status: courseData.status || 'draft',  // draft|published|archived|ended
      duration: courseData.duration,         // e.g., "10 hours"
      level: courseData.level,               // beginner|intermediate|advanced
      language: courseData.language || 'en', // ISO code
      subtitle: courseData.subtitle,
      target_group: courseData.targetGroup,
      hours_to_complete: courseData.hours,   // Number
      findable: courseData.findable ?? true, // Show in listings
      public: courseData.public ?? false,    // Free access
      active_from: courseData.activeFrom,    // ISO date string
      active_to: courseData.activeTo,        // ISO date string or null
      authors: courseData.authorIds,         // Array of user IDs
      categories: courseData.categoryIds,    // Array of category IDs
      tags: courseData.tags                  // Array of tag strings
    })
  });

  const result = await response.json();
  if (result.success) {
    return result.data; // Returns created course with ID
  }
  throw new Error(result.message);
}
```

### Update Course
```javascript
async function updateCourse(token, courseId, updates) {
  // NOTE: Uses POST, not PUT/PATCH (for file upload support)
  const response = await fetch(`${API_BASE_URL}/api/admin/courses/${courseId}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  });

  return await response.json();
}
```

### Delete Course
```javascript
async function deleteCourse(token, courseId) {
  const response = await fetch(`${API_BASE_URL}/api/admin/courses/${courseId}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  });

  const result = await response.json();
  if (!result.success) {
    throw new Error(result.message);
  }
  return result;
}
```

## 3. Course Structure Management

### Course Hierarchy
```
Course
├── Lesson 1 (Chapter/Module)
│   ├── Topic 1.1 (Content Item)
│   │   ├── Topicable (RichText/Video/PDF/etc.)
│   │   └── Resources (Additional files)
│   └── Topic 1.2
└── Lesson 2
    ├── Topic 2.1
    └── Topic 2.2
```

### Create Lesson
```javascript
async function createLesson(token, courseId, lessonData) {
  const response = await fetch(`${API_BASE_URL}/api/admin/lessons`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      course_id: courseId,
      title: lessonData.title,
      summary: lessonData.summary,
      duration: lessonData.duration,
      order: lessonData.order || 1,
      active: lessonData.active ?? true,
      parent_lesson_id: lessonData.parentId || null
    })
  });

  return await response.json();
}
```

### Create Topic (Content)
```javascript
// Available topic types
const TOPIC_TYPES = {
  RICH_TEXT: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\RichText',
  VIDEO: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\Video',
  AUDIO: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\Audio',
  IMAGE: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\Image',
  PDF: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\PDF',
  H5P: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\H5P',
  SCORM: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\ScormSco'
};

async function createTopic(token, lessonId, topicData) {
  const response = await fetch(`${API_BASE_URL}/api/admin/topics`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      lesson_id: lessonId,
      title: topicData.title,
      topicable_type: topicData.type || TOPIC_TYPES.RICH_TEXT,
      value: topicData.content,        // HTML for RichText, URL for video/audio
      summary: topicData.summary,
      introduction: topicData.intro,
      description: topicData.description,
      order: topicData.order || 1,
      active: topicData.active ?? true,
      preview: topicData.preview ?? false,  // Allow free preview
      can_skip: topicData.canSkip ?? false,
      duration: topicData.duration
    })
  });

  return await response.json();
}
```

## 4. Role-Based Endpoint Selection

```javascript
function getCourseEndpoint(userRole, action) {
  const endpoints = {
    admin: {
      list: '/api/admin/courses',
      detail: '/api/admin/courses/:id',
      create: '/api/admin/courses',
      update: '/api/admin/courses/:id',
      delete: '/api/admin/courses/:id',
      program: '/api/admin/courses/:id/program'
    },
    tutor: {
      list: '/api/courses/authored',
      detail: '/api/admin/courses/:id',
      create: '/api/admin/courses',
      update: '/api/admin/courses/:id',
      program: '/api/admin/courses/:id/program'
    },
    student: {
      list: '/api/courses',
      detail: '/api/courses/:id',
      program: '/api/courses/:id/program',
      myCourses: '/api/courses/my',
      progress: '/api/courses/progress'
    }
  };

  return endpoints[userRole]?.[action];
}
```

## 5. Course Progress Tracking

### Get User's Course IDs
```javascript
async function getMyCourseIds(token) {
  const response = await fetch(`${API_BASE_URL}/api/courses/my`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });

  const result = await response.json();
  return result.data; // Returns array of course IDs [1, 3, 5, 7]
}
```

### Get/Update Course Progress
```javascript
async function getCourseProgress(token, courseId) {
  const response = await fetch(`${API_BASE_URL}/api/courses/progress/${courseId}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });

  return await response.json();
}

async function updateTopicProgress(token, courseId, topicId, status) {
  const response = await fetch(`${API_BASE_URL}/api/courses/progress/${courseId}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      progress: [{ topic_id: topicId, status: status }]
    })
  });

  return await response.json();
}
```

## 6. Database Schema Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | varchar(255) | Yes | Course title |
| `summary` | text | No | Brief description |
| `description` | text | No | Full HTML description |
| `status` | varchar(255) | Yes | published, draft, archived, ended |
| `duration` | varchar(255) | No | e.g., "10 hours" |
| `level` | varchar(100) | No | beginner, intermediate, advanced |
| `language` | varchar(2) | No | ISO language code |
| `subtitle` | varchar(255) | No | Secondary title |
| `target_group` | varchar(100) | No | Target audience |
| `hours_to_complete` | integer | No | Numeric hours |
| `findable` | boolean | Yes | Show in public listings |
| `public` | boolean | No | Free access without enrollment |
| `active_from` | timestamp | No | Course start date |
| `active_to` | timestamp | No | Course end date |
| `fields` | json | No | Custom metadata |

## 7. Error Handling

```javascript
class APIError extends Error {
  constructor(response, data) {
    super(data.message || 'API Error');
    this.status = response.status;
    this.errors = data.errors || {};
  }
}

async function apiRequest(url, options = {}) {
  try {
    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
      throw new APIError(response, data);
    }

    return data;
  } catch (error) {
    if (error.status === 401) {
      // Token expired - redirect to login
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    throw error;
  }
}
```

## 8. Test Data

### Available Test Course
```javascript
const TEST_COURSE = {
  id: 11,
  title: "Introduction to Web Development",
  author: "admin2@escolalms.com",
  lessons: [
    { title: "Getting Started", topics: 2 },
    { title: "HTML Basics", topics: 2 },
    { title: "CSS Fundamentals", topics: 1 }
  ]
};
```

### Sample API Calls
```javascript
// 1. Login as admin
const token = await login('admin2@escolalms.com', 'secret');

// 2. Get all courses
const courses = await getAdminCourses(token);

// 3. Get specific course with curriculum
const courseProgram = await fetch(
  `${API_BASE_URL}/api/courses/11/program`,
  { headers: { 'Authorization': `Bearer ${token}` }}
);

// 4. Create a new course
const newCourse = await createCourse(token, {
  title: "JavaScript Fundamentals",
  summary: "Learn JS from scratch",
  status: "published",
  level: "beginner",
  duration: "20 hours"
});
```

## 9. Important Notes

1. **Token Expiration**: Tokens expire after 5 minutes. Implement auto-refresh or re-login.

2. **File Uploads**: For courses with images/videos, use FormData instead of JSON:
```javascript
const formData = new FormData();
formData.append('title', 'Course Title');
formData.append('image', fileInput.files[0]);
```

3. **Pagination**: Most list endpoints support `page` and `per_page` parameters.

4. **Course Status**:
   - `draft`: Not visible to students
   - `published`: Active and available
   - `archived`: No longer active but preserved
   - `ended`: Course has concluded

5. **Preview Topics**: Topics with `preview: true` can be accessed without enrollment.

## 10. Complete Working Example

```javascript
class CourseAPI {
  constructor(baseURL = 'http://api.localhost') {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('auth_token');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(url, { ...options, headers });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'API Error');
    }

    return data;
  }

  async login(email, password) {
    const result = await this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });

    this.token = result.data.token;
    localStorage.setItem('auth_token', this.token);
    return result.data;
  }

  async getCourses() {
    return this.request('/api/admin/courses');
  }

  async createCourse(courseData) {
    return this.request('/api/admin/courses', {
      method: 'POST',
      body: JSON.stringify(courseData)
    });
  }

  async updateCourse(id, updates) {
    return this.request(`/api/admin/courses/${id}`, {
      method: 'POST',
      body: JSON.stringify(updates)
    });
  }

  async deleteCourse(id) {
    return this.request(`/api/admin/courses/${id}`, {
      method: 'DELETE'
    });
  }
}

// Usage
const api = new CourseAPI();
await api.login('admin2@escolalms.com', 'secret');
const courses = await api.getCourses();
console.log('Courses:', courses.data);
```

## Support & Troubleshooting

- **401 Unauthorized**: Token expired or invalid. Re-login required.
- **403 Forbidden**: User lacks permission for this action.
- **404 Not Found**: Resource doesn't exist or is not accessible.
- **422 Unprocessable Entity**: Validation error. Check `errors` field in response.
- **500 Internal Server Error**: Server issue. Check Docker logs.

## Database Access (for debugging)
- **Adminer URL**: http://localhost:8078
- **Database**: PostgreSQL
- **Credentials**: username: default, password: secret