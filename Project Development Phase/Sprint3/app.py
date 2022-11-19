from flask import Flask, render_template, request
import pandas as pd
import joblib
import numpy as np

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
    prediction = preprocessAndPredict(inputs)
    # Pass prediction to prediction template
    return render_template('/result.html', prediction=prediction)


def preprocessAndPredict(inputs):
    test_data = np.array(inputs).reshape((1, 17))
    # test_data = inputs

    model_file = open('model_forest_reg.pkl', 'rb')

    trained_model = joblib.load(model_file)

    # df = pd.DataFrame(data=test_data[0:, 0:], columns=['FL_NUM', 'MONTH', 'DAY_OF_MONTH','DAY_OF_WEEK', 'origin', 'dest', 'CRS_DEP_TIME', 'CRS_ARR_TIME', 'DEP_TIME'])

    df = pd.DataFrame(data=test_data[0:, 0:], columns=['FL_NUM', 'MONTH', 'DAY_OF_MONTH', 'DAY_OF_WEEK', 'CRS_DEP_TIME', 'CRS_ARR_TIME', 'DEP_TIME',
                      'ORIGIN_ATL', 'ORIGIN_DTW', 'ORIGIN_JFK', 'ORIGIN_MSP', 'ORIGIN_SEA', 'DEST_ATL', 'DEST_DTW', 'DEST_JFK', 'DEST_MSP', 'DEST_SEA'])

    data = df.values

    result = trained_model.predict(data)

    print(result)
    return result


if __name__ == '__main__':
    app.run(debug=True)
