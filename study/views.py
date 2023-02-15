from rest_framework import viewsets, generics
from study.models import Curs, Lesson
from study.serializers import CursSerializer, LessonSerializer


class CursViewSet(viewsets.ModelViewSet):
    queryset = Curs.objects.all()
    serializer_class = CursSerializer


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer