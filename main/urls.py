from django.urls import path
from rest_framework.routers import DefaultRouter

from main.apps import MainConfig
from main.views import CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscribeToCourse, UnsubscribeFromCourse

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  # lessons
                  path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
                  path('lessons/create', LessonCreateAPIView.as_view(), name='lesson_create'),
                  path('lessons/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson_view'),
                  path('lessons/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lessons_update'),
                  path('lessons/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lessons_delete'),
                  # sub
                  path('subscribe/<int:course_id>/', SubscribeToCourse.as_view(), name='subscribe_to_course'),
                  path('unsubscribe/<int:course_id>/', UnsubscribeFromCourse.as_view(), name='unsubscribe_from_course'),
              ] + router.urls
