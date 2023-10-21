from rest_framework import serializers

from main.models import Course, Lesson, Payment, CourseSubscription
from main.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(field='video_url')]


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [UrlValidator(field='video_url')]

    def get_lessons_count(self, instance):
        if instance.lesson_set is not None:
            return instance.lesson_set.count()
        return 0

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        if user.is_authenticated:
            subscription = CourseSubscription.objects.filter(user=user, course=instance).exists()
            return subscription
        return False


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
