# System requirements and setup

(to be much expanded)

## Mac

You need at least Python 3.11.

## All platforms

`python3 -m pip install -r src/requirements.txt`

## Chromebooks

1. Under the main menu, open Terminal. Follow the instructions to enable the Linux environment if necessary. (Note that this environment may not be available for guest users)
2. In the terminal, run these commands:
```
sudo apt-get update
sudo apt-get install python3.11-venv python3.11-tk pip openssl
python3 -m venv venv
. venv/bin/activate
python3 -m pip install -r src/requirements.txt
```

## Mac

Install the latest version of Python from [the Python website](https://www.python.org/).