# Dependency
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Print all of the classes mapped to the Base
Base.classes.keys()

# Save references to each table
# Assign the 'measurement' to a variable called 'Measurement'
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# "/" Start at the homepage. List all the available routes.

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>" 
        f"/api/v1.0/<start>/<end>")

# Convert the query results to a dictionary by using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query all passengers
    results_date = session.query(measurement.date).all()
    results_prcp = session.query(measurement.prcp).all()

    results_date_list = list(np.ravel(results_date))
    results_prcp_list = list(np.ravel(results_prcp))

    date_prcp_list = dict(zip(results_date_list, results_prcp_list))

    return jsonify(date_prcp_list)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():

    stations = session.query(station.station).all()

    # Convert list of tuples into normal list
    list_stations = list(np.ravel(stations))

    return jsonify(list_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    # list date, tobs for  the most active station (USC00519281) 
    date_USC00519281 = session.query(measurement.date).filter(measurement.station == 'USC00519281', \
        measurement.date <= '2017-08-23', measurement.date >= '2016-08-23').all()

    tobs_USC00519281 = session.query(measurement.tobs).filter(measurement.station == 'USC00519281', \
        measurement.date <= '2017-08-23', measurement.date >= '2016-08-23').all()

    date_USC00519281_list = list(np.ravel(date_USC00519281))
    tobs_USC00519281_list = list(np.ravel(tobs_USC00519281))

    USC00519281_list = dict(zip(date_USC00519281_list, tobs_USC00519281_list))

    return jsonify(USC00519281_list)

@app.route("/api/v1.0/<start>")
def start_route(start_date):

    # Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
    tobs_min = session.query(func.min(measurement.tobs)).filter(measurement.date >= start_date).all()
    tobs_max = session.query(func.max(measurement.tobs)).filter(measurement.date >= start_date).all()
    tobs_avg = session.query(func.mean(measurement.tobs)).filter(measurement.date >= start_date).all()

    return jsonify({f"The minimum temperature is {tobs_min}, the maximum temperature is {tobs_max} \
                        and the average temperature is {tobs_avg}."})

@app.route("/api/v1.0/<start>/<end>")
def start_route(start_date,end_date):

    # Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
    tobs_min = session.query(func.min(measurement.tobs)).filter(measurement.date >= start_date, measurement.date <= end_date).all()
    tobs_max = session.query(func.max(measurement.tobs)).filter(measurement.date >= start_date, measurement.date <= end_date).all()
    tobs_avg = session.query(func.mean(measurement.tobs)).filter(measurement.date >= start_date, measurement.date <= end_date).all()

    return jsonify({f"The minimum temperature is {tobs_min}, the maximum temperature is {tobs_max} \
                        and the average temperature is {tobs_avg}."})

if __name__ == "__main__":
    app.run(debug=True)