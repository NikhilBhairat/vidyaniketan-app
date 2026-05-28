from django.db.models import Q, Sum, Count, Avg, F, ExpressionWrapper, DecimalField
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.models import User
from apps.attendance.models import Attendance
from apps.fees.models import Fee, FeeReceipt
from apps.gallery.models import GalleryItem, GalleryCategory
from apps.lectures.models import RecordedLecture
from apps.notifications.models import Notification, NotificationRead
from apps.results.models import Exam, Mark
from apps.students.models import Student
from apps.study_material.models import QuestionPaper, Note
from apps.api.serializers import (
    AttendanceSerializer,
    ExamSerializer,
    FeeSerializer,
    FeeReceiptSerializer,
    GalleryItemSerializer,
    GalleryCategorySerializer,
    MarkSerializer,
    MobileTokenObtainPairSerializer,
    NotificationSerializer,
    NoteSerializer,
    ProfileSerializer,
    QuestionPaperSerializer,
    RegisterSerializer,
    RecordedLectureSerializer,

    StudentSerializer,
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics for admin panel"""
    stats = {
        'students_count': Student.objects.filter(is_active=True).count(),
        'attendance_count': Attendance.objects.count(),
        'fees_count': Fee.objects.count(),
        'notifications_count': Notification.objects.count(),
        'total_fees_amount': Fee.objects.aggregate(total=Sum('amount'))['total'] or 0,
        'paid_fees_amount': Fee.objects.filter(status='Paid').aggregate(total=Sum('amount'))['total'] or 0,
        'pending_fees_amount': Fee.objects.filter(status='Pending').aggregate(total=Sum('amount'))['total'] or 0,
    }
    return Response(stats)


class LoginView(TokenObtainPairView):
    serializer_class = MobileTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StudentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.STUDENT:
            return Student.objects.filter(user=user)
        return Student.objects.all()


class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AttendanceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.STUDENT and hasattr(user, 'student_profile'):
            return Attendance.objects.filter(student=user.student_profile)
        return Attendance.objects.all()


class FeeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FeeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.STUDENT and hasattr(user, 'student_profile'):
            return Fee.objects.filter(student=user.student_profile)
        return Fee.objects.all()


class ExamViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExamSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()


class MarkViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MarkSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.STUDENT and hasattr(user, 'student_profile'):
            return Mark.objects.filter(student=user.student_profile)
        return Mark.objects.all()


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != User.STUDENT:
            return Notification.objects.filter(is_sent=True)
        
        # For students, filter by audience and target_standard
        queryset = Notification.objects.filter(
            Q(audience='all') | 
            Q(audience='standard', target_standard=user.student_profile.standard) |
            Q(target_students__user=user)
        ).filter(is_sent=True).distinct()
        return queryset


class RecordedLectureViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecordedLectureSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = RecordedLecture.objects.filter(is_active=True)


class GalleryItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GalleryItemSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = GalleryItem.objects.all()


class QuestionPaperViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionPaperSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = QuestionPaper.objects.all()


# ── Custom API Views for Flutter App ──────────────────────────────────────────

class StudentDashboardView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer

    def get_object(self):
        return self.request.user.student_profile

    def get(self, request, *args, **kwargs):
        try:
            student = self.get_object()
        except:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Calculate quick stats
        attendance_stats = Attendance.objects.filter(student=student).aggregate(
            present_count=Count('id', filter=Q(status='P')),
            total_count=Count('id'),
        )
        attendance_percentage = (attendance_stats['present_count'] / attendance_stats['total_count'] * 100) if attendance_stats['total_count'] > 0 else 0

        unpaid_fees_count = Fee.objects.filter(student=student, status='unpaid').count()
        unpaid_fees_balance = Fee.objects.filter(student=student).aggregate(
            remaining=Sum(ExpressionWrapper(F('total_fee') - F('amount_paid'), output_field=DecimalField()))
        )['remaining'] or 0
        unread_notifications = NotificationRead.objects.filter(user=request.user, read_at__isnull=True).count()

        recent_fees = FeeSerializer(
            Fee.objects.filter(student=student).order_by('-created_at')[:5],
            many=True,
        ).data
        recent_receipts = FeeReceiptSerializer(
            FeeReceipt.objects.filter(fee__student=student).order_by('-payment_date')[:5],
            many=True,
        ).data
        recent_gallery = GalleryItemSerializer(
            GalleryItem.objects.all().order_by('-uploaded_at')[:10],
            many=True,
        ).data

        data = {
            'id': student.id,
            'student_id': student.student_id,
            'full_name': student.full_name,
            'standard': student.standard,
            'standard_display': student.get_standard_display(),
            'school_name': student.school_name,
            'profile_photo_url': request.build_absolute_uri(student.profile_photo.url) if student.profile_photo else None,
            'mobile_number': student.mobile_number,
            'date_of_birth': student.date_of_birth,
            'gender': student.gender,
            'blood_group': student.blood_group,
            'address': student.address,
            'admission_date': student.admission_date,
            'quick_stats': {
                'attendance_percentage': round(attendance_percentage, 1),
                'fees_due_amount': unpaid_fees_balance,
                'unread_notifications': unread_notifications,
                'unpaid_fees_count': unpaid_fees_count,
            },
            'recent_fees': recent_fees,
            'recent_receipts': recent_receipts,
            'recent_gallery': recent_gallery,
        }
        return Response(data)


class AttendanceSummaryView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        student = self.request.user.student_profile
        year = self.request.query_params.get('year', timezone.now().year)
        return Attendance.objects.filter(student=student, date__year=year)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        present_count = queryset.filter(status='P').count()
        absent_count = queryset.filter(status='A').count()
        total_count = queryset.count()
        percentage = (present_count / total_count * 100) if total_count > 0 else 0

        data = {
            'present_days': present_count,
            'absent_days': absent_count,
            'total_days': total_count,
            'attendance_percentage': round(percentage, 1),
        }
        return Response(data)


class AttendanceMonthlyView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        student = self.request.user.student_profile
        month = int(self.request.query_params.get('month', timezone.now().month))
        year = int(self.request.query_params.get('year', timezone.now().year))
        return Attendance.objects.filter(student=student, date__month=month, date__year=year).order_by('date')


class FeesSummaryView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FeeSerializer

    def get_queryset(self):
        student = self.request.user.student_profile
        return Fee.objects.filter(student=student)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_fee = queryset.aggregate(Sum('total_fee'))['total_fee__sum'] or 0
        total_paid = queryset.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        total_balance = total_fee - total_paid

        data = {
            'total_fee': total_fee,
            'total_paid': total_paid,
            'total_balance': total_balance,
        }
        return Response(data)


class MarksExamsView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()


class MarksResultView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MarkSerializer

    def get_object(self):
        exam_id = self.request.query_params.get('exam')
        student = self.request.user.student_profile
        return Mark.objects.filter(student=student, exam_id=exam_id)

    def retrieve(self, request, *args, **kwargs):
        marks = self.get_object()
        total_marks = marks.aggregate(Sum('marks_obtained'))['marks_obtained__sum'] or 0
        total_possible = marks.aggregate(Sum('exam__total_marks'))['exam__total_marks__sum'] or 0
        percentage = (total_marks / total_possible * 100) if total_possible > 0 else 0

        data = {
            'marks': MarkSerializer(marks, many=True).data,
            'overall_percentage': round(percentage, 1),
            'overall_grade': 'A' if percentage >= 90 else 'B' if percentage >= 80 else 'C' if percentage >= 70 else 'D' if percentage >= 60 else 'F',
        }
        return Response(data)


class MarksPerformanceView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MarkSerializer

    def get_queryset(self):
        student = self.request.user.student_profile
        return Mark.objects.filter(student=student).order_by('-created_at')


class GalleryCategoriesView(ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = GalleryCategorySerializer
    queryset = GalleryCategory.objects.all()


class NotificationMarkReadView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        NotificationRead.objects.get_or_create(
            notification=notification,
            user=request.user,
            defaults={'read_at': timezone.now()}
        )
        return Response({'status': 'marked as read'})


class NotificationMarkAllReadView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(
            Q(audience='all') | Q(target_students__user=request.user)
        ).distinct()
        for notification in notifications:
            NotificationRead.objects.get_or_create(
                notification=notification,
                user=request.user,
                defaults={'read_at': timezone.now()}
            )
        return Response({'status': 'all marked as read'})


class NotificationUnreadCountView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        unread_count = NotificationRead.objects.filter(user=request.user, read_at__isnull=True).count()
        return Response({'unread_count': unread_count})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # Invalidate tokens on server side if needed
    return Response({'status': 'logged out'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_fcm_token_view(request):
    token = request.data.get('fcm_token')
    if token:
        request.user.fcm_token = token
        request.user.save()
    return Response({'status': 'updated'})

class NotesView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        student = self.request.user.student_profile
        return Note.objects.filter(student=student)


class FeeReceiptsView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FeeReceiptSerializer

    def get_queryset(self):
        student = self.request.user.student_profile
        return FeeReceipt.objects.filter(fee__student=student)