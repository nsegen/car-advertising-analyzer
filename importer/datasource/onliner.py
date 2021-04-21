import asyncio
from .base import BaseDataSource
from .data_items import Pagination

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
        loaders = [self._load_page(page, pagination.page_size) for page in range(1, pagination.pages + 1)]
        
        return await asyncio.gather(*loaders)