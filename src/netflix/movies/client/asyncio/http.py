from __future__ import annotations

import logging
from http import HTTPStatus
from typing import TYPE_CHECKING, Awaitable, Callable, Iterable, Mapping

import aiohttp
from aiohttp import ContentTypeError

from netflix.movies.client.asyncio import exceptions
from netflix.movies.client.http import _exception_message
from netflix.movies.client.version import __version__

if TYPE_CHECKING:
    from netflix.movies.client.types import TimeoutScalarType


class AsyncMovieSession(aiohttp.ClientSession):
    """Async HTTP session for working with Netflix Movies API."""

    base_api_path: str = "/api/v1"

    timeout: TimeoutScalarType = 3
    max_attempts: int = 3

    log = logging.getLogger(__name__)

    _base_request = aiohttp.ClientSession._request

    def __init__(
        self,
        base_url: str, *,
        timeout: TimeoutScalarType | None = None,
        max_attempts: int | None = None,
    ) -> None:
        super().__init__()
        self.headers["User-Agent"] = f"movies.async_client/{__version__}"
        self.headers["Accept"] = "application/json,*/*;q=0.9"
        self.base_url = base_url.rstrip("/")
        self.base_api_url = f"{self.base_url}{self.base_api_path}"
        if timeout is not None:
            self.timeout = timeout
        if max_attempts is not None:
            assert max_attempts > 0
            self.max_attempts = max_attempts

    async def _request(
        self, method: str, url: str, *, max_attempts: int | None = None, **kwargs,
    ) -> aiohttp.ClientResponse:
        log_msg = f"{method.upper()} {url}"
        if "params" in kwargs:
            log_msg = f"{log_msg} with query params: {kwargs['params']}"
        if "json" in kwargs:
            log_msg = f"{log_msg} with JSON body: {kwargs['json']}"
        self.log.debug(log_msg)
        if url.startswith("/"):
            url = f"{self.base_api_url}{url}"
        if max_attempts is None:
            max_attempts = self.max_attempts
        else:
            assert max_attempts > 0
        return await self._retry(self.__request, args=(method, url), kwargs=kwargs, max_attempts=max_attempts)

    async def __request(
        self, method: str, url: str, *, timeout: TimeoutScalarType | None = None, **kwargs,
    ) -> aiohttp.ClientResponse:
        kwargs["timeout"] = timeout or self.timeout
        response = await self._base_request(method, url, **kwargs)
        if response.ok:
            return response
        raise exceptions.HTTPError(response, HTTPStatus(response.status), await self._get_error_dict(response))

    async def _retry(
        self,
        func: Callable[..., Awaitable[aiohttp.ClientResponse]],
        args: Iterable,
        kwargs: Mapping,
        max_attempts: int,
    ) -> aiohttp.ClientResponse:
        _exc: Exception | None = None
        error_attempt = 1
        errors: list[Exception] = []
        while error_attempt <= max_attempts:
            try:
                return await func(*args, **kwargs)
            except (OSError, exceptions.ServerError) as exc:
                self.log.warning(f"attempt {error_attempt} failed: {_exception_message(exc)}")
                _exc = exc
                error_attempt += 1
                errors.append(exc)
        raise exceptions.MaxAttemptsError(errors, attempts=max_attempts) from _exc

    async def _get_error_dict(self, response: aiohttp.ClientResponse) -> dict | None:
        try:
            response_json = await response.json()
        except (ValueError, ContentTypeError):
            self._error_dict = None
            return None
        if not isinstance(response_json, dict):
            self.log.warning(f"Unexpected error body: {response_json!r}")
            self._error_dict = None
        else:
            self._error_dict = response_json
        return self._error_dict
