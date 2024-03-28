# Generated by Django 5.0.2 on 2024-03-25 18:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_cost_course_updated_at'),
        ('users', '0003_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Платеж', 'verbose_name_plural': 'Платежи'},
        ),
        migrations.RemoveField(
            model_name='payment',
            name='paid_lesson',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='payment',
            name='is_confirmed',
            field=models.BooleanField(default=False, verbose_name='Подтвержден'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_intent_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ID намерения платежа Stripe'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_method_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ID метода платежа Stripe'),
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Stripe cтатус платежа'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма оплаты'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paid_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.course', verbose_name='Оплаченный курс'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterModelTable(
            name='payment',
            table='payments',
        ),
    ]
