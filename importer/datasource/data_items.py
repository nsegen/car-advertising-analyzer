class DataItem:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class Pagination:
    def __init__(self, page_size, pages, total):
        self.page_size = page_size
        self.pages = pages
        self.total = total
