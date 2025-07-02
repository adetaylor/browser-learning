# Exercise 4b: find security bugs (automatically)

Congratulations! If you're reading this, you must have successfully found all
the hidden security bugs in the previous exercise.

Now you're going to write a program to find more security bugs. A program which
finds security bugs by testing another program is called a "fuzzer".

**Note**: this exercise probably only works on Linux, Mac or Chromebooks.

Do this:

* Do *NOT* look at the code for `src/browser/html_table.py`. That is cheating!
* Open `src/fuzzer/fuzzer.py` in your editor and read the first bit.
* Run `python3 src/fuzzer/fuzzer.py`. Watch what it does.
* Control-C to cancel it.

Now:

1. Modify *one single number* in the `generate_testcase` function so that it
   finds one of the security bugs. Run the fuzzer again.
2. Now, modify `generate_testcase` to find another bug which is hidden in
   `src/browser/html_table.py`. Do *not* look at its code - that's cheating!
   To be clear, this is an _extra_ security bug which wasn't in `browser.py`.

## General hints (no spoilers! Fine to read)

Writing a good fuzzer is hard. You'll need to think about:

* How long it takes the fuzzer to explore all the things you want it to
  explore.
* Whether you are aiming to generate fake HTML tags, or snippets of HTML
  consisting of valid tags, or both. Both is hard.
* Generating all possible HTML tags. Consider using [`random.choice`](https://docs.python.org/3/library/random.html#random.choice).
* Connecting several HTML tokens together, possibly by generating multiple tags in a loop
  and then building a string containing all the tokens you made. You can go through
  the loop a [random number of times](https://docs.python.org/3/library/random.html#random.choice).
* Sometimes it's worth calculating roughly how long it might take before the
  fuzzer happens upon the test case you want. If it's too long to be
  realistic, change the fuzzer to be more targeted.
* Sometimes your fuzzer will need to actively _avoid_ existing known bugs.
  In this case, you'll want to write `generate_testcase` to avoid triggering
  the bug with headers, or it may prevent you finding the other bug you're
  looking for.

## Specific hints (spoilers ahead!)

Read one at a time and see if it's enough for you to write a fuzzer to find it...

* [Hint one](exercise-4b-hints/hint1.md)
* [Hint two](exercise-4b-hints/hint2.md)
* [Hint three](exercise-4b-hints/hint3.md)
* [Hint four](exercise-4b-hints/hint4.md)
* [Hint five](exercise-4b-hints/hint5.md)

## Bonus exercise

Congratulations again, you've got to the end of the course!

If you've got spare time, do this:

* Pair up with someone else who has finished.
* One of you now has to hide an *extra* security bug in the browser.
* And the other one has to make sure your fuzzer is good enough to find it.
* Then swap round!
