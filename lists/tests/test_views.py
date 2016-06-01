from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.views import home_page
from lists.models import (
    Item,
    List,
)


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('lists/home.html')
        self.assertTrue(response.content.decode(), expected_html)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{list_.id}/'.format_map(locals()))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        for number in range(1, 3, 1):
            Item.objects.create(text='itemey {}'.format(number),
                                list=correct_list)
        other_list = List.objects.create()
        for number in range(1, 3, 1):
            Item.objects.create(text='other list item {}'.format(number),
                                list=other_list)

        response = self.client.get(
            '/lists/{correct_list.id}/'.format_map(locals())
        )

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        List.objects.create()
        correct_list = List.objects.create()
        uri = '/lists/{correct_list.id}/'.format_map(locals())
        response = self.client.get(uri)
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        uri = '/lists/{correct_list.id}/'.format_map(locals())

        response = self.client.post(uri, data={'item_text': 'new item text'})

        self.assertEqual(Item.objects.count(), 1)
        items = Item.objects.filter(list=correct_list)
        self.assertEqual(items.count(), 1)
        new_item = items.first()
        self.assertEqual(new_item.text, 'new item text')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        uri = '/lists/{correct_list.id}/'.format_map(locals())

        response = self.client.post(uri, data={'item_text': 'new item text'})
        self.assertRedirects(response,
                             '/lists/{correct_list.id}/'.format_map(locals()))


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'do stuff'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'do stuff')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'do stuff'}
        )
        list_ = List.objects.first()
        self.assertRedirects(response,
                             '/lists/{list_.id}/'.format_map(locals()))

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
        expected_error = escape("You can't have an empty list item.")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_are_not_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
