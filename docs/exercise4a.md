# Exercise 4a: find security bugs

Imagine you're a website operator who wants to deceive the browser user or
cause them harm. Muahahaha.

Find a way to do that! There are several bugs hidden in the browser.

Any of the following counts as a success:

* Any way you can *crash* the browser, that is, cause it to exit without
  the user asking for it to exit.
* A way you can make the user think they're looking at one website
  when they're actually looking at another. (Imagine visiting a website
  showing the bank account details of somebody you're paying.)
* A way that one website can find out what was displayed in some
  other website.

Rules:
* You can only do this by *altering the HTML content of the web page*. Remember,
  you're a website operator. You *cannot* change the browser code.
* You *must not* look in the `html_table.py` file, because that's for
  a subsequent exercise.

> [!TIP]
> If you find a bug which makes one website look like another one,
> maybe you want to involve `src/server/pages/spoofable.html` to make
> a convincing demo.

There are (at least) three different crashes to find, plus one other bug.
(There might be others as well!)

## What sorts of things cause security bugs?

* [Buffer overflow](https://en.wikipedia.org/wiki/Buffer_overflow)
* [Divide by zero](https://en.wikipedia.org/wiki/Division_by_zero)
* [Type confusion](https://www.microsoft.com/en-us/security/blog/2015/06/17/understanding-type-confusion-vulnerabilities-cve-2015-0336/)
* [Use after free](https://en.wikipedia.org/wiki/Dangling_pointer#use_after_free) (not possible in Python)
* [Violations of the Line of Death](https://textslashplain.com/2017/01/14/the-line-of-death/) or other spoofing of parts of the user interface that the user might base their security judgements on

## If you find a security bug in a real browser

[The browser maker will pay you!](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#reward-amounts).

> [!TIP]
> In a real browser, not all _crashes_ are security bugs - it depends whether attackers can
> use them to steal some data instead of crashing. In our demo browser,
> any crash counts as a win.