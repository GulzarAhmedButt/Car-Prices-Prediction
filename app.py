from flask import Flask,render_template,request,jsonify,redirect,url_for
from wtforms import Form,IntegerField,FloatField,validators,SelectField
import numpy as np
import pickle


app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))



class DataForm(Form):
    transmission = SelectField('Transmission',choices=['Manual','Automatic'])
    Year = IntegerField('Year',[validators.NumberRange(min=2000,max=2020,message='Please Enter Year from 2000 onwards')])
    fuel = SelectField('Fuel Type',choices=['Petrol','Diesel','CNG','LPG','Electric'])
    Owner = SelectField('Owner',choices=['First Owner','Second Owner','Fourth & Above Owner','Third Owner','Test Drive Car'])
    Km_driven = IntegerField('Km Driven')


@app.route('/')
def homepage():
    form = DataForm(request.form)
    return render_template('home.html',form=form)

@app.route('/predict',methods=['POST'])
def predict():
    form = DataForm(request.form)
    transmission = form.transmission.data
    Year = form.Year.data
    fuel = form.fuel.data
    Owner = form.Owner.data
    Km_driven = form.Km_driven.data
    if transmission == 'Manual':
        transmission_encoded = 1
    else:
        transmission_encoded = 0
    if fuel == 'Petrol':
        fuel_encoded = 4
    elif fuel == 'Diesel':
        fuel_encoded=1
    elif fuel == 'CNG':
        fuel_encoded=0
    elif fuel == 'LPG':
        fuel_encoded=3
    elif fuel == 'Electric':
        fuel_encoded = 2
    if Owner == 'First Owner':
        owner_encoded = 0
    elif Owner == 'Second Owner':
        owner_encoded = 2
    elif Owner == 'Third Owner':
        owner_encoded = 4
    elif Owner == 'Fourth & Above Owner':
        owner_encoded = 1
    elif Owner == 'Test Drive Car':
        owner_encoded = 3

    features = [transmission_encoded,Year,fuel_encoded,owner_encoded,Km_driven]
    final_features = [np.array(features)]
    prediction = model.predict(final_features)
    output = round(prediction[0],2)
    return render_template('predict.html',form=form,prediction_text="The price of Car is {}".format(output))



if __name__=='__main__':
    app.run(debug=True)
