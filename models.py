# from app import db
# from sqlalchemy.dialects.postgresql import JSON


# class Zipcode(db.Model):
#     __tablename__ = 'zipcodes'

#     key = db.Column(db.String(9), primary_key=True)
#     place_name = db.Column(db.String())
#     admin_name1 = db.Column(db.String())
#     latitude = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
#     longitude = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
#     accuracy = db.Column(db.Integer)

#     def __init__(self, url, result_all, result_no_stop_words):
#         pass
        

#     def __repr__(self):
#         return '<id {}>'.format(self.id)

import psycopg2
from flask import jsonify, flash
import os
class Database:
    def __init__(self):

        self.con=psycopg2.connect("dbname='abc' user='postgres' password='UbuntuGNOME' host='localhost' port='5432' ")
        self.cur=self.con.cursor()
        self.cur.execute("""CREATE TABLE if not exists zip_codes(
        key char(9) PRIMARY KEY,
        place_name varchar,
        admin_name1 varchar,
        latitude double precision,
        longitude double precision,
        accuracy int);""")
        self.con.commit()

    def load_data(self, location=None):
        if location != None:
            import pandas
            from sqlalchemy import create_engine
            datas = pandas.read_csv(location)
            engine = create_engine(os.environ['DATABASE_URL'])
            datas.to_sql('zip_codes', engine, if_exists='replace')
            self.cur.execute("ALTER TABLE zip_codes ADD PRIMARY KEY (key)")
            self.con.commit()
            return "Data loaded"

    def insert(self,pincode,address,city,latitude, longitude, accuracy):
      try:
        self.cur.execute("INSERT INTO zip_codes(key,place_name,admin_name1,latitude, longitude, accuracy) VALUES(%s,%s,%s,%s,%s,%s)",(pincode,address,city,latitude, longitude, accuracy))
        self.con.commit()
        return "Inserted"
      except psycopg2.DatabaseError as e:
        if self.con:
            self.con.rollback()
        print('Error %s', e)
        return "Row already exists.."

    def view(self):
        self.cur.execute("SELECT * FROM zipcode")
        rows=self.cur.fetchall()
        zips_as_dict = []
        for row in rows:
            zip_as_dict = {"sl":row[0],
                           "pincode":row[1],
                           "address": row[2],
                           "city": row[3],
                           "latitude":row[4],
                           "longitude":row[5],
                           "accuracy":row[6]}
            zips_as_dict.append(zip_as_dict)
        return jsonify(zips_as_dict)

    def fetch_locations_using_postgres(self,latitude,longitude,radius):
        self.cur.execute("SELECT * FROM zip_codes WHERE earth_box(ll_to_earth(%s, %s), %s)@> ll_to_earth(latitude, longitude)",(latitude, longitude, radius))
        rows=self.cur.fetchall()
        zips_as_dict = []
        for row in rows:
            zip_as_dict = {"sl":row[0],
                           "pincode":row[1],
                           "address": row[2],
                           "city": row[3],
                           "latitude":row[4],
                           "longitude":row[5],
                           "accuracy":row[6]}
            zips_as_dict.append(zip_as_dict)
        return jsonify(zips_as_dict)

