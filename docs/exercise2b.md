# Exercise 2b: Add support for other tags

Do some [research on standard HTML tags](https://www.w3schools.com/tags/), and add support for another one of your choice.

* (Hopefully) easy choices: anything that just alters the appearance of the text, e.g. `h1`-`h6`, `font color`.
* Slightly harder: support the horizontal rule, `hr`
* Medium choices: change the title bar of the browser window when it finds a `title` tag. (Hint: this will
  probably involve adding another function to the `Browser` class which you'll call from the `Renderer` class).
* Very hard choice: add support for `img src` which will include pictures on the page.
  This will likely take several hours even if you're a Python wizard. You'd need to do this:
  1. Get an absolute URI to the image (see the existing code in `link_clicked` which does the same)
  2. Download the image file using [`requests`](https://pypi.org/project/requests/), perhaps into a
     [`NamedTemporaryFile`](https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile)
  3. Use `create_image` on the `canvas` to draw it.
* Another very hard choice: the `blink` tag. This will require you to set a timer to re-draw the page
  periodically.
* Impossible choice: anything to do with page layout. Don't attempt to support tables, frames or anything
  fancy like that. It would take hundreds of hours - it's all very complicated. Don't even try.

Good choices might be h1-h6 or `font color`.

