from flask import Flask, request
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, mapper, declarative_base

engine = create_engine('sqlite:///cats.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base(bind=engine)

class Cat(Base):
    __tablename__ = 'cats'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    #breed = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    #img_path = Column(String)

    def __repr__(self) -> str:
        return f'{self.id} {self.name}'

Base.metadata.create_all()



app: Flask = Flask(__name__)
dir_path: str = 'cats.db'

sql_request = '''
SELECT * FROM `cats` 
'''

class Cats(object):
    def __init__(self, path: str) -> None:
        self.path = path

    def get_id(self, _id: int) -> dict:
        return session.query(Cat).filter(Cat.id == _id).first()

        with sqlite3.connect(self.path) as cats:
            cursor = cats.cursor()
            cursor.execute(sql_request)
            list_tuples_cat = cursor.fetchall()
            list_cat = []
            for tuples in list_tuples_cat:
                list_cat.append({
                    "id": tuples[0],
                    "name": tuples[1],
                    "age": tuples[2],
                    "bread": tuples[3],
                    "description": tuples[4],
                    "rating": tuples[5]})
            for row in list_cat:
                if int(row['id']) == _id:
                    return dict(row)

    def get_list(self, params):
        with sqlite3.connect(self.path) as cats:
            cursor = cats.cursor()
            '''
            list_cat = [dict(or_row) for or_row in reader]
            list_cat.sort(key=lambda x: x['age'], reverse=(params.sort_age ==
                                                           'ASK'))
            list_cat.sort(key=lambda x: x['name'], reverse=(params.sort_name
                                                            == 'ASK'))
            if params.search_name is not None:
                for dictik in list_cat.copy():
                    if params.search_name.lower() not in dictik['name'].lower():
                        list_cat.remove(dictik)
            if params.size * (params.page - 1) > len(list_cat):
                start_index = len(list_cat)
            else:
                start_index = params.size * (params.page - 1)
            if params.size * params.page > len(list_cat):
                end_index = len(list_cat)
            else:
                end_index = params.size * params.page
            end_list = list_cat[start_index: end_index]
            '''
            sql_request_for_all_cats = sql_request
            args_for_sql = []

            if params.search_name is not None:
                sql_request_for_all_cats += f'WHERE name LIKE ?'
                args_for_sql.append('%' + params.search_name + '%')

            sql_request_for_all_cats += 'ORDER BY '
            if params.sort_age == 'ASC':
                sql_request_for_all_cats += 'age ASC,'
            else:
                sql_request_for_all_cats += 'age DESC,'

            if params.sort_name == 'ASC':
                sql_request_for_all_cats += ' name ASC'
            else:
                sql_request_for_all_cats += ' name DESC'

            cursor.execute(sql_request_for_all_cats, args_for_sql)
            result = cursor.fetchall()
            return result


class QueryParams(object):
    def __init__(self, query: dict):
        self.sort_age = query.get('sort_age', 'ASC')
        self.sort_name = query.get('sort_name', 'ASC')
        self.search_name = query.get('search_name')
        self.page = int(query.get('page', 1))
        self.size = int(query.get('size', 5))


@app.route('/cats', methods=['GET'])
def list_cats() -> str:
    params = QueryParams(request.args)
    catalog = Cats(path=dir_path)
    return f'просто пробую вывести данные \n {catalog.get_list(params)}'


@app.route('/cats/<int:cat_id>', methods=['GET'])
def one_cat(cat_id):
    repo_cat = Cats(path=dir_path)
    return f'а тут надо вывести одного кота, допустим '\
           f'{repo_cat.get_id(cat_id)}'


app.run(port=8080, debug=True)
