from flask import Flask, render_template, request
import csv
import pickle
import pandas as pd
import joblib
import numpy as np

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "dOwmdbcncwb3HcJuEMKQH7AHy66viTvlYB31FoRQnmzm"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('Flightdelay.html')


@app.route('/result', methods=['POST'])
def predict():
    fl_num = int(request.form.get('fno'))
    month = int(request.form.get('month'))
    dayofmonth = int(request.form.get('daym'))
    dayofweek = int(request.form.get('dayw'))
    origin = str(request.form.get("org"))
    dest = str(request.form.get("dest"))
    sdeptime = request.form.get('sdt')
    sarrtime = int(request.form.get('sat'))
    adeptime = request.form.get('adt')

    inputs = list()
    inputs.append(fl_num)
    inputs.append(month)
    inputs.append(dayofmonth)
    inputs.append(dayofweek)
    inputs.append(sdeptime)
    inputs.append(sarrtime)
    inputs.append(adeptime)

    if(origin == "ATL"):
        a = [1, 0, 0, 0, 0]
        inputs.extend(a)
    elif(origin == "DTW"):
        a = [0, 1, 0, 0, 0]
        inputs.extend(a)
    elif(origin == "JFK"):
        a = [0, 0, 1, 0, 0]
        inputs.extend(a)
    elif(origin == "MSP"):
        a = [0, 0, 0, 1, 0]
        inputs.extend(a)
    elif(origin == "SEA"):
        a = [0, 0, 0, 0, 1]
        inputs.extend(a)

    if(dest == "ATL"):
        b = [1, 0, 0, 0, 0]
        inputs.extend(b)
    elif(dest == "DTW"):
        b = [0, 1, 0, 0, 0]
        inputs.extend(b)
    elif(dest == "JFK"):
        b = [0, 0, 1, 0, 0]
        inputs.extend(b)
    elif(dest == "MSP"):
        b = [0, 0, 0, 1, 0]
        inputs.extend(b)
    elif(dest == "SEA"):
        b = [0, 0, 0, 0, 1]
        inputs.extend(b)

    # inputs.append(origin)
    # inputs.append(dest)

    print(inputs)

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [
        ['FL_NUM', 'MONTH', 'DAY_OF_MONTH', 'DAY_OF_WEEK', 'CRS_DEP_TIME', 'CRS_ARR_TIME', 'DEP_TIME',
         'ORIGIN_ATL', 'ORIGIN_DTW', 'ORIGIN_JFK', 'ORIGIN_MSP', 'ORIGIN_SEA', 'DEST_ATL', 'DEST_DTW', 'DEST_JFK', 'DEST_MSP', 'DEST_SEA']], "values": [inputs]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/4d3b06b1-4fe8-4775-bc6c-f85e8544e21f/predictions?version=2022-11-19',
                                     json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(response_scoring.json())

    predict = predictions['predictions'][0]['values'][0][0]
    print(predict)

    return render_template('/result.html', prediction=predict)


if __name__ == '__main__':
    app.run(debug=True)
