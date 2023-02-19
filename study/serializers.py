from django.contrib.auth.models import User
from rest_framework import serializers

from study.models import Curs, Lesson, Payments


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'description',]


class CursSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons_of_curs = serializers.SerializerMethodField()

    class Meta:
        model = Curs
        fields = ['title', 'description', 'lessons_count', 'lessons_of_curs']

    def get_lessons_of_curs(self, instance):
        return [les.title for les in Lesson.objects.filter(curs=instance)]

    def get_lessons_count(self, instance):
        lessons_count = Lesson.objects.filter(curs=instance).count()
        if lessons_count:
            return lessons_count
        return 0


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['user_id', 'data_of_payments', 'curs_id', 'summa', ]


