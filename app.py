from flask import Flask, jsonify
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
from sqlalchemy import create_engine, func
import json


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    """API Routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f""
        f""
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = last_date[0]
    precip = session.query(Measurement.date).filter(Measurement.date >= last_date)
    prev_year = dt.datetime.strptime(last_date, "%Y-%m-%d")- dt.timedelta(days=365)
    precip_scores = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=prev_year).all()

    result = dict(precip_scores)
    return jsonify(result)

    session.close()

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station,Station.name).all()
    result = dict(stations)
    return jsonify(result)
    session.close()


@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def temperature(start=None, end=None):
    session = Session(engine)

    if end != None:
        temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()

    #convert list of tuples into normal list
    result = list(np.ravel(temps))

    #return json representation of the list
    return jsonify(result)
    session.close()


if __name__ == '__main__':
    app.run(debug=True)
