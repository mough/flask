from flask import Flask, render_template, request
from sqlalchemy import create_engine
import json

app = Flask(__name__)
app.config["DEBUG"] = True

recipe_data = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="mslavin",
    password="iamnotspam",
    hostname="mslavin.mysql.pythonanywhere-services.com",
    databasename="mslavin$MyData")

@app.route('/', methods=["GET"])
def index():
    return render_template("main_page.html")

@app.route('/recipes', methods=["GET"])
def get_recipes():
    title = request.args.get("name")
    category = request.args.get("category")
    url= request.args.get("url")

    engine = create_engine(recipe_data)
    sql_query_string = "select * from RecipeData where recipe_name LIKE '%{0}%' OR recipe_link = '{1}' OR category = '{2}';".format(title, url, category)
    print(sql_query_string)
    results = engine.execute(sql_query_string)
    return json.dumps([(dict(row.items())) for row in results])
