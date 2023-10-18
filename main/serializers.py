from rest_framework import serializers

from main.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, instance):
        if instance.lesson_set is not None:
            return instance.lesson_set.count()
        return 0


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
