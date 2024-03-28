from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='media/course_previews/')
    description = models.TextField()
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=50000, verbose_name='Стоимость курса')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    @classmethod
    def get_all_courses(cls):
        """
        Возвращает список всех курсов
        """
        return cls.objects.all()

    @classmethod
    def get_by_id(cls, course_id: int):
        """
        Возвращает курс по его идентификатору
        """
        try:
            return cls.objects.get(id=course_id)
        except cls.DoesNotExist:
            return None


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='media/lesson_previews/')
    video_link = models.URLField()
    course = models.ForeignKey('courses.Course', related_name='lessons', on_delete=models.CASCADE)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    link = models.CharField(max_length=255)


class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
