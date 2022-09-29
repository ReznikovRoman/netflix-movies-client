from .version import __version__

# XXX: Для сборки пакета setuptools'ами
try:
    from .asynchronous import AsyncMovieClient, AsyncMovieSession, init_async_movie_client
    from .clients import MovieClient, init_movie_client
    from .http import MovieSession
except ImportError:
    pass

__all__ = [
    "__version__",
    "MovieSession",
    "MovieClient",
    "init_movie_client",
    "AsyncMovieSession",
    "AsyncMovieClient",
    "init_async_movie_client",
]
