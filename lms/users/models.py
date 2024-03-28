from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# from courses.models import Course, Lesson
from django.contrib.auth.models import BaseUserManager

NULLABLE = {'blank': True, 'null': True}


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set_permissions')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='media/avatars/')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class Payment(models.Model):
    """Модель, описывающая платеж"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name='Пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, **NULLABLE, verbose_name='Оплаченный курс')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='ID метода платежа Stripe')
    payment_intent_id = models.CharField(max_length=255, blank=True, null=True,
                                         verbose_name='ID намерения платежа Stripe')
    status = models.CharField(max_length=50, blank=True, null=True, verbose_name='Stripe cтатус платежа')
    is_confirmed = models.BooleanField(default=False, verbose_name='Подтвержден')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        db_table = 'payments'

    def __str__(self):
        return f"{self.user} - {self.payment_date}"

    @classmethod
    def get_all_payments(cls):
        """
        Возвращает список всех платежей
        """
        return cls.objects.all()

    @classmethod
    def get_by_payment_intent_id(cls, payment_intent_id: str):
        """
        Возвращает платеж по идентификатору намерения платежа
        """
        try:
            return cls.objects.get(payment_intent_id=payment_intent_id)
        except cls.DoesNotExist:
            return None

    def confirm_payment(self):
        """
        Делает платеж подтвержденным.
        """
        self.is_confirmed = True
        self.save()
