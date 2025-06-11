class SessyException(Exception):
    pass

class SessyLoginException(SessyException):
    pass

class SessyNotSupportedException(SessyException):
    pass

class SessyConnectionException(SessyException):
    pass

class SessyUnavailableException(SessyException):
    pass
