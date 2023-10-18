from rest_framework import viewsets, generics
from rest_framework.response import Response

from main.filters import PaymentFilter
from main.models import Course, Lesson, Payment
from main.permissions import IsModerator, CanChangeCourse, CannotCreateCourse, CannotDeleteCourse, IsOwner
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsOwner]

    def get_permissions(self):
        if self.request.user.is_authenticated:
            if IsModerator().has_permission(self.request, self):
                return [CanChangeCourse(), CannotCreateCourse(), CannotDeleteCourse()]
        return [CanChangeCourse()]

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
        return [CanChangeCourse()]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.is_authenticated:
            if IsModerator().has_permission(self.request, self):
                return [CanChangeCourse(), CannotCreateCourse(), CannotDeleteCourse()]
        return [CanChangeCourse()]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.is_authenticated:
            if IsModerator().has_permission(self.request, self):
                return [CanChangeCourse(), CannotCreateCourse(), CannotDeleteCourse()]
        return [CanChangeCourse()]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.is_authenticated:
            if IsModerator().has_permission(self.request, self):
                return [CanChangeCourse(), CannotCreateCourse(), CannotDeleteCourse()]
        return [CanChangeCourse()]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.is_authenticated:
            if IsModerator().has_permission(self.request, self):
                return [CanChangeCourse(), CannotCreateCourse(), CannotDeleteCourse()]
        return [CanChangeCourse()]


# payment

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_class = PaymentFilter
    ordering_fields = ['date']
