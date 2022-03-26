from flask import Flask
from routes import module_cats
from routes import Base, engine, Cat, session

app = Flask(__name__)
app.register_blueprint(module_cats)



def before_app_func():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    objects = []
    breed_list = ['scottish fold', 'egyptian mau', 'russian blue']
    for i in range(20):
        objects.append(
            Cat(
                id=i,
                name=chr(i + 97) + 'Kot' + str(i),
                age=i + 1,
                description='its cat ' + str(i + 1) + '.His a nice cat!',
                rating=i % 6,
                breed=breed_list[i % len(breed_list)],
                img_path=f'{i + 1}.jpeg',
            )
        )
    session.bulk_save_objects(objects)
    session.commit()



before_app_func()
app.run(port=8080, debug=True, host='0.0.0.0')
