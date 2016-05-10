# Standard Library
import unittest

# Third party
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)  # Implicit wait makes me sad

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):

        # Moose, a cantankerous web scraper, heard about a cool new online todo
        # app. It goes to check out its homepage:
        self.browser.get('http://localhost:8000')

        # It notices the page title and header mention todo lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # It is immediately invited to enter a todo item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # It types "Make up a better story" into a text box.
        inputbox.send_keys('Make up a better story')

        # When it hits enter, the page updates, and now lists,
        # "1: Make up a better story", as an item in a todo list.
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Make up a better story')

        # A textbox invites it to enter another item. It enters
        # "Tell the better story to a stranger".
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Tell the better story to a stranger')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again with both items on its list
        self.check_for_row_in_list_table('1: Make up a better story')
        self.check_for_row_in_list_table(
            '2: Tell the better story to a stranger'
        )

        # It wonders if the site will remember the lsit. Then it notices that
        # the site generated a unique URL for it.
        self.fail('Finish the test!')

        # It visits that URL; the todo list is there.

        # Satisfied, it crawls away.

if __name__ == '__main__':
    unittest.main()
