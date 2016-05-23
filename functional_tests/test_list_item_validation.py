# Superlists
from .base import (
    FunctionalTest,
)


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list(self):
        # Boar needs a new todo list. So he visits our site. He presses
        # enter before typing anything into the input box.

        # The home page refreshes and displays an error message stating
        # that list items may not be blank.

        # Boar tries again with some text. The application accepts the
        # list item.

        # The warning re-appears.

        # Boar liked the error message so much that he gets the site
        # to display it again by intentionally submitting an empty list
        # item.

        # He can correct it by filling in some text.
        self.fail('write me!')
