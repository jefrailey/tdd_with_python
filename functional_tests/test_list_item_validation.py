# Superlists
from .base import (
    FunctionalTest,
)


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Boar needs a new todo list. So he visits our site. He presses
        # enter before typing anything into the input box.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        # The home page refreshes and displays an error message stating
        # that list items may not be blank.
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item.")

        # Boar tries again with some text. The application accepts the
        # list item.
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        # Boar liked the error message so much that he gets the site
        # to display it again by intentionally submitting an empty list
        # item.
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        # The warning re-appears.
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item.")

        # He can correct it by filling in some text.
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
