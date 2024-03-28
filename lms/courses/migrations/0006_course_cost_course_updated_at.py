# Generated by Django 5.0.2 on 2024-03-25 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_owner_lesson_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=50000, max_digits=10, verbose_name='Стоимость курса'),
        ),
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Время обновления'),
        ),
    ]
