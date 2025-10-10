# EscolaLMS Course API Documentation

## Overview
This document provides comprehensive API documentation for course-related endpoints in the EscolaLMS system. All API endpoints require proper authentication unless marked as public.

## Authentication
Most endpoints require Bearer token authentication. Include the token in the Authorization header:
```
Authorization: Bearer {your-token}
```

## Base URL
```
http://api.localhost
```

---

## Public Course Endpoints

### 1. List All Courses (Public)
Get a paginated list of published courses.

**Endpoint:** `GET /api/courses`

**Authentication:** Optional (authenticated users may see more courses)

**Query Parameters:**
- `page` (integer): Page number for pagination
- `per_page` (integer): Items per page (default: 15)
- `order` (string): Sort field
- `order_by` (string): Sort direction (asc/desc)
- `title` (string): Filter by title
- `category_id` (integer): Filter by category
- `tag` (string): Filter by tag
- `status` (string): Filter by status (public sees only published)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Introduction to Programming",
      "summary": "Learn the basics of programming",
      "image_url": "http://api.localhost/storage/courses/1/image.jpg",
      "duration": "10 hours",
      "level": "beginner",
      "authors": [
        {
          "id": 1,
          "name": "John Doe",
          "email": "john@example.com"
        }
      ],
      "categories": [],
      "tags": ["programming", "basics"],
      "users_count": 25,
      "lessons_count": 5
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 15,
    "total": 50
  }
}
```

### 2. Get Course Details
Get detailed information about a specific course.

**Endpoint:** `GET /api/courses/{course_id}`

**Authentication:** Optional

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Introduction to Programming",
    "summary": "Learn the basics of programming",
    "description": "Full course description...",
    "image_url": "http://api.localhost/storage/courses/1/image.jpg",
    "video_url": "http://api.localhost/storage/courses/1/intro.mp4",
    "duration": "10 hours",
    "level": "beginner",
    "language": "en",
    "subtitle": "From Zero to Hero",
    "target_group": "Beginners",
    "hours_to_complete": 10,
    "active_from": "2024-01-01T00:00:00Z",
    "active_to": null,
    "authors": [...],
    "categories": [...],
    "tags": [...],
    "lessons": [...]
  }
}
```

### 3. Get Course Curriculum/Program
Get the full course structure with lessons and topics.

**Endpoint:** `GET /api/courses/{course_id}/program`

**Authentication:** Optional (authenticated users see more details)

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Introduction to Programming",
    "lessons": [
      {
        "id": 1,
        "title": "Getting Started",
        "summary": "Setup your environment",
        "order": 1,
        "duration": "1 hour",
        "topics": [
          {
            "id": 1,
            "title": "Installing IDE",
            "summary": "How to install development tools",
            "topicable_type": "EscolaLms\\TopicTypes\\Models\\TopicContent\\RichText",
            "topicable_id": 1,
            "order": 1,
            "active": true,
            "can_skip": false,
            "duration": "30 minutes"
          }
        ]
      }
    ]
  }
}
```

### 4. Preview Course Topic
Preview a specific topic without enrollment (only for topics marked as preview).

**Endpoint:** `GET /api/courses/{course_id}/preview/{topic_id}`

**Authentication:** Not required

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 5,
    "title": "Course Introduction",
    "topicable": {
      "value": "<h1>Welcome to the course!</h1><p>Course content...</p>"
    }
  }
}
```

---

## Authenticated User Endpoints

### 5. Get My Course IDs
Get list of course IDs the authenticated user has access to.

**Endpoint:** `GET /api/courses/my`

**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "data": [1, 3, 5, 7]
}
```

### 6. Get Authored Courses
Get courses created/taught by the authenticated user.

**Endpoint:** `GET /api/courses/authored`

**Authentication:** Required

**Query Parameters:**
- `page` (integer): Page number
- `per_page` (integer): Items per page (default: 20)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 2,
      "title": "Advanced JavaScript",
      "status": "published",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

---

## Course Progress Endpoints

### 7. Get All Course Progress
Get progress for all enrolled courses.

**Endpoint:** `GET /api/courses/progress`

**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "course": {
        "id": 1,
        "title": "Introduction to Programming"
      },
      "progress": 75,
      "finished": false,
      "started_at": "2024-01-20T10:00:00Z",
      "finished_at": null
    }
  ]
}
```

### 8. Get Paginated Course Progress
Get paginated progress for enrolled courses.

**Endpoint:** `GET /api/courses/progress/paginated`

**Authentication:** Required

**Query Parameters:**
- `page` (integer): Page number
- `per_page` (integer): Items per page

### 9. Get Specific Course Progress
Get progress for a specific course.

**Endpoint:** `GET /api/courses/progress/{course_id}`

**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "data": {
    "course_id": 1,
    "progress": 75,
    "finished": false,
    "started_at": "2024-01-20T10:00:00Z",
    "finish_date": null,
    "topics": [
      {
        "topic_id": 1,
        "status": "complete",
        "started_at": "2024-01-20T10:00:00Z",
        "finished_at": "2024-01-20T10:30:00Z"
      }
    ]
  }
}
```

### 10. Update Course Progress
Mark topics as started/completed.

**Endpoint:** `PATCH /api/courses/progress/{course_id}`

**Authentication:** Required

**Request Body:**
```json
{
  "progress": [
    {
      "topic_id": 1,
      "status": "complete"
    }
  ]
}
```

### 11. Ping Topic Progress
Update time spent on a topic (for tracking).

**Endpoint:** `PUT /api/courses/progress/{topic_id}/ping`

**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "message": "Progress updated"
}
```

### 12. Update H5P Progress
Update progress for H5P interactive content.

**Endpoint:** `POST /api/courses/progress/{topic_id}/h5p`

**Authentication:** Required

**Request Body:**
```json
{
  "event": "completed",
  "score": 95
}
```

---

## Admin Course Management Endpoints

### 13. List Courses (Admin)
Get all courses with admin privileges.

**Endpoint:** `GET /api/admin/courses`

**Authentication:** Required (Admin role)

**Query Parameters:**
- Same as public course list, plus:
- `author_id` (integer): Filter by author
- `findable` (boolean): Filter by visibility

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Introduction to Programming",
      "status": "draft",
      "findable": true,
      "public": false,
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-15T14:30:00Z"
    }
  ]
}
```

### 14. Create Course (Admin)
Create a new course.

**Endpoint:** `POST /api/admin/courses`

**Authentication:** Required (Admin role)

**Request Body:**
```json
{
  "title": "New Course Title",
  "summary": "Brief course description",
  "description": "Detailed course description",
  "status": "draft",
  "duration": "5 hours",
  "level": "intermediate",
  "language": "en",
  "subtitle": "Course subtitle",
  "target_group": "Developers",
  "hours_to_complete": 5,
  "findable": true,
  "public": false,
  "active_from": "2024-02-01T00:00:00Z",
  "active_to": null,
  "authors": [1, 2],
  "categories": [3, 4],
  "tags": ["programming", "web development"]
}
```

### 15. Update Course (Admin)
Update an existing course.

**Endpoint:** `POST /api/admin/courses/{course_id}`

**Authentication:** Required (Admin role)

**Request Body:** Same as Create Course

**Note:** Uses POST instead of PUT due to file upload support

### 16. Delete Course (Admin)
Delete a course permanently.

**Endpoint:** `DELETE /api/admin/courses/{course_id}`

**Authentication:** Required (Admin role)

**Response:**
```json
{
  "success": true,
  "message": "Course deleted successfully"
}
```

### 17. Get Course Program (Admin)
Get full course curriculum with admin details.

**Endpoint:** `GET /api/admin/courses/{course_id}/program`

**Authentication:** Required (Admin role)

**Response:** Similar to public program but includes:
- Hidden topics
- Draft lessons
- Internal metadata
- Edit permissions

### 18. Sort Course Content
Reorder lessons and topics.

**Endpoint:** `POST /api/admin/courses/sort`

**Authentication:** Required (Admin role)

**Request Body:**
```json
{
  "class": "Lesson",
  "orders": [
    {"id": 3, "order": 1},
    {"id": 1, "order": 2},
    {"id": 2, "order": 3}
  ]
}
```

---

## Lesson Management Endpoints

### 19. Create Lesson
Add a new lesson to a course.

**Endpoint:** `POST /api/admin/lessons`

**Authentication:** Required (Admin role)

**Request Body:**
```json
{
  "course_id": 1,
  "title": "New Lesson",
  "summary": "Lesson description",
  "duration": "45 minutes",
  "order": 1,
  "active": true,
  "active_from": null,
  "active_to": null
}
```

### 20. Update Lesson
Update lesson details.

**Endpoint:** `PUT /api/admin/lessons/{lesson_id}`

**Authentication:** Required (Admin role)

### 21. Delete Lesson
Remove a lesson from a course.

**Endpoint:** `DELETE /api/admin/lessons/{lesson_id}`

**Authentication:** Required (Admin role)

### 22. Clone Lesson
Duplicate a lesson with all its topics.

**Endpoint:** `POST /api/admin/lessons/{lesson_id}/clone`

**Authentication:** Required (Admin role)

---

## Topic Management Endpoints

### 23. Get Topic Types
List available topic content types.

**Endpoint:** `GET /api/admin/topics/types`

**Authentication:** Required (Admin role)

**Response:**
```json
{
  "success": true,
  "data": [
    "EscolaLms\\TopicTypes\\Models\\TopicContent\\RichText",
    "EscolaLms\\TopicTypes\\Models\\TopicContent\\Video",
    "EscolaLms\\TopicTypes\\Models\\TopicContent\\Audio",
    "EscolaLms\\TopicTypes\\Models\\TopicContent\\H5P",
    "EscolaLms\\TopicTypes\\Models\\TopicContent\\PDF"
  ]
}
```

### 24. Create Topic
Add a new topic to a lesson.

**Endpoint:** `POST /api/admin/topics`

**Authentication:** Required (Admin role)

**Request Body:**
```json
{
  "lesson_id": 1,
  "title": "Topic Title",
  "topicable_type": "EscolaLms\\TopicTypes\\Models\\TopicContent\\RichText",
  "value": "<h1>Topic Content</h1><p>HTML content here...</p>",
  "summary": "Brief summary",
  "introduction": "Topic introduction",
  "description": "Detailed description",
  "order": 1,
  "active": true,
  "preview": false,
  "can_skip": false,
  "duration": "15 minutes"
}
```

### 25. Update Topic
Modify topic content.

**Endpoint:** `POST /api/admin/topics/{topic_id}`

**Authentication:** Required (Admin role)

**Note:** Uses POST for file upload support

### 26. Delete Topic
Remove a topic from a lesson.

**Endpoint:** `DELETE /api/admin/topics/{topic_id}`

**Authentication:** Required (Admin role)

### 27. Clone Topic
Duplicate a topic.

**Endpoint:** `POST /api/admin/topics/{topic_id}/clone`

**Authentication:** Required (Admin role)

---

## Topic Resources Endpoints

### 28. List Topic Resources
Get files attached to a topic.

**Endpoint:** `GET /api/admin/topics/{topic_id}/resources`

**Authentication:** Required (Admin role)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "slides.pdf",
      "url": "http://api.localhost/storage/resources/1/slides.pdf",
      "size": 2048576,
      "created_at": "2024-01-20T10:00:00Z"
    }
  ]
}
```

### 29. Upload Topic Resource
Attach a file to a topic.

**Endpoint:** `POST /api/admin/topics/{topic_id}/resources`

**Authentication:** Required (Admin role)

**Request:** Multipart form data
- `resource` (file): The file to upload
- `name` (string): Optional custom name

### 30. Rename Topic Resource
Change resource file name.

**Endpoint:** `PATCH /api/admin/topics/{topic_id}/resources/{resource_id}`

**Authentication:** Required (Admin role)

**Request Body:**
```json
{
  "name": "new-filename.pdf"
}
```

### 31. Delete Topic Resource
Remove a resource file.

**Endpoint:** `DELETE /api/admin/topics/{topic_id}/resources/{resource_id}`

**Authentication:** Required (Admin role)

---

## Course Access Management

### 32. Get Course Access List
Get users with access to a course.

**Endpoint:** `GET /api/admin/courses/{course_id}/access`

**Authentication:** Required (Admin role)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "user_id": 5,
      "name": "Jane Smith",
      "email": "jane@example.com",
      "enrolled_at": "2024-01-15T10:00:00Z",
      "end_date": null
    }
  ]
}
```

### 33. Grant Course Access
Give users access to a course.

**Endpoint:** `POST /api/admin/courses/{course_id}/access/add`

**Authentication:** Required (Admin role)

**Request Body:**
```json
{
  "users": [5, 6, 7],
  "end_date": "2024-12-31T23:59:59Z"
}
```

### 34. Remove Course Access
Revoke user access to a course.

**Endpoint:** `POST /api/admin/courses/{course_id}/access/remove`

**Authentication:** Required (Admin role)

**Request Body:**
```json
{
  "users": [5, 6]
}
```

### 35. Set Course Access
Replace entire access list for a course.

**Endpoint:** `POST /api/admin/courses/{course_id}/access/set`

**Authentication:** Required (Admin role)

**Request Body:**
```json
{
  "users": [1, 2, 3, 4, 5]
}
```

---

## Course Authors/Tutors Endpoints

### 36. List All Tutors
Get list of course instructors.

**Endpoint:** `GET /api/tutors`

**Authentication:** Not required

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "bio": "Experienced developer and instructor",
      "courses_count": 5
    }
  ]
}
```

### 37. Get Tutor Details
Get specific tutor information.

**Endpoint:** `GET /api/tutors/{tutor_id}`

**Authentication:** Not required

### 38. Get Assignable Users (Admin)
List users who can be assigned as course authors.

**Endpoint:** `GET /api/admin/courses/users/assignable`

**Authentication:** Required (Admin role)

### 39. Assign Tutor to Course
Add an author to a course.

**Endpoint:** `POST /api/admin/tutors/{user_id}/assign/{course_id}`

**Authentication:** Required (Admin role)

### 40. Unassign Tutor from Course
Remove an author from a course.

**Endpoint:** `POST /api/admin/tutors/{user_id}/unassign/{course_id}`

**Authentication:** Required (Admin role)

---

## Tag Management

### 41. Get Unique Course Tags
Get all unique tags from active courses.

**Endpoint:** `GET /api/tags/uniqueTags`

**Authentication:** Not required

**Response:**
```json
{
  "success": true,
  "data": [
    "programming",
    "web development",
    "javascript",
    "python"
  ]
}
```

---

## SCORM Support

### 42. Launch SCORM Course
Launch SCORM player for a course.

**Endpoint:** `GET /api/courses/{course_id}/scorm`

**Authentication:** Required

**Response:** HTML page with SCORM player

---

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Request successful, no content to return
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Authentication required or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation errors
- `500 Internal Server Error` - Server error

## Error Response Format

```json
{
  "success": false,
  "message": "Error message",
  "errors": {
    "field_name": [
      "Validation error message"
    ]
  }
}
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- Authenticated users: 60 requests per minute
- Unauthenticated users: 30 requests per minute

## Pagination

Most list endpoints support pagination with these parameters:
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 15, max: 100)

Paginated responses include metadata:
```json
{
  "meta": {
    "current_page": 1,
    "from": 1,
    "last_page": 5,
    "per_page": 15,
    "to": 15,
    "total": 75
  }
}
```

## File Uploads

For endpoints that accept file uploads:
1. Use `multipart/form-data` content type
2. Maximum file sizes:
   - Images: 5MB
   - Videos: 500MB
   - Documents: 20MB
3. Accepted formats:
   - Images: jpg, jpeg, png, gif, webp
   - Videos: mp4, webm, ogg
   - Documents: pdf, doc, docx, ppt, pptx

## Filtering and Sorting

Many list endpoints support filtering and sorting:
- Use query parameters for filtering (e.g., `?status=published&level=beginner`)
- Use `order` and `order_by` for sorting (e.g., `?order=title&order_by=asc`)
- Multiple filters are combined with AND logic

## Best Practices

1. **Always include authentication headers** for protected endpoints
2. **Handle pagination** for large datasets
3. **Implement proper error handling** for all status codes
4. **Cache responses** where appropriate (especially for course lists and curricula)
5. **Use appropriate HTTP methods** (GET for reading, POST for creating, PUT/PATCH for updating, DELETE for removing)
6. **Validate input** before sending requests
7. **Respect rate limits** to avoid being throttled