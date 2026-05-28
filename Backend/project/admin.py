from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count

# Import all admin classes
from apps.accounts.admin import CustomUserAdmin
from apps.students.admin import StudentAdmin
from apps.attendance.admin import AttendanceAdmin
from apps.fees.admin import FeeAdmin, FeeReceiptAdmin
from apps.notifications.admin import NotificationAdmin
from apps.gallery.admin import GalleryCategoryAdmin, GalleryItemAdmin
from apps.results.admin import ExamAdmin, MarkAdmin
from apps.study_material.admin import NoteAdmin, QuestionPaperAdmin
from apps.lectures.admin import RecordedLectureAdmin

# Import models
from apps.accounts.models import User
from apps.students.models import Student
from apps.attendance.models import Attendance
from apps.fees.models import Fee, FeeReceipt
from apps.notifications.models import Notification
from apps.gallery.models import GalleryCategory, GalleryItem
from apps.results.models import Exam, Mark
from apps.study_material.models import Note, QuestionPaper
from apps.lectures.models import RecordedLecture

# Register all models with the default admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Institute, InstituteAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Fee, FeeAdmin)
admin.site.register(FeeReceipt, FeeReceiptAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(QuestionPaper, QuestionPaperAdmin)
admin.site.register(GalleryCategory, GalleryCategoryAdmin)
admin.site.register(GalleryItem, GalleryItemAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Mark, MarkAdmin)
admin.site.register(StudyMaterial, StudyMaterialAdmin)
admin.site.register(RecordedLecture, RecordedLectureAdmin)

# Customize the admin site
admin.site.site_header = "Vidyaniketan EduPanel Administration"
admin.site.site_title = "Vidyaniketan EduPanel"
admin.site.index_title = "Welcome to Vidyaniketan EduPanel"