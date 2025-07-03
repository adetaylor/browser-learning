# Exercise 1a: Use a real browser, spot things in HTML

* Open up Chrome (or any other browser)
* Go to https://en.wikipedia.org in that browser
* Look for:
  * Some text which is **bold** (remember what it says)
  * Some text which is _italic_ (remember what it says)
  * Some text which is a hyperlink (remember what it says)
* Right-click and choose "Inspect"

Here's what's happening:

```mermaid
graph LR;
    browser(Browser on your computer)
    server(Wikipedia web server)
    browser-- request for a particular page --> server;
    server -- response containing HTML -->browser;
```

Questions:

* What's the HTML tag meaning 'bold'?
* What's the HTML tag meaning 'italic'?
* What's the HTML tag meaning hyperlink? What happens when you click the link?
  The browser goes to another web page - how does it know where to go?

(you'll need to know these things later!)