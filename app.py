# Import the dependencies.

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################


# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# mapped classes are now created with names by default
# matching that of the table name.
Station = Base.classes.station
Measurement = Base.classes.measurement

Station

# reflect the tables

# View all of the classes that automap found
for class_name in Base.classes.keys():
    print(class_name)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB







# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


database = [
    # name, vehicle, city
    ('tom', 'truck', 'South Lake Tahoe'),
    ('brett', 'shoes', 'Philadelphia'),
    ('tomdoc', 'septa', 'Moms House')
]


#################################################
# Flask Routes
#################################################
@app.route('/')
def root():
    return f'''
        The routes are:
        <ul>
            <li>
                <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a>
            </li>
            <li>
                <a href="/api/v1.0/stations">/api/v1.0/stations</a>
            </li>
             <li>
                <a href="/api/v1.0/tobs">/api/v1.0/tobs</a>
            </li>
             <li>
                <a href="/api/v1.0/<start>">/api/v1.0/starts</a>
            </li>
             <li>
                <a href="/api/v1.0/<end>">/api/v1.0/end</a>
            </li>



        </ul>'''




@app.route('/api/v1.0/precipitation')
def precipitation():
    with Session(engine) as session:
        # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
        # Starting from the most recent data point in the database. 
        # Calculate the date one year from the last date in data set.

        prevyear = dt.date(2017,8,23) - dt.timedelta(days=365)

        # Perform a query to retrieve the data and precipitation scores

        results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prevyear)

        # Save the query results as a Pandas DataFrame. Explicitly set the column names

        df = pd.DataFrame(results, columns=("date", 'precipitation'))

        result = {}
        for (date, precipitation) in df.itertuples(index=False, name=None):
            result[date] = precipitation

        return jsonify(result)


@app.route('/api/v1.0/stations')
def stations():
    with Session(engine) as session:
        result = []
        for x in session.query(Station).all():
            result.append(x.name)
        return jsonify(result)


@app.route('/api/v1.0/tobs')
def tobs():
    with Session(engine) as session:
        result = []
        for x in session.query(Measurement).filter(Measurement.station == "USC00519281").all():
            result.append({"date": x.date, "tobs": x.tobs})

        
        return jsonify(result)



@app.route('/api/v1.0/<start>')
def bretts(start: str):
    with Session(engine) as session:
        result = []
        for (min, max, avg) in (session.query(func.min(Measurement.tobs) , func.max(Measurement.tobs) , func.avg(Measurement.tobs))).filter(Measurement.date >= start).all():
            result.append({"TMIN": min, "TMAX": max, "TAVG": avg})
        return jsonify(result)
    

@app.route('/api/v1.0/<start>/<end>')
def tomg(start: str, end: str):
    with Session(engine) as session:
        result = []
        for (min, max, avg) in (session.query(func.min(Measurement.tobs) , func.max(Measurement.tobs) , func.avg(Measurement.tobs))).filter(Measurement.date >= start).filter(Measurement.date <= end).all():
            result.append({"TMIN": min, "TMAX": max, "TAVG": avg})
        return jsonify(result)



#@app.route('/profiles/<name>')
#def profile(name: str):
#    for (n, transport, location) in database:
#        if name == n:
#            return f'''
#                Profile for <strong>{n}</strong>,
#                who uses <strong>{transport}</strong> to get around,
#                and who lives at <strong>{location}</strong>
#            '''
#        
#    return '404 not found'

#@app.route('/square/<s>')
#def square(s: str):
#    return f'Your number squared is {int(s) ** 2}'