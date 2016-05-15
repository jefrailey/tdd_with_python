This repository contains code and notes from my follow along reading of [Test Driven Development with Python](http://shop.oreilly.com/product/0636920029533.do) by Harry Percival. In following along with this book I hope to:

 - Practice rigid test first development
 - Understand and articulate which components should be unit tested and which should be functionally tested and if/when to overlap.
 - gain exposure to another developer's test and commit cadence
 - become more familiar with Django 1.8


# Notes
## The Basics of TDD and Django
### 1. Getting Django Set up Using a Functional Test
Write a test before writing any application code. Running this test and seeing fail in an expected fashion will help indicate that the test
is written correctly.
### 2. Extending Our Functional Test Using the unittest Module.
Use comments to write a story for an entire functional test. This allows
for the goal of the test to remain clear while the test and application
are initially written and modified. Consider scoping changes tightly
enough that `git commit -a` (-a -> all modified tracked files) can be
used.
### 3. Testing a Simple Home Page with Unit Tests
*Functional tests*: test the application from the outside--the user's perspective. These tests represent a user interacting with the
application to achieve a specific goal. Functional tests aid in the
creation of an application that affords the user a specific
functionality.
*Unit tests*: test the application from the programmers perspective.
These tests should cover (that is, each line of application code should
be executed by one or more unit tests, not that each line of code needs
its own unit test) each line of the application code to ensure
that the logic represented by the code is sound. Unit tests aid in
writing clean and bug free code.
The Test Driven Development loop is an iterative four step process:

1. Write a functional test that describes an interaction between the
user and the application. Assert that this test currently fails.
2. Think about how to structure application code to get the functional
test to pass. Write a unit test for the smallest conceivable group of application code that could be written to successfully execute the first
failing line in the functional test. Assert that this test currently
fails.
3. Write the smallest amount of application code possible to get the
new unit test to pass. Assert that the unit test passes and, if
applicable, that the functional test progresses further before failing.
4. Repeat until the functional test passes.

Django 1.8 maps the URL of a request to a view function via the
`reslove` function. This function compares the URL to the regular
expressions defined in the project and application `urls.py` modules.
The view function receives the request and returns an HTTP response.

Respond to test failures by **making the smallest possible change**
**required to correct the current test failure.**
### 4. What Are We Doing with All These Tests?
Test driven development acts as a scaffolding and safety net that
provides assurances of correctness regardless of complexity.
Test driven development is a discipline, which means it is an unnatural
activity that requires consistent repetition and adherence.
Unit tests are for testing:
 - Logic
 - Flow control
 - Configuration
Refactoring: Improving code without changing functionality.
### 5. Saving User Input
In a purist's view, a unit test does not rely on any external systems,
including a database. Tests that rely on external systems are called
integrated tests. Unit tests and integrated tests are both low level
tests that exemplify the programmer interacting with the application;
functional tests test the application from the user's perspective.
DJANGO: `<Model>.objects.create(<field>=<value>)` is a shortcut for
creating and saving new rows.
### 6. Getting to the Minimum Viable Site
DJANGO: `django.test.LiveServerTestCase` is a subclass of
`unittest.TestCase` that will automatically manage test database setup
and teardown. This provides better test isolation.
GIT: `git diff -M` take into account moved files when creating a diff.
HTML: The `action` attribute of the `form` tag indicates which URI to
submit the form to.
####Process for Incrementally Altering Design
1. Run the functional tests to establish the baseline functionality.
1. Adjust functional tests to test against the new design.
1. Run the functional tests and record the first failure.
1. Change the unit tests to have the same expectation as the
the line in the functional test that failed.
1. Run the unit tests and record the first failure.
1. Make the smallest change possible to the application code to fix the
current unit test failure.
1. Repeat the previous two steps until all the unit tests pass.
1. Verify application meet or exceed previous baseline functionality.
1. Refactor if necessary.