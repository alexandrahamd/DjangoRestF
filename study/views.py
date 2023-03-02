import hashlib
from hashlib import sha256
from http.client import responses
import json
import requests
from django.conf import settings
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from study.models import Curs, Lesson, Subscription, PaymentLog, Payments
from study.permissions import IsOwner, IsModerator
from study.serializers import CursSerializer, LessonSerializer, SubscriptionSerializer, PaymentYouMoneySerializer


class CursViewSet(viewsets.ModelViewSet):
    queryset = Curs.objects.all()
    serializer_class = CursSerializer
    # permission_classes = [IsAuthenticated]
    #
    # def create(self, request, *args, **kwargs):
    #     if request.user.has_perm('study.create_curs') or request.user.is_authenticated:
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if request.user.has_perm('stydy.update_curs') or request.user == self.request.user:
    #         partial = kwargs.pop('partial', False)
    #         serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_update(serializer)
    #
    #         if getattr(instance, '_prefetched_objects_cache', None):
    #             instance._prefetched_objects_cache = {}
    #
    #         return Response(serializer.data)
    #
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if request.user.has_perm('stydy.delete_curs') or request.user == self.request.user:
    #         self.perform_destroy(instance)
    #         return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & IsModerator]


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    # permission_classes = [IsAuthenticated]


class PaymentAPIView(APIView):

    def get(self, *args, **kwargs):
        curs_pk = self.kwargs.get('pk')
        curs_item = get_object_or_404(Curs, pk=curs_pk)

        user_item = self.request.user

        # pay = Payments.objects.create(
        #     curs_id=curs_item,
        #     user_id=self.request.user,
        #     summa=curs_item.prise
        # )

        data = {
            "TerminalKey": settings.TERMINALKEY,
            "Amount": curs_item.prise,
            "OrderId": curs_item.pk,
            "Description": "Оплата заказа",
            "DATA": {
                "Phone": user_item.phone,
                "Email": user_item.email
            },
            "Receipt": {
                "Email": 'email@ya.ru',
                "Phone": 123456,
                "EmailCompany": "b@test.ru",
                "Taxation": "osn",
                "Items": [
                    {
                        "Name": curs_item.title,
                        "Price": curs_item.prise,
                        "Quantity": 1.00,
                        "Amount": curs_item.prise,
                        "PaymentMethod": "full_prepayment",
                        "PaymentObject": "commodity",
                        "Tax": "vat10",
                        "Ean13": "0123456789"
                    }
                ]
            }
        }

        r = requests.post('https://securepay.tinkoff.ru/v2/Init', json=data)
        PaymentLog.objects.create(**r.json())

        return Response(
            {
                'url': r.json().get('PaymentURL'),
            }
        )


class PaymentStatusAPIView(APIView):

    def get(self, *args, **kwargs):
        payment_id = self.kwargs.get('PaymentId')
        payment_item = get_object_or_404(PaymentLog, PaymentId=payment_id)
        amount = str(payment_item.Amount)
        description = 'Оплата заказа'
        orderId = str(payment_item.OrderId)
        password = settings.PASSWORD
        terminalKey = settings.TERMINALKEY

        token = amount+description+orderId+password+terminalKey
        hash = hashlib.sha256(token.encode('utf-8')).hexdigest()

        data_status = {
                "TerminalKey": settings.TERMINALKEY,
                "PaymentId": payment_id,
                "Token": hash
        }

        r = requests.post('https://securepay.tinkoff.ru/v2/GetState', json=data_status)

        return Response(
            {
                'url': r.json()
            }
        )

