# Exercise 1b: Using our own browser

* Do the same in our own browser, by running `python3 src/browser/browser.py`.
  (If you're using IDLE you can open the file from within IDLE and then run it.)
* Does it support:
  * **Bold** text
  * _Italic_ text
  * Hyperlinks
* Open up the browser source code (open the file `src/browser/browser.py`) -
  it's recommended to use Visual Studio Code. (Specifically, if you're using a Chromebook,
  choose File -> Open Folder, click browser-learning once, and click Open. You can then use
  the side panel to navigate to `src/browser/browser.py`). You can also open the file in
  IDLE instead.
  (Incidentally, `src` is short for "source code".)
* Find where it handles these tags. See which is missing.

## About reading code

This exercise is about _reading_ code, not writing it. It's a different skill!
Look for clues. See if you can piece together how the whole browser works,
by cross-referencing the way different bits of the code work with each other.
Use "find" (or equivalent options in Visual Studio Code or IDLE).

**Top tip**: try to understand how the whole thing roughly fits together
before worrying about the details. Skip over bits you don't understand.

Clues below! But get reading the code first, then come back to this.

## What's  up with...

### The editor

Top tip for reading code: make the window as big as possible.

### The overall structure

The program itself is near the bottom of the file. One of the first things
it does is create an object belonging to a `class` called `Browser` - see
below! It then tells the brower to do things.

### `class`

If your program had 1000 functions, you'd get lost. Large programs are
often organized into "classes". A "class" represents a type of _thing_ in
your program - called an _object_. It might be a physical object that appears on
the screen, such as an icon, or a non-tangible thing in the background
(like an image decoder or a score calculator).

Think of classes like nouns.

Objects have:
* A bunch of functions. One object can tell another object to do something -
  that will call one of its functions. Think of these as the verbs which
  act on the noun.
* Some data. Think of these things as facts about the object.

For instance, in Python:

```python
class Dinosaur:
  def __init__(self):
    self.number_of_legs = 0   # data belonging to each object in the class.
         # Although each dinosaur has a number of legs, they might be different
         # in different dinosaurs.
    self.tummy_fullness = 0

  def eat_something(self):  # other code can tell the dinosaur to eat something
    self.tummy_fullness = self.tummy_fullness + 1  # modify some data belonging
      # to this dinosaur
```

In this browser, we have exactly two classes: `Renderer` and `Browser`.
There's one object of the `Browser` class existing for the whole life of the
program. We create a new `Renderer` each time we visit a new page.

### `self`

Most of the functions in this browser code are functions belonging to classes
of objects - see `class`, above. `self` represents the current object.

### `browser.navigate()`

We have an object of the class `Browser` kept in a variable called `browser`.
This is calling one of the functions belonging to the `Browser` class.

### `self.canvas.create_text()` and stuff like that

The class we're in has some data called `canvas` which itself contains
another object, and we're calling one of the canvas' functions.

### `class Renderer(HTMLParser):`

Good question! That means that our class `Renderer` is a special type of
a different class called `HTMLParser` which happens to be provided by one
of the libraries we're using.
