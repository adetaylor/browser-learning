# System requirements and setup

## Mac

You need at least Python 3.11.

## All platforms

`python3 -m pip install -r src/requirements.txt`

## Chromebooks

1. Under the main menu in bottom left corner of the screen, open Terminal. Follow the instructions to turn on the Linux environment if necessary. Go with all the standard settings. (Note that this environment may not be available for guest users)
2. In the terminal, run these commands:
```
sudo apt-get update
sudo apt-get install python3.11-venv python3.11-tk pip openssl tcpdump libnss3 libnspr4
python3 -m venv venv
. venv/bin/activate
python3 -m pip install -r src/requirements.txt
```
3. In a browser, fetch the Visual Studio code `.deb` from [this page](https://code.visualstudio.com/download) and then copy
   the file into the Linux environment
4. Back in the terminal, run `sudo dpkg -i <name of that .deb file>`

## Mac

Install the latest version of Python from [the Python website](https://www.python.org/).