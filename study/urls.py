from django.urls import path

from study.apps import StudyConfig
from study.views import CursViewSet, LessonListAPIView, LessonUpdateAPIView, LessonCreateAPIView, LessonDestroyAPIView, \
    SubscriptionViewSet
from rest_framework.routers import DefaultRouter


app_name = StudyConfig.name

router = DefaultRouter()
router.register(r'curs', CursViewSet, basename='curs')
router.register(r'subscription', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
              ] + router.urls

