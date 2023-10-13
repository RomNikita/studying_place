from django.urls import path
from rest_framework.routers import DefaultRouter

from main.apps import MainConfig
from main.views import CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
                  path('lessons/create', LessonCreateAPIView.as_view(), name='lesson_create'),
                  path('lessons/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson_view'),
                  path('lessons/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lessons_update'),
                  path('lessons/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lessons_delete'),
              ] + router.urls
