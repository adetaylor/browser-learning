# Exercise 4a: find security bugs (automatically)

Congratulations! If you're reading this, you must have successfully found all
the hidden security bugs in the previous exercise.

Now you must *forget* everything you just found, because you're going to write
a program to find them instead. A program which finds security bugs by testing
another program is called a "fuzzer".

Do this:

* Open `src/fuzzer/fuzzer.py` in VSCode and read it.
* Run `python3 src/fuzzer/fuzzer.py`. Watch what it does.
* Control-C to cancel it.

Now:

1. Modify *one single number* in `fuzzer.py` so that it finds one
   of the security bugs. Run the fuzzer again.
2. Modify the `generate_testcase` more extensively to generate random-
   but-realistic HTML that can find all the hidden crashes (or at least,
   some more of them)

## Rules

* Your fuzzer must *NOT* have knowledge about the specific security bugs
  it's looking for. That's cheating!
* But it's OK for it to know about HTML in general.

## Hints

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

## Bonus exercise

Congratulations again, you've got to the end of the course!

If you've got spare time, do this:

* Pair up with someone else who has finished.
* One of you now has to hide an *extra* security bug in the browser.
* And the other one has to make sure your fuzzer is good enough to find it.
* Then swap round!
