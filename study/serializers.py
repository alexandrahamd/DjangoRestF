from django.contrib.auth.models import User
from django.http import request
from rest_framework import serializers
from study.models import Curs, Lesson, Payments, Subscription
from study.validators import LessonLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'link_video']
        validators = [LessonLinkValidator(field='link_video')]


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['user_id', 'data_of_payments', 'curs_id', 'summa', ]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['user', 'curs', ]


class CursSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons_of_curs = serializers.SerializerMethodField()
    info_scription = serializers.SerializerMethodField()
    # info = SubscriptionSerializer(source='subscription_set', many=True, blank=True, null=True)

    class Meta:
        model = Curs
        fields = ['id', 'title', 'description', 'lessons_count', 'lessons_of_curs', 'info_scription',]

    def get_info_scription(self, instance):
        '''Получение информации, о том подписан пользователь на курс или нет'''
        user = self.context['request'].user
        try:
            lesson_scription = Subscription.objects.get(user=user)
        except:
            return "Вы не подписаны на курс"
        title = Curs.objects.get(title=instance)

        # если текущий пользователь тот же, что и пользователь из модели
        # и название курса из модели совпадает с текущим курсом
        if lesson_scription.user == user and lesson_scription.curs == title:
            return "Вы подписаны на курс"
        return "Вы не подписаны на курс"

    def get_lessons_of_curs(self, instance):
        return [les.title for les in Lesson.objects.filter(curs=instance)]

    def get_lessons_count(self, instance):
        lessons_count = Lesson.objects.filter(curs=instance).count()
        if lessons_count:
            return lessons_count
        return 0


class PaymentYouMoneySerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    receiver = serializers.IntegerField(default='123456789')
    quickpay_form = serializers.CharField(default='button')
    paymentType = serializers.CharField(default='AC')
    sum = serializers.IntegerField(default='0')

