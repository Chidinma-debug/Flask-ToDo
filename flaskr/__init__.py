#init.py contains application factory and tells python that flaskr dir should be treated as a package
import os
from flask import Flask, appcontext_popped

def create_app(test_config=None):
    #create and configure the app
    #instance_rel... tells the app that configuration files are relative to the instance folder. The instance
    #folder is located outside flaskr
    app = Flask(__name__, instance_relative_config=True)
    #app.config.from_mapping sets default configuration that the app will use. Secret key keeps data safe
    # database is the path where sqlite file will be saved
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    if test_config is None:
        #load the instance config, if it exists, when not testing
        #app.config.from_pyfile overrides default configuration with values taken from configp.py file in instance folder
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)
    #ensure the instance folder exists
    try:
        #os.makedirs ensures the instace folder (app.instance_path) exists
        os.makedirs(app.instance_path)
    except OSError:
        pass
    @app.route("/hello")
    def hello():
        return "Hello World!"
    
    from . import db
    db.init_app(app)
    return app
#import and call the function in db.py from the factory
    

