from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from payments.views import (
    PaymentCancelView,
    PaymentFailView,
    PaymentInitView,
    PaymentIPNView,
    PaymentSuccessView,
    PaymentVerifyView,
)

urlpatterns = [
    path('init/', PaymentInitView.as_view(), name='payment-init'),
    path('verify/', PaymentVerifyView.as_view(), name='payment-verify'),
    path('ipn/', csrf_exempt(PaymentIPNView.as_view()), name='payment-ipn'),
    path('success/', csrf_exempt(PaymentSuccessView.as_view()), name='payment-success'),
    path('fail/', csrf_exempt(PaymentFailView.as_view()), name='payment-fail'),
    path('cancel/', csrf_exempt(PaymentCancelView.as_view()), name='payment-cancel'),
]
