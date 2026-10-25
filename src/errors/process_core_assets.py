from src.errors.base import OperationError


class CoreAssetsProcessingError(OperationError):
    """Raised when a file in assets/core-assets/ can't be processed into dist/."""
