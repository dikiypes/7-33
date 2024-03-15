from rest_framework import viewsets, generics, permissions
from .models import Payment, User
from rest_framework.response import Response
from .serializers import PaymentSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django_filters.rest_framework import DjangoFilterBackend


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'email'


class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
        return Response(data)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.query_params.get('order_by')
        if order_by:
            queryset = queryset.order_by(order_by)

        return queryset
