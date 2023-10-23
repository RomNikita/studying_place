from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Course, Lesson, Payment, CourseSubscription
from main.paginators import MyPaginator
from main.permissions import IsModerator, CanChangeCourse, CannotCreateCourse, CannotDeleteCourse, IsOwner
from main.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsOwner]
    pagination_class = MyPaginator

    def get_permissions(self):
        if self.request.user.is_authenticated:
            if IsModerator().has_permission(self.request, self):
                return [CanChangeCourse(), CannotCreateCourse(), CannotDeleteCourse()]
        return []

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]

    def get_permissions(self):
        if self.request.user.is_authenticated:
            if IsModerator().has_permission(self.request, self):
                return [CanChangeCourse(), CannotCreateCourse(), CannotDeleteCourse()]
        return []

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MyPaginator

    def get_permissions(self):
        if self.request.user.is_authenticated:
            if IsModerator().has_permission(self.request, self):
                return [CanChangeCourse(), CannotCreateCourse(), CannotDeleteCourse()]
        return []


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.is_authenticated:
            if IsModerator().has_permission(self.request, self):
                return [CanChangeCourse(), CannotCreateCourse(), CannotDeleteCourse()]
        return []


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.is_authenticated:
            if IsModerator().has_permission(self.request, self):
                return [CanChangeCourse(), CannotCreateCourse(), CannotDeleteCourse()]
        return []


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.is_authenticated:
            if IsModerator().has_permission(self.request, self):
                return [CanChangeCourse(), CannotCreateCourse(), CannotDeleteCourse()]
        return []


# subscription

class SubscribeToCourse(APIView):
    def post(self, request, course_id):
        user = request.user
        course = Course.objects.get(pk=course_id)
        subscription, created = CourseSubscription.objects.get_or_create(user=user, course=course)
        if created:
            return Response({"message": "Подписка успешно установлена."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Вы уже подписаны на этот курс."}, status=status.HTTP_400_BAD_REQUEST)


class UnsubscribeFromCourse(APIView):
    def post(self, request, course_id):
        user = request.user
        course = Course.objects.get(pk=course_id)
        try:
            subscription = CourseSubscription.objects.get(user=user, course=course)
            subscription.delete()
            return Response({"message": "Подписка успешно удалена."}, status=status.HTTP_204_NO_CONTENT)
        except CourseSubscription.DoesNotExist:
            return Response({"message": "Вы не были подписаны на этот курс."}, status=status.HTTP_400_BAD_REQUEST)
