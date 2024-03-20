# Exercise 1c: Make your own HTML file

Inside the `src` directory is another directory called `server`, and inside
there is `pages`.

Create a new HTML file in there. Use the (few!) types of tag supported by
the browser.

You should make sure you know how to add these tags:
* `a href`
* `b`

Make it work end-to-end!

Here's how to run the server:

`python3 src/server/http_server.py`

Then use the browser to visit (exactly):

`http://localhost:8000/exercise1c.html`
(change `exercise1c.html` to whatever you called your page)

> [!TIP]
> You need to run the browser and the server at the same time. The best way to
> do this is to type Control-Z, and then type `bg`, which will run the browser
> in the background. (You can see this by typing `jobs`.) Another way is to
> open another terminal and then run `cd browser-learning` then `. venv/bin/activate`.

Ensure you can see bold text and hyperlinks.

## What's up with?

### `http://localhost:8000/exercise1c.html`

* `http` here is the "scheme". That is, it's an agreement in the way that
  the browser and server communicate. There are others including `https`
  and `ftp`. We'll see the details of `http` later
* `localhost`: this is a special name which means "your own computer".
  Since the web server is running on your own computer, that's what we'll
  connect to.
* `:8000`: this is called the "port number" and isn't very important right now.
  A single computer can be running several different web servers, and each
  has its own port number. We chose 8000 for our server. (The standard port is
  80, but we're not using that for our exercises in case something else is
  already using that port number.)
* `exercise1c.html`: the nae of the HTML page that the browser will request
  from the server.
