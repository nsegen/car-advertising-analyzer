import aiohttp
import asyncio

class DataItem:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class Pagination:
    def __init__(self, page_size, pages, total):
        self.page_size = page_size
        self.pages = pages
        self.total = total

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

class OnlinerDataSource(BaseDataSource):

    base_url = 'https://ab.onliner.by/sdapi/ab.api/search/vehicles'
    
    def __init__(self):
        super(OnlinerDataSource, self).__init__()  

    async def _fetch(self, **kwargs):
        kwargs['extended'] = str(True)
        return await super(OnlinerDataSource, self)._fetch(**kwargs)

    def _extract_pagination_info(self, data):
        return Pagination(data['page']['limit'], data['page']['last'], data['total'])

    async def _load_page(self, page, size) -> list:
        print(f'start {page}')
        data = await self._fetch(limit=size, page=page)
        print(f'end {page}')
        if not data:
            return []
        return self._process_items(data['adverts'])
    
    async def get_items(self):
        pagination = await self._get_pagination()
        pagination.pages = 10
        loaders = [self._load_page(page, pagination.page_size) for page in range(1, pagination.pages + 1)]
        
        return await asyncio.gather(*loaders)
