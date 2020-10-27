# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 15:00:47 2020

@author: RussellP
"""
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv('C:/Users/RussellP/Documents/Data Engineering/Projects/salary_estimator_project/eda_data.csv')

# Choose relevant columns for our model
df.columns

df_model = df[['avg_salary','Rating', 'Size', 'Type of ownership', 'Industry', 'Sector', 'Revenue', 'age', 'python', 'sql', 'excel', 'spark', 'aws', 'experience_2years', 'job_simplified', 'seniority', 'desc_len' ]]

# Get dummy data
df_dummy = pd.get_dummies(df_model)

# Train/Test Split
# Assigning axis for dummy data
x = df_dummy.drop('avg_salary', axis = 1)
y = df_dummy.avg_salary.values

# Splits out data into a training data and testing data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 44)

# Multiple Linear Regression - Stats Model
import statsmodels.api as sm
# Creating a constant like this creates an intercept for the slope of the line (needed for statsmodel implementation)
x_sm = x = sm.add_constant(x, has_constant='add') # if there are any attributes/columns with all '0' 
model = sm.OLS(y, X_sm)
model.fit().summary()


# Multiple Linear Regression - sklearn
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(x_train, y_train)

# Cross validation  - if you see -7.14 for values that equals 7k off (error)
np.mean(cross_val_score(lm, x_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3))



# Lasso Regression - good for small/sparse datasets and normalization of data
lm_l = Lasso(alpha=0.03)
lm_l.fit(x_train, y_train)
# -13 , so this starts off as a worse model than linear regression above
np.mean(cross_val_score(lm_l, x_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3))

alpha = []
error = []

# Increased to 1000 in order for optimum alpha to be visible on the plot
for i in range(1,100):
    alpha.append(i/1000)
    lml = Lasso(alpha = (i/1000))
    error.append(np.mean(cross_val_score(lml, x_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3)))
    
plt.plot(alpha, error)

# ties the two values together into a paired list (tuple) non iteratable
err = tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns = ['alpha', 'error'])
# Displaying the highest alpha (best performing parameter value for our model)
df_err[df_err.error == max(df_err.error)]

# optimum alpha 0.03 err = -6.88



# Random Forest
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor()

# error = -5.77 (Best model yet, and it has not yet been tuned)
np.mean(cross_val_score(rf, x_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3))

# Tune models GridsearchCV - put in all paramters runs a number of models and outputs model and parameters with best results
# Doing full exhaustive Gridserch is recommended over a randomized gridsearch (if resources allow)
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators': range(10, 300, 10), 'criterion':('mse', 'mae'), 'max_features':('auto', 'sqrt', 'log2') }

gs = GridSearchCV(rf, parameters, scoring ='neg_mean_absolute_error', cv = 3)
gs.fit(x_train, y_train)


gs.best_score_

gs.best_estimator_

# Test Ensembles
tpred_lm = lm.predict(x_test)
tpred_lml = lm_l.predict(x_test)
tpred_rf = gs.best_estimator_.predict(x_test)

# MAE - Comparing Models Accuracy/Performance
from sklearn.metrics import mean_absolute_error

mean_absolute_error(y_test, tpred_lm) # 7.428409067226264
mean_absolute_error(y_test, tpred_lml) # 7.413931573433786
mean_absolute_error(y_test, tpred_rf) # 5.202090686274509  - Best Model

# (tpred_lm + tpred_rf)/2
# We could run this through a regression model and use weights instead of just adding them together
# This ensemble approach is better for classification problems
mean_absolute_error(y_test, (tpred_lm + tpred_rf)/2)

# Productionizing the model
import pickle

# Creating pickle file for the model
pickl = {'model': gs.best_estimator_}
pickle.dump(pickl, open('model_file' + ".p", "wb"))

file_name= 'model_file.p'
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

x_test.iloc[1,:].values
# Testing that the pickled model works
model.predict(x_test.iloc[1,:].values.reshape(1, -1))


list(x_test.iloc[1,:])
    





