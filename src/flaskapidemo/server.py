from datetime import datetime
import random
from sqlite3 import Connection as SQLite3Connection
from types import SimpleNamespace as struct

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine


# ------------------------------- Local Imports ------------------------------ #
import linked_list
import hash_table
import binary_search_tree
import stack_queue


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
    post = db.relationship("BlogPost", cascade="all, delete")


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
    users = User.query.all()

    users_llist = linked_list.LinkedList()

    for user in users:
        users_llist.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    return jsonify(users_llist.to_list()), 200


@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    users = User.query.all()

    users_llist = linked_list.LinkedList()

    for user in users:
        users_llist.append(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    return jsonify(users_llist.to_list()), 200


def compare_id(data, user_id):
    return True if data["id"] == user_id else False


@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    users = User.query.all()

    users_llist = linked_list.LinkedList()

    for user in users:
        users_llist.append(
            data={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    target_user = users_llist.search(attr=int(user_id), match=compare_id)

    if target_user is not None:
        return jsonify(target_user), 200
    else:
        return jsonify({"message": "User not found!"}), 400


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user_to_delete = User.query.filter_by(id=user_id).first()
    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({"message": "User deleted."}), 200


@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    data = request.get_json()

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User does not exist."}), 400

    blogposts = hash_table.HashTable(10)
    post = struct(title=data["title"], body=data["body"], date=now, user_id=user_id)

    # Demo code to insert into the hashtable
    blogposts.insert(key=user.name, value=post)
    # Demo code to search the hashtable
    content = blogposts.search(key=user.name)
    newPost = BlogPost(
        title=content.title,
        body=content.body,
        date=content.date,
        user_id=content.user_id,
    )

    """Alternative way to insert (DIRECT):
    newPost = BlogPost(
        title=data["title"],
        body=data["body"],
        date=now,
        user_id=user_id
    )
    """

    db.session.add(newPost)
    db.session.commit()

    return (
        jsonify({"message": f"Blogpost successfully added for user {user.name}!"}),
        200,
    )


def compare_post_id(probe, cursor):
    if probe["id"] < cursor["id"]:
        return -1
    elif probe["id"] > cursor["id"]:
        return 1
    elif probe["id"] == cursor["id"]:
        return 0


def compare_post_id_by_key(blogpost_id, cursor):
    if blogpost_id < cursor["id"]:
        return -1
    elif blogpost_id > cursor["id"]:
        return 1
    elif blogpost_id == cursor["id"]:
        return 0


@app.route("/blog_post/<blogpost_id>", methods=["GET"])
def get_one_blog_post(blogpost_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)

    bst = binary_search_tree.BinarySearchTree()

    for post in blog_posts:
        bst.insert(
            data={
                "id": post.id,
                "title": post.title,
                "body": post.body,
                "user_id": post.user_id,
            },
            compare=compare_post_id,
        )

    target_post = bst.search(key=int(blogpost_id), compare=compare_post_id_by_key)

    if target_post is None:
        return jsonify({"message": "Blog post does not exist."}), 400
    else:
        return jsonify(target_post), 200


@app.route("/user/blog_post/<user_id>", methods=["POST"])
def insert_multiple_blogposts(user_id):
    blogposts = request.get_json()

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User does not exist."}), 400

    post_queue = stack_queue.Queue()

    for post in blogposts:
        post_queue.enqueue(data=post)

    for _ in range(post_queue.length):
        post = post_queue.dequeue()
        record = BlogPost(
            title=post["title"], body=post["body"], date=now, user_id=user_id
        )

        db.session.add(record)
        db.session.commit()

    return (
        jsonify(
            {
                "message": f"{len(blogposts)} blogpost/s successfully added for user {user.name}!"
            }
        ),
        200,
    )


@app.route("/user/blog_post/<user_id>", methods=["GET"])
def get_all_blog_posts(user_id):
    pass


@app.route("/blog_post/delete_last_ten", methods=["DELETE"])
def delete_last_ten_blogposts():
    blogposts = BlogPost.query.all()

    post_stack = stack_queue.Stack()

    for post in blogposts:
        post_stack.push(post)

    for _ in range(10):
        post_to_delete = post_stack.pop()
        db.session.delete(post_to_delete)
        db.session.commit()

    return jsonify({"message": "Deleted last ten blog posts."}), 200


@app.route("/blog_post/<blogpost_id>", methods=["DELETE"])
def delete_one_blog_post(user_id):
    pass


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_all_blog_posts(user_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
