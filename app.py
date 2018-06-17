# import necessary libraries

import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, desc

from flask import Flask, jsonify, render_template

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

engine = create_engine('sqlite:///db/wine.sqlite')

Base = automap_base()
Base.prepare(engine, reflect=True)

Wine = Base.classes.wine
Coordinate = Base.classes.coordinate


session = Session(engine)

#################################################
# Routes
#################################################

@app.route("/")
def index():
    return render_template('index.html')
    
@app.route('/variety')
def varieties():

    stmt = session.query(Wine).statement
    wine_df = pd.read_sql_query(stmt, session.bind)
    wine_unique = wine_df.variety.unique()
    
    cleanedList = [x for x in wine_unique if str(x) != 'None']
    return jsonify(cleanedList)

@app.route('/country')
def counts():

    stmt = session.query(Wine).statement
    con_df = pd.read_sql_query(stmt, session.bind)
    con_unique = con_df.country.unique()
    
    con_cleanedList = [x for x in con_unique if str(x) != 'None']
    return jsonify(con_cleanedList)

@app.route("/coords")
def coordinate():
    stmt = session.query(Coordinate).statement
    region_df = pd.read_sql_query(stmt, session.bind)
    data = [{
        "region": region_df["region_1"].values.tolist(),
        "country": region_df["country"].values.tolist(),
        "coordinates": region_df["coordinates"].values.tolist()
    }]
    return jsonify(data)

@app.route('/type/<varietyname>')
def wines(varietyname):

    variety_stmt = session.query(Wine).statement
    df = pd.read_sql_query(variety_stmt, session.bind)
    
    if varietyname not in df.variety.unique():
        return jsonify(f"Error: Variety: {variety} Not Found!"), 400
    
    data = [{
        "region": df["region_1"].values.tolist(),
        "rating": df["points"].values.tolist(),
        "price": df["price"].values.tolist(),
        "title": df["title"].values.tolist()
    }]
    return jsonify(data)


@app.route('/country/<country>')
def countries(country):

    country_stmt = session.query(Wine).statement
    df = pd.read_sql_query(country_stmt, session.bind)
    
    if country not in df.country.unique():
        return jsonify(f"Error: Region: {region} Not Found!"), 400
    
    data = [{
        "variety": df["variety"].values.tolist(),
        "rating": df["points"].values.tolist(),
        "price": df["price"].values.tolist(),
        "title": df["title"].values.tolist()
    }]
    return jsonify(data)
    
@app.route("/varieties/<variety>")
@app.route("/varieties/<variety>/<country>")
def varcon(variety=None, country=None):
    

    # Select statement
    sel = [Wine.country, Wine.price, Wine.title]

    if not country:
        # Get top 10 wine variety based on variety
        results = session.query(*sel).\
            filter(Wine.variety == variety).order_by(desc(Wine.points)).limit(10)
        # convert to a list
        top = list(results)
        return jsonify(top)

    # Get top 10 wine variety based on variety and country
    results = session.query(*sel).\
        filter(Wine.variety == variety).\
        filter(Wine.country == country).order_by(desc(Wine.points)).limit(10)
    # convert to a list
    top_list = list(results)
    return jsonify(top_list)

@app.route("/wine/<variety>")
@app.route("/wine/<variety>/<country>")
def winevarcon(variety=None, country=None):
    

    # Select statement
    sel = [Wine.country, Wine.points, Wine.price, Wine.title]

    if not country:
        # Get top 10 wine variety based on variety
        results = session.query(*sel).\
            filter(Wine.variety == variety).all()
        # Unravel results into a 1D array and convert to a list
        variety = list(np.ravel(results))
        return jsonify(variety)

    # Get top 10 wine variety based on variety and country
    results = session.query(*sel).\
        filter(Wine.variety == variety).\
        filter(Wine.country == country).all()
    # Unravel results into a 1D array and convert to a list
    variety_con = list(np.ravel(results))
    return jsonify(variety_con)
    
if __name__ == "__main__":
    app.run(debug=True)
        