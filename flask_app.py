from __future__ import print_function
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
#from car_data import get_cars_by  # Week 12 Day 1 Sample Demo code
import json
import sys

app = Flask(__name__)
app.config["DEBUG"] = True

recipe_data = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="code2college",
    password="iamnotspam",
    hostname="code2college.mysql.pythonanywhere-services.com",
    databasename="code2college$MyData")

### START Week12 Day 1 demo code ###
# @app.route('/', methods=["GET"])
# def index():
#     return render_template("week12day1examplecode.html")

# @app.route('/carsearch', methods=["GET"])
# def car_search():
#     #print "Entering method car_search"

#     year = request.args["year"] if request.args.has_key("year") else None
#     make = request.args["make"] if request.args.has_key("make") else None
#     model = request.args["model"] if request.args.has_key("model") else None

#     #print "year: " + year + " make: " + make + " model: " + model

#     result = {"message": "No results"}

#     result["rows"] = get_cars_by(year, make, model)


#     if result["rows"]:
#         result["message"] = str(len(result["rows"])) + " results"

#     return jsonify(result)

### END Week12 Day 1 demo code ###


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
    # we're adding this limit to cover the scenario the user didn't supply any
    # paramters. We don't want to return ALL the rows in our DB!
    query_string += " limit 1"

    return query_string, params
