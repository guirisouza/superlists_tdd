from django.test import TestCase
from .models import ItemModel
from django.urls import resolve
from .views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

class HomePageTest(TestCase):


    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

    def test_saving_and_retrieving_items(self):
        first_item = ItemModel()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = ItemModel()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = ItemModel.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')