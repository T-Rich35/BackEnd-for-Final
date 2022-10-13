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





if __name__ == '__main__':
    app.run(debug=True)