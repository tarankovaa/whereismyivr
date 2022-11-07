from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Card


class CardTestCase(TestCase):
    # создание объектов для тестовой БД
    def setUp(self):
        user1 = User.objects.create(username="test1")
        user2 = User.objects.create(username="test2")
        Card.objects.create(title="Test 1", user=user1, field_of_card="design", customer=True, partner=True,
                            product_image="Test 1")
        Card.objects.create(title="Test 2", user=user2, field_of_card="marketing", consultant=True,
                            product_image="Test 2")

    # корректность возвращаемых требуемых должностей
    def test_get_search_for(self):
        card1 = Card.objects.get(title="Test 1")
        card2 = Card.objects.get(title="Test 2")
        self.assertEqual(card1.get_search_for(), ["Заказчик", "Напарник"])
        self.assertEqual(card2.get_search_for(), ["Консультант"])

    # корректность возвращаемой области проекта/исследования
    def test_get_field_of_card(self):
        card1 = Card.objects.get(title="Test 1")
        card2 = Card.objects.get(title="Test 2")
        self.assertEqual(card1.get_field_of_card(), "Дизайн")
        self.assertEqual(card2.get_field_of_card(), "Маркетинг")
