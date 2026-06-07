from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import User
from apps.students.models import Student, Parent
from apps.attendance.models import Attendance
from apps.fees.models import Fee, FeeReceipt, FeeStructure
from apps.gallery.models import GalleryItem, GalleryCategory
from apps.lectures.models import RecordedLecture
from apps.notifications.models import Notification, NotificationRead
from apps.results.models import Exam, Mark
from apps.study_material.models import QuestionPaper, Note


class MobileTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD  # 'mobile_number'

    def validate(self, attrs):
        # Call parent validation - it will use self.username_field ('mobile_number') automatically
        try:
            data = super().validate(attrs)
        except Exception as e:
            # Provide clear error message for login failures
            raise serializers.ValidationError({
                'non_field_errors': [
                    'Invalid mobile number or password. Please check your credentials.'
                ]
            })
        
        # Add user data to response
        data['user'] = UserSerializer(self.user).data
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'mobile_number', 'email', 'role', 'is_active', 'date_joined', 'fcm_token']
        read_only_fields = ['id', 'date_joined', 'role', 'is_active']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'mobile_number', 'password', 'email', 'role']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'mobile_number', 'email', 'role', 'is_active', 'fcm_token', 'date_joined']
        read_only_fields = ['id', 'mobile_number', 'role', 'is_active', 'date_joined']


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'full_name', 'mobile_number', 'alternate_phone', 'email', 'occupation', 'annual_income', 'address', 'relation']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    standard_display = serializers.CharField(source='get_standard_display', read_only=True)
    profile_photo_url = serializers.SerializerMethodField()  # ✅ NEW: Cache-busting URL

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'full_name', 'standard', 'standard_display', 'profile_photo', 'profile_photo_url', 
            'date_of_birth', 'gender', 'blood_group', 'roll_number', 'mobile_number', 'school_name', 'address', 
            'admission_date', 'receive_admin_alerts', 'is_active', 'user',
        ]

    def get_profile_photo_url(self, obj):
        """Return absolute URL with cache-busting timestamp"""
        if obj.profile_photo:
            request = self.context.get('request')
            if request:
                url = request.build_absolute_uri(obj.profile_photo.url)
                # Add timestamp to bust cache
                from django.utils import timezone
                timestamp = int(timezone.now().timestamp())
                return f"{url}?t={timestamp}"
            return obj.profile_photo.url
        return None


class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    subject = serializers.StringRelatedField()
    marked_by = serializers.StringRelatedField()

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'date', 'status', 'subject', 'marked_by', 'remarks', 'created_at']


class FeeStructureSerializer(serializers.ModelSerializer):
    standard = serializers.StringRelatedField()
    academic_year = serializers.StringRelatedField()

    class Meta:
        model = FeeStructure
        fields = ['id', 'standard', 'academic_year', 'term', 'tuition_fee', 'exam_fee', 'library_fee', 'sports_fee', 'other_fee', 'due_date']


class FeeSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    remaining_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Fee
        fields = ['id', 'student', 'total_fee', 'amount_paid', 'remaining_fee', 'status', 'number_of_installments', 'next_installment_date', 'remarks', 'created_at']


class FeeReceiptSerializer(serializers.ModelSerializer):
    fee_id = serializers.IntegerField(source='fee.id', read_only=True)
    total_fee = serializers.DecimalField(source='fee.total_fee', max_digits=10, decimal_places=2, read_only=True)
    amount_paid = serializers.DecimalField(source='fee.amount_paid', max_digits=10, decimal_places=2, read_only=True)
    remaining_fee = serializers.SerializerMethodField()
    fee_status = serializers.CharField(source='fee.status', read_only=True)
    student_name = serializers.CharField(source='fee.student.full_name', read_only=True)
    school_name = serializers.CharField(source='fee.student.school_name', read_only=True)

    def get_remaining_fee(self, obj):
        return obj.fee.remaining_fee

    class Meta:
        model = FeeReceipt
        fields = [
            'id',
            'receipt_number',
            'fee_id',
            'student_name',
            'school_name',
            'amount',
            'payment_date',
            'payment_mode',
            'transaction_id',
            'receipt_pdf',
            'issued_by',
            'total_fee',
            'amount_paid',
            'remaining_fee',
            'fee_status',
            'created_at',
        ]


class ExamSerializer(serializers.ModelSerializer):
    standard = serializers.StringRelatedField()
    academic_year = serializers.StringRelatedField()

    class Meta:
        model = Exam
        fields = ['id', 'name', 'exam_type', 'standard', 'academic_year', 'start_date', 'end_date', 'total_marks', 'passing_marks']


class MarkSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    exam = serializers.StringRelatedField()
    subject = serializers.StringRelatedField()
    entered_by = serializers.StringRelatedField()

    class Meta:
        model = Mark
        fields = ['id', 'student', 'exam', 'subject', 'marks_obtained', 'grade', 'is_absent', 'remarks', 'entered_by', 'created_at', 'updated_at']


class RecordedLectureSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    chapter = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()

    class Meta:
        model = RecordedLecture
        fields = ['id', 'title', 'subject', 'chapter', 'teacher', 'platform', 'video_url', 'video_file', 'thumbnail', 'duration_minutes', 'description', 'uploaded_at', 'is_active', 'view_count']


class GalleryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'description']


class GalleryItemSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = GalleryItem
        fields = ['id', 'category', 'file', 'video_url', 'uploaded_at']


class QuestionPaperSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    solution_file = serializers.SerializerMethodField()

    class Meta:
        model = QuestionPaper
        fields = ['id', 'title', 'subject', 'standard', 'exam_type', 'year', 'file', 'solution_file', 'uploaded_at', 'download_count']

    def get_file(self, obj):
        if not obj.file:
            return None
        return obj.file.url

    def get_solution_file(self, obj):
        if not obj.solution_file:
            return None
        return obj.solution_file.url


class NotificationSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'audience', 'target_standard', 'is_sent', 'sent_at', 'created_at', 'created_by', 'is_read']

    def get_is_read(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # ✅ FIXED: Check if read_at is not None (actually marked as read)
            return NotificationRead.objects.filter(notification=obj, user=request.user, read_at__isnull=False).exists()
        return False


class NoteSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    pdf_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            'id',
            'student',
            'standard',
            'subject',
            'chapter',
            'title',
            'content',
            'pdf_file',
            'pdf_file_url',
            'is_important',
            'created_at',
            'updated_at',
        ]

    def get_pdf_file_url(self, obj):
        if not obj.pdf_file:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.pdf_file.url)
        return obj.pdf_file.url
