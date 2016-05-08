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
