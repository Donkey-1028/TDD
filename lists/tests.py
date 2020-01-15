from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

import re
from .views import home_page

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

        self.assertIn('신규 작업 아이템', response.content.decode())
        expected_html = self.remove_csrftoken(
            render_to_string('home.html', {'new_item_text': '신규 작업 아이템'})
        )
        removed_decode = self.remove_csrftoken(
            response.content.decode()
        )
        self.assertEqual(removed_decode, expected_html)
