from rest_framework import viewsets, generics, status, permissions
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from .paginators import CustomPaginator
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsModerator | IsOwner | IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Moderators').exists():
                return Course.objects.all()
            else:
                return Course.objects.filter(owner=self.request.user)
        else:
            return Course.objects.none()


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner | IsAuthenticated]
    pagination_class = CustomPaginator

    def get_queryset(self):
        if self.request.user.is_authenticated:
            # Если пользователь модератор, возвращаем все уроки
            if self.request.user.groups.filter(name='Moderators').exists():
                return Lesson.objects.all()

            # Если пользователь не модератор, возвращаем только уроки, созданные им
            return Lesson.objects.filter(owner=self.request.user)
        else:
            return Lesson.objects.none()

# просмотр деталей одного объекта GET


class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner | IsAuthenticated]
    lookup_field = 'pk'

# удаление объекта


class LessonDestroyView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner | IsAuthenticated]
    lookup_field = 'pk'

# обновление объекта


class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner | IsAuthenticated]
    lookup_field = 'pk'


class SubscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)
        permission_classes = [IsAuthenticated]

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Subscription removed'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Subscription added'

        return Response({"message": message})
