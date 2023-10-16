# Generated by Django 4.2.6 on 2023-10-15 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_course_lessons'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True, verbose_name='дата платежа')),
                ('amount', models.IntegerField(verbose_name='сумма оплаты')),
                ('method', models.CharField(max_length=30, verbose_name='способ оплаты')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.course', verbose_name='оплата курса')),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.lesson', verbose_name='оплата урока')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'платеж',
                'verbose_name_plural': 'платежи',
            },
        ),
    ]