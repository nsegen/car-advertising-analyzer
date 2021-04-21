import aiohttp
import asyncio
from .data_items import (
    DataItem, 
    Pagination,
)

class RequestsManager:
    def __init__(self, url):
        self.base_url = url
        self.session = aiohttp.ClientSession()
        self.lock = False

    async def _parse_response(self, response):
        if response.content_type == 'application/json':
            return await response.json()
        
        print('WARN')
        print(response)

        return None

    async def _make_request(self, params):
        async with self.session.get(self.base_url, params=params) as response:
            return await self._parse_response(response)

    async def fetch(self, params):
        while self.lock:
            await asyncio.sleep(0.1)
        self.lock = True
        response = await self._make_request(params)
        self.lock = False

        return response

    async def close(self):
        return await self.session.close()

    async def __aenter__(self):
            return self

    async def __aexit__(self, type, value, traceback):
        return await self.close()

class BaseDataSource:

    base_url = None

    def __init__(self):
        self.requests_manager = RequestsManager(self.base_url)

    def _process_items(self, items):
        return [DataItem(**item) for item in items]

    async def _fetch(self, **kwargs):
        return await self.requests_manager.fetch(kwargs)

    def _extract_pagination_info(self, data) -> Pagination:
        return Pagination(0, 0, 0)

    async def _get_pagination(self):
        data = await self._fetch()
        
        return self._extract_pagination_info(data)

    async def get_items(self):
        pass

    async def __aenter__(self):
            return self

    async def __aexit__(self, type, value, traceback):
        await self.requests_manager.close()
