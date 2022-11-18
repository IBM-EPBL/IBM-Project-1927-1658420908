import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np

dataset = pd.read_csv("flightdata.csv")
dataset = pd.DataFrame(dataset)

dataset=dataset[["FL_NUM","MONTH","DAY_OF_MONTH","DAY_OF_WEEK","ORIGIN","DEST","CRS_ARR_TIME","DEP_DEL15","ARR_DEL15"]]

dataset=dataset.fillna({'ARR_DEL15':1})
dataset=dataset.fillna({'DEP_DEL15':0})

import math
for index,row in dataset.iterrows():
    dataset.loc[index,'CRS_ARR_TIME']=math.floor(row['CRS_ARR_TIME']/100)

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
dataset['DEST'] = le.fit_transform(dataset['DEST'])
dataset['ORIGIN']=le.fit_transform(dataset['ORIGIN'])
from sklearn.preprocessing import OneHotEncoder
oh = OneHotEncoder()
x=dataset.values
z = oh.fit_transform(x[:,3:4]).toarray()
t=oh.fit_transform(x[:,4:5]).toarray()

x=dataset.iloc[:,0:8].values
#print(x)
y=dataset.iloc[:,8:9].values

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=0)

from sklearn.ensemble import RandomForestClassifier
forest_reg = RandomForestClassifier(n_estimators = 10, criterion = 'entropy',random_state = 42)
forest_reg.fit(x_train,y_train)

#print(x_test)
def prediction(x1_test):
    x1 = x1_test
    x2 = pd.DataFrame(x1)
    x3 =  x2.values
    #z1 = oh.fit_transform(x3[:,4:5]).toarray()
    #t2=oh.fit_transform(x3[:,5:6]).toarray()
    '''print("The value of t is ",t)
    x1_test[4]=z
    x1_test[5]=t'''
    print("the values of x3 is ",x3)
    pred = forest_reg.predict(x3)
    return pred



