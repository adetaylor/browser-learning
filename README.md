# Browser learning exercises

This project provides games for high school / secondary school computer scientists
to learn about how browsers work and what security bugs might exist in them.

See [Contributing](docs/contributing.md) to contribute.

## For teachers

See [For Teachers](docs/for-teachers.md), and [setup](docs/setup.md).

## For students

If your teacher has already run through the [setup instructions](docs/setup.md),
or you're comfortable doing them yourself, then proceed to the actual content
below.

## Part One: What's a browser and a server

* [Exercise 1a](docs/exercise1a.md): Use a real browser. Navigate to [wikipedia](https://en.wikipedia.org).
  View source. Find some things in the HTML.
* [Exercise 1b](docs/exercise1b.md): Use our mini Python browser. Go to the same place. Look in
  the code of our Python browser to see how it handles `b` and `a` tags.
* [Exercise 1c](docs/exercise1c.md): Run our mini Python web server. Create your own HTML file.
  See how the browser responds.

## Part Two: Building a browser

* [Exercise 2a](docs/exercise2a.md): Add support for italic text in the browser.
* [Exercise 2b](docs/exercise2b.md): Add support for `h1` or `font color` or similar.
* [Exercise 2a](docs/exercise2c.md): Add word wrap in the browser. (HARD!)
* [Exercise 2d](docs/exercise2d.md): Invent your own HTML tag. Add it to the browser and to some
  HTML pages in the server. See how it works end-to-end.

## Part Three: Encryption

* [Exercise 3a](docs/exercise3a.md): See the web traffic flowing between the mini browser and
  the mini server when using HTTP. See what happens when you try different
  URIs. See what happens when different types of error occur.
* [Exercise 3b](docs/exercise3b.md): Try the same with HTTPS.

## Part Four: Security bugs

* [Exercise 4a](docs/exercise4a.md): Find some security bugs hidden in the code of our mini
  browser.