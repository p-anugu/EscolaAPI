# Wellms (EscolaLMS) API Complete Reference

## Overview

Wellms (EscolaLMS) is a **headless, API-first Learning Management System** built with Laravel. It's designed as a modular, developer-friendly platform that provides comprehensive e-learning capabilities through a REST API.

## Core Architecture Principles

### 1. Headless Architecture
- **No built-in frontend** - Pure API that can work with any frontend framework
- **Stateless design** - All configuration via environment variables
- **RESTful endpoints** - Standard HTTP methods and status codes
- **JSON responses** - Consistent response format across all endpoints

### 2. Modular Package System
- **40+ specialized packages** - Each handling specific functionality
- **Loose coupling** - Packages can be added/removed independently
- **Event-driven** - Packages communicate via Laravel events
- **Extensible** - Easy to add custom packages

### 3. Configuration Philosophy
- **Environment variables** - All config via `LARAVEL_*` prefixed vars
- **No .env file editing in production** - Stateless deployments
- **Database-stored settings** - Runtime configuration via Settings package
- **Multi-tenant support** - Domain-based configuration

## Authentication & Authorization

### Authentication Methods
1. **Laravel Passport OAuth2**
   - Bearer token authentication
   - Personal access tokens
   - OAuth2 authorization flows
   - Token expiration and refresh

2. **Social Login Support**
   - Google, Facebook, LinkedIn integration
   - Automatic account creation
   - Profile data synchronization

### Authorization System
- **Role-Based Access Control (RBAC)**
  - Predefined roles: Admin, Tutor, Student
  - Custom role creation
  - Granular permissions system

- **Group-Based Access**
  - User groups for organizational structure
  - Nested groups support
  - Group-based course access

### API Authentication Flow
```
1. POST /api/auth/login
   -> Returns: access_token, refresh_token, expires_at

2. Include in requests:
   Authorization: Bearer {access_token}

3. Refresh when expired:
   POST /api/auth/refresh
```

## Request/Response Formats

### Standard Request Format
```json
{
  "data": {
    "field1": "value1",
    "field2": "value2"
  },
  "filters": {
    "search": "keyword",
    "category": 1
  },
  "pagination": {
    "page": 1,
    "per_page": 15
  }
}
```

### Standard Response Format
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "meta": {
    "current_page": 1,
    "total": 100,
    "per_page": 15,
    "last_page": 7
  },
  "message": "Operation successful"
}
```

### Error Response Format
```json
{
  "success": false,
  "message": "Validation error",
  "errors": {
    "field_name": [
      "The field is required"
    ]
  },
  "code": 422
}
```

## HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET/PUT |
| 201 | Created | Successful POST creating resource |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid request format |
| 401 | Unauthorized | Missing/invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

## Common API Patterns

### 1. Pagination
All list endpoints support pagination:
```
GET /api/resource?page=1&per_page=15&order_by=created_at&order=DESC
```

### 2. Filtering
Standard filter parameters:
```
GET /api/resource?search=keyword&status=active&category_id=5
```

### 3. Including Relations
Use `with` parameter to include related data:
```
GET /api/courses?with=lessons,author,categories
```

### 4. Field Selection
Limit returned fields:
```
GET /api/users?fields=id,name,email
```

### 5. Sorting
Multiple field sorting:
```
GET /api/courses?sort=title:asc,created_at:desc
```

## File Handling

### Upload Process
1. **Direct upload** to topic/course
2. **Temporary storage** via Files package
3. **S3/MinIO storage** for production
4. **CDN support** for delivery

### File Types Support
- **Documents**: PDF, DOCX, XLSX, PPTX
- **Images**: JPG, PNG, GIF, SVG, WEBP
- **Videos**: MP4, WEBM, OGG
- **Audio**: MP3, WAV, OGG
- **SCORM/H5P**: ZIP packages

## Event System

### Core Events
- `UserRegistered` - New user registration
- `CourseAssigned` - User enrolled in course
- `CourseFinished` - Course completion
- `TopicFinished` - Topic completion
- `PaymentSuccessful` - Payment processed

### Event Listeners
- Email notifications
- Progress tracking
- Certificate generation
- Analytics recording
- Webhook dispatching

## Caching Strategy

### Cache Layers
1. **Response caching** - Full response caching
2. **Query caching** - Database query results
3. **Object caching** - Computed values
4. **CDN caching** - Static assets

### Cache Headers
```
Cache-Control: public, max-age=3600
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Last-Modified: Wed, 21 Oct 2024 07:28:00 GMT
```

## Rate Limiting

### Default Limits
- **Anonymous**: 60 requests/minute
- **Authenticated**: 600 requests/minute
- **Admin**: Unlimited

### Headers
```
X-RateLimit-Limit: 600
X-RateLimit-Remaining: 599
X-RateLimit-Reset: 1634850234
```

## Webhook System

### Webhook Events
- Course enrollment
- Payment completion
- User registration
- Progress updates
- Certificate issued

### Webhook Payload
```json
{
  "event": "course.enrolled",
  "timestamp": "2024-01-01T00:00:00Z",
  "data": {
    "user_id": 123,
    "course_id": 456
  },
  "signature": "sha256=..."
}
```

## API Versioning

### Current Version
- **v1** - Current stable version
- Versioning via URL path: `/api/v1/`
- Backward compatibility maintained

### Deprecation Policy
- 6-month deprecation notice
- Sunset headers in responses
- Migration guides provided

## Security Features

### Request Security
- **HTTPS only** in production
- **CORS configuration** for cross-origin requests
- **CSRF protection** for state-changing operations
- **SQL injection prevention** via query builder
- **XSS protection** via output encoding

### Data Security
- **Password hashing** - Bcrypt with salt
- **Encryption at rest** - Sensitive data encrypted
- **PII handling** - GDPR compliant
- **Audit logging** - All admin actions logged

## Performance Optimizations

### Database
- **Query optimization** - Eager loading, indexes
- **Connection pooling** - Persistent connections
- **Read replicas** - Load distribution
- **Query caching** - Repeated query optimization

### Application
- **OpCode caching** - PHP OPcache
- **Route caching** - Compiled routes
- **Config caching** - Compiled configuration
- **Class autoloading** - Optimized composer autoload

## Monitoring & Logging

### Application Logs
- **Laravel logs** - `storage/logs/laravel.log`
- **Error tracking** - Sentry integration
- **Performance monitoring** - New Relic/DataDog
- **Custom metrics** - StatsD integration

### API Metrics
- Request count
- Response times
- Error rates
- Cache hit rates
- Database query times

## Development Tools

### API Documentation
- **Swagger/OpenAPI** - Interactive documentation
- **Postman collections** - Pre-built requests
- **SDK generation** - Auto-generated clients

### Testing
- **PHPUnit** - Unit and integration tests
- **Pest PHP** - Modern testing framework
- **API testing** - Automated endpoint testing
- **Load testing** - Performance validation

## Deployment

### Environments
- **Development** - Local Docker setup
- **Staging** - Pre-production testing
- **Production** - Scaled deployment

### Infrastructure
- **Containerized** - Docker images
- **Orchestration** - Kubernetes support
- **Auto-scaling** - Horizontal scaling
- **Load balancing** - Traffic distribution

## Best Practices

### API Usage
1. **Use pagination** for large datasets
2. **Cache responses** when possible
3. **Batch operations** to reduce requests
4. **Handle errors gracefully**
5. **Implement exponential backoff** for retries

### Integration
1. **Use webhooks** for real-time updates
2. **Store tokens securely**
3. **Validate webhook signatures**
4. **Log all API interactions**
5. **Monitor rate limits**

## Support & Resources

### Documentation
- Official docs: https://docs.wellms.io
- API reference: `/api/documentation`
- GitHub: https://github.com/EscolaLMS

### Community
- GitHub Issues for bug reports
- Discussions for questions
- Discord/Slack channels
- Stack Overflow tags

## Compliance & Standards

### Educational Standards
- **SCORM 1.2/2004** - Full support
- **xAPI/Tin Can** - Learning Record Store
- **CMI5** - Next-gen SCORM support
- **QTI** - Assessment interoperability

### Data Protection
- **GDPR compliant** - EU data protection
- **COPPA compliant** - Children's privacy
- **FERPA compliant** - Educational records
- **SOC 2** - Security standards