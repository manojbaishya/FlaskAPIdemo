from datetime import datetime
from sqlite3 import Connection as SQLite3Connection

from sqlalchemy import event
from sqlalchemy.engine import Engine

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy


# ======= sqlite3 foreign key constraint =======
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


# ======= main app =======
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
now = datetime.now()


# data models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    post = db.relationship("Blogpost")


class BlogPost(db.Model):
    __tablename__ = "blogpost"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(500))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# ======= app routes =======
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.j2")


@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name=data["name"],
        email=data["email"],
        address=data["address"],
        phone=data["phone"],
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created."}), 200


@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    pass


@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    pass


@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    pass


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    pass


@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    pass


@app.route("/user/<user_id>", methods=["GET"])
def get_all_blog_posts(user_id):
    pass


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_blog_posts(user_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
