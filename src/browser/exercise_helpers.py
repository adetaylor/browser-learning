# Stuff which is part of the python demo browser but is specifically
# to allow some of the advanced exercises to work. It's not very
# interesting and you don't need to read this.

import os
import signal
from PyQt6.QtCore import QSocketNotifier, QTimer

try:
    import win32event
    windows_events_available = True
    from PyQt6.QtCore import QWinEventNotifier
except:
    windows_events_available = False

def setup_encryption(url):
    """
    Ignore this function - it's used to set up
    encryption for some of the later exercises.
    """
    if "localhost" in url:
        os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), "server/tls_things/server.crt")
    elif "REQUESTS_CA_BUNDLE" in os.environ:
        del os.environ["REQUESTS_CA_BUNDLE"]

def setup_fuzzer_handling(window):
    """
    Ignore this function - it's used to set up
    fuzzing for some of the later exercises.
    """
    reader, writer = os.pipe()
    if hasattr(signal, "SIGHUP"):
        signal.signal(signal.SIGHUP, lambda _s, _h: os.write(writer, b'a'))
        notifier = QSocketNotifier(reader, QSocketNotifier.Type.Read, window)
        notifier.setEnabled(True)
        def signal_received():
            os.read(reader, 1)
            window.go_button_clicked()
        notifier.activated.connect(signal_received)
        # Every 100 msec, check if we've been asked to reload -
        # this is only relevant for exercise 4b and works around a bug
        # in the GUI toolkit.
        timer = QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(100)
    elif windows_events_available:
        event = win32event.OpenEvent(win32event.EVENT_ALL_ACCESS, 0, "PYTHON_BROWSER_RELOAD")
        win_event_notifier = QWinEventNotifier(event)
        win_event_notifier.activated.connect(lambda: window.go_button_clicked())
