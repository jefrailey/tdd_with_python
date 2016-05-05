# Standard Library
import unittest

# Third party
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)  # Implicit wait makes me sad

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # Moose, a cantankerous web scraper, heard about a cool new online todo
        # app. It goes to check out its homepage:
        self.browser.get('http://localhost:8000')

        # It notices the page title and header mention todo lists.
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # It is immediately invited to enter a todo item.

        # It types "Make up a better story" into a text box.

        # When it hits enter, the page updates, and now lists,
        # "1: Make up a better story", as an item in a todo list.

        # A textbox invites it to enter another item. It enters
        # "Tell the better story to a stranger".

        # The page updates again with both items on its list

        # It wonders if the site will remember the lsit. Then it notices that
        # the site generated a unique URL for it.

        # It visits that URL; the todo list is there.

        # Satisfied, it crawls away.

if __name__ == '__main__':
    unittest.main()
