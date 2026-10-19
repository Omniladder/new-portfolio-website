from src.errors.base import OperationError


class AssetProcessingError(OperationError):
    """Raised when an image in assets/ can't be processed into dist/assets/."""
