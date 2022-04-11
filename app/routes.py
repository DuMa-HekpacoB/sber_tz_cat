from flask import request, send_file, Blueprint
from utils import QueryParams
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.expression import desc

module_cats = Blueprint('module_cats', __name__)

engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres:5432')
#engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5433')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


class Cat(Base):
    __tablename__ = 'cats'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    breed = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    img_path = Column(String)


class Cats(object):
    @classmethod
    def get_id(cls, _id: int):
        return session.query(Cat).filter(Cat.id == _id).first()

    @classmethod
    def get_list(cls, params):
        query_cats = session.query(Cat)
        if params.search_age:
            query_cats = query_cats.filter(Cat.age == params.search_age)
        if params.search_description:
            query_cats = query_cats.filter(
                Cat.description.ilike(f'%{params.search_description}%'))
        if params.sort_rating is not None:
            type_sort_rating = Cat.rating if params.sort_rating == 'ASC' else desc(
                Cat.rating)
            query_cats = query_cats.order_by(type_sort_rating)
        if params.search_breed:
            query_cats = query_cats.filter(Cat.breed.ilike(f'%{params.search_breed}%'))
        if params.search_name:
            query_cats = query_cats.filter(Cat.name.ilike(f'%{params.search_name}%'))
        if params.sort_breed:
            type_sort_breed = Cat.breed if params.sort_breed == 'ASC' else desc(
                Cat.breed)
            query_cats = query_cats.order_by(type_sort_breed)
        if params.sort_age is not None:
            type_sort_age = Cat.age if params.sort_age == 'ASC' else desc(
                Cat.age)
            query_cats = query_cats.order_by(type_sort_age)
        if params.sort_name is not None:
            type_sort_name = Cat.name if params.sort_name == 'ASC' else desc(
                Cat.name)
            query_cats = query_cats.order_by(type_sort_name)
        count_cats = query_cats.count()
        query_cats = query_cats.limit(params.size).offset((params.page - 1) * params.size)
        return query_cats.all(), count_cats


@module_cats.route('/images/<path:name_file>', methods=['GET'])
def up_photo(name_file):
    return send_file(f'cats_image/{name_file}', mimetype='image/jpeg')


@module_cats.route('/cats', methods=['GET'])
def list_cats() -> str:
    params = QueryParams(request.args)
    cats, count_cats = Cats.get_list(params)

    result = f'''
    <table>
        <tr>
            <td>id</td>
            <td>name</td>
            <td>age</td>
            <td>description</td>
            <td>breed</td>
            <td>rating</td>
            <td>photo</td>
        </tr>
        <tr>
            <td></td>
            <td>
            <a href='/cats?sort_name=ASC'>↑</a>
            <a href='/cats?sort_name=DESC'>↓</a>
            </td>
            <td>
            <a href='/cats?sort_age=ASC'>↑</a>
            <a href='/cats?sort_age=DESC'>↓</a>
            </td>
            <td></td>
            <td>
            <a href='/cats?sort_breed=ASC'>↑</a>
            <a href='/cats?sort_breed=DESC'>↓</a>
            </td>
            <td>
            <a href='/cats?sort_rating=ASC'>↑</a>
            <a href='/cats?sort_rating=DESC'>↓</a>
            </td>
        </tr>
    '''
    for row in cats:
        result += f'''
        <tr>
            <td>{row.id}</td>
            <td><a href='/cats/{row.id}'>{row.name}</a></td>
            <td>{row.age}</td>
            <td>{row.description}</td>
            <td>{row.breed}</td>
            <td>{row.rating}</td>
            <td><img src="/images/{row.img_path}" 
  width="100" height="100" alt="lorem"></td>
        </tr>
        '''
    result += '</table>'
    pages = count_cats // params.size + 1 if count_cats % params.size != 0 \
        else count_cats // params.size
    for i in range(pages):
        result += f'''
        <a href='/cats?{params.to_query_str(page=i+1)}'>{i + 1}</a>
        '''
    return result


@module_cats.route('/cats/<int:cat_id>', methods=['GET'])
def one_cat(cat_id):
    cat = Cats.get_id(cat_id)
    if cat is None:
        return 'извините кота не нашли'
    else:
        result = f'''
        <table>
            <tr>
                <td>id</td>
                <td>{cat_id}</td>
            </tr>
            <tr>
                <td>name</td>
                <td>{cat.name}</td>
            </tr>
            <tr>
                <td>age</td>
                <td>{cat.age}</td>
            </tr>
            <tr>
                <td>description</td>
                <td>{cat.description}</td>
            </tr>
            <tr>
                <td>breed</td>
                <td>{cat.breed}</td>
            </tr>
            <tr>
                <td>rating</td>
                <td>{cat.rating}</td>
            </tr>
        </table>
        <a href='/cats'>Показать всех котиков!</a>
        '''
    return result
