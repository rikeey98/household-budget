from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user']

class ChildCategorySummarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    total = serializers.DecimalField(max_digits=12, decimal_places=0)

class CategorySummarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.CharField()
    total = serializers.DecimalField(max_digits=12, decimal_places=0)
    children = ChildCategorySummarySerializer(many=True)

class WeekSummarySerializer(serializers.Serializer):
    week = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    summary = serializers.DictField()  # {'expense': ..., 'income': ...}
    categories = CategorySummarySerializer(many=True)

class WeeklySummaryResponseSerializer(serializers.Serializer):
    weeks = WeekSummarySerializer(many=True) 