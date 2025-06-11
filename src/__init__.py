import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    db_folder = os.path.join(basedir, 'database')
    os.makedirs(db_folder, exist_ok= True)
    db_path = os.path.join(db_folder, 'Fruteria.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    #Se registran los endponit para ya quedar habilitados
    from src.routes.category_routes import category_bp
    app.register_blueprint(category_bp, url_prefix='/fruteria/v1')
    return app
