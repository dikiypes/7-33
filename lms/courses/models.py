from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='previews/')
    description = models.TextField()
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/')
    video_link = models.URLField()
    course = models.ForeignKey('courses.Course', related_name='lessons', on_delete=models.CASCADE)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    link = models.CharField(max_length=255)


class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
