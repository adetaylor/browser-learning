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

import tkinter  # needed for PyDroid3 compatibility
import PySimpleGUI as sg
import requests
from html.parser import HTMLParser
from urllib.parse import urlparse


class Renderer(HTMLParser):
    """
    Instructs Python how we wish to handle the start, middle, and end
    of HTML tags.

    For instance, with this HTML:
      <b>Some text</b>
    we would get a call to 'handle_starttagg', then 'handle_data'
    then 'handle_endtag'.
    """

    def __init__(self, canvas, browser):
        """
        Our HTML understanding engine needs to maintain some information
        about what it's already discovered. For example, if we've been
        past a <b> tag, we need to remember that we should draw text in
        bold.
        """
        super().__init__()
        self.canvas = canvas  # the GUI 'canvas' on which we draw
        self.browser = browser  # the main browser object

        # Information we are remembering as we draw the page,
        # to influence how we draw subsequent bits of the page.
        self.y_pos = 0  # where we should draw the next text
        self.x_pos = 0  # where we should draw the next text
        self.ignore_current_text = False
        self.is_bold = False
        self.current_link = None
        self.known_links = dict()  # stores the relationship between
        # the bits of text shown in the UI (remembered by number)
        # and the URL we want to visit when it's clicked.

        # First ensure the canvas is blank.
        self.canvas.delete('all')

    def link_clicked(self, link_event):
        """
        This code is called by the PySimpleGUI canvas when
        a link is clicked. We look up which link was clicked
        and then inform the main application by calling a
        function that's stored in "self.link_clicked_callback".
        """
        widget_id = link_event.widget.find_withtag('current')[0]
        url = self.known_links[widget_id]
        self.browser.link_clicked(url)

    def handle_starttag(self, tag, attrs):
        """
        Handle an HTML start tag, for instance,
        <b> or <a href="foo.html">. In these cases, 'b' and 'a'
        are the tag, and in the latter case we also have an attr.
        """
        if tag == 'script' or tag == 'style':
            # Stuff inside these two tags isn't actually HTML;
            # it's JavaScript and CSS. Our browser doesn't support
            # such things. Ignore.
            self.ignore_current_text = True
        if tag == 'br' or tag == 'p':  # move to a new line
            self.y_pos += 12
            self.x_pos = 0
        if tag == 'b' or tag == 'strong':
            self.is_bold = True
        if tag == 'a':  # hyperlink.
            for tag_name, tag_value in attrs:
                if tag_name == 'href':
                    self.current_link = tag_value

    def handle_endtag(self, tag):
        """
        Handle an HTML end tag, for example </a> or </b>
        """
        if tag == 'script' or tag == 'style':
            self.ignore_current_text = False
        if tag == 'b' or tag == 'strong':
            self.is_bold = False
        if tag == 'a':
            self.current_link = None

    def handle_data(self, data):
        """
        Handle some actual text, found in between tag starts
        and ends or outside of all of them.
        """
        data = data.rstrip()
        if self.ignore_current_text or data == '':
            return
        # Work out what font we'll draw this in.
        font = 'Helvetica 12'
        if self.is_bold:
            font = font + ' bold'
        fill = 'black'
        if self.current_link is not None:
            fill = 'blue'
            font = font + ' underline'
        text_obj_id = self.canvas.create_text(
            self.x_pos, self.y_pos, text=data, fill=fill, font=font, anchor=sg.tk.NW)
        # Work out how wide this text was, so we
        # can draw the next bit alongside.
        text_bounding_box = self.canvas.bbox(text_obj_id)
        self.x_pos = text_bounding_box[2]
        # If we're in a hyperlink, tell the GUI that we need
        # to be informed if it's clicked.
        if self.current_link is not None:
            self.known_links[text_obj_id] = self.current_link
            self.canvas.tag_bind(text_obj_id, '<Button-1>', self.link_clicked)



class Browser:
    """
    The overall state of the browser.
    """
    def __init__(self, window):
        self.current_url = None
        self.window = window

    def link_clicked(self, url):
        """
        Called when a link on the page was clicked.
        """
        if not ':' in url:
            # The hyperlink was a relative URL, e.g. just "some_page.html".
            # We need to change that into an absolute URL, e.g.
            # https://en.wikipedia.org/some_page.html
            # by combining it with parts of the currently-viewed URL
            current_url_parts = urlparse(self.current_url)
            url = current_url_parts._replace(path=url).geturl()
        self.window['-URL-'].update(url)  # fill in the URL bar with the new URL
        self.window['Go'].click()  # pretend the user clicked Go


    def set_status(self, message):
        """
        Update the status line at the bottom of the screen
        """
        self.window['-STATUS-'].update(message)


    def set_window_title(self, message):
        """
        Sets the title of the window
        """
        self.window.set_title(message)

    def navigate(self, url):
        """
        Navigates the browser to a new URL
        """
        if not ':' in url:
            url = 'https://' + url
            self.window['-URL-'].update(url)
        sg.user_settings_set_entry('-URL-', url)
        self.current_url = url
        self.set_status('Status: loading...')
        try:
            response = requests.get(url)
        except:
            self.set_status('Status: unable to connect to %s' % url)
            return
        if response.ok:
            self.set_status('Status: OK, rendering')
            page_html = response.text
            canvas_in_which_to_draw_page = self.window['-CANVAS-'].TKCanvas
            parser = Renderer(canvas_in_which_to_draw_page, self)
            parser.feed(page_html)
            self.set_status('Status: OK')
        else:
            self.set_status('Status: web server gave us error code %d' %
                       response.status_code)


#########################################
# Main program here
#########################################


# Set up the graphical user interface (GUI)
sg.theme('DarkAmber')
sg.user_settings_filename(path='.')
initial_url = sg.user_settings_get_entry(
    '-URL-', 'https://en.wikipedia.org')  # load the last URL that
# the user used in this browser, or use wikipedia if they never used it before
# Set up the GUI layout. All the '-SOMETHING-' bits are the names we give
# each UI control so we can read or modify their contents later.
layout = [[sg.Text('URL:'), sg.Input(initial_url, key='-URL-'), sg.Button('Go', bind_return_key=True), sg.Exit()],
          [sg.Canvas(size=(300, 300), key='-CANVAS-', expand_x=True,
                     expand_y=True, background_color='White')],
          [sg.Text('Status:', key='-STATUS-')]]
window = sg.Window('Simple Browser', layout, resizable=True)

browser = Browser(window)


# The "event loop". We keep looping through this until
# Exit is clicked or the window is closed.
while True:
    # See what the user has asked us to do
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Go':  # navigate to a new page
        browser.navigate(values['-URL-'])

window.close()
