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
measurement = Base.classes.measurement
station_list = Base.classes.station

# Create our session (link) from Python to the DB
# Create a session
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
# "/" Start at the homepage. List all the available routes.

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>" 
        f'input date in the format of YYYY-MM-DD<br/>'
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>" 
        f'input date in the format of YYYY-MM-DD')

# Convert the query results to a dictionary by using date as the key and prcp as the value.
# Return the JSON representation of the dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query date and prcp
    result_date = session.query(measurement.date).all()
    result_prcp = session.query(measurement.prcp).all()

    result_date_list = list(np.ravel(result_date))
    result_prcp_list = list(np.ravel(result_prcp))

    date_prcp_list = dict(zip(result_date_list, result_prcp_list))

    return jsonify(date_prcp_list)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():

    stations = session.query(station_list.station).all()

    # Convert list of tuples into normal list
    stations_all = list(np.ravel(stations))

    return jsonify(stations_all)

# list date, tobs for the most active station (USC00519281) 
@app.route("/api/v1.0/tobs")
def tobs():

    date_USC00519281 = session.query(measurement.date).filter(measurement.station == 'USC00519281', \
        measurement.date <= '2017-08-23', measurement.date >= '2016-08-23').all()

    tobs_USC00519281 = session.query(measurement.tobs).filter(measurement.station == 'USC00519281', \
        measurement.date <= '2017-08-23', measurement.date >= '2016-08-23').all()

    date_USC00519281_list = list(np.ravel(date_USC00519281))
    tobs_USC00519281_list = list(np.ravel(tobs_USC00519281))

    USC00519281_list = dict(zip(date_USC00519281_list, tobs_USC00519281_list))

    return jsonify(USC00519281_list)

# Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
@app.route("/api/v1.0/<start_date>")
def start_route(start_date):

    tobs_min = session.query(func.min(measurement.tobs)).filter(measurement.date >= start_date).all()
    tobs_max = session.query(func.max(measurement.tobs)).filter(measurement.date >= start_date).all()
    tobs_avg = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start_date).all()

    return jsonify({'min_temperature': tobs_min},{'max_temperature':tobs_max},{'avg_temperature':tobs_avg})

# Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_route(start_date,end_date):

    tobs_min_1 = session.query(func.min(measurement.tobs)).filter(measurement.date >= start_date, measurement.date <= end_date).all()
    tobs_max_1 = session.query(func.max(measurement.tobs)).filter(measurement.date >= start_date, measurement.date <= end_date).all()
    tobs_avg_1 = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start_date, measurement.date <= end_date).all()

    return jsonify({'min_temperature': tobs_min_1},{'max_temperature':tobs_max_1},{'avg_temperature':tobs_avg_1})

if __name__ == "__main__":
    app.run(debug=True)