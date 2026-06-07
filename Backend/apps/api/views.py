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
from apps.students.models import StandardFeatureAccess
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


def _get_student_feature_access(student):
    notes_enabled = True
    question_papers_enabled = True

    standard = str(getattr(student, 'standard', '') or '').strip()
    if standard:
        standard_config = StandardFeatureAccess.objects.filter(standard=standard).first()
        if standard_config:
            notes_enabled = standard_config.notes_enabled
            question_papers_enabled = standard_config.question_papers_enabled

    notes_enabled = notes_enabled and getattr(student, 'notes_access_enabled', True)
    question_papers_enabled = question_papers_enabled and getattr(student, 'question_papers_access_enabled', True)

    return {
        'notes': notes_enabled,
        'question_papers': question_papers_enabled,
    }


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
        
        # ✅ Auto-create NotificationRead records for tracking
        for notification in queryset:
            NotificationRead.objects.get_or_create(
                notification=notification,
                user=user,
                defaults={'read_at': None}
            )
        
        return queryset


class RecordedLectureViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecordedLectureSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = RecordedLecture.objects.filter(is_active=True)


class GalleryItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GalleryItemSerializer
    queryset = GalleryItem.objects.all()


class QuestionPaperViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionPaperSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role == User.STUDENT and hasattr(user, 'student_profile'):
            access = _get_student_feature_access(user.student_profile)
            if not access['question_papers']:
                return Response(
                    {'detail': 'Question papers are disabled for your account. Please contact admin.'},
                    status=status.HTTP_403_FORBIDDEN,
                )
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        if user.role == User.STUDENT and hasattr(user, 'student_profile'):
            access = _get_student_feature_access(user.student_profile)
            if not access['question_papers']:
                return QuestionPaper.objects.none()

            student_standard = str(user.student_profile.standard or '').strip()
            student_digits = ''.join(ch for ch in student_standard if ch.isdigit())
            standard_candidates = {
                student_standard,
                f'{student_standard}th',
                f'{student_standard}th Standard',
                f'{student_standard} Standard',
            }
            standard_candidates = {value for value in standard_candidates if value}

            filters = Q(standard__in=standard_candidates) | Q(standard__iexact=student_standard)
            if student_digits:
                filters = (
                    filters |
                    Q(standard__startswith=student_digits) |
                    Q(standard__istartswith=f'{student_digits}th')
                )

            return QuestionPaper.objects.filter(filters).distinct()

        return QuestionPaper.objects.all()


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
        note_standard = str(student.standard or '').strip()
        note_standard_candidates = {
            note_standard,
            f'{note_standard}th',
            f'{note_standard}th Standard',
            f'{note_standard} Standard',
        }
        note_standard_candidates = {value for value in note_standard_candidates if value}

        feature_access = _get_student_feature_access(student)

        if feature_access['notes']:
            recent_notes = NoteSerializer(
                Note.objects.filter(
                    Q(standard__in=note_standard_candidates) |
                    Q(standard__iexact=note_standard)
                ).order_by('-is_important', '-updated_at')[:5],
                many=True,
                context={'request': request},
            ).data
        else:
            recent_notes = []

        if feature_access['question_papers']:
            paper_filters = Q(standard__in=note_standard_candidates) | Q(standard__iexact=note_standard)
            if note_standard:
                paper_filters = (
                    paper_filters |
                    Q(standard__startswith=note_standard) |
                    Q(standard__istartswith=f'{note_standard}th')
                )
            recent_question_papers = QuestionPaperSerializer(
                QuestionPaper.objects.filter(paper_filters)
                .order_by('-uploaded_at')[:5],
                many=True,
                context={'request': request},
            ).data
        else:
            recent_question_papers = []
        recent_lectures = RecordedLectureSerializer(
            RecordedLecture.objects.filter(is_active=True).order_by('-uploaded_at')[:5],
            many=True,
            context={'request': request},
        ).data
        recent_gallery = GalleryItemSerializer(
            GalleryItem.objects.all().order_by('-uploaded_at')[:10],
            many=True,
        ).data

        profile_photo_url = None
        if student.profile_photo:
            profile_photo_url = request.build_absolute_uri(student.profile_photo.url)
            timestamp = int(timezone.now().timestamp())
            profile_photo_url = f"{profile_photo_url}?t={timestamp}"

        data = {
            'id': student.id,
            'student_id': student.student_id,
            'full_name': student.full_name,
            'standard': student.standard,
            'standard_display': student.get_standard_display(),
            'school_name': student.school_name,
            'profile_photo_url': profile_photo_url,
            'feature_access': feature_access,
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
            'recent_notes': recent_notes,
            'recent_question_papers': recent_question_papers,
            'recent_lectures': recent_lectures,
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
    serializer_class = GalleryCategorySerializer
    queryset = GalleryCategory.objects.all()


class NotificationMarkReadView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        notif_read, created = NotificationRead.objects.get_or_create(
            notification=notification,
            user=request.user,
        )
        if not notif_read.read_at:
            notif_read.read_at = timezone.now()
            notif_read.save()
        return Response({'status': 'marked as read', 'notification_id': notification.id})


class NotificationMarkAllReadView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        
        if user.role == User.STUDENT and hasattr(user, 'student_profile'):
            notifications = Notification.objects.filter(
                Q(audience='all') | 
                Q(audience='standard', target_standard=user.student_profile.standard) |
                Q(target_students__user=user)
            ).filter(is_sent=True).distinct()
        else:
            notifications = Notification.objects.filter(is_sent=True)
        
        count = 0
        for notification in notifications:
            notif_read, created = NotificationRead.objects.get_or_create(
                notification=notification,
                user=user,
            )
            if not notif_read.read_at:
                notif_read.read_at = timezone.now()
                notif_read.save()
                count += 1
        
        return Response({
            'status': 'all marked as read', 
            'count': count,
            'total_notifications': notifications.count()
        })


class NotificationUnreadCountView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        
        if user.role == User.STUDENT and hasattr(user, 'student_profile'):
            total_count = Notification.objects.filter(
                Q(audience='all') | 
                Q(audience='standard', target_standard=user.student_profile.standard) |
                Q(target_students__user=user),
                is_sent=True
            ).distinct().count()
            
            unread_count = NotificationRead.objects.filter(
                user=user,
                read_at__isnull=True,
                notification__is_sent=True
            ).count()
        else:
            total_count = Notification.objects.filter(is_sent=True).count()
            unread_count = NotificationRead.objects.filter(
                user=user,
                read_at__isnull=True
            ).count()
        
        return Response({
            'unread_count': unread_count,
            'total_count': total_count
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
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

    def list(self, request, *args, **kwargs):
        student = request.user.student_profile
        access = _get_student_feature_access(student)
        if not access['notes']:
            return Response(
                {'detail': 'Chapter-wise notes are disabled for your account. Please contact admin.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        student = self.request.user.student_profile
        access = _get_student_feature_access(student)
        if not access['notes']:
            return Note.objects.none()

        subject = self.request.query_params.get('subject')
        chapter = self.request.query_params.get('chapter')
        student_standard = str(student.standard or '').strip()

        standard_candidates = {
            student_standard,
            f'{student_standard}th',
            f'{student_standard}th Standard',
            f'{student_standard} Standard',
        }

        # Keep only non-empty candidates to avoid broad matches.
        standard_candidates = {value for value in standard_candidates if value}

        queryset = Note.objects.filter(
            Q(standard__in=standard_candidates) |
            Q(standard__iexact=student_standard)
        ).order_by('-is_important', '-updated_at')

        if subject:
            queryset = queryset.filter(subject__iexact=subject)
        if chapter:
            queryset = queryset.filter(chapter__iexact=chapter)

        return queryset


class FeeReceiptsView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FeeReceiptSerializer

    def get_queryset(self):
        student = self.request.user.student_profile
        return FeeReceipt.objects.filter(fee__student=student)
