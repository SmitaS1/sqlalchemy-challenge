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
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    engine =  create_engine("sqlite:///C:/Users/shah_/Documents/Rutgers_Data_Science_Boot_Camp_Local/sqlalchemy-challenge10_to_Github/sqlalchemy-challenge/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
    Base = automap_base()

# reflect the tables
    Base.prepare(autoload_with=engine)

# Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station

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
    engine =  create_engine("sqlite:///C:/Users/shah_/Documents/Rutgers_Data_Science_Boot_Camp_Local/sqlalchemy-challenge10_to_Github/sqlalchemy-challenge/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
    Base = automap_base()
# reflect the tables
    Base.prepare(autoload_with=engine)

# Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station

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
    engine =  create_engine("sqlite:///C:/Users/shah_/Documents/Rutgers_Data_Science_Boot_Camp_Local/sqlalchemy-challenge10_to_Github/sqlalchemy-challenge/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
    Base = automap_base()

# reflect the tables
    Base.prepare(autoload_with=engine)

# Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station

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
  
@app.route("/api/v1.0/<start_date>")
def startDateOnly(start_date):
    engine =  create_engine("sqlite:///C:/Users/shah_/Documents/Rutgers_Data_Science_Boot_Camp_Local/sqlalchemy-challenge10_to_Github/sqlalchemy-challenge/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
    Base = automap_base()
    \
# reflect the tables
    Base.prepare(autoload_with=engine)

# Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station

# Create our session (link) from Python to the DB
    session = Session(engine)
    Base.metadata.create_all(bind=engine)


# Create a query for a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
       filter(Measurement.date >= start_date).all()
    
    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict) 
    
    session.close()
    return jsonify(start_date_tobs)
    
 ##################################################################################################   

@app.route("/api/v1.0/<start_date>/<end_date>")
def startDateEndDate(start_date,end_date):
    engine =  create_engine("sqlite:///C:/Users/shah_/Documents/Rutgers_Data_Science_Boot_Camp_Local/sqlalchemy-challenge10_to_Github/sqlalchemy-challenge/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
    Base = automap_base()

# reflect the tables
    Base.prepare(autoload_with=engine)

# Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station

# Create our session (link) from Python to the DB
    session = Session(engine)
    Base.metadata.create_all(bind=engine)


# Create a query to find the minimum temperature, the average temperature, and the maximum temperature for a specified start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 

    
    session.close()

    return jsonify(start_end_tobs)

  
if __name__ == '__main__':
    app.run(debug=True)