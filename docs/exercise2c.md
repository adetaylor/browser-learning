# Exercise 2c: word wrap!

You might notice that the browser doesn't have word wrap. Really long lines
of text flow right off the side of the window and you can't read them. Word
wrap is the way most browsers (and other apps) will chop those long lines
into shorter lines automatically, so you can read all of it.

How would you do that?

Hints:
* This will all be inside the `Renderer` class.
* In `handle_data`
* Wrap to 300 pixels wide. Don't draw anything beyond that.
* Do it _approximately_ first.
* Right now, it receives all the text inside each HTML tag in one go, for
  example `<b>All this text arrives in one call to that function and
  this might be too wide to fit on the screen in one line.</b>`
* Maybe you can split that into words and draw one word at a time?
* That sounds like a loop, right?
* The Python [`split` function](https://www.w3schools.com/python/ref_string_split.asp) might be useful.
* We already measure how wide the text was. Perhaps you can use that to
  decide when to start a new line?
* If you're a perfectionist, you might find that some words have gone too far.
  Maybe `canvas.delete` helps!
