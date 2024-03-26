from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
