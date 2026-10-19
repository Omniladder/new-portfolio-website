from src.errors.base import OperationError


class DownloadsCopyError(OperationError):
    """Raised when assets/download/ can't be copied into dist/assets/download/."""
