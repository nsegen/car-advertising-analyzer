import asyncio

from base_data_source import OnlinerDataSource

class BaseImporter:

    async def init(self):
        async with OnlinerDataSource() as base_importer:
            items = await base_importer.get_items()
            print(items)
            for page in items:
                print(len(page))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    importer = BaseImporter()

    loop.run_until_complete(importer.init())
