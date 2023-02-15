from django.urls import path

from study.apps import StudyConfig
from study.views import CursViewSet, LessonListAPIView, LessonUpdateAPIView, LessonCreateAPIView, LessonDestroyAPIView
from rest_framework.routers import DefaultRouter


app_name = StudyConfig.name

router = DefaultRouter()
router.register(r'curs', CursViewSet, basename='curs')

urlpatterns = [
    path('', LessonListAPIView.as_view(), name='lesson_list'),
    path('update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
              ] + router.urls

