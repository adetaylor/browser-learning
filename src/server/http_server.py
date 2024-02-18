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

from http.server import HTTPServer, SimpleHTTPRequestHandler

import os

class PagesDirectoryRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        pages_dir = os.path.join(os.path.dirname(__file__), "pages")
        super().__init__(request, client_address, server, directory=pages_dir)

httpd = HTTPServer(('localhost', 8000), PagesDirectoryRequestHandler)

httpd.serve_forever()
