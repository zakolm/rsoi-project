from unittest import mock

import aiohttp
import fastapi
from aiohttp import ClientSession
import asyncio


class CircuitBreakerSession(ClientSession):
    closed: bool = False
    closing_interval_sec: int = 5
    max_attempts = 3
    _lock: asyncio.Lock = asyncio.Lock()

    async def _delayed_request(self, *args, **kwargs):
        await asyncio.sleep(self.closing_interval_sec)
        self.closed = False
        print('open cb')
        resp = await self._request(*args, **kwargs, raise_exception=False)
        if resp:
            print('queued request succeed')
            await resp.release()

    async def _request(self, *args, ensure=False, raise_exception=False, **kwargs):
        if not self.closed:
            async with self._lock:
                for _ in range(self.max_attempts):
                    try:
                        print('try request')
                        response = await super()._request(*args, **kwargs, timeout=300)
                        if response.content_type != 'application/json':
                            raise Exception
                        return response
                    except:
                        continue
                print('close cb')
                self.closed = True
                if ensure:
                    print('request added to queue')
                    asyncio.create_task(self._delayed_request(*args, ensure=ensure, **kwargs))
        if raise_exception:
            raise Exception
        else:
            fallback_response = mock.MagicMock()
            fallback_response.json = mock.AsyncMock()
            fallback_response.json.return_value = {}
            return fallback_response
