from rest_framework import serializers
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'job',
            'job_title',
            'purpose',
            'amount',
            'currency',
            'status',
            'tran_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class PaymentInitSerializer(serializers.Serializer):
    job_id = serializers.IntegerField()
