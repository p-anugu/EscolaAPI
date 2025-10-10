# EscolaLMS Package Capabilities Reference

## Core Packages

### 1. Auth Package (`escolalms/auth`)
**Purpose**: Complete user authentication and authorization system

**Capabilities**:
- User registration with email verification
- Login/logout with JWT tokens
- Password reset/recovery
- Social authentication (Google, Facebook, LinkedIn)
- Two-factor authentication support
- User profile management
- Avatar upload/management
- Role-based access control (Admin, Tutor, Student)
- Custom permissions system
- User groups and organizational hierarchy
- User interests and onboarding tracking
- Account deletion with GDPR compliance
- User impersonation for admins
- Session management and device tracking

**Key Features**:
- Soft deletes for user preservation
- Email verification workflows
- Account security settings
- Login history and audit trails

---

### 2. Courses Package (`escolalms/courses`)
**Purpose**: Complete course management and delivery system

**Capabilities**:
- Course creation with rich metadata
- Multi-level curriculum structure (Course → Lessons → Topics)
- Multiple content types per topic
- Course scheduling and availability windows
- Course prerequisites and dependencies
- Progress tracking per user
- Course completion certificates
- Course cloning and templating
- Bulk course operations
- Course categories and tags
- Course search and filtering
- Course enrollment management
- Course completion rules
- Course authors/instructors management

**Content Delivery**:
- Sequential/non-sequential navigation
- Topic preview for non-enrolled users
- Skip-able topics configuration
- Timed content release
- Adaptive learning paths

---

### 3. Cart Package (`escolalms/cart`)
**Purpose**: E-commerce shopping cart functionality

**Capabilities**:
- Shopping cart management
- Product catalog integration
- Multiple product types (courses, consultations, bundles)
- Cart persistence across sessions
- Guest checkout support
- Cart abandonment tracking
- Quantity management
- Price calculations with tax
- Discount/voucher application
- Cart expiration settings
- Multi-currency support
- Bulk operations

**Checkout Process**:
- Address management
- Shipping calculations
- Payment method selection
- Order creation

---

### 4. Payments Package (`escolalms/payments`)
**Purpose**: Payment processing and gateway integration

**Capabilities**:
- Multiple payment gateway support
- Payment method management
- Recurring payments/subscriptions
- Payment history tracking
- Refund processing
- Payment notifications
- Invoice generation
- Tax calculations
- Payment reconciliation
- Failed payment recovery
- Payment webhooks handling
- PCI compliance helpers

**Supported Gateways**:
- Stripe
- PayPal
- Przelewy24
- Bank transfers
- Custom gateway integration

---

### 5. Consultations Package (`escolalms/consultations`)
**Purpose**: One-on-one consultation/tutoring system

**Capabilities**:
- Consultation scheduling
- Calendar integration
- Availability management
- Booking system
- Jitsi Meet integration for video calls
- Consultation categories
- Pricing tiers
- Consultation duration settings
- Automated reminders
- Consultation history
- Feedback and ratings
- Consultation recordings
- Time zone handling
- Recurring consultations

**User Features**:
- Proposed term negotiations
- Rescheduling requests
- Cancellation policies
- Waiting lists

---

### 6. Webinar Package (`escolalms/webinar`)
**Purpose**: Live streaming and webinar functionality

**Capabilities**:
- Live webinar creation
- YouTube Live integration
- Jitsi integration
- Webinar scheduling
- Registration management
- Attendee limits
- Automated email reminders
- Recording capabilities
- Chat/Q&A features
- Polls and surveys
- Screen sharing
- Webinar series support
- Replay access
- Analytics and reporting

**Streaming Features**:
- Multiple presenters
- Breakout rooms
- Waiting rooms
- Stream quality settings

---

## Content Type Packages

### 7. Headless H5P Package (`escolalms/headless-h5p`)
**Purpose**: Interactive HTML5 content integration

**Capabilities**:
- H5P content creation
- H5P library management
- Interactive video support
- Quizzes and assessments
- Drag-and-drop activities
- Timeline interactions
- Virtual tours
- Branching scenarios
- Content embedding
- Score tracking
- xAPI support
- Content reuse
- H5P content import/export

---

### 8. SCORM Package (`escolalms/scorm`)
**Purpose**: SCORM package support

**Capabilities**:
- SCORM 1.2 support
- SCORM 2004 support
- Package upload and validation
- Progress tracking
- Score reporting
- Bookmark support
- Suspend data handling
- Multi-SCO support
- SCORM cloud integration
- Debugging tools
- Manifest parsing
- Asset management

---

### 9. Topic Types Package (`escolalms/topic-types`)
**Purpose**: Various content types for course topics

**Supported Types**:
- **RichText**: HTML/Markdown content
- **Video**: Video streaming with player
- **Audio**: Audio playback
- **Image**: Image galleries
- **PDF**: PDF viewer integration
- **OEmbed**: External content embedding
- **H5P**: Interactive content
- **SCORM**: SCORM packages
- **Cmi5Au**: CMI5 content

**Features per Type**:
- Progress tracking
- Time tracking
- Completion rules
- Resource attachments
- Metadata storage

---

### 10. Topic Type Gift Package (`escolalms/topic-type-gift`)
**Purpose**: GIFT format quiz support

**Capabilities**:
- GIFT format parsing
- Multiple question types
- Quiz attempt tracking
- Score calculation
- Time limits
- Attempt restrictions
- Feedback display
- Question randomization
- Answer shuffling
- Partial credit
- Quiz reports
- Export capabilities

---

### 11. Topic Type Project Package (`escolalms/topic-type-project`)
**Purpose**: Student project submissions

**Capabilities**:
- Project assignment creation
- File upload support
- Submission deadlines
- Grading system
- Feedback mechanisms
- Peer review options
- Rubric support
- Version control
- Plagiarism checking integration
- Group projects
- Project templates

---

## Communication Packages

### 12. Templates Email Package (`escolalms/templates-email`)
**Purpose**: Email template management

**Capabilities**:
- Dynamic email templates
- Variable replacement
- Multi-language support
- Template categories
- MJML support
- Preview functionality
- A/B testing
- Delivery tracking
- Bounce handling
- Template versioning
- Default templates
- Custom headers/footers

---

### 13. Notifications Package (`escolalms/notifications`)
**Purpose**: Multi-channel notification system

**Capabilities**:
- Email notifications
- SMS notifications
- Push notifications
- In-app notifications
- Notification preferences
- Digest options
- Real-time delivery
- Notification history
- Read/unread tracking
- Notification templates
- Channel routing
- Failure handling

---

### 14. Bulk Notifications Package (`escolalms/bulk-notifications`)
**Purpose**: Mass notification campaigns

**Capabilities**:
- Bulk email sending
- Segmentation tools
- Campaign scheduling
- Template selection
- Personalization
- Delivery reports
- Open/click tracking
- Unsubscribe handling
- Bounce management
- Campaign analytics

---

## User Management Packages

### 15. CSV Users Package (`escolalms/csv-users`)
**Purpose**: Bulk user import/export

**Capabilities**:
- CSV import validation
- Bulk user creation
- User data export
- Field mapping
- Error reporting
- Progress tracking
- Update existing users
- Custom field support
- Encoding detection
- Large file handling

---

### 16. Assign Without Account Package (`escolalms/assign-without-account`)
**Purpose**: Pre-enrollment before registration

**Capabilities**:
- Course assignment via email
- Bulk assignment
- Invitation tracking
- Auto-enrollment on registration
- Expiration dates
- Custom messages
- Reminder emails
- Assignment reports

---

## Analytics & Reporting Packages

### 17. Reports Package (`escolalms/reports`)
**Purpose**: Comprehensive reporting system

**Capabilities**:
- Course completion reports
- User progress reports
- Financial reports
- Custom report builder
- Scheduled reports
- Export formats (PDF, Excel, CSV)
- Data visualization
- Drill-down capabilities
- Real-time dashboards
- Report sharing
- Report templates

---

### 18. Questionnaire Package (`escolalms/questionnaire`)
**Purpose**: Survey and feedback system

**Capabilities**:
- Survey creation
- Multiple question types
- Conditional logic
- Response collection
- Anonymous responses
- Result analysis
- Export capabilities
- Template library
- Multi-page surveys
- Response validation

---

## Integration Packages

### 19. Mattermost Package (`escolalms/mattermost`)
**Purpose**: Mattermost chat integration

**Capabilities**:
- User synchronization
- Channel creation
- Direct messaging
- File sharing
- Notification routing
- Bot integration
- Webhook support
- SSO integration

---

### 20. Jitsi Package (`escolalms/jitsi`)
**Purpose**: Video conferencing integration

**Capabilities**:
- Room creation
- JWT authentication
- Custom branding
- Recording support
- Screen sharing
- Chat integration
- Participant management
- Meeting scheduling
- Webhooks for events

---

### 21. YouTube Package (`escolalms/youtube`)
**Purpose**: YouTube integration

**Capabilities**:
- Video import
- Channel integration
- Playlist sync
- Live streaming
- Analytics import
- Comment sync
- Automatic upload
- Thumbnail generation

---

## Storage & Media Packages

### 22. Files Package (`escolalms/files`)
**Purpose**: File management system

**Capabilities**:
- File upload/download
- Storage abstraction
- S3/MinIO support
- File versioning
- Access control
- Temporary URLs
- File compression
- Metadata storage
- Virus scanning
- CDN integration

---

### 23. Images Package (`escolalms/images`)
**Purpose**: Image processing and optimization

**Capabilities**:
- Automatic resizing
- Format conversion
- Compression
- Lazy loading support
- Responsive images
- Watermarking
- Thumbnail generation
- EXIF handling
- CDN optimization

---

### 24. Video Package (`escolalms/video`)
**Purpose**: Video processing and streaming

**Capabilities**:
- Video transcoding
- Adaptive bitrate streaming
- Thumbnail extraction
- Subtitle support
- Chapter markers
- Video analytics
- DRM support
- Live streaming
- Cloud encoding

---

## E-commerce Extensions

### 25. Vouchers Package (`escolalms/vouchers`)
**Purpose**: Discount and promotion system

**Capabilities**:
- Voucher generation
- Usage limits
- Expiration dates
- Product restrictions
- User restrictions
- Percentage/fixed discounts
- Bulk generation
- Voucher categories
- Usage tracking
- Campaign management

---

### 26. Invoices Package (`escolalms/invoices`)
**Purpose**: Invoice generation and management

**Capabilities**:
- Automatic invoice generation
- Custom numbering
- Multi-language support
- Tax calculations
- PDF generation
- Email delivery
- Invoice templates
- Credit notes
- Recurring invoices
- Integration with accounting systems

---

## Infrastructure Packages

### 27. Settings Package (`escolalms/settings`)
**Purpose**: Dynamic configuration management

**Capabilities**:
- Runtime configuration
- Database-stored settings
- Setting categories
- Type validation
- Default values
- Cache management
- Public/private settings
- Setting groups
- Import/export
- Audit trail

---

### 28. Model Fields Package (`escolalms/model-fields`)
**Purpose**: Dynamic model field extension

**Capabilities**:
- Custom field creation
- Field types support
- Validation rules
- Field metadata
- Searchable fields
- Field permissions
- Field groups
- Import/export
- Migration support

---

### 29. Categories Package (`escolalms/categories`)
**Purpose**: Hierarchical categorization system

**Capabilities**:
- Tree structure
- Multiple parents
- Category metadata
- Icon/image support
- Slug generation
- Breadcrumbs
- Category templates
- Import/export
- Category permissions

---

### 30. Tags Package (`escolalms/tags`)
**Purpose**: Flexible tagging system

**Capabilities**:
- Polymorphic tags
- Tag groups
- Auto-suggestions
- Tag merging
- Usage statistics
- Tag clouds
- Weighted tags
- Tag permissions
- Bulk operations

---

## Testing & Development Packages

### 31. Core Package (`escolalms/core`)
**Purpose**: Core utilities and base classes

**Capabilities**:
- Base repositories
- Base controllers
- Common traits
- Helper functions
- Testing utilities
- Database seeders
- Validation rules
- Response formatters
- Query builders
- Cache helpers

---

## Security & Compliance Packages

### 32. Permissions Package (`escolalms/permissions`)
**Purpose**: Advanced permission management

**Capabilities**:
- Granular permissions
- Permission groups
- Dynamic permissions
- Permission inheritance
- Role templates
- Permission auditing
- Temporary permissions
- Permission delegation

---

### 33. LRS Package (`escolalms/lrs`)
**Purpose**: Learning Record Store for xAPI

**Capabilities**:
- xAPI statement storage
- Statement validation
- Query API
- Aggregation pipelines
- Activity streams
- Actor profiles
- State management
- Document storage
- Analytics API

---

## Each Package Provides:

### Standard Features
- RESTful API endpoints
- Database migrations
- Event dispatching
- Permission definitions
- Configuration options
- Seeders for testing
- Comprehensive tests
- Documentation

### Integration Points
- Laravel service providers
- Event listeners
- Middleware
- Console commands
- Scheduled tasks
- Queue jobs
- Validation rules
- Blade components

### Extensibility
- Configurable options
- Hook points
- Custom implementations
- Override capabilities
- Plugin architecture
- Theme support
- Translation files
- Asset publishing