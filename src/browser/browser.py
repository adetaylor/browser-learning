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

# Simple demo python web browser. Lacks all sorts of important features.

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSizePolicy
from PyQt6.QtCore import QSettings, Qt, QPoint, QSize, QSocketNotifier
from PyQt6.QtGui import QFont, QMouseEvent, QPainter, QFontMetrics
import requests
import os
import signal
import sys
import html_table # do not look inside this file, that would be cheating on a later exercise
from html.parser import HTMLParser
from urllib.parse import urlparse

# How much bigger to make the font when we come across <h1> to <h6> tags
FONT_SIZE_INCREASES_FOR_HEADERS_1_TO_6 = [10, 6, 4, 3, 2, 1]


class Renderer(HTMLParser, QWidget):
    """
    Represents the area of the screen occupied by the web content (as
    opposed to the URL bar, etc.) Knows how to convert HTML tags
    (e.g. <b>some text</b>) into actual pixels on the screen, by drawing
    the right sort of text in the right places.
    """

    def __init__(self, browser, parent=None):
        """
        Code which is run when we create a new Renderer.
        """
        # Set up the underlying HTML parser and user interface code.
        super(Renderer, self).__init__()
        QWidget.__init__(self, parent)
        # Tell the user interface code that we are stretchy, in case
        # the window is resized.
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.known_links = list()  # stores clickable UI areas
        # and the URL we want to visit when it's clicked
        # as a list of five-tuples like this:
        #  (x1, y1, x2, y2, url)
        # e.g.
        #  (10, 20, 50, 30, "http://foo.com")
        self.html = ""
        self.browser = browser

    def minimumSizeHint(self):
        """
        Returns the smallest possible size on the screen for our renderer.
        """
        return QSize(800, 400)

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        """
        Handle a click somewhere in the renderer area. See if it
        matches any known link.
        """
        if event is not None and self.browser is not None:
            x = event.position().x()
            y = event.position().y()
            for possible_link in self.known_links:
                (x1, y1, x2, y2, url) = possible_link
                if x >= x1 and x <= x2 and y >= y1 and y <= y2:
                    self.browser.link_clicked(url)
                    return None
        return super().mouseReleaseEvent(event)

    def set_html(self, html):
        """
        Store the HTML text we've been given. We'll use it when
        the user interface asks us to repaint.
        """
        self.html = html
        self.update() # redraw. This will arrange for the UI
          # library to call paintEvent, just below.

    def paintEvent(self, event):
        """
        This is called by the user interface whenever we need
        to draw the screen. This may be called because of the
        "self.update()" call just above, or because the UI
        has decided we need to redraw for some other reason.

        Take the HTML we were given by the website, and draw it
        onto the screen.
        """
        self.painter = QPainter(self)
        # Clear the area.
        self.painter.fillRect(self.rect(), Qt.GlobalColor.white)
        # Information we are remembering as we draw the page,
        # to influence how we draw subsequent bits of the page.
        self.y_pos = 0  # where we should draw the next text
        self.x_pos = 0  # where we should draw the next text
        self.ignore_current_text = False
        self.is_bold = False
        self.is_strikethrough = False
        self.font_size = 12
        self.tallest_text_in_previous_line = 0
        self.space_needed_before_next_data = False
        self.current_link = None # if we're in a <a href=...> hyperlink
        self.known_links = list() # Links anywhere on the page
        self.table = None # whether we're in an HTML table
        # The following call interprets all the HTML in page_html.
        # You can't see most of the code which does this because it's
        # in the library which provides the HTMLParser class. But it will
        # result in lots of calls to handle_starttag, handle_endtag and
        # handle_data.
        # So you can think of this as lots of calls to handle_starttag,
        # handle_data and handle_endtag depending on what's inside self.html.
        self.feed(self.html)
        self.painter = None
        # Ignore the following two lines, they're used for exercise 4b only
        if os.environ.get("OUTPUT_STATUS") is not None:
            print("Rendering completed\n", flush=True)

    def handle_starttag(self, tag, attrs):
        """
        Handle an HTML start tag, for instance,
        <b> or <a href="foo.html">. In these cases, 'b' and 'a'
        are the tag, and in the latter case we also have an "attrbute"
        (attr)
        """
        if tag == 'script' or tag == 'style' or tag == 'title':
            # Stuff inside these tags isn't actually HTML
            # to display on the screen.
            self.ignore_current_text = True
        if self.table is not None:
            # If we're inside a table, handle table-related tags but no others
            if tag == 'tr':
                self.table.handle_tr_start()
            if tag == 'td':
                self.table.handle_td_start()
            return
        if tag == 'b' or tag == 'strong':
            self.is_bold = True
        if tag == 's':
            self.is_strikethrough = True
        if tag == 'a':  # hyperlink.
            for tag_name, tag_value in attrs:
                if tag_name == 'href':
                    self.current_link = tag_value
        if tag == 'meta':  # sometimes sites redirect users to other sites
            # Looks like <meta http-equiv="refresh" content="delay; new-url">
            is_refresh = False
            content = None
            for tag_name, tag_value in attrs:
                if tag_name == 'http-equiv':
                    if tag_value == 'refresh':
                        is_refresh = True
                if tag_name == 'content':
                    content = tag_value
            if is_refresh and content is not None:
                parts = content.split('; ')
                if len(parts) == 2:
                    self.browser.set_window_url(parts[1])
                    if parts[0] == '0':  # navigate immediately to the requested URL
                        self.browser.navigate(parts[1])
                    # Delayed navigations not yet supported by this browser
        if tag == 'small':
            self.font_size -= 1
        if tag == 'big':
            self.font_size += 1
        # h1...h6 header tags
        if len(tag) == 2 and tag[0] == 'h' and tag != 'hr':
            self.newline()
            heading_number = int(tag[1])
            font_size_difference = FONT_SIZE_INCREASES_FOR_HEADERS_1_TO_6[heading_number - 1]
            self.font_size += font_size_difference
        if tag == 'table':
            self.table = html_table.HTMLTable()
        self.space_needed_before_next_data = True

    def handle_endtag(self, tag):
        """
        Handle an HTML end tag, for example </a> or </b>
        """
        if self.table is not None:
            # If we're inside a table, handle table end but no other tags
            if tag == 'table':
                self.y_pos = self.table.handle_table_end(self.y_pos, lambda x, y, content: self.draw_text(x, y, content))
                self.table = None
            return
        if tag == 'br' or tag == 'p':  # move to a new line
            self.newline()
        if tag == 'script' or tag == 'style' or tag == 'title':
            self.ignore_current_text = False
        if tag == 'b' or tag == 'strong':
            self.is_bold = False
        if tag == 'a':
            self.current_link = None
        if tag == 's':
            self.is_strikethrough = False
        if tag == 'small':
            self.font_size += 1
        if tag == 'big':
            self.font_size -= 1
        if len(tag) == 2 and tag[0] == 'h' and tag != 'hr':
            self.newline()
            heading_number = int(tag[1])
            font_size_difference = FONT_SIZE_INCREASES_FOR_HEADERS_1_TO_6[heading_number - 1]
            self.font_size -= font_size_difference
        self.space_needed_before_next_data = True

    def newline(self):
        """
        Start a new line of text.
        """
        SPACING = 3 # just allow a bit of extra space between lines
        self.y_pos += self.tallest_text_in_previous_line + SPACING
        self.x_pos = 0
        self.tallest_text_in_previous_line = 0

    def handle_data(self, data):
        """
        Handle some actual text, found within a tag or outside them. For example,
        FOO in <b>FOO</b>.
        """
        data = data.rstrip()
        if self.ignore_current_text or data == '':
            return
        if self.space_needed_before_next_data:
            self.space_needed_before_next_data = False
            data = ' ' + data
        if self.table is not None:
            # If we're inside a table, ask our table layout code to
            # figure out where to draw it later
            self.table.handle_data(data)
        else:
            (text_width, text_height) = self.draw_text(self.x_pos, self.y_pos, data)
            self.x_pos = self.x_pos + text_width
            if text_height > self.tallest_text_in_previous_line:
                self.tallest_text_in_previous_line = text_height

    def draw_text(self, x_pos, y_pos, text):
        """
        Draw some text on the screen.
        Returns a tuple of (x, y) space occupied
        """
        # Work out what font we'll draw this in.
        weight = QFont.Weight.Normal
        if self.is_bold:
            weight = QFont.Weight.Bold
        font = QFont("Helvetica", weight=weight, pointSize=self.font_size, italic=False)
        self.painter.setFont(font)
        fill = Qt.GlobalColor.black
        if self.current_link is not None:
            fill = Qt.GlobalColor.blue
        self.painter.setPen(fill)
        # Work out the size of the text we're about to draw.
        text_measurer = QFontMetrics(font)
        text_width = int(text_measurer.horizontalAdvance(text))
        text_height = int(text_measurer.height())
        # Tell our GUI canvas to draw some text! The important bit!
        self.painter.drawText(QPoint(x_pos, y_pos + text_height), text)
        # If we're in a hyperlink, underline it and record its coordinates
        # in case it gets clicked later.
        if self.current_link is not None:
            self.painter.drawLine(x_pos, y_pos + text_height, x_pos + text_width, y_pos + text_height)
            self.known_links.append((x_pos, y_pos, x_pos + text_width, y_pos + text_height, self.current_link))
        # Strikethrough - draw a line over the text but only
        # if we don't cover more than 50% of it, we don't want it illegible
        if self.is_strikethrough:
           fraction_of_text_covered = 6 / self.font_size
           if fraction_of_text_covered <= 0.5:
               strikethrough_line_y_pos = y_pos + (self.font_size / 2) - 80
               self.canvas.create_line(x_pos, strikethrough_line_y_pos,
                                       x_pos + text_width, strikethrough_line_y_pos)
        return (text_width, text_height)


class Browser(QMainWindow):
    """
    A class of objects representing the browser window. At any time there's
    exactly one of these Browser objects existing.
    """

    def __init__(self, initial_url):
        """
        Code which is run when our Browser is created.
        """
        super(Browser, self).__init__()
        self.current_url = None
        # All the following code lays out the UI.
        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(QLabel("URL:"))
        self.url_box = QLineEdit()
        self.url_box.returnPressed.connect(self.go_button_clicked)
        toolbar_layout.addWidget(self.url_box)
        go_button = QPushButton("Go")
        go_button.clicked.connect(self.go_button_clicked)
        toolbar_layout.addWidget(go_button)
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(lambda: QApplication.quit())
        toolbar_layout.addWidget(exit_button)
        toolbar = QWidget()
        toolbar.setLayout(toolbar_layout)
        overall_layout = QVBoxLayout()
        overall_layout.addWidget(toolbar)
        self.renderer = Renderer(self)
        overall_layout.addWidget(self.renderer)
        self.status_bar = QLabel("Status:")
        overall_layout.addWidget(self.status_bar)
        widget = QWidget()
        widget.setLayout(overall_layout)
        self.setCentralWidget(widget)
        # Set up somewhere to remember the last URL the user used
        self.settings = QSettings("browser-learning", "browser")
        if initial_url is None:
            initial_url = self.settings.value("url", "https://en.wikipedia.org", type=str)
        else:
            self.navigate(initial_url)
        self.set_window_url(initial_url)
        self.setup_fuzzer_handling() # ignore

    def go_button_clicked(self):
        """
        Called when the Go button is clicked
        """
        url = self.url_box.text()
        self.navigate(url)

    def link_clicked(self, url):
        """
        Called when a link on the page was clicked.
        """
        if not ':' in url:
            # The hyperlink was a relative URL, e.g. just "some_page.html".
            # We need to change that into an absolute URL, e.g.
            # https://en.wikipedia.org/some_page.html
            # by combining it with parts of the currently-viewed URL.
            # (This is a simplification of the real checks for relative URLs...)
            current_url_parts = urlparse(self.current_url)
            url = current_url_parts._replace(path=url).geturl()
        # fill in the URL bar with the new URL
        self.set_window_url(url)
        self.navigate(url)

    def set_status(self, message):
        """
        Update the status line at the bottom of the screen
        """
        self.status_bar.setText(message)

    def set_window_url(self, url):
        """
        Sets the URL bar
        """
        self.url_box.setText(url)

    def navigate(self, url):
        """
        Navigates the browser to a new URL
        """
        if not ':' in url:
            url = 'https://' + url
            self.set_window_url(url)
        self.settings.setValue("url", url)
        self.current_url = url
        self.set_status('Status: loading...')
        self.setup_encryption(url)
        # Connect over the network to a web server to get the HTML
        # at this URL.
        try:
            response = requests.get(url)
        except:
            self.set_status('Status: unable to connect to %s' % url)
            self.renderer.set_html("")
            return
        if not response.ok:
            self.set_status('Status: web server gave us error code %d' %
                            response.status_code)
            self.renderer.set_html("")
            return
        page_html = response.text
        # Tell the renderer about the HTML.
        # It doesn't actually handle it until it's asked to paint.
        self.renderer.set_html(page_html)
        self.set_status('Status: OK')

    def setup_encryption(self, url):
        """
        Ignore this function - it's used to set up
        encryption for some of the later exercises.
        """
        if "localhost" in url:
            os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.path.dirname(
                os.path.dirname(__file__)), "server/tls_things/server.crt")
        elif "REQUESTS_CA_BUNDLE" in os.environ:
            del os.environ["REQUESTS_CA_BUNDLE"]

    def setup_fuzzer_handling(self):
        """
        Ignore this function - it's used to set up
        fuzzing for some of the later exercises.
        """
        self.reader, self.writer = os.pipe()
        signal.signal(signal.SIGHUP, lambda _s, _h: os.write(self.writer, b'a'))
        notifier = QSocketNotifier(self.reader, QSocketNotifier.Type.Read, self)
        notifier.setEnabled(True)
        def signal_received():
            os.read(self.reader, 1)
            window.go_button_clicked()
        notifier.activated.connect(signal_received)


#########################################
# Main program here
#########################################

# Set up the graphical user interface (GUI)
app = QApplication([])

# See if we were given a URL on the command-line
initial_url = None
if len(sys.argv) > 1:
    initial_url = sys.argv[1]

# Create the one (and only) example of our Browser class.
window = Browser(initial_url)
window.show()

# The "event loop". An event is something like a click or the user
# typing something. Keep handling those events from the user until
# Exit is clicked or the window is closed. All of this happens
# within app.exec().
# In particular, this will end up calling the "repaint" method whenever
# we need to display something on the screen, along with
# methods above like "go_button_clicked" or "mouseReleaseEvent"
# when the user interacts with the app.
app.exec()