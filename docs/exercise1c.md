# Exercise 1c: Make your own HTML file

Inside the `src` directory is another directory called `server`, and inside
there is `pages`.

Create a new HTML file in there. Use the (few!) types of tag supported by
the browser. (There are a couple of files already that you can use as
examples).

Make it work end-to-end!

Here's how to run the server:

`src/server/http_server.py`

Then use the browser to visit (exactly):

`http://localhost:8000/exercise1c.html`
(change `exercise1c.html` to whatever you called your page)

Ensure you can see bold text and hyperlinks.

What's wrong with the browser we've made?

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