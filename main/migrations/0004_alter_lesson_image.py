# Generated by Django 4.2.6 on 2023-10-16 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='lessons/', verbose_name='картинка'),
        ),
    ]
