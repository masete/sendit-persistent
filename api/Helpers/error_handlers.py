"""Helpers execption class, to handle error responses"""


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """to show the dict format for the error responses"""
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv
