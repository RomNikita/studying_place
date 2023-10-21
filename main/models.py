from django.db import models
from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    image = models.ImageField(upload_to='course/', verbose_name='картинка', null=True, blank=True)
    description = models.TextField(verbose_name='описание')
    video_url = models.URLField(verbose_name='ссылка на видео', null=True, blank=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='владелец', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='lessons/', verbose_name='картинка', null=True, blank=True)
    video_url = models.URLField(verbose_name='ссылка на видео', null=True, blank=True)
    course = models.ForeignKey('Course', models.CASCADE, null=True, blank=True, verbose_name='курс')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='владелец', null=True, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, verbose_name='пользователь')
    date = models.DateField(auto_now=True, verbose_name='дата платежа')
    course = models.ForeignKey('Course', on_delete=models.PROTECT, null=True, blank=True, verbose_name='оплата курса')
    lesson = models.ForeignKey('Lesson', on_delete=models.PROTECT, null=True, blank=True, verbose_name='оплата урока')
    amount = models.IntegerField(verbose_name='сумма оплаты')
    method = models.CharField(max_length=30, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.user} {self.date} оплатил {self.lesson if self.lesson else self.course} {self.amount} руб.({self.method})'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class CourseSubscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='курс')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        unique_together = ('user', 'course')
