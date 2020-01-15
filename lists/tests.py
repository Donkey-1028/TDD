from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

import re
from .views import home_page
from .models import Item

# Create your tests here.


class HomePageTest(TestCase):

    def remove_csrftoken(self, objects):
        """
        csrf_token 값이 다르기 때문에 테스트 안되는것을 막기 위해
        토큰 삭제를 하는 함수.
        """
        csrf_token = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_token, '', objects)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = self.remove_csrftoken(render_to_string('home.html', request=request))
        response_decode = self.remove_csrftoken(response.content.decode())

        self.assertEqual(response_decode, expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first().text
        self.assertEqual(new_item, '신규 작업 아이템')

        """self.assertIn('신규 작업 아이템', response.content.decode())
        expected_html = self.remove_csrftoken(
            render_to_string('home.html', {'new_item_text': '신규 작업 아이템'})
        )
        removed_decode = self.remove_csrftoken(
            response.content.decode()
        )
        self.assertEqual(removed_decode, expected_html)"""
    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_display_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = '첫 번째 아이템'
        first_item.save()

        second_item = Item()
        second_item.text = '두 번째 아이템'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '첫 번째 아이템')
        self.assertEqual(second_saved_item.text, '두 번째 아이템')
