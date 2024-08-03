from django.test import TestCase

# Create your tests here.

# news/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import News

class NewsTests(APITestCase):
    def setUp(self):
        self.new = News.objects.create(title="Test Title", text="Test text", tags="Test tag", source = "Test source", category = "OTHER" )
        self.list_url = reverse('new-list')


    def test_get_news(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_news_by_tags(self):
        response = self.client.get(self.list_url, {'search': 'Test tag'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_new(self):
        data = {'title': 'New Title', 'text': 'New text', 'tags': 'New tag', 'source': 'New source', 'category': 'OTHER'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 2)