from src.errors.base import OperationError


class DistScaffoldError(OperationError):
    """Raised when dist/ can't be cleared and recreated."""
