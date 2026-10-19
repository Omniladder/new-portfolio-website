from src.errors.base import OperationError


class PageGenerationError(OperationError):
    """Raised when a page template can't be rendered to dist/."""
