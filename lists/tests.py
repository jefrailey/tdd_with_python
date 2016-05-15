from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

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


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        new_list = List()
        new_list.save()
        item_texts = ['The first (ever) list item', 'Item the second']
        for text in item_texts:
            Item.objects.create(text=text, list=new_list)

        saved_list = List.objects.first()
        self.assertEqual(saved_list, new_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item, second_saved_item = saved_items
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, new_list)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, new_list)


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


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        uri = '/lists/{correct_list.id}/add-item'.format_map(locals())

        response = self.client.post(uri, data={'item_text': 'new item text'})

        self.assertEqual(Item.objects.count(), 1)
        items = Item.objects.filter(list=correct_list)
        self.assertEqual(items.count(), 1)
        new_item = items.first()
        self.assertEqual(new_item.text, 'new item text')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        uri = '/lists/{correct_list.id}/add-item'.format_map(locals())

        response = self.client.post(uri, data={'item_text': 'new item text'})
        self.assertRedirects(response,
                             '/lists/{correct_list.id}/'.format_map(locals()))
