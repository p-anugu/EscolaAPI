# Course API Documentation & Questions

**Date:** 2024-01-10
**From:** Frontend Team
**Priority:** High - Blocking course creation feature development

---

## 📚 Documentation Index

This directory contains comprehensive documentation for the Course Creation API:

### Available Documents

1. **`course-api-specification.md`** - Complete API documentation
   - Full endpoint specifications
   - Request/response examples
   - Authentication & authorization
   - Data model definitions
   - Validation rules & business logic
   - Integration guide with code examples

2. **`course-api-quick-reference.md`** - Quick lookup guide
   - Essential endpoint information
   - Common integration patterns
   - JavaScript code snippets
   - Testing checklist

3. **`backend-api-questions.md`** (this document)
   - Critical questions for backend team
   - Missing endpoint documentation
   - API inconsistencies and gaps
   - Recommended improvements

---

## 🚀 Quick Start

### Base URL
```
Production: https://api.yourdomain.com/api
Staging: https://staging-api.yourdomain.com/api
Development: http://localhost:8000/api
```

### Authentication
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Create Course Endpoint
```
POST /api/admin/courses
```

### Minimal Request
```json
{
  "title": "Course Title"
}
```

---

## ⚠️ Critical Blockers

The following issues are **blocking frontend development**:

1. ❌ **Permission checking** - No way to verify user permissions before API calls
2. ❌ **Lesson/Topic creation** - Workflow for adding course content not documented
3. ❌ **File upload limits** - Actual size limits and constraints unknown
4. ❌ **Category/Tag endpoints** - Missing or undocumented
5. ❌ **Response format** - Inconsistencies between spec and implementation

**See Critical Questions section below for details.**

---

## 📊 API Endpoint Summary

### Course Management (Admin)
| Method | Endpoint | Purpose | Status |
|--------|----------|---------|--------|
| POST | `/api/admin/courses` | Create course | ✅ Documented |
| POST | `/api/admin/courses/{id}` | Update course | ✅ Documented |
| DELETE | `/api/admin/courses/{id}` | Delete course | ✅ Documented |
| GET | `/api/admin/courses/{id}/program` | Get full curriculum | ❓ Needs confirmation |

### Lessons & Topics
| Method | Endpoint | Purpose | Status |
|--------|----------|---------|--------|
| POST | `/api/admin/lessons` | Create lesson | ✅ Found in code |
| POST | `/api/admin/topics` | Create topic | ✅ Found in code |
| GET | `/api/admin/topics/types` | Get topic types | ❓ Undocumented |

### Missing Endpoints
| Endpoint | Purpose | Status |
|----------|---------|--------|
| `/api/categories` | List categories | ❌ Missing docs |
| `/api/tags` | List tags | ❌ Missing docs |
| `/api/user/permissions` | Check permissions | ❌ Unknown if exists |

---

## 🔍 Data Model Quick Reference

### Course Object Structure
```typescript
interface Course {
  id: number;
  title: string;                    // Required, min 3 chars
  summary?: string;
  description?: string;
  status: 'draft' | 'published' | 'archived' | 'published_unactivated';

  // Metadata
  subtitle?: string;
  language?: string;                // ISO 639-1 (2 chars)
  level?: string;
  duration?: string;
  hours_to_complete?: number;
  target_group?: string;

  // Visibility
  findable: boolean;
  public: boolean;
  active_from?: Date;
  active_to?: Date;

  // Media
  image_url?: string;
  video_url?: string;
  poster_url?: string;
  teaser_url?: string;

  // Relationships
  authors: User[];
  categories: Category[];
  tags: Tag[];
  lessons: Lesson[];

  // Extensibility
  fields?: Record<string, any>;
}
```

---

## 📈 Recommended Development Workflow

```
1. Create Course (draft)
   POST /api/admin/courses
   { "title": "...", "status": "draft" }

2. Add Basic Info
   POST /api/admin/courses/{id}
   { "summary": "...", "description": "..." }

3. Upload Media
   POST /api/admin/courses/{id}
   multipart/form-data with image, video, poster

4. Add Lessons (❓ NEEDS CONFIRMATION)
   POST /api/admin/lessons
   { "course_id": id, "title": "...", "order": 1 }

5. Add Topics to Lessons (❓ NEEDS CONFIRMATION)
   POST /api/admin/topics
   { "lesson_id": id, "title": "...", "type": "video" }

6. Publish Course
   POST /api/admin/courses/{id}
   { "status": "published", "findable": true }
```

---

## Executive Summary

After reviewing the API specification and analyzing the actual codebase, we've identified several critical gaps, inconsistencies, and missing information that will block our frontend development. This document outlines questions that need immediate answers from the backend team.

---

## 🚨 Critical Questions

### 1. Authentication & Permissions

**Question:** How does the frontend verify if a user has required permissions before attempting course operations?

**Details:**
- The API spec mentions permissions like `course_create`, `course_update`, `course_delete`
- Currently, we have no way to check if the logged-in user has these permissions before showing UI elements or making API calls
- This leads to poor UX (user sees "Create Course" button, clicks it, then gets 403 error)

**Needed:**
- [ ] Is there a `GET /api/user/permissions` endpoint?
- [ ] Or should we check `GET /api/user/profile` and it includes permissions?
- [ ] What's the exact response structure for permissions?
- [ ] Example response please

**Current Issue:**
```javascript
// Frontend needs to do this:
if (user.hasPermission('course_create')) {
  showCreateCourseButton();
}

// But we don't know where to get hasPermission() data from
```

---

**Question:** Auth token format inconsistency

**Details:**
- Spec shows: `Authorization: Bearer YOUR_ACCESS_TOKEN`
- Current implementation stores token as `auth_token`
- Login endpoint returns token in what format?

**Needed:**
- [ ] Confirm the exact header format expected
- [ ] Does login return `{ token: "..." }` or `{ access_token: "..." }`?
- [ ] Token expiration handling - is there a refresh token endpoint?

---

### 2. File Upload Handling

**Question:** What are the actual file size limits and upload constraints?

**Details:**
- Spec mentions "typically 100MB for videos" but doesn't specify actual server limits
- No information about image size limits
- No guidance on concurrent upload limits

**Needed:**
- [ ] Maximum file size for images (in MB)
- [ ] Maximum file size for videos (in MB)
- [ ] Supported image formats (jpg, png, gif, webp, svg?)
- [ ] Supported video formats (mp4, webm, ogg only?)
- [ ] Recommended image dimensions for thumbnails
- [ ] Recommended video encoding settings
- [ ] Rate limits on file upload endpoints

---

**Question:** Should files be uploaded separately or with course data?

**Details:**
Two possible approaches:
1. Upload files first, get URLs, then create course with URLs
2. Upload everything together in one `multipart/form-data` request

**Needed:**
- [ ] Which approach is supported/preferred?
- [ ] If separate uploads: What's the endpoint? `POST /api/admin/media/upload`?
- [ ] If separate uploads: How do we associate uploaded files with courses?
- [ ] Is there a temporary file storage with expiration?

---

**Question:** Video processing and async handling

**Details:**
- Large video uploads take time to process
- Need to know if there's a background processing queue

**Needed:**
- [ ] Are videos processed asynchronously?
- [ ] If yes, how do we check processing status?
- [ ] Is there a webhook or polling endpoint?
- [ ] What's the expected processing time for a 50MB video?
- [ ] Can users edit course while video is processing?

---

### 3. Course Creation Workflow

**Question:** How do we add lessons/modules to a course?

**Critical Issue:**
- The spec shows course creation but doesn't document how to add course content structure
- We need to build a course builder with modules → lessons → topics hierarchy
- No endpoints documented for this

**Needed:**
- [ ] `POST /api/admin/courses/{id}/lessons` - Does this exist?
- [ ] How do we create topics within lessons?
- [ ] Can we send entire course structure in one request?
- [ ] Example of nested course structure request
- [ ] What's the recommended workflow: bottom-up or top-down?

**Example of what we need to send:**
```json
{
  "title": "My Course",
  "lessons": [
    {
      "title": "Lesson 1",
      "order": 1,
      "topics": [
        {
          "title": "Introduction",
          "type": "video",
          "content": "..."
        }
      ]
    }
  ]
}
```

**Is this supported? Or do we need multiple API calls?**

---

**Question:** Course drafts and autosave

**Details:**
- Users may spend 30+ minutes creating a course
- Need to prevent data loss

**Needed:**
- [ ] Can we save incomplete courses as drafts?
- [ ] Is there a rate limit on draft saves?
- [ ] Should we implement debounced autosave?
- [ ] Recommended autosave interval?

---

### 4. Field Clarifications

**Question:** How do we get the current user's ID for the authors field?

**Details:**
- `authors` field expects array of user IDs: `[1, 2, 3]`
- When instructor creates a course, they should be added as author automatically
- But we don't know how to get their user ID

**Needed:**
- [ ] Does `GET /api/user/profile` return `id` field?
- [ ] Exact response structure of profile endpoint
- [ ] Should backend auto-add current user as author, or must frontend send it?

---

**Question:** Where do we get the list of available categories?

**Details:**
- `categories` field expects array of category IDs
- We need to show a category picker in the UI

**Needed:**
- [ ] Is there a `GET /api/categories` endpoint?
- [ ] Response format?
- [ ] Are categories hierarchical (parent/child)?
- [ ] Can we create new categories from course creation UI?

---

**Question:** Tags - where's the endpoint?

**Details:**
- Courses have `tags` field
- Need to implement tag autocomplete/suggestions

**Needed:**
- [ ] `GET /api/tags` endpoint?
- [ ] Can users create new tags on the fly?
- [ ] Tag validation rules?
- [ ] Max number of tags per course?

---

**Question:** SCORM support - is this implemented?

**Details:**
- Model has `scorm_sco_id` field
- Spec mentions SCORM integration
- No documentation on how to use it

**Needed:**
- [ ] Is SCORM fully implemented?
- [ ] How do we upload SCORM packages?
- [ ] Endpoint for SCORM upload?
- [ ] Should frontend support SCORM creation UI?
- [ ] Or is this admin-only feature?

---

**Question:** Custom fields object - what's supported?

**Details:**
- `fields` is a JSON object for "extensibility"
- No documentation on what fields are recognized

**Needed:**
- [ ] List of all supported custom fields
- [ ] Are there any validated/special fields?
- [ ] Can we add arbitrary fields?
- [ ] Are custom fields searchable/filterable?

**Example confusion:**
```json
{
  "fields": {
    "prerequisites": "...",  // Is this recognized?
    "certification": true,   // Does this trigger anything?
    "custom_field_123": "..." // Will this just be stored?
  }
}
```

---

### 5. Missing Endpoints

**Critical Missing Endpoints:**

We found references to these in the code but no documentation:

- [ ] `GET /api/categories` - Get list of all categories
- [ ] `POST /api/admin/categories` - Create category
- [ ] `GET /api/tags` - Get list of tags
- [ ] `GET /api/tags/uniqueTags` - Found in routes but not documented
- [ ] `GET /api/admin/courses/{id}/program` - Spec mentions it, does it work?
- [ ] `POST /api/admin/lessons` - Create lesson
- [ ] `PUT/PATCH /api/admin/lessons/{id}` - Update lesson
- [ ] `DELETE /api/admin/lessons/{id}` - Delete lesson
- [ ] `POST /api/admin/topics` - Create topic
- [ ] `GET /api/topics/types` - Found in routes, what does it return?

**Quiz/Assessment Endpoints (Completely Missing):**
- [ ] How do we create quizzes?
- [ ] How do we add questions to topics?
- [ ] Question types supported?
- [ ] Answer validation?

**Media Management:**
- [ ] Is there a generic media upload endpoint?
- [ ] Can we list uploaded media?
- [ ] Can we delete uploaded media?

---

### 6. Status Workflow

**Question:** What's the exact course status state machine?

**Details:**
Four statuses exist: `draft`, `published`, `published_unactivated`, `archived`

**Needed:**
- [ ] Can course go directly `draft → published`?
- [ ] Or must it be `draft → published_unactivated → published`?
- [ ] What triggers `published_unactivated → published`?
- [ ] Is there an approval/review process?
- [ ] Who can approve courses for publishing?
- [ ] Can published courses go back to draft?

**State diagram needed:**
```
draft → ? → published → archived
            ↓
       published_unactivated → ?
```

---

**Question:** Active date validation

**Details:**
- `active_from` and `active_to` control when course is accessible
- Interaction with `status` field unclear

**Needed:**
- [ ] If status is `published` but `active_from` is in future, what happens?
- [ ] If `active_to` passes, does status change to `archived` automatically?
- [ ] Is there a CRON job that updates course status based on dates?
- [ ] Should frontend validate these dates, or does backend handle it?

---

### 7. Response Format Inconsistency

**Question:** What's the actual API response format?

**Spec shows:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Course saved successfully"
}
```

**But Laravel standard is:**
```json
{
  "data": { ... }
}
```

**And errors are:**
```json
{
  "message": "...",
  "errors": { ... }
}
```

**Needed:**
- [ ] Confirm exact response format for success
- [ ] Confirm exact response format for validation errors
- [ ] Confirm exact response format for server errors (500)
- [ ] Are there any endpoints that deviate from this format?

---

### 8. Validation Rules

**Question:** Title uniqueness validation

**Details:**
- Spec mentions "Title must be unique per organization"
- Multi-tenancy implications unclear

**Needed:**
- [ ] Is title uniqueness enforced?
- [ ] Unique per organization or globally?
- [ ] How do we handle course cloning/duplication?
- [ ] Can two instructors have courses with same title?

---

**Question:** Other business rules not documented

**Needed:**
- [ ] Can a course exist without any lessons?
- [ ] Minimum/maximum number of lessons?
- [ ] Can lessons be reordered after creation?
- [ ] Can course be deleted if students are enrolled?
- [ ] What happens to student progress when course is archived?

---

## 🎯 Recommendations for Backend Team

### High Priority

1. **Create a `/api/user/permissions` endpoint**
   - Returns array of permission strings for current user
   - Enables frontend to show/hide features based on permissions

2. **Document the complete course structure creation workflow**
   - Either: Support nested creation in one request
   - Or: Document the multi-step process clearly

3. **Add preflight validation endpoint**
   - `POST /api/admin/courses/validate` (doesn't save, just validates)
   - Enables frontend to show validation errors before user clicks "Save"

4. **Implement progress tracking for async operations**
   - Video processing status endpoint
   - Large file upload progress

### Medium Priority

5. **Create comprehensive resource listing endpoints**
   - `GET /api/categories`
   - `GET /api/tags`
   - `GET /api/admin/users?role=instructor` (for author picker)

6. **Add batch operations**
   - `POST /api/admin/courses/batch` - Create multiple courses
   - `PATCH /api/admin/courses/batch` - Update multiple courses

7. **Course templates**
   - `GET /api/admin/courses/templates` - Get predefined course structures
   - `POST /api/admin/courses/{id}/duplicate` - Clone existing course

### Nice to Have

8. **Course preview endpoint**
   - `POST /api/admin/courses/preview` (doesn't save, returns preview)
   - Frontend can show "Preview" before publishing

9. **Validation rules endpoint**
   - `GET /api/admin/courses/validation-rules`
   - Returns JSON schema for frontend validation

10. **Upload progress tracking**
    - Support for chunked uploads
    - Progress callback/webhook

---

## 📋 Action Items

**For Backend Team:**

- [ ] Review all questions in this document
- [ ] Provide answers to critical questions (sections 1-4)
- [ ] Document missing endpoints or confirm they don't exist
- [ ] Update API documentation with clarifications
- [ ] Create example requests/responses for complex operations
- [ ] Consider implementing high-priority recommendations

**For Frontend Team (blocked on):**

- [ ] Cannot implement permission-based UI until Q1 answered
- [ ] Cannot build course content editor until Q3 answered
- [ ] Cannot implement file upload until Q2 answered
- [ ] Cannot implement category/tag pickers until Q4 answered

---

## 🔗 Related Documents

- `course-api-specification.md` - Current API spec (needs updates)
- `course-api-quick-reference.md` - Quick reference for frontend
- EscolaLMS vendor code: `vendor/escolalms/courses/`

---

## Contact

**Frontend Team Lead:** [Your Name]
**Slack Channel:** #api-questions
**Urgency:** High - Blocking sprint goals

---

## 🧪 Testing & Validation

### Manual Testing Steps

1. **Authentication:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@example.com","password":"password"}'
   ```

2. **Create Course:**
   ```bash
   curl -X POST http://localhost:8000/api/admin/courses \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title":"Test Course"}'
   ```

3. **Get Course:**
   ```bash
   curl -X GET http://localhost:8000/api/courses/1 \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

### Testing Checklist

Frontend team needs to test:
- [ ] Create course with only title
- [ ] Create course with all fields
- [ ] Upload image file
- [ ] Upload video file
- [ ] Handle validation errors
- [ ] Test with invalid auth token
- [ ] Test file type validation
- [ ] Test array fields (authors)
- [ ] Test custom fields (JSON)

Backend team should provide:
- [ ] Postman collection
- [ ] Test environment credentials
- [ ] Sample valid/invalid requests
- [ ] Expected response examples

---

## 📝 Document Status

| Document | Status | Last Updated | Needs Review By |
|----------|--------|--------------|-----------------|
| course-api-specification.md | ✅ Complete | 2024-01-10 | Backend team |
| course-api-quick-reference.md | ✅ Complete | 2024-01-10 | Frontend team |
| backend-api-questions.md | ⚠️ Pending answers | 2024-01-10 | Backend team |

---

## 🎯 Next Steps

### Immediate Actions (This Week)

**Backend Team:**
1. Review sections 1-4 of Critical Questions (highest priority)
2. Confirm or deny existence of missing endpoints
3. Provide file upload limits and constraints
4. Document lesson/topic creation workflow

**Frontend Team:**
1. Implement basic course creation with minimal fields
2. Create UI mockups for full course builder
3. Wait for answers before implementing file uploads
4. Prepare test cases based on specifications

### Short Term (Next Sprint)

**Backend Team:**
1. Implement missing high-priority endpoints
2. Create comprehensive API documentation
3. Set up testing environment for frontend
4. Provide Postman collection

**Frontend Team:**
1. Implement full course creation workflow
2. Add file upload functionality
3. Build lesson/topic management UI
4. Implement permission-based UI

### Long Term

**Both Teams:**
1. Regular API review meetings
2. Keep documentation in sync with implementation
3. Automated API testing
4. Performance optimization

---

## 📚 Additional Resources

- **Codebase Location:** `vendor/escolalms/courses/`
- **Routes File:** `vendor/escolalms/courses/src/routes.php`
- **Course Model:** `vendor/escolalms/courses/src/Models/Course.php`
- **Controller:** `vendor/escolalms/courses/src/Http/Controllers/CourseAPIController.php`

---

*Please schedule a meeting to discuss these questions if written responses are insufficient.*

*Document generated: 2024-01-10*
*API Version: 1.0 (EscolaLMS)*