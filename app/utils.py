import copy

class QueryParams(object):  # инициализирует параметры
    # нужен чтобы сделать из словаря инстанцию класса
    def __init__(self, query: dict):
        self._old_query = query
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

    def to_query_str(self, **kwargs) -> str:
        # params = {
        #     'search_age': self.search_age,
        #     'search_description': self.search_description,
        #     'sort_rating': self.sort_rating,
        #     'sort_breed': self.sort_breed,
        #     'search_breed': self.search_breed,
        #     'size': self.size
        #
        # }
        result = []
        old_query = dict(copy.deepcopy(self._old_query))
        old_query.update(kwargs)
        for i_name_param, i_value_param in old_query.items():
            some_string = i_name_param + '=' + str(i_value_param)
            result.append(some_string)
        return '&'.join(result)
