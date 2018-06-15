# import necessary libraries

import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

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
    
@app.route('/varieties')
def varieties():

    stmt = session.query(Wine).statement
    wine_df = pd.read_sql_query(stmt, session.bind)
    
    return jsonify(list(df.variety.unique()))

@app.route("/region")
def region():
    stmt = session.query(Coord).statement
    region_df = pd.read_sql_query(stmt, session.bind)
    data = [{
        "region": region_df["region_1"].values.tolist(),
        "coordinates": region_df["coordinates"].values.tolist()
        "country" : region_df["country"].values.tolist()
    }]

@app.route('/varieties/<variety>')
def wines(variety):

    variety_stmt = session.query(Wine).statement
    df = pd.read_sql_query(variety_stmt, session.bind)
    
    if variety not in df.variety.unique():
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
if __name__ == "__main__":
    app.run(debug=True)
        