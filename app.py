from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False)
    content = db.Column(db.String, unique=False)
    image = db.Column(db.String, unique=False)

    def __init__(self, title, content, image):
        self.title = title
        self.content = content
        self.image = image


class BlogSchema(ma.Schema):
    class Meta:
        fields = ("id", 'title', 'content','image')


blog_schema = BlogSchema() 
blogs_schema = BlogSchema(many=True) 

# Endpoint for deleting a record
@app.route("/", methods=["GET","POST"])
def home():
    return "Tarrance API is Working"




# Endpoint to create a new blog
@app.route("/blog", methods=["POST"])
def add_blog():
    title = request.json['title']
    content = request.json['content']
    image = request.json['image']
    
    new_blog = Blog(title, content, image)

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

def read_blog(id):
    try:
        blog= db(id)
        if blog != None:
            return jsonify({'blog': blog, 'Message': "blog found.", 'successful': True})
        else:
            return jsonify({'Message': "blog not found.", 'successful': False})
    except Exception as ex:
        return jsonify({'Message': "Error", 'successful': False})






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

    return "Blog was successfully deleted"




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(50), unique=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password 

class UserSchema(ma.Schema):
    class Meta:
        fields = ('name', 'email', 'password')      


user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Endpoint query login
@app.route('/login', methods=["POST"])
def read_user():
    email = request.json['email'] 
    password = request.json['password'] 

    user = db.session.query(User).filter(User.email == email).first()

    if user is None:
        return jsonify({'successful': False})
    if user.password !=password:
        return jsonify({'successful': False})


    return jsonify({ 'successful': True})









# Endpoint to create a new user
@app.route('/user', methods=["POST"])
def add_user():
    name = request.json['name'] 
    email = request.json['email'] 
    password = request.json['password']

    new_user = User(name, email, password) 
    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return user_schema.jsonify(user)



   # Endpoint to query user
@app.route("/user", methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result) 




if __name__ == '__main__':
    app.run(debug=True)