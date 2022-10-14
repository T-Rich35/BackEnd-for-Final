from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)




class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False)
    content = db.Column(db.String, unique=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content


class BlogSchema(ma.Schema):
    class Meta:
        fields = ("id", 'title', 'content')


blog_schema = BlogSchema() 
blogs_schema = BlogSchema(many=True) 


# Endpoint to create a new blog
@app.route("/blog", methods=["POST"])
def add_blog():
    title = request.json['title']
    content = request.json['content']
    
    new_blog = Blog(title, content)

    db.session.add(new_blog)
    db.session.commit()

    blog = Blog.query.get(new_blog.id)

    return blog_schema.jsonify(blog)


# Endpoint to query all blogs
@app.route("/blogs", methods=["GET"])
def get_allblogs():
    all_blogs = Blog.query.all()
    result = blogs_schema.dump(all_blogs)

    return jsonify(result)


# Endpoint for querying a single blog
@app.route("/blog/<id>", methods=["GET"])
def get_blog(id):
    blog = Blog.query.get(id)
    return blog_schema.jsonify(blog)


# Endpoint for updating a blog
@app.route("/blog/<id>", methods=["PUT"])    
def blog_update(id):
    blog = Blog.query.get(id)
    title = request.json['title']
    content = request.json['content']
    blog.title = title
    blog.content = content

    db.session.commit()
    return blog_schema.jsonify(blog)


# Endpoint for deleting a record    
@app.route("/blog/<id>", methods=["DELETE"])
def blog_delete(id):
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()

    return "Blog was deleted"



if __name__ == '__main__':
    app.run(debug=True)