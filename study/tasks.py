import requests
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from study.models import Subscription, Curs


@shared_task
def send_email_curs(curs_pk):
    # получение подписок, чей курс был изменен
    lst_subscription = [sub.user for sub in Subscription.objects.filter(curs=curs_pk)]
    # получение списка имейлов
    lst_email = [sub.email for sub in lst_subscription]
    curs = Curs.objects.get(pk=curs_pk)
    title='Информация по курсу'
    body=f'Курс {curs} был изменен'
    try:
        send_mail(
            title,
            body,
            settings.EMAIL_HOST_USER,
            lst_email,
            fail_silently=False,
        )
        print('ok')
    except Exception:
        print('ошибка отправки сообщения')


@shared_task
def check_status_task():
    return requests.get(f'localhost:8000/study/payment_status/{2423967522}/')