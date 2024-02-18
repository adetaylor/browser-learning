# Exercise 2c: word wrap!

You might notice that the browser doesn't have word wrap.
How would you do that?

Hints:
* This will all be inside the `Renderer` class.
* In `handle_data`
* Do it _approximately_ first
* Right now, it receives all the text inside each HTML tag in one go, for
  example `<p>All this text arrives in one call to that function</p>`
* Maybe you can split that into words and draw one word at a time?
* We already measure how wide the text was. Perhaps you can use that to
  decide when to start a new line?
* But you already drew too much text, right? Maybe `canvas.delete` helps!
