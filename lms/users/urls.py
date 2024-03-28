from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, UserListView, UserDetailView, RegistrationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import PaymentRetrieveView, PaymentIntentCreateView, PaymentMethodCreateView, PaymentIntentConfirmView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('payments/<int:pk>/', PaymentRetrieveView.as_view(), name='payment_detail'),
    path('payments/create/', PaymentIntentCreateView.as_view(), name='payment_create'),
    path('payments/method/create', PaymentMethodCreateView.as_view(), name='payment_method_create'),
    path('payments/confirm/', PaymentIntentConfirmView.as_view(), name='payments_confirm'),
]
