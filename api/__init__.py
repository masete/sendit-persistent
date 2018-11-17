
from flask import Flask


def create_app():

    app = Flask(__name__)
    #app.config['JWT_SECRET_KEY'] = 'masete'

    from api.views.parcels import parcel_blueprint as parcel_blueprint
    from api.views.auth import user_blueprint as user_blueprint

    app.register_blueprint(parcel_blueprint)
    app.register_blueprint(user_blueprint)

    return app
