# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**EscolaLMS (Wellms)** is a Laravel-based headless LMS (Learning Management System) that provides a complete REST API for educational platforms. The system is built on a modular package architecture with 40+ specialized packages.

### Key Characteristics
- **Stateless Architecture**: All configuration via environment variables (no .env file editing)
- **Package-Based**: Core functionality distributed across `vendor/escolalms/*` packages
- **Headless**: Pure REST API, no frontend (frontend consumed separately)
- **Multi-Tenant**: Supports multiple domains/organizations
- **Docker-First**: Designed for containerized deployment

## Architecture

### Package System
This application extends Laravel with 40+ EscolaLMS packages located in `vendor/escolalms/`:
- `auth` - Authentication, users, roles, permissions
- `courses` - Course management, lessons, topics
- `cart` - Shopping cart and product management
- `consultations` - One-on-one consultations
- `webinar` - Webinar/live event management
- `scorm` - SCORM e-learning content
- `headless-h5p` - H5P interactive content
- `payments` - Payment processing
- `templates-email` - Email template system
- Many more specialized packages

**Important Pattern**: The `app/Models/` directory contains models that **extend** vendor package models:
```php
// app/Models/Course.php extends vendor/escolalms/courses/src/Models/Course.php
class Course extends \EscolaLms\Courses\Models\Course implements Productable
{
    // Add custom behavior while inheriting package functionality
}
```

### Configuration Philosophy
- **NO .env file editing** - Configuration is controlled by environment variables
- Environment variables use `LARAVEL_` prefix (e.g., `LARAVEL_DB_HOST`, `LARAVEL_APP_URL`)
- See `docker-compose.yml` for reference environment variables
- This enables stateless, scalable deployments

### Authentication
- Laravel Passport for OAuth2/Bearer token authentication
- Default test credentials (see Database section)
- API routes protected by `auth:api` middleware
- Profile endpoint: `GET /api/profile/me`

### Storage
- MinIO (S3-compatible) for file storage
- Files accessible at `http://storage.localhost/wellms`
- Internal Docker endpoint: `http://minio:9000`

## Development Environment

### Initial Setup
```bash
# 1. Clone and start containers
docker compose up -d

# 2. Initialize everything (database, composer, migrations, seeders)
make init

# 3. Access API documentation
# http://api.localhost/api/documentation
```

### Essential Commands

**Container Access:**
```bash
make bash                      # Enter API container shell
docker compose logs -f api     # View API logs
docker compose logs -f caddy   # View web server logs
```

**Database:**
```bash
make migrate-fresh-quick       # Reset database and run seeders
make migrate-fresh             # Full reset including H5P seeding
make backup-postgres           # Backup database to data/ folder
make import-postgres BACKUP_FILE=backup-latest.sql  # Restore backup
```

**Testing:**
```bash
make test-phpunit              # Run all PHPUnit tests
make test-fresh                # Fresh DB + tests
./vendor/bin/phpunit           # Run tests directly in container
```

**Development:**
```bash
make composer-update           # Update Composer dependencies
make swagger-generate          # Regenerate API documentation
make tinker                    # Laravel Tinker REPL (CTRL+D to refresh)
```

**Logs:**
```bash
docker compose logs -f                                          # All services
docker compose logs -f api                                      # API + PHP-FPM
docker compose exec api tail -f storage/logs/laravel-$(date +%Y-%m-%d).log
```

### Services

| Service | URL/Access | Purpose |
|---------|------------|---------|
| API | http://api.localhost | Main API endpoint |
| Swagger | http://api.localhost/api/documentation | API documentation |
| Adminer | http://localhost:8078 | Database UI |
| MinIO Storage | http://storage.localhost/wellms | File storage |
| Mailhog | Internal (mailhog:1025) | Email testing |

## Database

### Connection
- **Type**: PostgreSQL
- **Host**: postgres (Docker service name)
- **Database**: default
- **Username**: default
- **Password**: secret

### Adminer Access
- **URL**: http://localhost:8078
- **System**: PostgreSQL
- **Server**: postgres
- **Username**: default
- **Password**: secret
- **Database**: default

### Test Users (Created by Seeders)
```
Admin:   admin2@escolalms.com / secret
Student: student@escolalms.com / secret
Tutor:   tutor@escolalms.com / secret
```

### Migrations
Migrations are distributed across packages in `vendor/escolalms/*/database/migrations/`. Running `make migrate-fresh-quick` executes all package migrations and seeders.

## API Structure

### Routing
Routes are defined in vendor package files:
- `vendor/escolalms/auth/src/routes.php` - Authentication routes
- `vendor/escolalms/courses/src/routes.php` - Course routes
- And so on for each package

**Route Pattern:**
```
/api/auth/*           - Authentication (login, register, password reset)
/api/admin/*          - Admin endpoints (requires admin role)
/api/courses/*        - Course listing and access
/api/profile/*        - User profile management
```

### Key Endpoints
```
POST /api/auth/login                    - Login
GET  /api/profile/me                    - Get current user
POST /api/admin/courses                 - Create course (admin)
GET  /api/courses                       - List courses
GET  /api/courses/{id}                  - Course details
GET  /api/courses/{id}/program          - Course curriculum
```

### API Documentation
- Auto-generated Swagger documentation
- Available at: http://api.localhost/api/documentation
- Regenerate: `make swagger-generate`

## Testing

### Running Tests
```bash
# All tests across all packages
make test-phpunit

# Inside container
docker compose exec api bash
./vendor/bin/phpunit

# Fresh database + tests
make test-fresh
```

### Test Structure
- Each EscolaLMS package contains its own tests
- Integration tests verify package interactions
- Tests use Orchestra Testbench for package testing

## Common Workflows

### Adding Custom Course Behavior
```bash
# 1. Extend the vendor model in app/Models/Course.php
# 2. Add custom methods/relationships
# 3. The system automatically uses your extended model
```

### Creating New Migrations
```bash
docker compose exec api bash
php artisan make:migration create_something_table
php artisan migrate
```

### Debugging
```bash
# View logs
docker compose logs -f api

# Laravel logs
docker compose exec api tail -f storage/logs/laravel-$(date +%Y-%m-%d).log

# Enter container and use Tinker
make tinker

# Check API response
curl -X POST http://api.localhost/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin2@escolalms.com","password":"secret"}'
```

### Understanding a Feature
When investigating a feature (e.g., courses, consultations):
1. Check `vendor/escolalms/{package}/src/Models/` for data models
2. Check `vendor/escolalms/{package}/src/routes.php` for endpoints
3. Check `vendor/escolalms/{package}/src/Http/Controllers/` for logic
4. Check `app/Models/` for any local extensions

## Key Files

### Application Entry Points
- `routes/api.php` - Additional application-specific routes
- `app/Models/` - Extended models (Course, User, Consultation, etc.)
- `database/seeders/` - Local seeders (UserTableSeeder, etc.)

### Configuration
- `docker-compose.yml` - Environment variables and service definitions
- `makefile` - Development task automation
- `config/` - Laravel config (but driven by env vars)

### Package Locations
- `vendor/escolalms/*/src/` - Package source code
- `vendor/escolalms/*/database/migrations/` - Package migrations
- `vendor/escolalms/*/tests/` - Package tests

## API Core Concepts

### API Architecture Principles
- **Headless Architecture**: Pure REST API with no built-in frontend
- **Stateless Design**: All configuration via environment variables
- **Modular Packages**: 40+ specialized packages, each handling specific functionality
- **Event-Driven**: Packages communicate via Laravel events
- **RESTful Standards**: Standard HTTP methods and status codes

### Request/Response Format
**Standard Response Format:**
```json
{
  "success": true,
  "data": { /* response data */ },
  "meta": {
    "current_page": 1,
    "total": 100,
    "per_page": 15,
    "last_page": 7
  },
  "message": "Operation successful"
}
```

**Error Response Format:**
```json
{
  "success": false,
  "message": "Validation error",
  "errors": {
    "field_name": ["The field is required"]
  },
  "code": 422
}
```

### Common Query Parameters
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 15, max: 100)
- `order_by` - Sort field
- `order` - Sort direction (ASC/DESC)
- `search` - Search query
- `with` - Include relations (comma-separated)
- `filter` - Filter conditions

### HTTP Status Codes
- **200**: OK - Successful GET/PUT
- **201**: Created - Successful POST creating resource
- **204**: No Content - Successful DELETE
- **400**: Bad Request - Invalid request format
- **401**: Unauthorized - Missing/invalid authentication
- **403**: Forbidden - Authenticated but not authorized
- **404**: Not Found - Resource doesn't exist
- **422**: Unprocessable Entity - Validation errors
- **500**: Internal Server Error

### Authentication Pattern
```bash
# 1. Login to get token
curl -X POST http://api.localhost/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin2@escolalms.com","password":"secret"}'
# Returns: {"data":{"token":"eyJ0eXAiOi..."}}

# 2. Use token in requests
curl -X GET http://api.localhost/api/profile/me \
  -H "Authorization: Bearer eyJ0eXAiOi..."
```

## Course Structure

### Course Hierarchy
```
Course
├── Lessons (Multiple)
│   ├── Topics (Multiple)
│   │   └── Topic Content (Polymorphic)
│   └── Sub-lessons (Optional, nested)
```

### Course Model Fields
- **Core**: title (required), summary, description, status
- **Media**: image_path, video_path, poster_path, teaser_url
- **Scheduling**: active_from, active_to, public, findable
- **Educational**: duration, hours_to_complete, target_group, level
- **Integration**: scorm_sco_id (optional SCORM package)

### Topic Content Types
- **Basic**: RichText, Video, Audio, Image, PDF
- **Interactive**: H5P, ScormSco, Cmi5Au, OEmbed
- **Assessment**: GiftQuiz, Project

## User Management

### Soft Deletion
- Users are soft-deleted (marked with deleted_at timestamp)
- Deleted users remain in database with all relationships intact
- Course enrollments preserved for soft-deleted users
- Can be restored via `$user->restore()`
- 7 soft-deleted users exist in seeded database (56 total, 49 active)
- API endpoint `DELETE /api/admin/users/{id}` performs soft delete
- No built-in restore API endpoint (must use Tinker or custom implementation)

### User Roles
- **Admin**: Full system access
- **Tutor**: Course creation and management
- **Student**: Course enrollment and learning

## Package Capabilities

### Core Packages
- **auth**: Authentication, roles, permissions, social login, 2FA
- **courses**: Course management, lessons, topics, progress tracking
- **cart**: Shopping cart, checkout, order management
- **payments**: Payment gateways (Stripe, PayPal, etc.)
- **consultations**: One-on-one sessions with Jitsi integration
- **webinar**: Live streaming with YouTube/Jitsi
- **headless-h5p**: Interactive HTML5 content
- **scorm**: SCORM 1.2/2004 package support
- **notifications**: Multi-channel notifications (email, SMS, push)
- **templates-email**: Dynamic email templates
- **files**: File management with S3/MinIO support
- **categories**: Hierarchical categorization
- **tags**: Flexible tagging system
- **settings**: Runtime configuration management

## Essential API Endpoints

### Authentication
```
POST /api/auth/login          - Login
POST /api/auth/register       - Register
POST /api/auth/logout         - Logout
GET  /api/auth/refresh        - Refresh token
```

### Courses
```
GET  /api/courses             - List courses
GET  /api/courses/{id}        - Course details
GET  /api/courses/{id}/program - Course curriculum
POST /api/admin/courses       - Create course (admin)
```

### User Profile
```
GET  /api/profile/me          - Current user
PUT  /api/profile/me          - Update profile
POST /api/profile/upload-avatar - Upload avatar
```

### Progress Tracking
```
GET  /api/course-progress/{course_id} - Get progress
PATCH /api/course-progress/{course_id} - Update progress
PUT  /api/course-progress/{topic_id}/ping - Mark topic active
```

## Git Conventions

- Keep commit messages to one concise sentence
- Example: "Add course enrollment validation" (not "Added validation for enrolling users into courses and updated tests")

## Troubleshooting

### Container Issues
```bash
docker compose down
docker compose up -d
make init
```

### Database Issues
```bash
make migrate-fresh-quick     # Nuclear option: reset everything
```

### Package Updates
```bash
make composer-update         # Updates all packages
make restart_queue_cron      # Restart background workers
```

### Permission Issues
```bash
docker compose exec api bash
chown -R www-data:www-data storage bootstrap/cache
```
