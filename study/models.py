
from django.db import models
from django.conf import settings


class Curs(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1000, blank=True, null=True)
    preview = models.ImageField(upload_to='curces', blank=True, null=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    curs = models.ForeignKey(Curs, on_delete=models.CASCADE, verbose_name='курс', blank=True, null=True)
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.CharField(max_length=1000, blank=True, null=True, verbose_name='описание')
    preview = models.ImageField(upload_to='curces', blank=True, null=True, verbose_name='превью')
    link_video = models.URLField(blank=True, null=True, verbose_name='ссылка на видео')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Payments(models.Model):
    CASH = "cash"
    BANK = "bank account"

    CHOICES = [
        (CASH, "cash"),
        (BANK, "bank account"),
        ]

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_of_payments = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    curs_id = models.ForeignKey(Curs, on_delete=models.CASCADE, verbose_name='курс')
    summa = models.PositiveIntegerField(default=0, verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=15, choices=CHOICES, verbose_name='способ оплаты')

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return f'{self.user_id}{self.curs_id}'


class Subscription(models.Model):
    curs = models.ForeignKey(Curs, on_delete=models.CASCADE, verbose_name='курс')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.curs} {self.user}'

