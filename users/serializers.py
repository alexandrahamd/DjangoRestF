from rest_framework import serializers

from study.models import Payments
from study.serializers import PaymentsSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    pays = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'phone', 'city', 'pays', ]

    def get_pays(self, instanse):
        return [f'{pay.data_of_payments}, {pay.curs_id}, {pay.summa}$' for pay in Payments.objects.filter(user_id=instanse)]