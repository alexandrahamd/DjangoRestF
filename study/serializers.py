from django.contrib.auth.models import User
from rest_framework import serializers

from study.models import Curs, Lesson

class CursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curs
        fields = ['title', 'description',]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'description',]