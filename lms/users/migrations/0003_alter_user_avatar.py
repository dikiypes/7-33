# Generated by Django 5.0.2 on 2024-03-05 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_payment_paid_course_payment_paid_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to='media/avatars/'),
        ),
    ]
