#!/usr/bin/env python3

import os
import pip

script_dir = os.path.dirname(os.path.realpath(__file__))
requirements_file = os.path.join(script_dir, "requirements.txt")
pip.main(["install", "--user", "-r", requirements_file])
requirements_file = os.path.join(script_dir, "requirements-win.txt")
pip.main(["install", "--user", "-r", requirements_file])
