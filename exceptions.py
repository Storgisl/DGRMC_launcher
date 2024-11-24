class CustomException(Exception):
    def __init__(self, message, error_code=None):
        self.message = message
        self.error_code = error_code
        super().__init__(message, error_code)


class UserDataException(CustomException):
    def __init__(self, message="User data error", error_code=1):
        # You can pass a default message or customize it when raising the exception
        super().__init__(message, error_code)

# UserOptionsException subclass
class UserOptionsException(CustomException):
    def __init__(self, message="User options error", error_code=2):
        # You can pass a default message or customize it when raising the exception
        super().__init__(message, error_code)


class UserDirException(CustomException):
    def __init__(self, message="User dir error", error_code=3):
        # You can pass a default message or customize it when raising the exception
        super().__init__(message, error_code)
