from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.api.views import (
    GalleryItemViewSet,
    LoginView,
    QuestionPaperViewSet,
    RecordedLectureViewSet,
    RefreshTokenView,
    RegisterView,

    NotificationViewSet,
    AttendanceViewSet,
    ExamViewSet,
    FeeViewSet,
    MarkViewSet,
    ProfileView,
    StudentViewSet,
    StudentDashboardView,
    AttendanceSummaryView,
    AttendanceMonthlyView,
    FeesSummaryView,
    MarksExamsView,
    MarksResultView,
    MarksPerformanceView,
    GalleryCategoriesView,
    NotificationMarkReadView,
    NotificationMarkAllReadView,
    NotificationUnreadCountView,
    logout_view,
    update_fcm_token_view,
    NotesView,
    FeeReceiptsView,
    dashboard_stats,
)

router = DefaultRouter()
router.register('students', StudentViewSet, basename='student')
router.register('attendance', AttendanceViewSet, basename='attendance')
router.register('fees', FeeViewSet, basename='fee')
router.register('exams', ExamViewSet, basename='exam')
router.register('marks', MarkViewSet, basename='mark')
router.register('notifications', NotificationViewSet, basename='notification')

router.register('lectures', RecordedLectureViewSet, basename='lecture')
router.register('gallery', GalleryItemViewSet, basename='gallery')
router.register('question-papers', QuestionPaperViewSet, basename='question-paper')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/fcm-token/', update_fcm_token_view, name='fcm_token'),
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('attendance/summary/', AttendanceSummaryView.as_view(), name='attendance_summary'),
    path('attendance/monthly/', AttendanceMonthlyView.as_view(), name='attendance_monthly'),
    path('fees/summary/', FeesSummaryView.as_view(), name='fees_summary'),
    path('marks/exams/', MarksExamsView.as_view(), name='marks_exams'),
    path('marks/result/', MarksResultView.as_view(), name='marks_result'),
    path('marks/performance/', MarksPerformanceView.as_view(), name='marks_performance'),
    path('gallery-categories/', GalleryCategoriesView.as_view(), name='gallery_categories'),
    path('notifications/<int:pk>/mark_read/', NotificationMarkReadView.as_view(), name='notification_mark_read'),
    path('notifications/mark_all_read/', NotificationMarkAllReadView.as_view(), name='notification_mark_all_read'),
    path('notifications/unread_count/', NotificationUnreadCountView.as_view(), name='notification_unread_count'),
    path('notes/', NotesView.as_view(), name='notes'),
    path('receipts/', FeeReceiptsView.as_view(), name='receipts'),
    path('dashboard/stats/', dashboard_stats, name='dashboard_stats'),
    path('', include(router.urls)),
]
