from src.errors.base import OperationError


class DataParseError(OperationError):
    """Raised when data.json can't be read as JSON or fails schema validation."""
