from django.http import HttpRequest
from django.contrib.auth.models import User
from django.utils import timezone
from .views import PostListView
from django.test import TestCase
from django.urls import reverse
from django.test import RequestFactory
from .views import search_results
from .models import Post


class Search_resultsTestCase(TestCase):
    def setUp(self):
        # Создание тестового пользователя
        user = User.objects.create_user(username='testuser', password='12345', email='test@example.com')

        # Создание тестовых постов
        for i in range(20):
            Post.objects.create(
                title=f'Test Post {i}',
                slug=f'test-post-{i}',
                author=user,
                preview='Preview text',
                original_author=f'Original Author {i}',
                body='Body text',
                status='published',
                publish=timezone.now(),
            )
        self.factory = RequestFactory()

    def test_post_list_view(self):
        # Создание запроса GET к представлению PostListView
        request = HttpRequest()
        request.method = 'GET'
        request.user = User.objects.get(username='testuser')
        response = PostListView.as_view()(request)

        # Проверка, что получен ответ с кодом 200
        self.assertEqual(response.status_code, 200)

    def test_search_results(self):
        # Создание запроса с параметром query
        request = self.factory.get(reverse('filmblog:search_results'), {'query': 'Test'})
        response = search_results(request)
        # Проверка, что запрос вернул код 200
        self.assertEqual(response.status_code, 200)
        # Проверка, что результаты содержат только записи, где в заголовке есть слово "Test (номер)"
        self.assertIn("Test Post 1", response.content.decode())
        self.assertIn("Test Post 11", response.content.decode())
        self.assertIn("Test Post 12", response.content.decode())

    def test_empty_query(self):
        # Создание запроса без параметра query
        request = self.factory.get(reverse('filmblog:search_results'))
        response = search_results(request)
        # Проверка, что запрос вернул код 200
        self.assertEqual(response.status_code, 200)
        # Проверка, что результаты пусты
        self.assertIn("No search query provided.", response.content.decode())


class PostListViewTestCase(TestCase):
    def test_post_list_View(self):
        response = self.client.get(reverse("filmblog:index"))
        self.assertContains(response, "Home")