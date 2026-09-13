from django.contrib import admin
from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'tran_id',
        'employer',
        'job',
        'purpose',
        'amount',
        'status',
        'created_at',
    )
    list_filter = ('status', 'purpose')
    search_fields = ('tran_id', 'employer__user__username', 'job__title')
    readonly_fields = (
        'employer',
        'job',
        'purpose',
        'amount',
        'currency',
        'status',
        'tran_id',
        'val_id',
        'session_key',
        'gateway_url',
        'created_at',
        'updated_at',
    )
