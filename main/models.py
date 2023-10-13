from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    image = models.ImageField(upload_to='course/', verbose_name='картинка')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='lessons/', verbose_name='картинка')
    video_url = models.URLField(verbose_name='ссылка на видео')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'