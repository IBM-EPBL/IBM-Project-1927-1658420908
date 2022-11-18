from flask import Flask, render_template, url_for, request, redirect
from flightdelayprediction import prediction
import numpy as np

app = Flask(__name__)
#/// - means relative path, ////- means absolute path

DEST = ['SEA', 'MSP', 'DTW', 'ATL', 'JFK']
ORI = ['ATL', 'DTW', 'SEA', 'MSP', 'JFK']
values =  { 'SEA':0,
            'MSP':1,
            'DTW':2,
            'ATL':3,
            'JFK':4}


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        flight_no = request.form['flight_no']
        month = request.form['month']
        day_of_month = request.form['day_of_month']
        day_of_week = request.form['day_of_week']
        origin = values[request.form['origin']]
        destination = values[request.form['destination']]
        #s_depature_time = request.form['s_depature_time']
        arrival_time = request.form['arrival_time']
        depature_delay = request.form['depature_delay']
        
        x_test = np.array([flight_no, month, day_of_month, day_of_week, origin, destination, arrival_time, depature_delay])
        print("The xtest value is", x_test)
        #print("The shape of array is",x_test.shape)
        pred = prediction(x_test)
        return render_template('output.html', value=pred)
    else:
        return render_template('index.html', Ori = ORI, lenori = len(ORI), Dest = DEST, lendes = len(DEST))

if __name__ == "__main__":
    app.run(debug=True)