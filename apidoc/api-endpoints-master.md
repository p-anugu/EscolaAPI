# API Endpoints Master List

## Authentication & User Management

### Authentication Endpoints
```
POST   /api/auth/register                 - User registration
POST   /api/auth/login                    - User login
POST   /api/auth/logout                   - User logout (requires auth)
GET    /api/auth/refresh                  - Refresh JWT token (requires auth)

GET    /api/auth/registerable-groups      - Get groups available for registration

POST   /api/auth/password/forgot          - Request password reset
POST   /api/auth/password/reset           - Reset password with token

GET    /api/auth/social/{provider}        - Social auth redirect (google, facebook, etc.)
GET    /api/auth/social/{provider}/callback - Social auth callback
POST   /api/auth/social/complete/{token}  - Complete social registration

GET    /api/auth/email/verify/{id}/{hash} - Verify email address
POST   /api/auth/email/resend             - Resend verification email (requires auth)

POST   /api/admin/auth/impersonate        - Impersonate user (admin only)
```

### Profile Management
```
GET    /api/profile/me                    - Get current user profile
PUT    /api/profile/me                    - Update profile information
PUT    /api/profile/me-auth               - Update authentication data
PUT    /api/profile/password              - Change password
PUT    /api/profile/interests             - Update user interests
GET    /api/profile/settings              - Get user settings
PUT    /api/profile/settings              - Update user settings
POST   /api/profile/upload-avatar         - Upload profile avatar
DELETE /api/profile/delete-avatar         - Delete profile avatar
DELETE /api/profile                       - Delete user account
POST   /api/profile/delete/init           - Initiate account deletion
GET    /api/profile/delete/{userId}/{token} - Confirm account deletion
```

### Admin User Management
```
GET    /api/admin/users                   - List all users (paginated)
POST   /api/admin/users                   - Create new user
GET    /api/admin/users/{id}              - Get user details
PUT    /api/admin/users/{id}              - Update user completely
PATCH  /api/admin/users/{id}              - Partial user update
DELETE /api/admin/users/{id}              - Delete user (soft delete)

POST   /api/admin/users/{id}/avatar       - Upload user avatar
DELETE /api/admin/users/{id}/avatar       - Delete user avatar

GET    /api/admin/users/{id}/settings     - Get user settings
PUT    /api/admin/users/{id}/settings     - Replace user settings
PATCH  /api/admin/users/{id}/settings     - Update user settings

GET    /api/admin/users/{id}/interests    - Get user interests
PUT    /api/admin/users/{id}/interests    - Replace user interests
POST   /api/admin/users/{id}/interests    - Add user interest
DELETE /api/admin/users/{id}/interests/{interest_id} - Remove interest
```

### User Groups Management
```
GET    /api/admin/user-groups             - List all groups
GET    /api/admin/user-groups/tree        - Get groups hierarchy tree
GET    /api/admin/user-groups/users       - List groups with users
POST   /api/admin/user-groups             - Create new group
GET    /api/admin/user-groups/{id}        - Get group details
PUT    /api/admin/user-groups/{id}        - Update group
PATCH  /api/admin/user-groups/{id}        - Partial group update
DELETE /api/admin/user-groups/{id}        - Delete group

POST   /api/admin/user-groups/{id}/members - Add group member
DELETE /api/admin/user-groups/{id}/members/{user_id} - Remove member
```

## Course Management

### Public Course Endpoints
```
GET    /api/courses                       - List available courses
GET    /api/courses/{course}              - Get course details
GET    /api/courses/{course}/program      - Get course curriculum
GET    /api/courses/{course}/preview/{topic_id} - Preview topic
GET    /api/courses/{course}/scorm        - Get SCORM package

GET    /api/courses/search/tags           - Search courses by tags
GET    /api/courses/search/{category_id}  - Search by category
GET    /api/courses/uniqueTags            - Get all unique course tags
```

### Course Progress (Authenticated)
```
GET    /api/course-progress               - Get all progress
GET    /api/course-progress/paginated     - Get paginated progress
GET    /api/course-progress/{course_id}   - Get course progress
PATCH  /api/course-progress/{course_id}   - Update progress
PUT    /api/course-progress/{topic_id}/ping - Mark topic as active
POST   /api/course-progress/{topic_id}/h5p  - Submit H5P progress
```

### Admin Course Management
```
GET    /api/admin/courses                 - List all courses (admin view)
POST   /api/admin/courses                 - Create new course
GET    /api/admin/courses/{id}            - Get course details (admin)
PUT    /api/admin/courses/{id}            - Update course
PATCH  /api/admin/courses/{id}            - Partial course update
DELETE /api/admin/courses/{id}            - Delete course

POST   /api/admin/courses/sort            - Sort courses order
POST   /api/admin/courses/{course}        - Update course (alternative)
GET    /api/admin/courses/{course}/program - Get course structure

GET    /api/courses/authored              - Get instructor's courses
```

### Lesson Management
```
GET    /api/admin/lessons                 - List all lessons
POST   /api/admin/lessons                 - Create lesson
GET    /api/admin/lessons/{id}            - Get lesson details
PUT    /api/admin/lessons/{id}            - Update lesson
PATCH  /api/admin/lessons/{id}            - Partial lesson update
DELETE /api/admin/lessons/{id}            - Delete lesson
POST   /api/admin/lessons/{id}/clone      - Clone lesson
```

### Topic Management
```
GET    /api/admin/topics                  - List all topics
POST   /api/admin/topics                  - Create topic
GET    /api/admin/topics/{id}             - Get topic details
PUT    /api/admin/topics/{id}             - Update topic
PATCH  /api/admin/topics/{id}             - Partial topic update
DELETE /api/admin/topics/{id}             - Delete topic

GET    /api/topics/types                  - List available topic types
POST   /api/admin/topics/{topic}          - Update topic (alternative)
POST   /api/admin/topics/{id}/clone       - Clone topic
```

### Topic Resources
```
GET    /api/topics/{topic_id}/resources   - List topic resources
POST   /api/admin/topics/{topic_id}/resources - Upload resource
PATCH  /api/admin/topics/{topic_id}/resources/{resource_id} - Rename
DELETE /api/admin/topics/{topic_id}/resources/{resource_id} - Delete
```

### Course Authors/Tutors
```
GET    /api/tutors                        - List all tutors
GET    /api/tutors/{id}                   - Get tutor details
GET    /api/courses/users/assignable      - List assignable users

POST   /api/admin/tutors/{id}/assign/{course}   - Assign tutor
POST   /api/admin/tutors/{id}/unassign/{course} - Unassign tutor
```

## E-Commerce

### Shopping Cart
```
GET    /api/cart                          - Get current cart
POST   /api/cart/products                 - Set product quantity
POST   /api/cart/missing                  - Add missing products
DELETE /api/cart/products/{id}            - Remove from cart
POST   /api/cart/add                      - Add productable to cart
```

### Products
```
GET    /api/products                      - List available products
GET    /api/products/{id}                 - Get product details
GET    /api/products/my                   - Get user's products
POST   /api/products/cancel/{id}          - Cancel product subscription

GET    /api/admin/products                - List all products (admin)
POST   /api/admin/products                - Create product
GET    /api/admin/products/{id}           - Get product (admin)
PUT    /api/admin/products/{id}           - Update product
DELETE /api/admin/products/{id}           - Delete product

POST   /api/admin/products/{id}/attach    - Attach to productable
POST   /api/admin/products/{id}/detach    - Detach from productable
POST   /api/admin/products/{id}/trigger-event-manually/{idTemplate} - Manual trigger
```

### Productables
```
GET    /api/admin/productables            - List productables
GET    /api/admin/productables/registered - Get registered types
GET    /api/admin/productables/product    - Get product details
POST   /api/admin/productables/attach     - Attach productable
POST   /api/admin/productables/detach     - Detach productable

POST   /api/productables/attach           - User attach productable
```

### Orders
```
GET    /api/orders                        - List user orders
GET    /api/orders/{id}                   - Get order details

GET    /api/admin/orders                  - List all orders (admin)
GET    /api/admin/orders/export           - Export orders
GET    /api/admin/orders/{id}             - Get order details (admin)
```

### Payments
```
POST   /api/cart/pay                     - Process cart payment
POST   /api/product/{id}/pay              - Pay for single product
```

## Consultations

### Public Consultations
```
GET    /api/consultations                 - List available consultations
GET    /api/consultations/{id}            - Get consultation details
```

### User Consultations
```
GET    /api/consultations/my              - Get user's consultations
POST   /api/consultations/{id}/book       - Book consultation
POST   /api/consultations/{id}/term       - Propose consultation term
POST   /api/consultations/{id}/cancel     - Cancel consultation
POST   /api/consultations/{id}/reschedule - Reschedule consultation
```

### Admin Consultations
```
GET    /api/admin/consultations           - List all consultations
POST   /api/admin/consultations           - Create consultation
GET    /api/admin/consultations/{id}      - Get consultation details
PUT    /api/admin/consultations/{id}      - Update consultation
DELETE /api/admin/consultations/{id}      - Delete consultation

POST   /api/admin/consultations/{id}/approve-term - Approve proposed term
POST   /api/admin/consultations/{id}/reject-term  - Reject proposed term
GET    /api/admin/consultations/report    - Get consultations report
```

## Webinars

### Public Webinars
```
GET    /api/webinars                      - List webinars
GET    /api/webinars/{id}                 - Get webinar details
```

### User Webinars
```
GET    /api/webinars/my                   - Get user's webinars
POST   /api/webinars/{id}/register        - Register for webinar
POST   /api/webinars/{id}/unregister      - Unregister from webinar
```

### Admin Webinars
```
GET    /api/admin/webinars                - List all webinars
POST   /api/admin/webinars                - Create webinar
GET    /api/admin/webinars/{id}           - Get webinar details
PUT    /api/admin/webinars/{id}           - Update webinar
DELETE /api/admin/webinars/{id}           - Delete webinar

POST   /api/admin/webinars/{id}/start     - Start streaming
POST   /api/admin/webinars/{id}/stop      - Stop streaming
GET    /api/admin/webinars/{id}/attendees - Get attendee list
```

## Categories & Tags

### Categories
```
GET    /api/categories                    - List categories
GET    /api/categories/tree               - Get category tree
GET    /api/categories/{id}               - Get category details

GET    /api/admin/categories              - List all categories
POST   /api/admin/categories              - Create category
GET    /api/admin/categories/{id}         - Get category details
PUT    /api/admin/categories/{id}         - Update category
DELETE /api/admin/categories/{id}         - Delete category
```

### Tags
```
GET    /api/tags                          - List all tags
GET    /api/tags/unique                   - Get unique tags
GET    /api/tags/morphable                - Get taggable types

POST   /api/admin/tags                    - Create tag
PUT    /api/admin/tags/{id}               - Update tag
DELETE /api/admin/tags/{id}               - Delete tag
```

## Settings & Configuration

### Public Settings
```
GET    /api/settings                      - Get public settings
```

### Admin Settings
```
GET    /api/admin/settings                - Get all settings
PUT    /api/admin/settings                - Update settings
POST   /api/admin/settings/{key}          - Set specific setting
DELETE /api/admin/settings/{key}          - Delete setting

GET    /api/admin/settings/groups         - Get setting groups
GET    /api/admin/settings/config         - Get configuration
```

## Files & Media

### File Management
```
POST   /api/files/upload                  - Upload file
GET    /api/files/{id}                    - Get file info
GET    /api/files/{id}/download           - Download file
DELETE /api/files/{id}                    - Delete file

GET    /api/admin/files                   - List all files
DELETE /api/admin/files/{id}              - Admin delete file
```

### Images
```
GET    /api/images/{path}                 - Get processed image
GET    /api/images/{path}/{params}        - Get image with transformations
```

### Videos
```
GET    /api/videos/{id}                   - Get video info
GET    /api/videos/{id}/stream            - Stream video
GET    /api/videos/{id}/poster            - Get video poster
```

## Notifications

### User Notifications
```
GET    /api/notifications                 - Get user notifications
GET    /api/notifications/unread          - Get unread count
POST   /api/notifications/{id}/read       - Mark as read
POST   /api/notifications/read-all        - Mark all as read
DELETE /api/notifications/{id}            - Delete notification

GET    /api/notification-settings         - Get preferences
PUT    /api/notification-settings         - Update preferences
```

### Admin Notifications
```
POST   /api/admin/notifications/send      - Send notification
POST   /api/admin/notifications/bulk      - Send bulk notifications
GET    /api/admin/notifications/templates - Get templates
POST   /api/admin/notifications/templates - Create template
```

## Reports & Analytics

### Admin Reports
```
GET    /api/admin/reports/courses         - Course reports
GET    /api/admin/reports/users           - User reports
GET    /api/admin/reports/revenue         - Revenue reports
GET    /api/admin/reports/custom          - Custom reports
POST   /api/admin/reports/generate        - Generate report
GET    /api/admin/reports/export          - Export report
```

### Course Analytics
```
GET    /api/admin/analytics/courses/{id}  - Course analytics
GET    /api/admin/analytics/courses/{id}/completion - Completion rates
GET    /api/admin/analytics/courses/{id}/engagement - Engagement metrics
```

## Questionnaires & Surveys

### Public Questionnaires
```
GET    /api/questionnaires                - List questionnaires
GET    /api/questionnaires/{id}           - Get questionnaire
POST   /api/questionnaires/{id}/submit    - Submit response
```

### Admin Questionnaires
```
GET    /api/admin/questionnaires          - List all questionnaires
POST   /api/admin/questionnaires          - Create questionnaire
GET    /api/admin/questionnaires/{id}     - Get questionnaire
PUT    /api/admin/questionnaires/{id}     - Update questionnaire
DELETE /api/admin/questionnaires/{id}     - Delete questionnaire

GET    /api/admin/questionnaires/{id}/responses - Get responses
GET    /api/admin/questionnaires/{id}/report    - Get report
```

## H5P Content

### H5P Content Access
```
GET    /api/h5p/content/{id}              - Get H5P content
GET    /api/h5p/content/{id}/embed        - Get embed code
POST   /api/h5p/content/{id}/state        - Save state
GET    /api/h5p/content/{id}/results      - Get results
```

### Admin H5P Management
```
GET    /api/admin/h5p/libraries           - List H5P libraries
POST   /api/admin/h5p/libraries           - Install library
GET    /api/admin/h5p/content             - List content
POST   /api/admin/h5p/content             - Create content
GET    /api/admin/h5p/content/{id}        - Get content
PUT    /api/admin/h5p/content/{id}        - Update content
DELETE /api/admin/h5p/content/{id}        - Delete content
```

## SCORM

### SCORM Content
```
GET    /api/scorm/{id}                    - Get SCORM package
POST   /api/scorm/{id}/launch             - Launch SCORM
POST   /api/scorm/{id}/track              - Track progress
GET    /api/scorm/{id}/report             - Get report
```

### Admin SCORM
```
POST   /api/admin/scorm/upload            - Upload SCORM package
GET    /api/admin/scorm                   - List packages
DELETE /api/admin/scorm/{id}              - Delete package
```

## Certificates

### User Certificates
```
GET    /api/certificates                  - List user certificates
GET    /api/certificates/{id}             - Get certificate
GET    /api/certificates/{id}/download    - Download certificate
GET    /api/certificates/{id}/verify      - Verify certificate
```

### Admin Certificates
```
GET    /api/admin/certificates/templates  - List templates
POST   /api/admin/certificates/templates  - Create template
PUT    /api/admin/certificates/templates/{id} - Update template
DELETE /api/admin/certificates/templates/{id} - Delete template

POST   /api/admin/certificates/generate   - Generate certificate
POST   /api/admin/certificates/bulk       - Bulk generate
```

## System & Health

### System Information
```
GET    /api/health                        - Health check
GET    /api/version                       - API version
GET    /api/documentation                 - Swagger documentation
```

### Admin System
```
GET    /api/admin/system/info             - System information
GET    /api/admin/system/logs             - View logs
POST   /api/admin/system/cache/clear      - Clear cache
POST   /api/admin/system/maintenance      - Toggle maintenance
GET    /api/admin/system/queue            - Queue status
```

## Webhooks

### Admin Webhooks
```
GET    /api/admin/webhooks                - List webhooks
POST   /api/admin/webhooks                - Create webhook
GET    /api/admin/webhooks/{id}           - Get webhook
PUT    /api/admin/webhooks/{id}           - Update webhook
DELETE /api/admin/webhooks/{id}           - Delete webhook

POST   /api/admin/webhooks/{id}/test      - Test webhook
GET    /api/admin/webhooks/{id}/logs      - Get webhook logs
```

## Request Parameters

### Common Query Parameters
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 15, max: 100)
- `order_by` - Sort field
- `order` - Sort direction (ASC/DESC)
- `search` - Search query
- `with` - Include relations (comma-separated)
- `fields` - Select fields (comma-separated)
- `filter` - Filter conditions (array)

### Common Headers
- `Authorization: Bearer {token}` - Authentication
- `Accept: application/json` - Response format
- `Content-Type: application/json` - Request format
- `X-Requested-With: XMLHttpRequest` - AJAX indicator
- `Accept-Language: en` - Preferred language

### Response Headers
- `X-RateLimit-Limit` - Rate limit maximum
- `X-RateLimit-Remaining` - Remaining requests
- `X-RateLimit-Reset` - Reset timestamp
- `X-Total-Count` - Total items (pagination)
- `Link` - Pagination links