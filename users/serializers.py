from rest_framework import serializers

from study.serializers import PaymentsSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    pays = PaymentsSerializer(many=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'city', 'pays', ]