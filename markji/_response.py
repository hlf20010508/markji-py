# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from typing import Any
from aiohttp import ClientResponse, ClientResponseError


class _ResponseWrapper:
    def __init__(self, response: ClientResponse):
        self._response = response

    async def json(self) -> Any:
        return await self._response.json()

    async def raise_for_status(self):
        response = self._response
        if not response.status == 200:
            # reason should always be not None for a started response
            assert response.reason is not None

            response.reason = f"{response.reason}: {await response.text()}"

            # If we're in a context we can rely on __aexit__() to release as the
            # exception propagates.
            if not response._in_context:
                response.release()

            raise ClientResponseError(
                response.request_info,
                response.history,
                status=response.status,
                message=response.reason,
                headers=response.headers,
            )
