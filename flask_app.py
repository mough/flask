from __future__ import print_function
from flask import Flask, render_template, request
from sqlalchemy import create_engine
import json
import sys

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
    name = request.args.get("name")
    category = request.args.get("category")
    url= request.args.get("url")
    # below is how we can print to our error log, will probably remove this once debugging is complete
    print("request recieved: name:{0} category: {1} url: {2}".format(name, category, url), file=sys.stderr)

    engine = create_engine(recipe_data)
    sql_query_string, params = create_query(name, category, url)
    # below is a good debug line, but will probably remove once debugging is complete
    print("sql_query_string: {0} params: {1}".format(sql_query_string, params), file=sys.stderr)
    # definition for this execute method signature here https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
    results = engine.execute(sql_query_string, params)
    return json.dumps([(dict(row.items())) for row in results])

def create_query(name, category, url):
    need_or_operator = False
    query_string = "SELECT recipe_name, recipe_link, category FROM RecipeData"
    params = ()
    # we will set convention to always add a space at the BEGINNING of the sql chunk we're adding
    if name != "":
        query_string += " WHERE recipe_name LIKE %s".format(name)
        need_or_operator = True
        params += ("%"+name+"%",)
    if category != "":
        if need_or_operator:
            query_string += " OR category = %s".format(category)
        else:
            query_string += " WHERE category = %s".format(category)
            need_or_operator = True
        params += (category,)
    if url != "":
        if need_or_operator:
            query_string += " OR recipe_link LIKE %s".format(url)
        else:
            query_string += " WHERE recipe_link LIKE %s".format(url)
        params += ("%"+url+"%",)

    return query_string, params
