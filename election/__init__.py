import os
from flask import Flask
from . import db
from . import results


def create_app(test_config=None):
    # create and configure the create_app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'election.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if paassed input
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Make functions availabe to Jinja template
    app.jinja_env.globals.update(sort=sorted, enum=enumerate)

    db.init_app(app)
    # register blueprints
    app.register_blueprint(results.bp)
    app.add_url_rule("/", endpoint='index')

    return app
