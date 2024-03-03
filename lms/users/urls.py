from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, UserListView, UserDetailView, RegistrationView, LoginView


router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
]
