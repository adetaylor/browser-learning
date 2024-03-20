# System requirements and setup

In all cases, open a browser to visit `https://github.com/adetaylor/browser-learning`
- you should be looking at these pages!

## Mac

1. Open Terminal.
2. Run `python3 --version`. See what Python version you have. You need at least Python 3.12. You can get it from the [main Python website](https://www.python.org/downloads/).
3. Fetch and install [Visual Studio Code](https://code.visualstudio.com/) if you don't already have it.
4. Fetch the zip of this course (your instructor will tell you how).
4. In Terminal, run:
```
git clone https://github.com/adetaylor/browser-learning.git
cd browser-learning
python3 -m venv venv
. venv/bin/activate
python3 -m pip install -r src/requirements.txt
```

## Chromebooks

1. Under the main menu in bottom left corner of the screen, open Terminal. Follow the instructions to turn on the Linux environment if necessary. Go with all the standard settings. (Note that this environment may not be available for guest users)
2. In the terminal, run these commands:
```
git clone https://github.com/adetaylor/browser-learning.git
cd browser-learning
./install-chromebook-prerequisites.sh
python3 -m venv venv
. venv/bin/activate
pip3 install -r src/requirements.txt
```
3. Keep the terminal open - you'll need it to run commands. (If you open a new terminal, run `cd browser-learning` and then `. venv/bin/activate`)
4. From the main menu, also open Visual Studio code.

## Computers without a command prompt

If you have a school computer with command prompt blocked but access to IDLE, do this:

* In IDLE open a file. Navigate to `src` then open `install-prerequisites.py`
* Run it

## Other types of machine

Do what's required to install:

* Python 3.12+
* `tcpdump`
* Visual Studio code, or some other good code editor (the students will be doing lots of _reading code_ so a good IDE is highly recommended)

## Troubleshooting

* I see `"If this fails your Python may not be configured for Tk".`
  This is probably on MacOS and you probably installed python using `brew`; `brew install python-tk` might work.
