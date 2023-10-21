from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from main.models import Lesson, CourseSubscription, Course
from users.models import User


class LessonCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='testuser@example.com',
            password='testpassword'
        )
        self.lesson_data = {
            'name': 'Test Lesson',
            'description': 'Test Lesson',
            'video_url': 'https://youtube.com'
        }
        self.lesson = Lesson.objects.create(
            name='Lesson',
            description='Lesson',
            owner=self.user,
            video_url='https://youtube.com'
        )

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/lessons/create', self.lesson_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lesson.objects.filter(name='Test Lesson').count(), 1)

    def test_create_lesson_invalid_url(self):
        self.client.force_authenticate(user=self.user)
        invalid_data = {
            'name': 'Invalid Lesson',
            'description': 'Invalid Lesson Description',
            'video_url': 'https://example.com'
        }
        response = self.client.post('/lessons/create', invalid_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_read_lesson_list(self):
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, 200)
        data = response.data

    def test_read_lesson_detail(self):
        response = self.client.get(f'/lessons/{self.lesson.id}')
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['name'], 'Lesson')
        self.assertEqual(data['description'], 'Lesson')

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        updated_data = {
            'name': 'Updated Lesson',
            'description': 'Updated Lesson Description',
            'video_url': 'https://youtube.com'
        }
        response = self.client.put(f'/lessons/update/{self.lesson.id}', updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Updated Lesson')
        self.assertEqual(self.lesson.description, 'Updated Lesson Description')

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/lessons/delete/{self.lesson.id}')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class CourseSubscriptionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email='testuser@example.com',
            password='testpassword'
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Course Description',
            owner=self.user
        )
        self.subscription = CourseSubscription.objects.create(
            user=self.user,
            course=self.course
        )

    def test_subscribe_to_course_created(self):
        new_user = get_user_model().objects.create(
            email='testuser2@example.com',
            password='testpassword')

        self.client.force_authenticate(user=new_user)
        response = self.client.post(f'/subscribe/{self.course.id}/')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscribe_to_course_existing(self):

        new_user = get_user_model().objects.create(
            email='testuser1@example.com',
            password='testpassword')
        new_course = Course.objects.create(
            name='Test Course1',
            description='Test Course Description1',
            owner=new_user
        )

        CourseSubscription.objects.create(user=new_user, course=new_course)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/subscribe/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Вы уже подписаны на этот курс.")

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/unsubscribe/{self.course.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())

    def test_course_serialization(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/course/{self.course.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['id'], self.course.id)
        self.assertEqual(data['name'], self.course.name)
        self.assertEqual(data['description'], self.course.description)
        self.assertEqual(data['is_subscribed'], True)

    def test_course_unsubscribed_serialization(self):
        self.client.force_authenticate(user=self.user)
        subscription = CourseSubscription.objects.get(user=self.user, course=self.course)
        subscription.delete()
        response = self.client.get(f'/course/{self.course.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['id'], self.course.id)
        self.assertEqual(data['name'], self.course.name)
        self.assertEqual(data['description'], self.course.description)
        self.assertEqual(data['is_subscribed'], False)

