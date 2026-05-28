from django.contrib import admin
from .models import Fee, FeeReceipt
from project.admin_site import vidyaniketan_admin_site


class FeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'total_fee', 'amount_paid', 'remaining_amount', 'status', 'number_of_installments', 'next_installment_date', 'created_at']
    search_fields = ['student__full_name', 'student__student_id']
    list_filter = ['status', 'number_of_installments', 'next_installment_date']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 20

    def remaining_amount(self, obj):
        return obj.remaining_fee
    remaining_amount.short_description = 'Remaining Fee'


class FeeReceiptAdmin(admin.ModelAdmin):
    list_display = ['id', 'receipt_number', 'fee', 'amount', 'payment_date', 'payment_mode', 'created_at']
    search_fields = ['receipt_number', 'fee__student__full_name', 'transaction_id']
    list_filter = ['payment_mode', 'payment_date']
    date_hierarchy = 'payment_date'
    ordering = ['-payment_date']
    list_per_page = 20


# Register with custom admin site
vidyaniketan_admin_site.register(Fee, FeeAdmin)
vidyaniketan_admin_site.register(FeeReceipt, FeeReceiptAdmin)