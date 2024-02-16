# Exercise 3a: spy on requests and responses

## What you need to know

We've seen that there is a web browser, which makes a request to a web server,
and receives a response.

```mermaid
graph LR;
    Browser-- request -->Server;
    Server-- response -->Browser;
```

That request, and its response, travels across wires and through airwaves.
Maybe it contains your credit card number, your secret crush, or your health
details.

What if someone is listening in?

```mermaid
graph LR;
    Browser-- request -->Hacker;
    Hacker --> Server
    Server-- response -->Hacker;
    Hacker-->Browser;
```

Let's be such a hacker! We're going to use a tool called `tcpdump` which can
spy on *all the network traffic*.

(`tcpdump` means `TCP` dump. `TCP` is the ["transmission control protocol", which
is an agreement about how computers can communicate over the internet.](https://en.wikipedia.org/wiki/Transmission_Control_Protocol))

## Running `tcpdump`

The computer you're using probably has several **interfaces**. That is, ways
it can talk over the network. It might have a wired network socket, and it might
also be able to work on wireless ("WiFi" networks).

Run this command to find out what interfaces you have:

```
sudo tcpdump -D
```

Hopefully, one of them is labelled "loopback". That's the one we want today,
which enables us to spy on a browser and server running on your computer.
What's it called? It might be called `lo0`. Remember that.

Now run

```
sudo tcpdump -i lo0 -A 'tcp port 8000'
```

(You might need to swap `lo0` with whatever your loopback interface was called.)

Imagine you're doing this on a computer that's somewhere in between the browser
and server. It would work just the same way.

## Spying on an HTTP request

Run the simple web browser. Navigate to `http://localhost:8000/exercise1b.html`.

You should see the HTTP request go past, and the response.

Here's an example request (yours will look slightly different):

```
GET /exercise1b.html HTTP/1.1
Host: localhost:8000
User-Agent: python-requests/2.31.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
```

Here's an example response (again yours will be a bit different):

```
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.12.2
Date: Fri, 16 Feb 2024 16:43:01 GMT
Content-type: text/html
Content-Length: 344
Last-Modified: Fri, 16 Feb 2024 16:13:49 GMT

<html>
<head>
<title>Here's a simple web page</title>
</head>
<body>
<h1>Here's a simple web page</h1>
<p>This is a paragraph of text.</p>
<p>And this is another paragraph of text. It has some <b>bold text</b>. It also has a <a href="exercise1b-anotherpage.html">link to another page</a> which you can click in the browser.</p>
</body>
</html>
```

This is the information flowing over the network between the browser and the
server.

If you sent your credit card number to a web page, or had your Valentine's
in the response, anyone doing this on the network would see it.

We're doing it on the same computer as the browser and server, but your
information passes across dozens of computers on the way, and normally,
any of them could spy.

What do we do?

Type Control-C to zap `tcpdump` when you're finished.