import os
from flask import Flask, render_template, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Database
from forms import InsertForm

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'UbuntuGNOME'
db = SQLAlchemy(app)

dbb = Database()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/get_using_postgres')
def earthdistance_using_postgres():
    return dbb.fetch_locations_using_postgres("28.55","77.2667","100")


@app.route('/add', methods=['GET', 'POST'])
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

@app.route('/load_data')
def load_data():
    path = os.path.join(app.instance_path, 'data', 'IN.csv')
    return dbb.load_data(location='data/IN.csv')

@app.route('/get_using_self')
def earthdistance_using_self(lat=28.55 , lon=77.2667):
    import math
    radius = 1
    N = 360 

    # generate points
    circlePoints = []
    for k in range(N):
        angle = math.pi*2*k/N
        dx = radius*math.cos(angle)
        dy = radius*math.sin(angle)
        point = {}
        point['lat']= lat + (180/math.pi)*(dy/6371) #Earth Radius
        point['lon']= lon + (180/math.pi)*(dx/6371)/math.cos(lon*math.pi/180) #Earth Radius
        # add to list
        circlePoints.append(point)

    return jsonify(circlePoints)


if __name__ == '__main__':
    app.run()