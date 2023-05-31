import os

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True) # load the instance config, if it exists, when not testing
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path) # ensure the instance folder exists
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/') # a simple page that says hello
    def index():
        return 'Hello, World!'

    return app