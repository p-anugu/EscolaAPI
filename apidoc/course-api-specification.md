# Course API Specification

## Table of Contents
1. [Overview](#overview)
2. [Use Cases](#use-cases)
3. [Authentication & Authorization](#authentication--authorization)
4. [Course Data Model](#course-data-model)
5. [API Endpoints](#api-endpoints)
6. [Request/Response Examples](#requestresponse-examples)
7. [Error Handling](#error-handling)
8. [Business Rules & Validation](#business-rules--validation)
9. [Integration Guide](#integration-guide)

---

## Overview

The Course API provides comprehensive functionality for managing educational courses within the EscolaLMS platform. This API enables course creation, management, and delivery of educational content through a RESTful interface.

### Base URL
```
https://api.yourdomain.com/api
```

### Content Type
All requests and responses use `application/json` unless otherwise specified (file uploads use `multipart/form-data`).

---

## Use Cases

### Primary Use Cases

1. **Course Creation & Management**
   - Instructors/Admins create new courses with structured content
   - Define course metadata (title, description, duration, etc.)
   - Set pricing and availability parameters
   - Upload media assets (images, videos, posters)

2. **Course Publishing Workflow**
   - Draft courses for internal review
   - Publish courses for student enrollment
   - Archive outdated courses
   - Schedule course availability with active dates

3. **Multi-Author Collaboration**
   - Assign multiple authors to a single course
   - Collaborative content development
   - Author permission management

4. **Course Discovery & Access Control**
   - Make courses findable in search/catalog
   - Control public vs. private access
   - Define target audience groups
   - Set course levels (beginner, intermediate, advanced)

5. **SCORM Integration**
   - Support for SCORM content packages
   - Track learning progress through SCORM
   - Compatibility with e-learning standards

---

## Authentication & Authorization

### Authentication
All protected endpoints require Bearer token authentication:
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Required Permissions

| Action | Permission Required | Description |
|--------|-------------------|-------------|
| Create Course | `course_create` | Ability to create new courses |
| Update Course | `course_update` or `course_update_authored` | Update any course or only authored courses |
| Delete Course | `course_delete` or `course_delete_authored` | Delete any course or only authored courses |
| List Courses | `course_list` or `course_list_authored` | View all courses or only authored courses |
| View Course | `course_read` or `course_read_authored` | Read course details |

### User Roles

- **Admin**: Full access to all course operations
- **Instructor/Tutor**: Can create and manage their own courses
- **Student**: Can view published courses and enroll
- **Guest**: Can view public courses only

---

## Course Data Model

### Core Fields

| Field | Type | Required | Description | Validation Rules |
|-------|------|----------|-------------|-----------------|
| `title` | string | Yes | Course title | Min: 3 chars, Max: 255 chars |
| `summary` | string | No | Brief course description | Text field |
| `description` | string | No | Detailed course description | Text field |
| `status` | string | No | Publication status | `draft`, `published`, `archived`, `published_unactivated` |
| `subtitle` | string | No | Course subtitle | Max: 255 chars |
| `language` | string | No | Course language code | ISO 639-1 (2 chars, e.g., 'en', 'es') |
| `level` | string | No | Difficulty level | Max: 100 chars (e.g., 'beginner', 'intermediate', 'advanced') |
| `duration` | string | No | Estimated course duration | Max: 255 chars (e.g., '3 hours', '6 weeks') |
| `hours_to_complete` | integer | No | Hours required to complete | Numeric value |
| `target_group` | string | No | Target audience description | Max: 100 chars |
| `findable` | boolean | No | Whether course appears in search | Default: true |
| `public` | boolean | No | Free public access | Default: false |
| `fields` | json | No | Custom additional fields | JSON object for extensibility |

### Media Fields

| Field | Type | Required | Description | Validation Rules |
|-------|------|----------|-------------|-----------------|
| `image` | file | No | Course thumbnail image | Formats: jpg, png, gif, etc. |
| `image_path` | string | No | Path to stored image | Max: 255 chars |
| `video` | file | No | Course intro video | Formats: mp4, ogg, webm |
| `video_path` | string | No | Path to stored video | Max: 255 chars |
| `poster` | file | No | Course poster/banner | Image file |
| `poster_path` | string | No | Path to poster image | Max: 255 chars |
| `teaser_url` | string | No | External teaser video URL | Valid URL |

### Scheduling Fields

| Field | Type | Required | Description | Format |
|-------|------|----------|-------------|--------|
| `active_from` | datetime | No | Course start date | ISO 8601 (YYYY-MM-DD or full datetime) |
| `active_to` | datetime | No | Course end date | ISO 8601 (YYYY-MM-DD or full datetime) |

### Relationship Fields

| Field | Type | Required | Description | Validation Rules |
|-------|------|----------|-------------|-----------------|
| `authors` | array | No | Array of author user IDs | Array of integers, must be valid user IDs |
| `categories` | array | No | Associated category IDs | Array of valid category IDs |
| `tags` | array | No | Associated tags | Array of tag objects |
| `scorm_sco_id` | integer | No | SCORM package ID | Must exist in scorm_sco table |

---

## API Endpoints

### 1. Create Course

**Endpoint:** `POST /api/admin/courses`

**Authorization:** Required (Bearer token)

**Permissions:** `course_create`

**Request Headers:**
```http
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Request Body:**
```json
{
  "title": "Introduction to Web Development",
  "summary": "Learn the fundamentals of modern web development",
  "description": "This comprehensive course covers HTML, CSS, JavaScript, and modern frameworks...",
  "status": "draft",
  "subtitle": "From Zero to Hero",
  "language": "en",
  "level": "beginner",
  "duration": "40 hours",
  "hours_to_complete": 40,
  "target_group": "Aspiring web developers",
  "findable": true,
  "public": false,
  "authors": [1, 2, 3],
  "active_from": "2024-01-01",
  "active_to": "2024-12-31",
  "teaser_url": "https://youtube.com/watch?v=example",
  "fields": {
    "prerequisites": "Basic computer skills",
    "certification": "Yes",
    "support_available": true
  }
}
```

**Success Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": 101,
    "created_at": "2024-01-10T10:00:00Z",
    "updated_at": "2024-01-10T10:00:00Z",
    "title": "Introduction to Web Development",
    "summary": "Learn the fundamentals of modern web development",
    "description": "This comprehensive course covers HTML, CSS, JavaScript, and modern frameworks...",
    "status": "draft",
    "subtitle": "From Zero to Hero",
    "language": "en",
    "level": "beginner",
    "duration": "40 hours",
    "hours_to_complete": 40,
    "target_group": "Aspiring web developers",
    "findable": true,
    "public": false,
    "authors": [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
      }
    ],
    "categories": [],
    "tags": [],
    "lessons": [],
    "active_from": "2024-01-01T00:00:00Z",
    "active_to": "2024-12-31T23:59:59Z",
    "image_url": null,
    "video_url": null,
    "poster_url": null,
    "teaser_url": "https://youtube.com/watch?v=example",
    "users_count": 0,
    "scorm_sco_id": null,
    "fields": {
      "prerequisites": "Basic computer skills",
      "certification": "Yes",
      "support_available": true
    }
  },
  "message": "Course saved successfully"
}
```

### 2. Create Course with Media Files

**Endpoint:** `POST /api/admin/courses`

**Content-Type:** `multipart/form-data`

**Form Fields:**
```
title: "Photography Masterclass"
summary: "Professional photography techniques"
status: "published"
image: [FILE - course thumbnail]
video: [FILE - intro video]
poster: [FILE - banner image]
authors[0]: 1
authors[1]: 2
findable: true
public: false
```

### 3. Update Course

**Endpoint:** `POST /api/admin/courses/{id}`

**Note:** Uses POST with multipart/form-data for file uploads (Laravel method spoofing)

**Authorization:** Required

**Permissions:** `course_update` or `course_update_authored`

### 4. List Courses

**Endpoint:** `GET /api/courses`

**Authorization:** Optional (affects visibility)

**Query Parameters:**
```
per_page: 15
page: 1
order_by: created_at
order: DESC
status: published
findable: true
```

### 5. Get Course Details

**Endpoint:** `GET /api/courses/{id}`

**Authorization:** Optional (affects visible details)

### 6. Get Course Curriculum/Program

**Endpoint:** `GET /api/admin/courses/{id}/program`

**Authorization:** Required

**Description:** Returns full course structure with lessons and topics

---

## Request/Response Examples

### Example 1: Minimal Course Creation

**Request:**
```json
{
  "title": "Quick Start Guide to Docker"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 102,
    "title": "Quick Start Guide to Docker",
    "status": "draft",
    "findable": true,
    "public": false,
    // ... other fields with defaults
  },
  "message": "Course saved successfully"
}
```

### Example 2: Course with Complete Information

**Request:**
```json
{
  "title": "Advanced Machine Learning with Python",
  "summary": "Deep dive into ML algorithms and implementations",
  "description": "This course covers supervised learning, unsupervised learning, deep learning, and reinforcement learning with practical Python examples...",
  "status": "published",
  "language": "en",
  "level": "advanced",
  "duration": "80 hours",
  "hours_to_complete": 80,
  "target_group": "Data scientists and ML engineers",
  "findable": true,
  "public": false,
  "authors": [5, 8],
  "active_from": "2024-02-01",
  "active_to": "2024-08-31",
  "fields": {
    "prerequisites": "Python programming, Linear algebra, Statistics",
    "tools_required": "Jupyter Notebook, TensorFlow, PyTorch",
    "certification": "Professional ML Certificate",
    "project_based": true
  }
}
```

---

## Error Handling

### Common Error Responses

#### 401 Unauthorized
```json
{
  "message": "Unauthenticated."
}
```

#### 403 Forbidden
```json
{
  "success": false,
  "message": "You do not have permission to create courses"
}
```

#### 422 Validation Error
```json
{
  "message": "The given data was invalid.",
  "errors": {
    "title": [
      "The title field is required.",
      "The title must be at least 3 characters."
    ],
    "authors.0": [
      "The selected author is invalid."
    ],
    "video": [
      "The video must be a file of type: mp4, ogg, webm."
    ]
  }
}
```

#### 404 Not Found
```json
{
  "success": false,
  "message": "Course not found"
}
```

---

## Business Rules & Validation

### Title Validation
- **Required field**
- **Minimum length:** 3 characters
- **Maximum length:** 255 characters
- **Must be unique per organization** (depending on configuration)

### Author Validation
- Authors must be existing users with instructor/tutor role
- At least one author can be required (configurable)
- Authors are validated through `ValidAuthor` rule

### Status Transitions
```
draft → published → archived
draft → published_unactivated → published
```

### Date Validation
- `active_from` must be a valid date
- `active_to` must be a valid date
- `active_to` must be after `active_from` when both are provided

### File Upload Limits
- **Images:** jpg, jpeg, png, gif, svg, webp
- **Videos:** mp4, ogg, webm
- **Maximum file size:** Configured at server level (typically 100MB for videos)

### Course Visibility Logic
- **Findable = true:** Course appears in search results
- **Public = true:** Course accessible without purchase/enrollment
- **Status = published:** Course is live and accessible
- **Status = draft:** Only visible to authors and admins
- **Active dates:** Course only accessible between active_from and active_to

---

## Integration Guide

### Step 1: Authentication Setup
```javascript
// Frontend example
const API_BASE = 'https://api.yourdomain.com/api';
const token = localStorage.getItem('auth_token');

const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json',
  'Accept': 'application/json'
};
```

### Step 2: Course Creation Workflow
```javascript
async function createCourse(courseData) {
  try {
    const response = await fetch(`${API_BASE}/admin/courses`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(courseData)
    });

    if (!response.ok) {
      const error = await response.json();
      handleValidationErrors(error);
      return;
    }

    const result = await response.json();
    console.log('Course created:', result.data);
    return result.data;
  } catch (error) {
    console.error('Network error:', error);
  }
}
```

### Step 3: File Upload Handling
```javascript
async function createCourseWithMedia(formData) {
  const headers = {
    'Authorization': `Bearer ${token}`
    // Do not set Content-Type for FormData
  };

  const response = await fetch(`${API_BASE}/admin/courses`, {
    method: 'POST',
    headers: headers,
    body: formData // FormData object
  });

  return response.json();
}

// Usage
const formData = new FormData();
formData.append('title', 'Photography Course');
formData.append('image', imageFile);
formData.append('video', videoFile);
formData.append('authors[0]', '1');
formData.append('status', 'draft');

const course = await createCourseWithMedia(formData);
```

### Step 4: Validation Error Handling
```javascript
function handleValidationErrors(errorResponse) {
  if (errorResponse.errors) {
    Object.keys(errorResponse.errors).forEach(field => {
      const messages = errorResponse.errors[field];
      messages.forEach(message => {
        displayFieldError(field, message);
      });
    });
  } else {
    displayGeneralError(errorResponse.message);
  }
}
```

### Step 5: Course Publishing Flow
```javascript
async function publishCourse(courseId) {
  const updateData = {
    status: 'published',
    findable: true
  };

  const response = await fetch(`${API_BASE}/admin/courses/${courseId}`, {
    method: 'POST', // Laravel uses POST for updates with files
    headers: headers,
    body: JSON.stringify(updateData)
  });

  return response.json();
}
```

---

## Best Practices

### 1. Progressive Course Creation
Start with minimal required fields, then progressively add content:
1. Create draft with title
2. Add description and metadata
3. Upload media assets
4. Add lessons and content
5. Review and publish

### 2. Error Handling
- Always validate on frontend before API call
- Handle network errors gracefully
- Display user-friendly error messages
- Implement retry logic for network failures

### 3. File Upload Optimization
- Compress images before upload
- Show upload progress for large files
- Validate file types on frontend
- Consider chunked uploads for large videos

### 4. Caching Strategy
- Cache course lists with appropriate TTL
- Invalidate cache on course updates
- Use ETags for conditional requests

### 5. Security Considerations
- Validate file types and sizes
- Scan uploaded files for malware
- Implement rate limiting
- Use HTTPS for all API calls
- Store tokens securely (not in localStorage for sensitive apps)

---

## Additional Notes

### SCORM Support
When `scorm_sco_id` is provided:
- Course content is delivered via SCORM player
- Progress tracking follows SCORM standards
- Access via `/api/courses/{id}/scorm` endpoint

### Multi-tenancy
The API supports multi-tenant architectures where:
- Courses can be organization-specific
- Permissions are scoped to organizations
- Course IDs are globally unique

### Webhooks
The system fires events on course lifecycle:
- `CourseCreated`
- `CourseUpdated`
- `CourseStatusChanged`
- `CourseDeleted`

### Rate Limits
- Standard: 60 requests per minute
- File uploads: 10 per minute
- Adjust based on your infrastructure

---

## Support & Resources

- **API Status:** https://status.yourdomain.com
- **Developer Documentation:** https://docs.yourdomain.com
- **Support Email:** api-support@yourdomain.com
- **Community Forum:** https://community.yourdomain.com

---

*Last Updated: January 2024*
*API Version: 1.0*