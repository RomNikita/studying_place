from datetime import timezone

from celery import shared_task
from django.core.mail import send_mail

from main.models import Course, CourseSubscription
from users.models import User


@shared_task
def send_mail_for_subs(course_id):

    course = Course.objects.get(id=course_id)

    subscribed_users = CourseSubscription.objects.filter(course=course).values_list('user__email', flat=True)

    for email in subscribed_users:
        send_mail('Обновление курса!',
                  f'Твой курс {course.name}, на который ты подписан получил обновление. Перейди на сайт и посмотри.',
                  'noreplyskypro9@gmail.com',
                  [email])


def check_last_login():
    time = timezone.now() - timezone.timedelta(days=30)

    inactive_users = User.objects.filter(last_login__lt=time, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()

