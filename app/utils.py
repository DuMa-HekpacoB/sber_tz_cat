class QueryParams(object):   #инициализирует параметры
    # нужен чтобы сделать из словаря инстанцию класса
    def __init__(self, query: dict):
        self.sort_age = query.get('sort_age')
        self.sort_name = query.get('sort_name')
        self.search_name = query.get('search_name')
        self.page = int(query.get('page', 1))
        self.size = int(query.get('size', 5))
        self.search_breed = query.get('search_breed')
        self.sort_breed = query.get('sort_breed')
        self.sort_rating = query.get('sort_rating')
        self.search_description = query.get('search_description')
        self.search_age = query.get('search_age')
