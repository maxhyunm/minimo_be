from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError


class PrjListSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Project
        fields = '__all__'