"""Thread-local storage for the request currently being handled.

Used so that ``log_activity`` (including calls from model signals) can
attribute an audit entry to the authenticated actor without every caller
having to pass the request/user explicitly.
"""
import threading

_state = threading.local()


def set_current_request(request):
    _state.request = request


def get_current_request():
    return getattr(_state, 'request', None)


def clear_current_request():
    _state.request = None
