from rest_framework import status
from rest_framework.exceptions import APIException


class WrapperException(APIException):

    def __init__(self, error, reason=None, status_code=status.HTTP_400_BAD_REQUEST, stack=None, origin_exception=None):
        if stack is None:
            stack = []
        if origin_exception:
            self.error = self._camel_case_error(type(origin_exception).__name__)
            self.reason = str(origin_exception)
        else:
            self.error = error

            self.reason = self.detail = reason
        self.stack = stack
        self.status_code = status_code

    def __str__(self):
        return self.reason if self.reason is not None else self.error

    @staticmethod
    def _camel_case_error(msg):
        if not msg:
            return ''
        if msg[0].isupper():
            out = msg[:1].lower()
        else:
            return msg
        for idx, c in enumerate(msg[1:], start=1):
            if c.isupper() and msg[idx + 1].isupper():
                out += msg[idx].lower()
            else:
                out += msg[idx:]
                break
        return out
