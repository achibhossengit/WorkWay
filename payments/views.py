from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.permissions import IsEmployerOwnerOrAdminReadonly
from jobs.paginations import CustomPageNumberPagination
from payments.models import Payment
from payments.serializers import PaymentInitSerializer, PaymentSerializer
from payments.services import create_featured_session, mark_from_gateway_payload


def _frontend_redirect(path, params=None):
    base = settings.SSL_FRONTEND_URL.rstrip('/')
    query = f'?{urlencode(params)}' if params else ''
    return redirect(f'{base}{path}{query}')


def _payload_from_request(request):
    data = {}
    data.update(request.query_params.dict())
    data.update(request.data.dict() if hasattr(request.data, 'dict') else dict(request.data))
    return data


class PaymentInitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.user_type != 'Employer':
            return Response(
                {'detail': 'Only employers can purchase featured listings.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PaymentInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            payment = create_featured_session(
                request.user.employer,
                serializer.validated_data['job_id'],
            )
        except ValidationError as exc:
            detail = exc.detail
            if isinstance(detail, (list, tuple)):
                message = str(detail[0])
            elif isinstance(detail, dict):
                first = next(iter(detail.values()))
                message = str(first[0] if isinstance(first, (list, tuple)) else first)
            else:
                message = str(detail)
            return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                'tran_id': payment.tran_id,
                'gateway_url': payment.gateway_url,
                'amount': str(payment.amount),
                'currency': payment.currency,
            },
            status=status.HTTP_201_CREATED,
        )


class PaymentVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tran_id = request.query_params.get('tran_id')
        if not tran_id:
            return Response(
                {'detail': 'tran_id is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payment = Payment.objects.select_related('job', 'employer').get(
                tran_id=tran_id
            )
        except Payment.DoesNotExist:
            return Response(
                {'detail': 'Payment not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        is_owner = (
            request.user.user_type == 'Employer'
            and payment.employer_id == request.user.id
        )
        if not is_owner and not request.user.is_staff:
            return Response(
                {'detail': 'You can only view your own payments.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(PaymentSerializer(payment).data)


@method_decorator(csrf_exempt, name='dispatch')
class PaymentIPNView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        payment = mark_from_gateway_payload(_payload_from_request(request))
        if not payment:
            return Response({'detail': 'Unknown transaction.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': payment.status})


@method_decorator(csrf_exempt, name='dispatch')
class PaymentSuccessView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return self._finish(request)

    def post(self, request):
        return self._finish(request)

    def _finish(self, request):
        payload = _payload_from_request(request)
        payment = mark_from_gateway_payload(payload)
        tran_id = payload.get('tran_id') or (payment.tran_id if payment else '')
        return _frontend_redirect(
            '/dashboard/payments/success',
            {'tran_id': tran_id} if tran_id else None,
        )


@method_decorator(csrf_exempt, name='dispatch')
class PaymentFailView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return self._finish(request, Payment.FAILED, '/dashboard/payments/fail')

    def post(self, request):
        return self._finish(request, Payment.FAILED, '/dashboard/payments/fail')

    def _finish(self, request, new_status, path):
        payload = _payload_from_request(request)
        payload.setdefault('status', 'FAILED' if new_status == Payment.FAILED else 'CANCELLED')
        payment = mark_from_gateway_payload(payload)
        tran_id = payload.get('tran_id') or (payment.tran_id if payment else '')
        return _frontend_redirect(path, {'tran_id': tran_id} if tran_id else None)


@method_decorator(csrf_exempt, name='dispatch')
class PaymentCancelView(PaymentFailView):
    def get(self, request):
        return self._finish(request, Payment.CANCELLED, '/dashboard/payments/cancel')

    def post(self, request):
        return self._finish(request, Payment.CANCELLED, '/dashboard/payments/cancel')


class EmployerPaymentViewSet(ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdminReadonly]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Payment.objects.filter(
            employer_id=self.kwargs.get('employer_pk')
        ).select_related('job')
