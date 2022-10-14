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


'''
 we get email and password from the body
 we validate that the email and password match in the database
 if it is correct to return in a json to the name of the user and his id
 if it is not correct return a credential error 
'''

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(50), nullable=False)

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
    query = "SELECT * FROM user WHERE email = '{0}' AND password ='{1}' ".format(email,password)
    results = db.session.execute(query)

   
    if results :
        return  jsonify({"user_data":users_schema.dump(results)}) 

    else :
        return jsonify({'Message': "User not found.", 'successful': False})


# Endpoint to create a new user
@app.route('/user/add', methods=["POST"])
def add_user():
    name = request.json['name'] 
    email = request.json['email'] 
    password = request.json['password']

    new_user = User(name,email,password) 
    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return blog_schema.jsonify(user) 


# Endpoint for updating a user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    name.name = name    
    email.name = email    
    password.name = password    

    db.session.commit()
    return user_schema.jsonify(user)


# Endpoint to query all users
@app.route("/users", methods=["GET"])
def get_allusers():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result)








if __name__ == '__main__':
    app.run(debug=True)