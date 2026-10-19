from src.errors.base import OperationError


class StaticCopyError(OperationError):
    """Raised when static/ can't be copied into dist/static/."""
