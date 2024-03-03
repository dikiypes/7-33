from rest_framework import viewsets, generics, permissions
from .models import Payment, User
from rest_framework.response import Response
from .serializers import PaymentSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
        return Response(data)


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.all()
        order_by = self.request.query_params.get('order_by')
        course_id = self.request.query_params.get('course_id')
        lesson_id = self.request.query_params.get('lesson_id')
        payment_method = self.request.query_params.get('payment_method')

        if order_by:
            queryset = queryset.order_by(order_by)
        if course_id:
            queryset = queryset.filter(paid_course_id=course_id)
        if lesson_id:
            queryset = queryset.filter(paid_lesson_id=lesson_id)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)

        return queryset
