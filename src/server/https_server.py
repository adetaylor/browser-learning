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
import ssl
import os
import subprocess
import tempfile


class PagesDirectoryRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        pages_dir = os.path.join(os.path.dirname(__file__), "pages")
        super().__init__(request, client_address, server, directory=pages_dir)


httpd = HTTPServer(('localhost', 4443), PagesDirectoryRequestHandler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

tls_things_dir = os.path.join(os.path.dirname(__file__), "tls_things")
server_certificate_file = os.path.join(tls_things_dir, "server.pem")

if not os.path.exists(server_certificate_file):
    if not os.path.exists(tls_things_dir):
        os.makedirs(tls_things_dir)
    with tempfile.NamedTemporaryFile(delete=False) as config:
        config.write(
            b"[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
        config.close()
        subprocess.check_call(["openssl", "req", "-x509", "-out", "server.crt", "-keyout", "server.key", "-newkey", "rsa:4096", "-nodes", "-sha256", "-subj", "/CN=localhost",
                               "-extensions", "EXT", "-config", config.name],
                              cwd=tls_things_dir)
    with open(server_certificate_file, "w") as outfile:
        with open(os.path.join(tls_things_dir, "server.crt")) as infile:
            outfile.write(infile.read())
        with open(os.path.join(tls_things_dir, "server.key")) as infile:
            outfile.write(infile.read())

context.load_cert_chain(certfile=server_certificate_file)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()
