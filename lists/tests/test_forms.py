# Third party
from django.test import TestCase

# Lists
from lists.forms import (
    EMPTY_ITEM_ERROR,
    ItemForm,
)


class ItemFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css_classes(self):

        form = ItemForm()
        form_html = form.as_p()
        self.assertIn('placeholder="Enter a to-do item"', form_html)
        self.assertIn('class="form-control input-lg"', form_html)

    def test_form_validation_for_blank_items(self):

        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
