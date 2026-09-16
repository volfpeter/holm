from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING
from urllib.parse import urlsplit

from fastapi.responses import PlainTextResponse

if TYPE_CHECKING:
    from starlette.types import ASGIApp, Receive, Scope, Send


class OriginCheckMiddleware:
    """
    Same-origin check for state-changing requests.

    The `Origin` header is validated first, falling back to `Referer`. A candidate passes when
    its hostname and port match the request `Host` or one of `trusted_origins` - forwarded
    headers are not trusted. The scheme is ignored, and a `null` or unparsable `Referer` is
    treated as if the header was missing. An `Origin` that fails to resolve is always rejected.
    A missing or unparsable `Host` is always rejected as well.

    Requests without cookies are skipped by default, so non-browser clients keep working.
    """

    __slots__ = ("_allow_missing", "_app", "_skip_if_no_cookies", "_trusted_hosts")

    def __init__(
        self,
        app: ASGIApp,
        *,
        trusted_origins: Iterable[str] | None = None,
        allow_missing: bool = True,
        skip_if_no_cookies: bool = True,
    ) -> None:
        """
        Initialization.

        Arguments:
            app: The application.
            trusted_origins: Additional trusted origins for legitimate cross-origin requests,
                as full origins (`https://app.example.com`) or bare hosts (`app.example.com:8000`).
            allow_missing: Allow requests with neither an `Origin` nor a `Referer` header.
            skip_if_no_cookies: Skip the check for requests without a cookie header.
        """
        self._app = app
        self._allow_missing = allow_missing
        self._skip_if_no_cookies = skip_if_no_cookies
        self._trusted_hosts: frozenset[tuple[str, int | None]] = frozenset(
            candidate
            for origin in (trusted_origins or ())
            if (candidate := _get_hostname_and_port(origin))[0]
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("type") != "http" or scope.get("method") not in _UNSAFE_METHODS:
            await self._app(scope, receive, send)
            return

        headers: dict[bytes, bytes] = dict(scope.get("headers", []))

        if self._allow(headers):
            await self._app(scope, receive, send)
        else:
            response = PlainTextResponse("Origin check failed", status_code=403)
            await response(scope, receive, send)

    def _allow(self, headers: Mapping[bytes, bytes]) -> bool:
        if self._skip_if_no_cookies and b"cookie" not in headers:
            return True

        raw_host = headers.get(b"host")
        if raw_host is None:
            return False

        host = _get_hostname_and_port(raw_host.decode("latin-1"))
        if not host[0]:
            return False

        raw_origin = headers.get(b"origin")
        if raw_origin is not None:
            candidate = _get_hostname_and_port(raw_origin.decode("latin-1"))
            return self._is_trusted(candidate, host)

        raw_referer = headers.get(b"referer")
        if raw_referer is None or raw_referer == b"null":
            return self._allow_missing

        candidate = _get_hostname_and_port(raw_referer.decode("latin-1"))
        if not candidate[0]:
            return self._allow_missing

        return self._is_trusted(candidate, host)

    def _is_trusted(self, candidate: tuple[str, int | None], host: tuple[str, int | None]) -> bool:
        return candidate == host or candidate in self._trusted_hosts


_UNSAFE_METHODS: frozenset[str] = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def _get_hostname_and_port(url: str) -> tuple[str, int | None]:
    """Returns the lowercase hostname and port of a URL, origin, or bare host."""
    try:
        parsed = urlsplit(url if "://" in url else f"//{url}")
        hostname = parsed.hostname or ""
        port = parsed.port
    except ValueError:
        return ("", None)
    if not hostname:
        return ("", None)
    return (hostname, port)
