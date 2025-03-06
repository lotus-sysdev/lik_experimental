from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Report, Lokasi, Tujuan, Kayu


class ReportSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField()

    class Meta:
        model = Report
        fields = '__all__'

        
    def validate(self, data):
        upload_date = data.get('upload_date')
        current_date = timezone.now().date()

        if upload_date and upload_date != current_date:
            raise serializers.ValidationError("The upload date must match the current date.")

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name','email', 'password']

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LokasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lokasi
        fields = '__all__'

class TujuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tujuan
        fields = '__all__'

class KayuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kayu
        fields = '__all__'

class ReportSummarySerializer(serializers.Serializer):
    total_plat = serializers.IntegerField()
    total_tonnage = serializers.IntegerField()
    total_rejects = serializers.IntegerField()