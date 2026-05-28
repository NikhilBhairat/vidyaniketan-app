# Vidyaniketan Backend - Complete Analysis Report

## Overview
A **Django REST Framework (DRF)** based backend for a school management system. The app serves a Flutter mobile frontend and provides comprehensive management of students, attendance, fees, results, lectures, and notifications.

---

## 🔐 LOGIN CREDENTIALS

### Admin Credentials
- **Username/Mobile**: `9999999999`
- **Password**: `admin123`
- **Role**: Admin
- **Access**: Django Admin Panel at `/admin/`

### Test Student Accounts
All student accounts use the same password: `password123`

| Name | Mobile | Email | Standard | Roll No | Student ID | Tuition Fee |
|------|--------|-------|----------|---------|-----------|------------|
| Rahul Sharma | 9876543210 | rahul.sharma@example.com | 8th | 001 | STD8001 | ₹10,000 |
| Priya Patel | 9876543211 | priya.patel@example.com | 9th | 002 | STD9002 | ₹12,000 |
| Amit Kumar | 9876543212 | amit.kumar@example.com | 10th | 003 | STD10003 | ₹15,000 |

**Login Endpoint**: `POST /api/auth/login/`
```json
{
  "mobile_number": "9876543210",
  "password": "password123"
}
```

---

## 📊 Technology Stack

### Framework & Libraries
- **Django**: 5.2.13
- **Django REST Framework**: 3.14.x
- **JWT Authentication**: `djangorestframework-simplejwt`
- **Database**: SQLite3 (db.sqlite3)
- **CORS**: Enabled for all origins (development)
- **Filters**: `django-filters`

### Key Settings
- **DEBUG**: True (Development mode)
- **SECRET_KEY**: `django-insecure-&-kgn1n*3a0ohpaz!1r7&ge+t0n((#pwkvf-3!975d8$m-1$^8`
- **ALLOWED_HOSTS**: `['127.0.0.1', 'localhost', 'testserver']`
- **JWT Token Lifetime**: 1 day
- **Timezone**: Asia/Kolkata (IST)
- **Language**: en-us

---

## 🏗️ Architecture & Project Structure

```
Backend/
├── project/                      # Django Project Settings
│   ├── settings.py              # Main configuration
│   ├── urls.py                  # Root URL router
│   ├── asgi.py                  # ASGI for async
│   └── wsgi.py                  # WSGI for production
│
├── apps/                         # Main application modules
│   ├── accounts/                # User authentication
│   ├── students/                # Student management
│   ├── attendance/              # Attendance tracking
│   ├── fees/                    # Fee management
│   ├── results/                 # Exam results
│   ├── study_material/          # Notes & Question Papers
│   ├── lectures/                # Video lectures
│   ├── gallery/                 # Photo/media gallery
│   ├── notifications/           # Push notifications
│   └── api/                     # API endpoints & serializers
│
├── media/                       # User uploaded files
├── static/                      # Static files (CSS, JS)
├── staticfiles/                 # Collected static files
├── templates/                   # HTML templates
├── db.sqlite3                  # Database
├── manage.py                   # Django management
├── create_dummy_data.py        # Test data generator
└── requirements.txt            # Python dependencies
```

---

## 📱 Database Models (14 Models)

### 1. **Accounts App**
- **User** (18 fields)
  - Primary auth model with custom USERNAME_FIELD = `mobile_number`
  - Fields: mobile_number, email, role, password, is_active, is_staff, is_superuser, date_joined, fcm_token
  - Roles: student, admin, teacher
  - Manager: `UserManager` for creating users/superusers

### 2. **Students App**
- **Student** (21 fields)
  - Main student profile model
  - FK: user (OneToOne)
  - Fields: student_id, full_name, standard, profile_photo, date_of_birth, gender, blood_group, roll_number, mobile_number, school_name, address, admission_date, is_active, receive_admin_alerts
  - Standards: 1st to 10th
  - Genders: Male, Female, Other
  - Blood groups: O+, A+, B+, AB+, O-, A-, B-, AB-

- **Parent** (8 fields)
  - Parent/Guardian information
  - FK: user (OneToOne, nullable)
  - Fields: full_name, mobile_number, alternate_phone, email, occupation, annual_income, address, relation

### 3. **Attendance App**
- **Attendance** (6 fields)
  - Daily attendance tracking
  - FK: student
  - Fields: date, status, remarks, created_at
  - Status: Present (P), Absent (A), Late (L), Holiday (H)
  - Unique constraint: (student, date)
  - Test data: April 2026 with 76%, 87%, 92% attendance percentages

### 4. **Fees App**
- **FeeStructure** (9 fields)
  - Fee configuration per standard/term
  - Fields: standard, academic_year, term, tuition_fee, exam_fee, library_fee, sports_fee, other_fee, due_date
  - Terms: Q1, Q2, Q3, Q4, Annual, Monthly

- **Fee** (10 fields)
  - Student fee records
  - FK: student
  - Fields: total_fee, amount_paid, number_of_installments, next_installment_date, status, remarks, created_at
  - Status: paid, unpaid, partial
  - Properties: remaining_fee, balance

- **FeeReceipt** (10 fields)
  - Payment receipts
  - FK: fee
  - Fields: receipt_number, amount, payment_date, payment_mode, transaction_id, receipt_pdf, issued_by, created_at
  - Payment modes: Cash, Online, Cheque, DD, UPI

### 5. **Results App**
- **Exam** (10 fields)
  - Exam configuration
  - Fields: name, exam_type, standard, academic_year, start_date, end_date, total_marks, passing_marks
  - Exam types: unit_test, midterm, prelim, final, practice

- **Mark** (11 fields)
  - Student exam marks
  - FK: student, exam
  - Fields: subject, marks_obtained, grade, is_absent, remarks, entered_by, created_at, updated_at
  - Grades: A+, A, B+, B, C, D, F
  - Unique constraint: (student, exam, subject)

### 6. **Study_Material App**
- **Note** (7 fields)
  - Student notes
  - FK: student
  - Fields: title, content, created_at, updated_at, is_important

- **QuestionPaper** (10 fields)
  - Exam question papers
  - Fields: title, subject, standard, exam_type, year, file, solution_file, uploaded_at, download_count
  - Exam types: board, unit_test, midterm, model

### 7. **Lectures App**
- **RecordedLecture** (14 fields)
  - Video lecture management
  - Fields: title, subject, chapter, teacher, platform, video_url, video_file, thumbnail, duration_minutes, description, uploaded_at, is_active, view_count
  - Platforms: youtube, vimeo, drive, upload

### 8. **Gallery App**
- **GalleryCategory** (3 fields)
  - Photo/video categories
  - Fields: name, description

- **GalleryItem** (5 fields)
  - Gallery photos/videos
  - FK: gallery_category
  - Fields: file, video_url, uploaded_at

### 9. **Notifications App**
- **Notification** (12 fields)
  - System notifications
  - FK: created_by (user), M2M: target_students
  - Fields: title, message, notification_type, audience, target_standard, is_sent, sent_at, created_at
  - Types: general, fees, marks, attendance, timetable, event, holiday
  - Audience: all, standard, specific_student
  - Test data: 6 notifications (1 holiday + 2 each for standards 8,9,10)

- **NotificationRead** (3 fields)
  - Notification read status tracking
  - FK: notification, user
  - Unique constraint: (notification, user)

---

## 🌐 API Endpoints

### Base URL
`http://localhost:8000/api/`

### Authentication Endpoints
- `POST /auth/login/` - Obtain JWT tokens
- `POST /auth/refresh/` - Refresh access token
- `POST /auth/register/` - Register new student
- `GET /profile/` - Get user profile
- `PATCH /profile/` - Update user profile
- `POST /logout/` - Logout user
- `POST /update-fcm-token/` - Update Firebase token

### Resource Endpoints (ViewSets)
- `GET /students/` - List/Filter students
- `GET /attendance/` - List attendance records
- `GET /fees/` - List fee records
- `GET /exams/` - List exams
- `GET /marks/` - List marks
- `GET /notifications/` - List notifications
- `GET /lectures/` - List recorded lectures
- `GET /gallery/` - List gallery items
- `GET /question-papers/` - List question papers
- `GET /notes/` - List study notes
- `GET /fee-receipts/` - List fee receipts

### Dashboard Endpoints
- `GET /dashboard-stats/` - Dashboard statistics
- `GET /student/dashboard/` - Student dashboard
- `GET /student/attendance-summary/` - Attendance summary
- `GET /student/attendance-monthly/` - Monthly attendance
- `GET /student/fees-summary/` - Fee summary
- `GET /student/marks-exams/` - Exam list for marks
- `GET /student/marks-result/` - Marks results
- `GET /student/marks-performance/` - Performance analytics

### Additional Endpoints
- `GET /gallery-categories/` - Gallery categories
- `PATCH /notifications/{id}/mark-read/` - Mark notification as read
- `PATCH /notifications/mark-all-read/` - Mark all as read
- `GET /notifications/unread-count/` - Unread notification count

---

## 🔐 Authentication & Security

### JWT Authentication
- **Header**: `Authorization: Bearer <access_token>`
- **Token Lifetime**: 1 day
- **Refresh Token**: Can be used to obtain new access token
- **Serializer**: `MobileTokenObtainPairSerializer` (custom)
- **Uses mobile_number** as USERNAME_FIELD instead of username

### Permissions
- Most endpoints require `IsAuthenticated`
- Auth endpoints allow `AllowAny`
- Student-specific endpoints filter by `user.role == 'student'`

### CORS Configuration
- **Status**: Enabled for all origins
- **Suitable for**: Development only
- **Should be restricted**: In production

---

## 📊 Serializers

| Serializer | Model(s) | Purpose |
|-----------|----------|---------|
| `MobileTokenObtainPairSerializer` | User | Custom JWT login using mobile_number |
| `UserSerializer` | User | Read-only user info |
| `RegisterSerializer` | User | User registration with password hashing |
| `ProfileSerializer` | User | User profile view/edit |
| `StudentSerializer` | Student | Student details with relationships |
| `ParentSerializer` | Parent | Parent/Guardian info |
| `AttendanceSerializer` | Attendance | Attendance records |
| `FeeSerializer` | Fee | Fee records with balance calculations |
| `FeeStructureSerializer` | FeeStructure | Fee structure display |
| `FeeReceiptSerializer` | FeeReceipt | Payment receipts |
| `ExamSerializer` | Exam | Exam configuration |
| `MarkSerializer` | Mark | Student exam marks |
| `NotificationSerializer` | Notification | System notifications |
| `GalleryItemSerializer` | GalleryItem | Gallery photos/videos |
| `GalleryCategorySerializer` | GalleryCategory | Gallery categories |
| `RecordedLectureSerializer` | RecordedLecture | Video lectures |
| `QuestionPaperSerializer` | QuestionPaper | Question papers |
| `NoteSerializer` | Note | Student study notes |

---

## 📁 File Structure Details

### Admin Configuration (`admin.py`)
- All 14 models registered in Django Admin
- Custom list displays, filters, and search fields configured
- Custom actions for bulk operations
- Read-only fields defined appropriately

### Migrations
- Initial migrations for all models already created
- Additional migration files for model updates:
  - `attendance`: 0002 (alter unique_together)
  - `fees`: 0002 (rename fields, remove fields)
  - `gallery`: 0002-0004 (alter fields, add new fields)
  - `lectures`: 0002 (alter subject)

### Media Directories
- `media/gallery/` - Gallery images/videos
- `media/students/photos/` - Student profile photos
- `media/lectures/videos/` - Lecture videos
- `media/lectures/thumbnails/` - Video thumbnails
- `media/receipts/` - Fee receipt PDFs
- `media/question_papers/` - Question paper uploads
- `media/question_papers/solutions/` - Answer key uploads

---

## 🛠️ Key Features Implemented

✅ **User Management**
- Role-based access (Student, Admin, Teacher)
- Mobile-number based authentication
- JWT token authentication
- FCM token management for push notifications

✅ **Student Management**
- Complete student profiles
- Parent/Guardian management
- Standard classification (1-10)
- Profile photo uploads
- Blood group tracking
- Admission records

✅ **Attendance Tracking**
- Daily attendance marking
- Presence/Absent/Late/Holiday status
- Attendance percentage calculations
- Monthly attendance reports
- Attendance summaries

✅ **Fee Management**
- Fee structure configuration per standard
- Flexible installment support
- Partial payment tracking
- Payment receipt generation
- Multiple payment modes (Cash, Online, UPI, etc.)
- Fee status tracking (Paid, Unpaid, Partial)
- Fee balance calculations

✅ **Results & Marks**
- Exam management with types and date ranges
- Grade recording (A+ to F)
- Subject-wise marks
- Absent handling
- Performance analytics

✅ **Study Material**
- Question papers library with filters
- Solution files support
- Student notes
- Download tracking

✅ **Video Lectures**
- Multi-platform support (YouTube, Vimeo, Google Drive, Direct Upload)
- Thumbnails and descriptions
- View count tracking
- Active/Inactive status

✅ **Gallery**
- Photo/video management
- Category organization
- Upload tracking
- Media file storage

✅ **Notifications**
- Multi-level targeting (all, standard, specific student)
- Multiple notification types
- Read status tracking
- Unread count
- Delivery timestamp

---

## 📋 Admin Fixes Completed

According to `ADMIN_FIXES_REPORT.txt`, all 14 models are now fully accessible in Django Admin:

1. **Accounts**: Users (fixed field references)
2. **Students**: Students & Institutes (removed non-existent fields)
3. **Attendance**: (fixed search_field reference)
4. **Fees**: Fee & FeeReceipt (working)
5. **Notifications**: (working)
6. **Gallery**: Categories & Items (working)
7. **Results**: Exams & Marks (fixed search fields)
8. **Study Material**: Notes & QuestionPapers (working)
9. **Lectures**: RecordedLectures (working)

---

## 🚀 Running the Backend

### Setup
```bash
cd Backend
pip install -r requirements.txt
python manage.py migrate
python create_dummy_data.py
python manage.py runserver
```

### Admin Access
- URL: `http://localhost:8000/admin/`
- Username: `9999999999`
- Password: `admin123`

### API Access
- Base URL: `http://localhost:8000/api/`
- Login: `POST /api/auth/login/` with mobile + password
- Authorization: Add `Authorization: Bearer <token>` header

---

## ⚠️ Security Notes for Production

1. **Change DEBUG to False**
2. **Update SECRET_KEY** - Currently exposed
3. **Restrict ALLOWED_HOSTS** - Only include actual domains
4. **Disable CORS_ALLOW_ALL_ORIGINS** - Configure specific origins
5. **Use environment variables** for sensitive data
6. **Use PostgreSQL** instead of SQLite
7. **Enable HTTPS** only
8. **Update password validators** from empty list
9. **Configure email backend** for notifications
10. **Add rate limiting** for API endpoints

---

## 📞 Contact Information (From Marketing)

**Vidyaniketan Classes & Academy**
- Website: [Not provided]
- Email: [Not provided]
- Contact: +91-97644 51714, +91-9730 70 7765
- Location: Yeaheep Apartment, Manglvwar Tale Road, Manglvwar Pet, Sattara

