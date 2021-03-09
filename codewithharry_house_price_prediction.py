# -*- coding: utf-8 -*-
"""CodeWithHarry_House_Price_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/139avVO_-Z_9roCw5O_QyHieYY_KnrBCi

# Price Predictor
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split , StratifiedShuffleSplit
from pandas.plotting import scatter_matrix
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

df = pd.read_csv("data.csv")
df.head()

df.shape

df['CHAS'].value_counts()

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

df.hist(bins=50 , figsize=(25,25))

# def train_test_split(train , test):
#     np.random.seed(42)
#     shuffle = np.random.permutation(len(train))
#     testsize = int(len(train) * test)
#     t1 = shuffle[:testsize]
#     t2 = shuffle[testsize:]
#     return train.iloc[t1], train.iloc[t2]

# X_test,X_train = train_test_split(df,0.2)
# X_train.shape , X_test.shape

df['CHAS'].unique()

X_train , X_test = train_test_split(df , test_size=0.2 , random_state = 51)
X_train.shape , X_test.shape

split = StratifiedShuffleSplit(n_splits=1 , random_state = 51 , test_size = 0.2)

for train_index , test_index in split.split(df , df["CHAS"]):
    train_stra_set = df.loc[train_index]
    test_stra_set = df.loc[test_index]

train_stra_set['CHAS'].value_counts()

test_stra_set['CHAS'].value_counts()

376//28 , 95//7

house = train_stra_set.copy()

"""# Looking for correlation"""

correlation = house.corr()

correlation['MEDV'].sort_values(ascending=False)

attributes = ['MEDV' , 'RM' , 'ZN' , 'LSTAT']
scatter_matrix(df[attributes] , figsize=(15,15) , alpha=0.8)

house.plot(kind = "scatter" , x='RM' , y='MEDV' ,alpha=0.8)

"""# Attribute combinations"""

house['TPR'] = house['TAX'] / house['RM']

house['TPR']

house.head()

correlation = house.corr() 
correlation['MEDV'].sort_values(ascending=False)

house.plot(kind = "scatter" , x="TPR", y="MEDV",alpha=0.8)

house = train_stra_set.drop("MEDV", axis=1)
house_labels = train_stra_set["MEDV"].copy()

"""
## Missing Attributes"""

# Before start filling missing values

house.describe()

# to take care of missing attributes
#     1.Get rid of missing data points
#     2.Get rid of the whole attributes
#     3.Set the value of the some values(0,Mean,Median)

house.isnull().sum()

# a = house.dropna(subset=['RM'])
# a.isnull().sum()
# a.shape

# b = house.drop(columns = 'RM',axis=1)
# b.shape
# b.keys()

# house.fillna(df['RM'].median()).isnull().sum()

imputer = SimpleImputer(strategy='median') #Use below
imputer.fit(house)

imputer.statistics_

imputer.statistics_.shape

X = imputer.transform(house)

house_tr = pd.DataFrame(X , columns=house.columns)

house_tr.describe()

"""# Scikit learn design

Primarilily three types of objects
1. Estimators = Estimates some parameters based on a dataset Eg. Imputer . It has a fit method . fit method fit the dataset and calculate internal parameters.
                
2. Transformers = transform method takes input and returns output based on the learning fit() method. It also has a convenience function called fit_transform().
                    which fits and transform.
    
3. Predictors = LinearRegression model is an example of predictor . fit() and predict() are two common functions . It also gives score function which will evaluate the predictions.

## Feature Scaling

Two types of Feature Scaling method.
1. Min-Max-Scaling (Normalization) - reduce minimize and divide with min-max ( (value-min) / (max-min) ) - all values are scale same
                                    sklearn provide class called MinMaxScaler for this.
    
2. Standardization - (value - mean) / std 
                    sklearn provide a class StandardScaler for this.

## Creating pipeline
"""

pipe  = Pipeline( [
    ('imputer' , SimpleImputer(strategy = 'median')) , 
    ('std_scaler' , StandardScaler())
] )

pipe

house_num = pipe.fit_transform(house)

house_num

house_num.shape

"""# selection a desired model for Price prediction"""

# model = LinearRegression()
# model = DecisionTreeRegressor()
model = RandomForestRegressor()
model.fit(house_num , house_labels)



some_data = house.iloc[:5]
some_labels = house_labels.iloc[:5]

prepared_data = pipe.transform(some_data)

model.predict(pred_data)

list(some_labels)

"""## Evaluating the model"""

house_pred = model.predict(house_num)
mse = mean_squared_error(house_labels , house_pred)
rmse = np.sqrt(mse)
mse , rmse

"""## Using better evaluation technique - Cross Validation"""

scores = cross_val_score(model , house_num ,house_labels , scoring ="neg_mean_squared_error" , cv=10)
rmse_scores = np.sqrt(-scores)

rmse_scores

def print_scores(scores):
    print("Scores:", scores)
    print("Mean: ", scores.mean())
    print("Standard deviation: ", scores.std())

print_scores(rmse_scores)

"""# Decision Tree output
Scores: [3.26227513 4.45894552 4.77912126 3.18211465 7.48566964 5.94445119
 6.12151942 3.75423095 2.536878   3.05986111]
Mean:  4.458506687027908
Standard deviation:  1.5311815379683849
    
# Linear Regression output
Scores: [4.828253   3.85444041 3.33816762 4.7566036  3.47826981 5.58579616
 8.2084182  5.71647241 4.3986239  5.19898139]
Mean:  4.936402650965274
Standard deviation:  1.341254376625896

# RandomForestRegressor output
Scores: [2.53691045 3.37036656 3.88705481 2.44876923 4.63883094 4.78152983
 4.66940869 3.96874319 2.61234282 2.80008839]
Mean:  3.571404490595821
Standard deviation:  0.8917713196236035

## Saving the model
"""

from joblib import dump, load
dump(model, 'Dragon.joblib')

"""## Testing the model"""

X_test = test_stra_set.drop('MEDV', axis=1)
Y_test = test_stra_set["MEDV"].copy()
X_test_prepared = pipe.transform(X_test)
finl_pred = model.predict(X_test_prepared)
fnl_mse = mean_squared_error(Y_test , finl_pred)
fnl_rmse = np.sqrt(fnl_mse)

fnl_rmse

finl_pred

list(Y_test)

house_num[0]

"""## Using the model"""

modeling = load('Dragon.joblib')
input1 = np.array([[ 0.77637881, -0.48303037,  1.04804981, -0.27288841,  0.94984411,
       -1.90695529,  1.10564745, -1.24213676,  1.63380532,  1.54294101,
        0.81921077,  0.4547    ,  3.01750331]])
modeling.predict(input1)

