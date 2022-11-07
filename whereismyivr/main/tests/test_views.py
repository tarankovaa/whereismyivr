from django.test import TestCase


class ViewsTestCase(TestCase):
    # страница index открывается правильно
    def test_index_loads_properly(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # страницы типа search/<param> открываются правильно
    def test_search_loads_properly(self):
        response = self.client.get('/search/customer')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/search/consultant')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/search/performer')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/search/partner')
        self.assertEqual(response.status_code, 200)
