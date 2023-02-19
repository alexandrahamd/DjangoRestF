from django.core.management import BaseCommand
from study.models import Lesson, Payments, Curs
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        curses = [
            {'title': 'Математика', 'description': 'Учимся считать', },
            {'title': 'Физика', 'description': 'Изучаем физические явления', },
            {'title': 'География', 'description': 'Изучаем страны', }
        ]

        curses_list = []
        for item in curses:
            curses_list.append(Curs(**item))

        Curs.objects.bulk_create(curses_list)

        lessons = [
            {'curs': Curs.objects.get(id=1), 'title': 'Алгебра'},
            {'curs': Curs.objects.get(pk=2), 'title': 'Закон Ома'},
            {'curs': Curs.objects.get(pk=3), 'title': 'Мадагаскар'},
            {'curs': Curs.objects.get(pk=3), 'title': 'Непал'},
        ]

        lessons_list = []
        for item in lessons:
            lessons_list.append(Lesson(**item))

        Lesson.objects.bulk_create(lessons_list)

        users = [
            {'email': '123@yandex.ru'},
            {'email': '321@yandex.ru'},
            {'email': '213@yandex.ru'},
        ]

        users_list = []
        for item in users:
            users_list.append(User(**item))

        User.objects.bulk_create(users_list)

        payments = [
            {'user_id': User.objects.get(id=1), 'curs_id': Curs.objects.get(id=1), 'summa': 200,
             'payment_method': "cash"},
            {'user_id': User.objects.get(id=2), 'curs_id': Curs.objects.get(id=2), 'summa': 300,
             'payment_method': "cash"},
            {'user_id': User.objects.get(id=3), 'curs_id': Curs.objects.get(id=3), 'summa': 400,
             'payment_method': "cash"}, ]

        payments_list = []
        for item in payments:
            payments_list.append(Payments(**item))

        Payments.objects.bulk_create(payments_list)
