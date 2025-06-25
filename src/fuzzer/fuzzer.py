#!/usr/bin/env python3

# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from http.server import HTTPServer, BaseHTTPRequestHandler

import os
import threading
import signal
import subprocess
import random
import sys

def generate_testcase():
    """
    Generate some HTML to try in the browser
    """
    # TODO: Modify this code for the exercises
    x = random.randrange(0, 7)
    return "<h%d>Test header</h%d>" % (x, x)

####################################################
# You should not need to modify anything below here
####################################################

testcase = ""
running = True
exited_intentionally = False

def signal_handler(sig, frame):
    print('Ctrl-C intercepted, finishing fuzzing!')
    global exited_intentionally, running
    exited_intentionally = True
    running = False
    sys.exit(0)

if hasattr(signal, "SIGINT"):
    signal.signal(signal.SIGINT, signal_handler)

class FuzzerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(testcase.encode())

    def log_message(self, format, *args):
        pass

httpd = HTTPServer(('localhost', 8001), FuzzerRequestHandler)

def run_http_server():
    httpd.serve_forever()

httpd_server_thread = threading.Thread(target=run_http_server, daemon=True)
httpd_server_thread.start()

print("Beginning fuzzing. Press Control-C (maybe several times) to stop.")

browser_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "browser", "browser.py")

url = "http://localhost:8001/testcase.html"

browserenv = os.environ
browserenv["OUTPUT_STATUS"] = "1"
browser_proc = subprocess.Popen([sys.executable, browser_path, url], stdout=subprocess.PIPE, env=browserenv, encoding="utf8")

first = True

while running:
    testcase = generate_testcase()
    print("Trying %s" % testcase)
    crashed = True
    render_completed = False
    if first:
        first = False
    elif hasattr(signal, "SIGHUP"):
        browser_proc.send_signal(signal.SIGHUP)
    else:
        print("Press Go in the browser.")
    while browser_proc.poll() is None and running and not render_completed:
        try:
            line = browser_proc.stdout.readline()
            if "Rendering completed\n" in line:
                crashed = False
                render_completed = True
        except:
            pass
    if crashed and not exited_intentionally:
        print("The HTML\n%s\ncrashed the browser! Good job!" % testcase)
        running = False
browser_proc.terminate()
