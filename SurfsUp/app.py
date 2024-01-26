# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine =  create_engine("sqlite:///C:/Users/shah_/Documents/Rutgers_Data_Science_Boot_Camp_Local/sqlalchemy-challenge10_to_Github/sqlalchemy-challenge/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

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
@app.route("/")
def welcome():
    """All available api routes are here."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/[start_date format:mm-dd-yyyy]<br/>"
        f"/api/v1.0/temp/[start_date format:mm-dd-yyyy]/[end_date format:mm-dd-yyyy]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
# Create our session (link) from Python to the DB
    session = Session(engine)
    Base.metadata.create_all(bind=engine)
                   
# Calculate the date before twelve months
    last_twelve_mths = dt.date(2017, 8, 23) - dt.timedelta(days=365)
  
# write query to retrieve last 12 months of data 
    results =  session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_twelve_mths).all()


    #to a dictionary using date as the key and prcp as the value.
    session.close()
# 
# Convert query result to a dictionary using date as the key and prcp as the value.
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)


    return jsonify(all_prcp)

##################################################################################################

@app.route("/api/v1.0/station")
def station():

# Create our session (link) from Python to the DB
    session = Session(engine)
    Base.metadata.create_all(bind=engine)
  
# Query all station data
    results = session.query(Station.station).all()

# Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

# close the session
    session.close()

#Return a JSON list of stations from the dataset.
    return jsonify(all_stations)

##################################################################################################

@app.route("/api/v1.0/tobs")
def tobs():

# Create our session (link) from Python to the DB
    session = Session(engine)
    Base.metadata.create_all(bind=engine)

# Calculate the date before twelve months
    last_twelve_mths = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Query the dates and temperature observations of the most-active station for the previous year of data.
    most_active_station = session.query(Measurement.station,func.count(Measurement.station)).\
                                        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    
    best_station = most_active_station[0][0]
    results = session.query(Measurement.date, (Measurement.tobs)).\
        filter((Measurement.station)== best_station , Measurement.date >= last_twelve_mths ).all()
                  
    # all_stations = list(np.ravel(results))
    all_stations = list(np.ravel(results))

    session.close()
    return jsonify(all_stations)

    
 ##################################################################################################   
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""
    session = Session(engine)
    Base.metadata.create_all(bind=engine)

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        start = dt.datetime.strptime(start, "%m-%d-%Y")
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()

        session.close()

        temps = list(np.ravel(results))
        return jsonify(temps)

    # calculate TMIN, TAVG, TMAX with start and stop
    start = dt.datetime.strptime(start, "%m-%d-%Y")
    end = dt.datetime.strptime(end, "%m-%d-%Y")

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
  
if __name__ == '__main__':
    app.run(debug=True)