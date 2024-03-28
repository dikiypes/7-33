from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, SubscriptionView
from .views import LessonCreateView, LessonDetailView, LessonDestroyView, LessonUpdateView, LessonListView


router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/delete/', LessonDestroyView.as_view(), name='lesson-delete'),
    path('lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson-update'),
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
]
