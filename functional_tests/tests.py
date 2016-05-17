# Standard library
import sys

# Third party
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):  # noqa
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

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
        self.browser.get(self.server_url)

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

        # When it hits enter, the page redirects to a unique URL for the
        # list, which displays, "1: Make up a better story", as an item
        # in a todo list.
        inputbox.send_keys(Keys.ENTER)

        moose_list_url = self.browser.current_url
        self.assertRegex(moose_list_url, '/lists/.+')
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

        # Now a new user, Bear, visits the site.

        ## Double hash indicates "meta-comments," which explain how
        ## the test is working and why.
        ## Use a new browser session to make sure that no information
        ## from Moose leaks to Bear via cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Bear visits the home page; he does not see Moose's list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Make up a better story', page_text)
        self.assertNotIn('2: Tell the better story to a stranger', page_text)

        # Bear starts a new list by entering an item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy beer')
        inputbox.send_keys(Keys.ENTER)

        # Bear's list gets its own URL
        bears_list_url = self.browser.current_url
        self.assertRegex(bears_list_url, '/lists/.+')
        self.assertNotEqual(bears_list_url, moose_list_url)

        # Again, no Moose in Bear
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Make up a better story', page_text)
        self.assertNotIn('2: Tell the better story to a stranger', page_text)
        self.assertIn('Buy beer', page_text)

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered:
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # She starts a new list and sees the input is nicely centered
        # there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )
