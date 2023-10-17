from django.core.validators import RegexValidator
from .models import Task
from .models import Courier
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'username', 'password', 'avatar']

    password = serializers.CharField(write_only=True, required=True, validators=[
        RegexValidator(regex='^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', message='密码至少8位，且不能为纯数字')])

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
