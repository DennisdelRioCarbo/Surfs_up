# import datetime as dt

# import numpy as np

# from numpy import dtype

# from numpy import ufunc

# import pandas as pd


# import sqlalchemy

# from sqlalchemy.ext.automap import automap_base

# from sqlalchemy.orm import Session

# from sqlalchemy import create_engine, func

# from flask import Flask, jsonify

# engine = create_engine("sqlite:///hawaii.sqlite")

# Base = automap_base()

# Base.prepare(engine, reflect=True)

# Measurement = Base.classes.measurement

# Station = Base.classes.station

# session = Session(engine)

# app = Flask(__name__)

# @app.route('/')

# def welcome():
#     return(
#     '''
#     Welcome to the Climate Analysis API! 
    
#     Available Routes: 
    
#     /api/v1.0/precipitation 
    
#     /api/v1.0/stations 
    
#     /api/v1.0/tobs 

#     /api/v1.0/temp/start/end 

#     ''')

# @app.route("/api/v1.0/precipitation")

# def precipitation():
#    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

#    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()

#    precip = {date: prcp for date, prcp in precipitation}

#    return jsonify(precip)

# @app.route("/api/v1.0/stations")

# def stations():
#     results = session.query(Station.station).all()

#     stations = list(np.ravel(results))

#     return jsonify(stations=stations)

# @app.route("/api/v1.0/tobs")

# def temp_monthly():
#     prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

#     results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()

#     temps = list(np.ravel(results))

#     return jsonify(temps=temps)

# @app.route("/api/v1.0/temp/<start>")

# @app.route("/api/v1.0/temp/<start>/<end>")

# def stats(start=None, end=None):
#     sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

#     if not end:
#         results = session.query(*sel). filter(Measurement.date >= start).all()

#         temps = list(np.ravel(results))
        
#         return jsonify(temps)

#     results = session.query(*sel). filter(Measurement.date >= start).filter(Measurement.date <= end).all()

#     temps = list(np.ravel(results))

#     return jsonify(temps)

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


################################################
#Database Setup
################################################
engine = create_engine("sqlite:///titanic.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Passenger = Base.classes.passenger

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    #"""List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/passengers"
    )


@app.route("/api/v1.0/names")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #"""Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Passenger.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/passengers")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #"""Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
