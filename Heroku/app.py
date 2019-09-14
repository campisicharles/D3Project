from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


app = Flask(__name__)

# setup Postgres connection
engine = create_engine('postgresql://postgres:postgres@localhost:5432/EnvironmentalData')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
NutritionData = Base.classes.NutritionData
clean_environment_data = Base.classes.clean_environment_data


@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/foodtypes<br/>"
        f"/api/v1.0/foodproducts"
    )

@app.route("/api/v1.0/foodtypes")
def names():
    session = Session(engine)
    results = session.query(NutritionData.Group).all()

    # Convert list of tuples into normal list
    all_groups = list(np.ravel(results))

    return jsonify(all_groups)


@app.route("/api/v1.0/foodproducts")
def types():

    session2 = Session(engine)
    results2 = session2.query(clean_environment_data.Product).all()

    # Convert list of tuples into normal list
    all_groups2 = list(np.ravel(results2))

    return jsonify(all_groups2)
   
if __name__ == "__main__":
    app.run(debug=True)
