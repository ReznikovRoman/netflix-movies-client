import warnings


class WarnMethodMixin:
    """Mixin for creating custom warnings."""

    @classmethod
    def warn(cls, message: str, stacklevel: int = 2, *, prefix: str | None = None):
        if prefix:
            message = f"{prefix}: {message}"
        warnings.warn(message, cls, stacklevel + 1)


class InvalidPageSizeWarning(WarnMethodMixin, UserWarning):
    """Invalid pagination parameter warning."""
