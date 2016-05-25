# Third party
from django.test import TestCase

# Lists
from lists.models import (
    Item,
    List,
)


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
