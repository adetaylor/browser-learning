#!/usr/bin/env python3

import os
import pip

script_dir = os.path.dirname(os.path.realpath(__file__))
requirements_file = os.path.join(script_dir, "requirements.txt")
requirements_win_file = os.path.join(script_dir, "requirements-win.txt")
files = [requirements_file, requirements_win_file]:
for f in files:
  pip.main(["install", "--user", "-r", f, "--trusted-host", "pypi.python.org", "--trusted-host", "pypi.org", "--trusted-host", "files.pythonhosted.org”])
