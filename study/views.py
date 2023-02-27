from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from study.models import Curs, Lesson, Subscription
from study.permissions import IsOwner, IsModerator
from study.serializers import CursSerializer, LessonSerializer, SubscriptionSerializer


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