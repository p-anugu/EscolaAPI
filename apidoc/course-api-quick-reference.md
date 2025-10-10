# Course API Quick Reference

## Essential Information for Frontend Team

### Authentication
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Create Course Endpoint
**URL:** `POST https://api.yourdomain.com/api/admin/courses`

### Minimal Required Request
```json
{
  "title": "Course Title Here"  // Only required field (min 3 chars)
}
```

### Complete Request Example
```json
{
  "title": "Complete Web Development Bootcamp",
  "summary": "Learn full-stack development from scratch",
  "description": "Detailed description with markdown support...",
  "status": "draft",              // Options: draft, published, archived, published_unactivated
  "subtitle": "2024 Edition",
  "language": "en",               // ISO 639-1 code (2 chars)
  "level": "beginner",            // beginner, intermediate, advanced
  "duration": "60 hours",         // Free text format
  "hours_to_complete": 60,        // Integer
  "target_group": "Career changers and beginners",
  "findable": true,               // Appears in search
  "public": false,                // Requires enrollment/purchase
  "authors": [1, 2],              // Array of user IDs
  "active_from": "2024-01-15",    // YYYY-MM-DD format
  "active_to": "2024-12-31",
  "teaser_url": "https://vimeo.com/123456789",
  "fields": {                     // Custom fields (JSON)
    "prerequisites": "None",
    "includes_certificate": true,
    "difficulty_rating": 2
  }
}
```

### File Upload (multipart/form-data)
```javascript
const formData = new FormData();
formData.append('title', 'Photography Masterclass');
formData.append('summary', 'Learn professional photography');
formData.append('image', imageFile);      // Course thumbnail
formData.append('video', videoFile);      // Intro video (mp4, webm, ogg)
formData.append('poster', posterFile);    // Banner image
formData.append('status', 'draft');
formData.append('authors[0]', '1');       // Array notation for authors
formData.append('authors[1]', '2');

fetch('/api/admin/courses', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
    // Don't set Content-Type with FormData
  },
  body: formData
});
```

### Success Response Structure
```json
{
  "success": true,
  "data": {
    "id": 101,
    "created_at": "2024-01-10T10:00:00Z",
    "updated_at": "2024-01-10T10:00:00Z",
    "title": "Course Title",
    "status": "draft",
    "authors": [{
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    }],
    "image_url": "https://cdn.example.com/courses/101/image.jpg",
    "video_url": "https://cdn.example.com/courses/101/video.mp4",
    "poster_url": "https://cdn.example.com/courses/101/poster.jpg",
    // ... all other fields
  },
  "message": "Course saved successfully"
}
```

### Validation Error Response
```json
{
  "message": "The given data was invalid.",
  "errors": {
    "title": ["The title must be at least 3 characters."],
    "video": ["The video must be a file of type: mp4, ogg, webm."]
  }
}
```

### Field Validation Rules

| Field | Rules | Example |
|-------|-------|---------|
| title | Required, min 3, max 255 chars | "Introduction to React" |
| summary | Optional, text | "Learn React from basics" |
| status | One of: draft, published, archived, published_unactivated | "draft" |
| language | 2-char ISO code | "en", "es", "fr" |
| level | Max 100 chars | "beginner" |
| duration | Max 255 chars | "6 weeks", "30 hours" |
| hours_to_complete | Integer | 30 |
| authors | Array of existing user IDs | [1, 2, 3] |
| active_from/to | Date format YYYY-MM-DD | "2024-01-15" |
| image | Image file | .jpg, .png, .gif |
| video | Video file | .mp4, .webm, .ogg |
| findable | Boolean | true/false |
| public | Boolean | true/false |

### Common Integration Patterns

#### 1. Basic Course Creation
```javascript
async function createBasicCourse() {
  const course = {
    title: "My New Course",
    status: "draft",
    summary: "Course summary here"
  };

  const response = await fetch('/api/admin/courses', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(course)
  });

  return response.json();
}
```

#### 2. Course with Media
```javascript
async function createCourseWithMedia(title, imageFile, videoFile) {
  const formData = new FormData();
  formData.append('title', title);
  formData.append('image', imageFile);
  formData.append('video', videoFile);
  formData.append('status', 'draft');

  const response = await fetch('/api/admin/courses', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });

  return response.json();
}
```

#### 3. Error Handling
```javascript
async function createCourse(courseData) {
  try {
    const response = await fetch('/api/admin/courses', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(courseData)
    });

    const result = await response.json();

    if (!response.ok) {
      // Handle validation errors
      if (result.errors) {
        console.error('Validation errors:', result.errors);
        // Display errors to user
      }
      return null;
    }

    // Success
    return result.data;
  } catch (error) {
    console.error('Network error:', error);
    // Handle network failure
  }
}
```

### Required Permissions
- User must have `course_create` permission
- Obtained through role assignment (Admin, Instructor, etc.)

### Tips for Frontend Implementation

1. **Start Simple**: Create with just title first, then update with more details
2. **Validate Client-Side**: Check required fields before API call
3. **Handle Loading States**: Show progress for file uploads
4. **Cache Responses**: Store created course data locally
5. **Implement Drafts**: Save as draft frequently during creation
6. **File Size Limits**: Validate before upload (typically max 100MB for videos)
7. **Image Optimization**: Compress images before upload
8. **Progress Indication**: Show upload percentage for large files

### Testing Checklist

- [ ] Create course with only title
- [ ] Create course with all fields
- [ ] Upload image file
- [ ] Upload video file
- [ ] Handle validation errors
- [ ] Test with invalid auth token
- [ ] Test file type validation
- [ ] Test special characters in title
- [ ] Test date field formats
- [ ] Test array fields (authors)
- [ ] Test custom fields (JSON)

### Postman Collection Variables
```json
{
  "base_url": "https://api.yourdomain.com/api",
  "auth_token": "YOUR_TOKEN_HERE",
  "course_id": "101"
}
```

---

**Need Help?**
- Check the full documentation: `course-api-specification.md`
- API errors? Check response status and message
- Validation failed? Check the `errors` object in response