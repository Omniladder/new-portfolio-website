from src.errors.base import OperationError


class CoreAssetsCopyError(OperationError):
    """Raised when assets/core-assets/ can't be copied into dist/assets/core-assets/."""
