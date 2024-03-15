from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses.views import CourseViewSet
from users.views import PaymentViewSet


router = DefaultRouter()
router.register(r'payments', PaymentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/courses/', include('courses.urls')),
    path('api/users/', include('users.urls')),
]
