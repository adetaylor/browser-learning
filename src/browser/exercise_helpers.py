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

def prepare_for_load(url, window):
    """
    Ignore this function - it's used to set up
    encryption for some of the later exercises.
    """
    if "localhost" in url:
        os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), "server/tls_things/server.crt")
    elif "REQUESTS_CA_BUNDLE" in os.environ:
        del os.environ["REQUESTS_CA_BUNDLE"]
    window.load_in_progress = True

def inform_fuzzer_paint_finished(window):
    """
    Ignore this function - it's used to talk to the fuzzer in exercise 4b.
    """
    if window.load_in_progress:
        if os.environ.get("OUTPUT_STATUS") is not None:
            print("Rendering completed\n", flush=True)
        window.load_in_progress = False

def setup_fuzzer_handling(window):
    """
    Ignore this function - it's used to set up
    fuzzing for some of the later exercises.
    """
    window.load_in_progress = True
    if hasattr(signal, "SIGHUP"):
        reader, writer = os.pipe()
        signal.signal(signal.SIGHUP, lambda _s, _h: os.write(writer, b'a'))
        window.notifier = QSocketNotifier(reader, QSocketNotifier.Type.Read, window)
        window.notifier.setEnabled(True)
        def signal_received():
            os.read(reader, 1)
            window.go_button_clicked()
        window.notifier.activated.connect(signal_received)
        # Every 100 msec, check if we've been asked to reload -
        # this is only relevant for exercise 4b and works around a bug
        # in the GUI toolkit.
        window.timer = QTimer()
        window.timer.timeout.connect(lambda: None)
        window.timer.start(100)
    elif windows_events_available:
        try:
            window.event = win32event.OpenEvent(win32event.EVENT_ALL_ACCESS, 0, "PYTHON_BROWSER_RELOAD")
            window.win_event_notifier = QWinEventNotifier(int(window.event))
            window.win_event_notifier.activated.connect(lambda: window.go_button_clicked())
            window.win_event_notifier.setEnabled(True)
        except:
            pass # not fuzzing
