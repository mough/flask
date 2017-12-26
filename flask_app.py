
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine

app = Flask(__name__)
app.config["DEBUG"] = True


# SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     username="mslavin",
#     password="iamnotspam",
#     hostname="mslavin.mysql.pythonanywhere-services.com",
#     databasename="mslavin$MyData")

# SQLALCHEMY_BINDS = {
#     # comments: "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     # username="mslavin",
#     # password="iamnotspam",
#     # hostname="mslavin.mysql.pythonanywhere-services.com",
#     # databasename="mslavin$comments")

#     recipe_data: "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     username="mslavin",
#     password="iamnotspam",
#     hostname="mslavin.mysql.pythonanywhere-services.com",
#     databasename="mslavin$MyData")
#     }
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)

# class Comment(db.Model):
#     __bind_key__ = "comments"
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(4096))

# class Recipes(db.Model):
#     __bind_key__ = "recipes"
#     id = db.Column(db.Integer, primary_key=True)
#     recipe_name = db.Column(db.String(100))
#     recipe_link = db.Column(db.String(100))


recipe_data = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="mslavin",
    password="iamnotspam",
    hostname="mslavin.mysql.pythonanywhere-services.com",
    databasename="mslavin$MyData")

engine = create_engine(recipe_data, convert_unicode=True)
comments = []
results = []

@app.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        results = engine.execute('select * from RecipeData;')
        return render_template("main_page.html", results=results)
        #return render_template("main_page.html", comments=Comment.query.all(), results=results)

# @app.route('/add_comment/', methods=['POST'])
# def add_comment():
#     comment = Comment(content=request.form["comment_text"])
#     db.session.add(comment)
#     db.session.commit()
#     return redirect(url_for('index'))

@app.route('/get_recipes/', methods=['POST'])
def get_recipes():
    zip_code = request.form["zip_code"]
    cuisine_pref = request.form["cuisine_pref"]
    return "zip_code: %s  cuisine_pref: %s" % (zip_code, cuisine_pref)
    #return redirect(url_for('index'))


@app.route('/bananas')
def hello_bananas():
    return 'Hello from Flask! Also, bananas!'
