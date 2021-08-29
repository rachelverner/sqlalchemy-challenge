import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import datetime
from datetime import timedelta
from scipy import stats
import pandas as pd
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
maxdate= '2017-08-23'

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/prcp<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#################################################

@app.route("/api/v1.0/prcp<br/>")
def precipitation():
    #Convert the query results to a dictionary using date as the key and prcp as the value.
    #Return the JSON representation of your dictionary.

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and prcp"""
    prcp_dates = session.query(Measurement.date, (Measurement.prcp)).filter(Measurement.date > maxdate).order_by(Measurement.date).all()
    return jsonify(prcp_dates)

#################################################

@app.route("/api/v1.0/station")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all passengers
    stations = session.query(Station.station).all()

    session.close()

 # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

#################################################

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)   
    year_ago = maxdate - dt.timedelta(days=364)

    tobs_info = (session.query(Measurement.tobs)\
                .filter(Measurement.station == 'USC00519281')\
                .filter(Measurement.date <= maxdate)\
                .filter(Measurement.date >= year_ago)\
                .order_by(Measurement.tobs).all())
    return jsonify(tobs_info)

#################################################
@app.route("/api/v1.0/<start>")
def startdate(start=None):
    session = Session(engine)
    start_only = (session.query(Measurement.tobs).filter(Measurement.date.between(start, maxdate)).all())
    
    start_df = pd.DataFrame(start_only)

    tavg = start_df["tobs"].mean()
    tmax = start_df["tobs"].max()
    tmin = start_df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)

#################################################

@app.route('/api/v1.0/<start>/<end>') 
def startend(start=None, end=None):
    session = Session(engine)
    start_end = (session.query(Measurement.tobs).filter(Measurement.date.between(start, end)).all())
    
    start_end_df = pd.DataFrame(start_end)

    tavg = start_end_df["tobs"].mean()
    tmax = start_end_df["tobs"].max()
    tmin = start_end_df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)

#################################################
if __name__ == '__main__':
    app.run(debug=True)