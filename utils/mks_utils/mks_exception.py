class MKSException(Exception):
    def __init__(self, message):
        super().__init__(message)
    
class CLIRuntimeError(MKSException):
    def __init__(self, errors=""):
        super().__init__("CLI Runtime Error")
        self.errors = errors
    
    def __str__(self):
        return "CLI Runtime Error\n" + self.errors

class CLISyntaxError(MKSException):
    def __init__(self, errors=""):
        super().__init__("CLI Syntax Error")
        self.errors = errors
    
    def __str__(self):
        return "CLI Syntax Error\n" + self.errors

class MKSConnectTimeoutError(MKSException):
    def __init__(self, timeout=None):
        timeout_mess = f"(in {timeout} seconds)" if timeout else ""
        super().__init__(f"MKS connect timeout {timeout_mess}")

class ProjectNotFoundError(MKSException):
    def __init__(self, errors=""):
        super().__init__("Project not found")
        self.errors = errors
    
    def __str__(self):
        return "Project not found\n" + self.errors