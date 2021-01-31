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
        self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(ItemModel.objects.count(), 1)
        new_item = ItemModel.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

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

    def test_only_save_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(ItemModel.objects.count(), 0)

    def test_displays_all_list_items(self):
        ItemModel.objects.create(text='Itemey 1')
        ItemModel.objects.create(text='Itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())