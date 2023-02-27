from rest_framework.test import APITestCase
from study.models import Curs, Subscription
from users.models import User
from rest_framework import status


class CursTestCase(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create(
            email='zaqw12@yandex.ru',
        )
        self.user.set_password('zaq123')
        self.user.save()

        response = self.client.post(
            '/user/api/token/',
            {'email': 'zaqw12@yandex.ru', 'password': 'zaq123'}
        )

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_curs_create(self):

        response = self.client.post('/study/curs/',
                                    {'title': 'NewTest'},
                                    format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

    def test_curs_update(self):
        self.test_curs_create()
        odj = Curs.objects.get(title='NewTest')

        response = self.client.put(
            f'/study/curs/{odj.id}/',
            {'title': 'New update Test'}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        p = Curs.objects.get()
        self.assertEqual(p.title, 'New update Test')

    def test_curs_delete(self):
        self.test_curs_create()
        odj = Curs.objects.get(title='NewTest')

        response = self.client.delete(
            f'/study/curs/{odj.id}/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_curs_list(self):
        self.test_curs_create()

        response = self.client.get(
            '/study/curs/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        json = response.json()

        self.assertEqual(len(json), 1)


class CursAndSubTestCase(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        # создание пользователя
        self.user = User.objects.create(
            email='zaqw12@yandex.ru',
        )
        self.user.set_password('zaq123')
        self.user.save()

        response = self.client.post(
            '/user/api/token/',
            {'email': 'zaqw12@yandex.ru', 'password': 'zaq123'}
        )

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.user = User.objects.get(email="zaqw12@yandex.ru")

        # создание двух курсов

        self.curs = Curs.objects.create(
            title='NewTest',)

        self.curs_second = Curs.objects.create(
            title='SecondTest',)

        self.curs = Curs.objects.get(title="NewTest")
        self.curs_id = self.curs.id

        self.curs_second = Curs.objects.get(title="SecondTest")
        self.curs_id_second = self.curs_second.id

        # создание подписки, где user это наш пользователь, а curs это первый созданный курс "NewTest"

        self.subscription = Subscription.objects.create(
            curs=self.curs,
            user=self.user
        )

    def test_sub_detail(self):

        # проверка ситуации, когда пользователь подписан на урок
        response = self.client.get(
            f'/study/curs/{self.curs_id}/',
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.curs_id,
                "title": "NewTest",
                "description": None,
                "lessons_count": 0,
                "lessons_of_curs": [],
                "info_scription": "Вы подписаны на курс"
            }
        )

        # проверка ситуации, когда пользователь НЕ подписан на урок
        response_second = self.client.get(
            f'/study/curs/{self.curs_id_second}/',
        )

        self.assertEqual(
            response_second.json(),
            {
                "id": self.curs_id_second,
                "title": "SecondTest",
                "description": None,
                "lessons_count": 0,
                "lessons_of_curs": [],
                "info_scription": "Вы не подписаны на курс"
            }
        )
