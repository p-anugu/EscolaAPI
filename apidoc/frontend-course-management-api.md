# Course Management API Guide for Frontend

## Purpose
This guide provides all API endpoints needed to CREATE, UPDATE, and DELETE courses and their components (lessons, topics, resources).

## Authentication
```javascript
// Login first - token expires after 5 minutes
POST /api/auth/login
Body: {"email": "admin2@escolalms.com", "password": "secret"}
Returns: { token: "Bearer token here" }

// Use token in all subsequent requests
Headers: { "Authorization": "Bearer {token}" }
```

---

# COURSE CRUD OPERATIONS

## 1. CREATE Course
**Endpoint:** `POST /api/admin/courses`

### ALL Available Fields (from database schema):
```javascript
{
  // REQUIRED
  "title": "Course Name",                    // varchar(255) - Course title

  // OPTIONAL TEXT CONTENT
  "summary": "Brief description",            // text - Short description
  "description": "Full HTML content",        // text - Complete course description
  "subtitle": "Secondary title",             // varchar(255) - Subtitle

  // MEDIA PATHS
  "image_path": "course/1/image.jpg",       // varchar(255) - Course thumbnail
  "video_path": "course/1/intro.mp4",       // varchar(255) - Intro video
  "poster_path": "course/1/poster.jpg",     // varchar(255) - Poster image
  "teaser_url": "https://youtube.com/...",  // varchar(255) - Preview video URL

  // COURSE SETTINGS
  "status": "published",                     // varchar(255) - published|draft|archived|ended
  "level": "beginner",                      // varchar(100) - beginner|intermediate|advanced
  "language": "en",                         // varchar(2) - ISO code (en, es, fr, etc)
  "target_group": "Developers",             // varchar(100) - Target audience

  // TIME SETTINGS
  "duration": "20 hours",                   // varchar(255) - Estimated duration
  "hours_to_complete": 20,                  // integer - Numeric hours
  "active_from": "2024-01-01T00:00:00Z",   // timestamp - Course start date
  "active_to": "2024-12-31T23:59:59Z",     // timestamp - Course end date

  // VISIBILITY
  "findable": true,                         // boolean - Show in public listings
  "public": false,                          // boolean - Free access without enrollment

  // ADVANCED
  "scorm_sco_id": null,                     // bigint - SCORM package ID
  "fields": {"custom": "metadata"},         // json - Custom metadata

  // RELATIONSHIPS (arrays of IDs)
  "authors": [1, 2],                        // Array of user IDs
  "categories": [3, 4],                     // Array of category IDs
  "tags": ["web", "javascript"]             // Array of tag strings
}
```

### Example Create Request:
```javascript
const response = await fetch('http://api.localhost/api/admin/courses', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    "title": "Complete Web Development",
    "summary": "Learn web dev from scratch",
    "description": "<h1>Course Overview</h1><p>Full HTML description here...</p>",
    "status": "published",
    "level": "beginner",
    "language": "en",
    "duration": "40 hours",
    "hours_to_complete": 40,
    "target_group": "Beginners and students",
    "teaser_url": "https://youtube.com/watch?v=abc123",
    "findable": true,
    "public": false
  })
});
```

## 2. READ Course
**Get Single Course:** `GET /api/admin/courses/{id}`
**List All Courses:** `GET /api/admin/courses`

### Response includes all database fields PLUS computed fields:
```javascript
{
  // All create fields plus:
  "id": 1,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-15T14:30:00Z",
  "author_id": 2,                         // Backward compatibility

  // Computed URL fields (read-only)
  "image_url": "http://storage.localhost/...",  // Full URL from image_path
  "video_url": "http://storage.localhost/...",  // Full URL from video_path
  "poster_url": "http://storage.localhost/...", // Full URL from poster_path

  // Relationships (read-only)
  "author": { /* user object */ },
  "authors": [ /* array of user objects */ ],
  "categories": [ /* array of category objects */ ],
  "tags": [ /* array of tag objects */ ],
  "lessons": [ /* array of lesson objects */ ],
  "users_count": 25
}
```

## 3. UPDATE Course
**Endpoint:** `POST /api/admin/courses/{id}`
*Note: Uses POST, not PUT (for file upload support)*

### All fields from CREATE are updatable:
```javascript
// Update any combination of fields
{
  "title": "Updated Course Title",
  "status": "draft",
  "teaser_url": "https://youtube.com/watch?v=new",
  "hours_to_complete": 45,
  "findable": false
}
```

## 4. DELETE Course
**Endpoint:** `DELETE /api/admin/courses/{id}`

```javascript
// No body required
const response = await fetch(`http://api.localhost/api/admin/courses/${courseId}`, {
  method: 'DELETE',
  headers: { 'Authorization': `Bearer ${token}` }
});
// Returns: { "success": true, "message": "Course deleted successfully" }
```

---

# COURSE COMPONENT MANAGEMENT

## Course Structure Hierarchy
```
Course (top level)
├── Lesson 1 (module/chapter)
│   ├── Topic 1.1 (content item)
│   │   ├── Topicable Content (RichText/Video/PDF/etc)
│   │   └── Resources (supplementary files)
│   └── Topic 1.2
└── Lesson 2
    └── Topic 2.1
```

---

# LESSON CRUD OPERATIONS

## 1. CREATE Lesson
**Endpoint:** `POST /api/admin/lessons`

```javascript
{
  "course_id": 1,                    // REQUIRED - Parent course ID
  "title": "Chapter 1: Introduction", // REQUIRED
  "summary": "Lesson description",    // Optional
  "duration": "2 hours",              // Optional
  "order": 1,                         // REQUIRED - Position in course
  "active": true,                     // Optional - Enable/disable
  "parent_lesson_id": null,           // Optional - For nested lessons
  "active_from": "2024-01-01T00:00:00Z", // Optional
  "active_to": null                   // Optional
}
```

## 2. UPDATE Lesson
**Endpoint:** `PUT /api/admin/lessons/{lesson_id}`

```javascript
{
  "title": "Updated Lesson Title",
  "order": 2,
  "active": false
}
```

## 3. DELETE Lesson
**Endpoint:** `DELETE /api/admin/lessons/{lesson_id}`

## 4. CLONE Lesson
**Endpoint:** `POST /api/admin/lessons/{lesson_id}/clone`
- Duplicates lesson with all its topics

---

# TOPIC CRUD OPERATIONS

## Available Topic Types
```javascript
const TOPIC_TYPES = {
  RICH_TEXT: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\RichText',
  VIDEO: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\Video',
  AUDIO: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\Audio',
  IMAGE: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\Image',
  PDF: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\PDF',
  H5P: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\H5P',
  SCORM: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\ScormSco',
  CIMI5: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\Cmi5Au',
  OEMBED: 'EscolaLms\\TopicTypes\\Models\\TopicContent\\OEmbed'
};
```

## 1. CREATE Topic
**Endpoint:** `POST /api/admin/topics`

```javascript
{
  // REQUIRED
  "lesson_id": 1,                           // Parent lesson ID
  "title": "Introduction to HTML",          // Topic title
  "topicable_type": "EscolaLms\\TopicTypes\\Models\\TopicContent\\RichText",

  // CONTENT (depends on type)
  "value": "<h1>HTML Basics</h1><p>Content here...</p>", // For RichText
  // OR
  "value": "http://example.com/video.mp4",  // For Video type
  // OR
  "value": "http://example.com/doc.pdf",    // For PDF type

  // OPTIONAL METADATA
  "summary": "Brief topic overview",
  "introduction": "Opening statement",
  "description": "Detailed description",
  "order": 1,                               // Position in lesson
  "active": true,                           // Enable/disable
  "preview": false,                         // Allow free preview
  "can_skip": false,                        // Make optional
  "duration": "15 minutes",                 // Estimated time
  "json": {"custom": "data"}                // Custom metadata
}
```

### Example: Create Different Topic Types

#### RichText Topic (HTML Content):
```javascript
{
  "lesson_id": 1,
  "title": "Welcome Message",
  "topicable_type": "EscolaLms\\TopicTypes\\Models\\TopicContent\\RichText",
  "value": "<h1>Welcome!</h1><p>Course content here...</p>",
  "order": 1
}
```

#### Video Topic:
```javascript
{
  "lesson_id": 1,
  "title": "Introduction Video",
  "topicable_type": "EscolaLms\\TopicTypes\\Models\\TopicContent\\Video",
  "value": "course/1/videos/intro.mp4",
  "order": 2,
  "duration": "10 minutes"
}
```

#### PDF Topic:
```javascript
{
  "lesson_id": 1,
  "title": "Course Handbook",
  "topicable_type": "EscolaLms\\TopicTypes\\Models\\TopicContent\\PDF",
  "value": "course/1/documents/handbook.pdf",
  "order": 3
}
```

## 2. UPDATE Topic
**Endpoint:** `POST /api/admin/topics/{topic_id}`
*Note: Uses POST for file support*

```javascript
{
  "title": "Updated Topic Title",
  "value": "<h1>Updated content</h1>",
  "order": 2,
  "preview": true
}
```

## 3. DELETE Topic
**Endpoint:** `DELETE /api/admin/topics/{topic_id}`

## 4. CLONE Topic
**Endpoint:** `POST /api/admin/topics/{topic_id}/clone`

## 5. GET Topic Types
**Endpoint:** `GET /api/admin/topics/types`
- Returns list of available topic content types

---

# TOPIC RESOURCES (File Attachments)

## 1. Upload Resource File
**Endpoint:** `POST /api/admin/topics/{topic_id}/resources`

```javascript
const formData = new FormData();
formData.append('resource', fileInput.files[0]);
formData.append('name', 'worksheet.pdf');

fetch(`/api/admin/topics/${topicId}/resources`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData
});
```

## 2. List Topic Resources
**Endpoint:** `GET /api/admin/topics/{topic_id}/resources`

## 3. Rename Resource
**Endpoint:** `PATCH /api/admin/topics/{topic_id}/resources/{resource_id}`

```javascript
{
  "name": "new-filename.pdf"
}
```

## 4. Delete Resource
**Endpoint:** `DELETE /api/admin/topics/{topic_id}/resources/{resource_id}`

---

# REORDERING CONTENT

## Sort Lessons or Topics
**Endpoint:** `POST /api/admin/courses/sort`

```javascript
// Reorder lessons within a course
{
  "class": "Lesson",
  "orders": [
    {"id": 3, "order": 1},  // Lesson 3 becomes first
    {"id": 1, "order": 2},  // Lesson 1 becomes second
    {"id": 2, "order": 3}   // Lesson 2 becomes third
  ]
}

// Reorder topics within a lesson
{
  "class": "Topic",
  "orders": [
    {"id": 5, "order": 1},
    {"id": 7, "order": 2},
    {"id": 6, "order": 3}
  ]
}
```

---

# COMPLETE WORKING EXAMPLE

## Create a Full Course with Content

```javascript
// 1. Login and get token
const loginResponse = await fetch('http://api.localhost/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'admin2@escolalms.com',
    password: 'secret'
  })
});
const { data: { token } } = await loginResponse.json();

// 2. Create course
const courseResponse = await fetch('http://api.localhost/api/admin/courses', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: "JavaScript Mastery",
    summary: "Master JavaScript from basics to advanced",
    status: "published",
    level: "beginner",
    duration: "30 hours",
    teaser_url: "https://youtube.com/watch?v=preview123",
    findable: true,
    public: false
  })
});
const { data: course } = await courseResponse.json();

// 3. Create lesson
const lessonResponse = await fetch('http://api.localhost/api/admin/lessons', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    course_id: course.id,
    title: "Chapter 1: JavaScript Basics",
    summary: "Introduction to JavaScript fundamentals",
    order: 1,
    active: true
  })
});
const { data: lesson } = await lessonResponse.json();

// 4. Create topic with content
const topicResponse = await fetch('http://api.localhost/api/admin/topics', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    lesson_id: lesson.id,
    title: "What is JavaScript?",
    topicable_type: "EscolaLms\\TopicTypes\\Models\\TopicContent\\RichText",
    value: "<h1>Introduction to JavaScript</h1><p>JavaScript is a programming language...</p>",
    order: 1,
    active: true,
    preview: true,
    duration: "10 minutes"
  })
});

console.log('Course created with ID:', course.id);
```

---

# FIELD REFERENCE

## Database Fields vs API Fields

### Writable Fields (you can set these):
- All fields listed in CREATE operations above

### Read-only Fields (computed by API):
- `id` - Auto-generated
- `created_at`, `updated_at` - Timestamps
- `image_url`, `video_url`, `poster_url` - Full URLs computed from path fields
- `author`, `authors` - User relationship objects
- `categories`, `tags` - Relationship objects
- `lessons` - Lesson array
- `users_count` - Enrolled count

### File Upload Fields:
For actual file uploads (not just paths), use FormData:
```javascript
const formData = new FormData();
formData.append('title', 'Course Title');
formData.append('image', imageFile);  // Actual file upload
formData.append('video', videoFile);  // Actual file upload
formData.append('poster', posterFile); // Actual file upload
```

---

# ERROR RESPONSES

```javascript
// Success
{ "success": true, "data": {...} }

// Validation Error (422)
{
  "success": false,
  "message": "The given data was invalid",
  "errors": {
    "title": ["The title field is required"],
    "order": ["The order must be a number"]
  }
}

// Unauthorized (401)
{ "message": "Unauthenticated." }

// Not Found (404)
{ "success": false, "message": "Course not found" }
```

---

# TEST CREDENTIALS & DATA

```javascript
// Admin login
const ADMIN = {
  email: 'admin2@escolalms.com',
  password: 'secret'
};

// Test course exists
const TEST_COURSE_ID = 11; // "Introduction to Web Development"
```