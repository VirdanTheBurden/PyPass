class PyPassException(Exception):
    """Creates a base exception class for PyPass exceptions to inherit. Inherits from Exception since the functionality
    of the program is being thrown into question."""

    pass


class FileCreationError(PyPassException):
    """Raised whenever a file / directory fails to be created."""

    pass