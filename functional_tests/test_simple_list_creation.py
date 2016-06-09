# Third party
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Superlists
from .base import (
    FunctionalTest,
)


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):

        # Moose, a cantankerous web scraper, heard about a cool new online todo
        # app. It goes to check out its homepage:
        self.browser.get(self.server_url)

        # It notices the page title and header mention todo lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # It is immediately invited to enter a todo item.
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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
