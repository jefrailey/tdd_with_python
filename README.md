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
enough that `git -a` (-a -> all modified tracked files) can be used.
### 3. Testing a Simple Home Page with Unit Tests