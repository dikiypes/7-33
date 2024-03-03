from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Course, Lesson, Subscription
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from django.shortcuts import get_object_or_404


# class CourseCreationTest(APITestCase):
#     def setUp(self):
#         # Создаем тестового пользователя
#         self.user = get_user_model().objects.create_user(email='bob@gmail.com', password='1234')
#         # Получаем JWT-токен для пользователя
#         self.access_token = self.get_access_token('bob@gmail.com', '1234')

#     def get_access_token(self, email, password):
#         # Запрос на получение JWT-токена
#         token_url = reverse('token_obtain_pair')  # Предполагаем, что у вас есть URL с именем 'token_obtain_pair'
#         response = self.client.post(token_url, {'email': email, 'password': password})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         return response.data['access']

#     def create_image(self, name='town2.png', image_type='png', size=(50, 50)):
#         """
#         Create a test image.
#         """
#         data = BytesIO()
#         Image.new('RGB', size).save(data, image_type)
#         data.seek(0)
#         return InMemoryUploadedFile(data, 'ImageField', name, 'image/png', data.__sizeof__(), None)

#     def test_create_course(self):
#         # Данные для создания курса
#         course_data = {
#             'title': 'Test Course',
#             'description': 'Course Description',
#             'owner': self.user.id,
#             'preview': self.create_image(),
#         }

#         # Заголовок с JWT-токеном для аутентификации
#         headers = {'HTTP_AUTHORIZATION': f'Bearer {str(self.access_token)}'}

#         # Создание курса
#         response = self.client.post('/api/courses/courses/', data=course_data, format='multipart', **headers)
#         print('result:', response.content)

#         # Проверки
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Course.objects.count(), 1)
#         self.assertEqual(Course.objects.get().title, 'Test Course')


class CourseLessonSubscriptionTest(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = get_user_model().objects.create_user(email='bob_test@gmail.com', password='1234', phone='+821425', city='M', avatar=self.create_image())
        # Получаем JWT-токен для пользователя
        self.access_token = self.get_access_token('bob_test@gmail.com', '1234')
        # Создаем тестовый курс
        self.course = Course.objects.create(title='Test Course', description='Course Description', owner=self.user, preview=self.create_image())
        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Lesson Description',
            owner=self.user,
            course=self.course,
            preview=self.create_image(),
            video_link='https://www.youtube.com/watch?v=V-YVDLoi5Ko&pp=ygUGcHl0aG9u',
            link='test'

        )

    def get_access_token(self, email, password):
        # Запрос на получение JWT-токена
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, {'email': email, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def create_image(self, name='town2.png', image_type='png', size=(50, 50)):
        """
        Create a test image.
        """
        data = BytesIO()
        Image.new('RGB', size).save(data, image_type)
        data.seek(0)
        return InMemoryUploadedFile(data, 'ImageField', name, 'image/png', data.__sizeof__(), None)

    def test_create_lesson(self):
        # Создание урока
        lesson_data = {
            'title': 'New Lesson',
            'description': 'Lesson Description',
            'owner': self.user.id,
            'course': self.course.id,
            'preview': self.create_image(),
            'video_link': 'https://www.youtube.com/watch?v=V-YVDLoi5Ko&pp=ygUGcHl0aG9u',
            'link': 'https://www.youtube.com/watch?v=V-YVDLoi5Ko&pp=ygUGcHl0aG9u'
        }

        headers = {'HTTP_AUTHORIZATION': f'Bearer {str(self.access_token)}'}
        response = self.client.post('/api/courses/lessons/create/', data=lesson_data, format='multipart', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)  # Учитывайте, что у вас уже есть один урок в setUp

    def test_update_lesson(self):
        # Обновление урока
        updated_title = 'Updated Lesson Title'
        lesson_data = {
            'title': updated_title,
            'description': 'Updated Lesson Description',
            'owner': self.user.id,
            'course': self.course.id,
            'preview': self.create_image(),
            'video_link': 'https://www.youtube.com/watch?v=V-YVDLoi5Ko&pp=ygUGcHl0aG9u',
            'link': 'https://www.youtube.com/watch?v=V-YVDLoi5Ko&pp=ygUGcHl0aG9u'
        }

        headers = {'HTTP_AUTHORIZATION': f'Bearer {str(self.access_token)}'}
        response = self.client.put(f'/api/courses/lessons/{self.lesson.id}/update/', data=lesson_data, format='multipart', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, updated_title)

    def test_delete_lesson(self):
        # Удаление урока
        headers = {'HTTP_AUTHORIZATION': f'Bearer {str(self.access_token)}'}
        response = self.client.delete(f'/api/courses/lessons/{self.lesson.id}/delete/', **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_subscribe_to_course_updates(self):
        # Подписка на обновления курса
        subscription_data = {
            'course_id': self.course.id,
        }

        headers = {'HTTP_AUTHORIZATION': f'Bearer {str(self.access_token)}'}
        response = self.client.post('/api/courses/subscribe/', data=subscription_data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(Subscription.objects.get().user, self.user)
