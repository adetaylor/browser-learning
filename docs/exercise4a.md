# Exercise 4a: find security bugs

Imagine you're a website operator who wants to deceive the browser user or
cause them harm. Muahahaha.

Find a way to do that! There is a bug hidden in the browser.

Any of the following counts as a success:

* Any way you can *crash* the browser, that is, cause it to exit without
  the user asking for it to exit.]
* A way you can make the user think they're looking at one website
  when they're actually looking at another. (Imagine visiting a website
  showing the bank account details of somebody you're paying.)
* A way that one website can find out what was displayed in some
  other website.

Rules:
* You can only do this by altering the HTML content of the web page.

There are (at least) three different crashes to find, plus one other bug.
(There might be others as well!)

## What sorts of things cause crashes?

* [Buffer overflow](https://en.wikipedia.org/wiki/Buffer_overflow)
* [Divide by zero](https://en.wikipedia.org/wiki/Division_by_zero)
* [Type confusion](https://www.microsoft.com/en-us/security/blog/2015/06/17/understanding-type-confusion-vulnerabilities-cve-2015-0336/)
* [Use after free](https://en.wikipedia.org/wiki/Dangling_pointer#use_after_free)

## If you find a security bug in a real browser

[The browser maker will pay you!](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#reward-amounts).