from flask import Flask, request
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, mapper, declarative_base
from sqlalchemy.sql.expression import desc
engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres'
                       ':5432')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


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
dir_path: str = '../cats.db'

sql_request = '''
SELECT * FROM `cats` 
'''

def before_request_func():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    objects = []
    for i in range(20):
        objects.append(Cat(id=i, name=chr(i+97)+'Kot'+str(i), age=i+1,\
                                                          description='its \
                    cat '+str(i+1), rating=i % 6))
    session.bulk_save_objects(objects)
    session.commit()


class Cats(object):
    def __init__(self, path: str) -> None:
        self.path = path

    def get_id(self, _id: int) -> dict:
        return session.query(Cat).filter(Cat.id == _id).first()

    def get_list(self, params):

        cats = session.query(Cat)
        if params.search_name:
            cats = cats.filter(Cat.name.ilike(f'%{params.search_name}%'))
        type_sort_age = Cat.age if params.sort_age == 'ASC' else desc(Cat.age)
        type_sort_name = Cat.name if params.sort_name == 'ASC' else desc(
            Cat.name)
        cats = cats.p
        cats = cats.order_by(type_sort_age)
        cats = cats.order_by(type_sort_name)
        return cats.all()


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


before_request_func()
app.run(port=8080, debug=True, host='0.0.0.0')
