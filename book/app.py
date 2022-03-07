from flask import Flask
from routes import book_blueprint
from flask_migrate import Migrate
from models import db,Book,init_app

app = Flask(__name__)
app.config["SECRET_KEY"] = "3qRZDlu0jKV2cW2SD0m7qg"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./database/book.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.register_blueprint(book_blueprint)
init_app(app=app)


migrate = Migrate(app,db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
