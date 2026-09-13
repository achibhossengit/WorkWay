import time
from datetime import timedelta
from decimal import Decimal

import requests
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from jobs.models import Job
from payments.models import Payment


def _gateway_base():
    if settings.SSL_IS_SANDBOX:
        return 'https://sandbox.sslcommerz.com'
    return 'https://securepay.sslcommerz.com'


def _callback_base():
    return settings.SSL_BACKEND_URL.rstrip('/') + '/api/v1/payments'


def _make_tran_id(job_id):
    return f"WW{job_id}{int(time.time())}"[-30:]


def apply_successful_payment(payment, val_id=''):
    if payment.status == Payment.SUCCESS:
        if val_id and not payment.val_id:
            payment.val_id = val_id
            payment.save(update_fields=['val_id', 'updated_at'])
        return payment

    payment.status = Payment.SUCCESS
    if val_id:
        payment.val_id = val_id
    payment.save(update_fields=['status', 'val_id', 'updated_at'])

    job = payment.job
    now = timezone.now()
    start = job.featured_until if job.featured_until and job.featured_until > now else now
    job.featured_until = start + timedelta(days=settings.FEATURED_JOB_DAYS)
    job.save(update_fields=['featured_until'])
    return payment


def validate_with_sslcommerz(val_id):
    if not val_id:
        return None
    if not settings.SSL_STORE_PASSWD:
        return None

    response = requests.get(
        f'{_gateway_base()}/validator/api/validationserverAPI.php',
        params={
            'val_id': val_id,
            'store_id': settings.SSL_STORE_ID,
            'store_passwd': settings.SSL_STORE_PASSWD,
            'format': 'json',
        },
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    status = str(data.get('status', '')).upper()
    if status in {'VALID', 'VALIDATED'}:
        return data
    return None


def mark_from_gateway_payload(payload):
    tran_id = payload.get('tran_id') or ''
    val_id = payload.get('val_id') or ''
    status = str(payload.get('status') or '').upper()

    try:
        payment = Payment.objects.select_related('job').get(tran_id=tran_id)
    except Payment.DoesNotExist:
        return None

    if payment.status == Payment.SUCCESS:
        return payment

    if status in {'VALID', 'VALIDATED'} or val_id:
        try:
            validated = validate_with_sslcommerz(val_id) if val_id else None
        except requests.RequestException:
            validated = None
        if validated or status in {'VALID', 'VALIDATED'}:
            return apply_successful_payment(payment, val_id=val_id or payment.val_id)

    if status in {'FAILED', 'UNATTEMPTED', 'EXPIRED'}:
        payment.status = Payment.FAILED
        payment.save(update_fields=['status', 'updated_at'])
    elif status in {'CANCELLED', 'CANCELED'}:
        payment.status = Payment.CANCELLED
        payment.save(update_fields=['status', 'updated_at'])

    return payment


def create_featured_session(employer, job_id):
    if not settings.SSL_STORE_ID or not settings.SSL_STORE_PASSWD:
        raise ValidationError(
            'SSLCommerz is not configured. Set SSL_STORE_ID and SSL_STORE_PASSWD.'
        )

    try:
        job = Job.objects.get(pk=job_id, employer=employer)
    except Job.DoesNotExist:
        raise ValidationError('You can only feature your own jobs.')

    if job.is_featured:
        raise ValidationError('This job is already featured.')

    Payment.objects.filter(
        job=job, employer=employer, status=Payment.PENDING, purpose=Payment.FEATURED
    ).update(status=Payment.CANCELLED)

    amount = Decimal(str(settings.FEATURED_JOB_AMOUNT))
    tran_id = _make_tran_id(job.id)
    callbacks = _callback_base()
    user = employer.user

    payload = {
        'store_id': settings.SSL_STORE_ID,
        'store_passwd': settings.SSL_STORE_PASSWD,
        'total_amount': f'{amount:.2f}',
        'currency': 'BDT',
        'tran_id': tran_id,
        'success_url': f'{callbacks}/success/',
        'fail_url': f'{callbacks}/fail/',
        'cancel_url': f'{callbacks}/cancel/',
        'ipn_url': f'{callbacks}/ipn/',
        'cus_name': (
            f'{user.first_name} {user.last_name}'.strip() or user.username
        ),
        'cus_email': user.email or 'employer@workway.local',
        'cus_add1': employer.location or 'Dhaka',
        'cus_city': 'Dhaka',
        'cus_country': 'Bangladesh',
        'cus_phone': user.contact_number or '01700000000',
        'shipping_method': 'NO',
        'product_name': f'Featured listing: {job.title}'[:160],
        'product_category': 'Jobs',
        'product_profile': 'general',
    }

    try:
        response = requests.post(
            f'{_gateway_base()}/gwprocess/v4/api.php',
            data=payload,
            timeout=25,
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise ValidationError(f'Could not start SSLCommerz session: {exc}') from exc

    if str(data.get('status', '')).upper() != 'SUCCESS' or not data.get('GatewayPageURL'):
        reason = data.get('failedreason') or data.get('failedReason') or 'Could not start payment.'
        raise ValidationError(reason)

    payment = Payment.objects.create(
        employer=employer,
        job=job,
        purpose=Payment.FEATURED,
        amount=amount,
        currency='BDT',
        status=Payment.PENDING,
        tran_id=tran_id,
        session_key=data.get('sessionkey') or '',
        gateway_url=data.get('GatewayPageURL'),
    )
    return payment
