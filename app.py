import os
from flask import Flask, render_template, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Database
from forms import *

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'UbuntuGNOME'
db = SQLAlchemy(app)

dbb = Database()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/load_data')
def load_data():
    path = os.path.join(app.instance_path, 'data', 'IN.csv')
    return dbb.load_data(location='data/IN.csv')

@app.route('/post_location', methods=['GET', 'POST'])
def add():
    form = InsertForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('Mandatory fields are required.')
            return render_template('insert.html', form=form)
        else:
            return dbb.insert(pincode=form.pincode.data,address = form.address.data,city=form.city.data,latitude =form.latitude.data,longitude =form.longitude.data, accuracy = form.accuracy.data)
    elif request.method == 'GET':
        return render_template('insert.html', form=form)

@app.route('/get_using_postgres',methods=['GET', 'POST'])
def earthdistance_using_postgres():
    form = DistanceForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('Mandatory fields are required.')
            return render_template('distancepostgres.html', form=form)
        else:
            return dbb.fetch_locations_using_postgres(latitude = form.latitude.data,longitude = form.longitude.data,radius = form.radius.data)
    elif request.method == 'GET':
        return render_template('distancepostgres.html', form=form)

@app.route('/get_using_self', methods=['GET', 'POST'])
def earthdistance_using_self():
    form = DistanceForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('Mandatory fields are required.')
            return render_template('distanceself.html', form=form)
        else:
            return dbb.fetch_locations_using_self(latitude = form.latitude.data,longitude = form.longitude.data,radius = form.radius.data)
    elif request.method == 'GET':
        return render_template('distanceself.html', form=form)
    
if __name__ == '__main__':
    app.run()