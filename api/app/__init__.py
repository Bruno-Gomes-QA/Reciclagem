from flask import Flask, g
from flask_pydantic_spec import FlaskPydanticSpec
import os
from dotenv import load_dotenv
from database import Database
from resources.products import create_products_blueprint
from resources.departments import create_departments_blueprint

def create_app():

    load_dotenv()

    user = os.environ['USERMYSQL']
    password = os.environ['PASSWORD']
    host = os.environ['HOST']
    port = os.environ['PORT']
    data = os.environ['DATABASE']

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}:{port}/{data}'
    
    db = Database(app.config['SQLALCHEMY_DATABASE_URI'])
    
    spec = FlaskPydanticSpec('flask', title='API')
    spec.register(app)
    
    app.db = db 
    app.register_blueprint(create_products_blueprint(spec))
    app.register_blueprint(create_departments_blueprint(spec))
    
    @app.before_request
    def before_request():
        g.db_session = app.db.get_session()

    @app.teardown_request
    def teardown_request(exception=None):
        db_session = g.pop('db_session', None)
        if db_session is not None:
            db_session.close()

    return app

def create_testing_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor@localhost:3306/test'
    
    db = Database(app.config['SQLALCHEMY_DATABASE_URI'])
    
    spec = FlaskPydanticSpec('flask', title='API')
    spec.register(app)
    
    app.db = db 
    app.register_blueprint(create_products_blueprint(spec))
    app.register_blueprint(create_departments_blueprint(spec))
    
    @app.before_request
    def before_request():
        g.db_session = app.db.get_session()

    @app.teardown_request
    def teardown_request(exception=None):
        db_session = g.pop('db_session', None)
        if db_session is not None:
            db_session.close()

    return app

