from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# from courses.models import Course, Lesson
from django.contrib.auth.models import BaseUserManager


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


class Payment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    payment_date = models.DateField()
    paid_course = models.ForeignKey('courses.Course', null=True, blank=True, on_delete=models.CASCADE)
    paid_lesson = models.ForeignKey('courses.Lesson', null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Cash'), ('transfer', 'Transfer')])


class User(AbstractUser):
    username = None
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set_permissions')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
