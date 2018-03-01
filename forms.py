from flask_wtf import Form
from wtforms import TextField, SubmitField, validators, ValidationError,DecimalField,IntegerField
 
class InsertForm(Form):
  pincode = TextField("Pincode",[validators.Required()])
  address = TextField("Address",[validators.Required()])
  city = TextField("City",[validators.Required()])
  latitude = DecimalField("Latitude",[validators.Required()])
  longitude = DecimalField("Longitude",[validators.Required()])
  accuracy = IntegerField("Accuracy")
  submit = SubmitField("Submit")