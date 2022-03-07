from flask import Flask, g
from flask.sessions import SecureCookieSessionInterface
from flask_login import user_loaded_from_header
from routing import user_blueprint
import models
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"] = '3qRZDlu0jKV2cW2SD0m7qg'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///./database/user.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
models.init_app(app=app)

app.register_blueprint(user_blueprint)

migrate = Migrate(app,models.db)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get("Authorization")
    if api_key:

        api_key = api_key.replace('Basic ', '', 1)
        user = models.User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    return None


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args,
                                                                **kwargs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
