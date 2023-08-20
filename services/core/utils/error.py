class Error(object):
    def __init__(self, error, reason, stack=None):
        if stack is None:
            stack = []
        self.error = error
        self.reason = reason

        if stack.__len__() == 0 or stack[0] is None or not hasattr(stack[0], 'error') or stack[0].error != self.error:
            stack.insert(0, self)
        self.__stack = stack

    @property
    def stack(self):
        return self.__stack

    @stack.setter
    def stack(self, stack):
        if stack.__len__() == 0 or stack[0] is None or not hasattr(stack[0], 'error') or stack[0].error != self.error:
            stack.insert(0, self)
        self.__stack = stack
