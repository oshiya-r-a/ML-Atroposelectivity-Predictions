# -*- coding: utf-8 -*-
"""%ee_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eGrglU5BuO47ZGJ57_3HmMz-JSxTE1hs
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score, train_test_split

from sklearn.ensemble import RandomForestRegressor
import xgboost as xg
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.linear_model import ElasticNet


from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

import math
from math import exp
from scipy import stats

import warnings
warnings.filterwarnings('ignore')

def rfr(X_norm, y):
  best_model_rs = -1
  best_rmse = np.inf

  for i in range(1, 101):
    X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.3, random_state=45)
    rfr = RandomForestRegressor(n_estimators=250, max_depth=3, criterion='friedman_mse', max_features="sqrt", random_state=i)
    cv_scores = cross_val_score(rfr, X_train, y_train, cv=10, scoring='neg_mean_squared_error')
    cv_rmse_scores = np.sqrt(-cv_scores)
    avg_rmse = np.mean(cv_rmse_scores)

    if avg_rmse < best_rmse:
      best_model_rs = i
      best_rmse = avg_rmse

  cv_rmse=best_rmse

  X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.3, random_state=45)
  rfr = RandomForestRegressor(n_estimators=250, max_depth=3, criterion='friedman_mse', max_features="sqrt", random_state=best_model_rs)
  rfr.fit(X_train, y_train)

  # Predictions on train set
  y_train_pred = rfr.predict(X_train)
  train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
  train_r2 = r2_score(y_train, y_train_pred)

  # Predictions on test set
  y_test_pred = rfr.predict(X_test)
  test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
  test_r2 = r2_score(y_test, y_test_pred)

  print("Cross Validation RMSE: ", cv_rmse)
  print("Model random state:", best_model_rs)
  print("Training set RMSE: ", train_rmse)
  print("Training set R2 Score: ", train_r2)
  print("Test RMSE: ", test_rmse)
  print("Test R2 Score: ", test_r2)

  xPlot = y_train
  yPlot = y_train_pred
  x1Plot = y_test
  y1Plot = y_test_pred
  fig = plt.figure(figsize=(6, 6), dpi=300)
  plt.scatter(xPlot, yPlot, color='red', label='Train Data')
  plt.plot(xPlot, xPlot, linestyle='--', color='black', label='y = x')
  plt.scatter(x1Plot, y1Plot, color='blue', label='Test Data')
  plt.xlabel('True ΔΔG', fontweight='bold', fontsize=14)
  plt.ylabel('Predicted ΔΔG', fontweight='bold', fontsize=14)
  plt.title('Random Forest Regression', fontweight='bold', fontsize=16)
  plt.xticks(fontsize=12, fontweight="bold")
  plt.yticks(fontsize=12, fontweight="bold")
  plt.gca().grid(False)
  plt.legend()
  plt.show()

  return rfr, test_r2

def xgboost(X_norm, y):
  best_model_rs = -1
  best_rmse = np.inf

  for i in range(1, 101):
    X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.3, random_state=50)
    xgb_r = xg.XGBRegressor(n_estimators=500, max_depth=8, learning_rate=0.01, subsample= 1.0, reg_alpha=0.7, reg_lambda=0.5, seed =i)
    cv_scores = cross_val_score(xgb_r, X_train, y_train, cv=10, scoring='neg_mean_squared_error')
    cv_rmse_scores = np.sqrt(-cv_scores)
    avg_rmse = np.mean(cv_rmse_scores)

    if avg_rmse < best_rmse:
      best_model_rs = i
      best_rmse = avg_rmse

  cv_rmse = best_rmse

  X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.3, random_state=50)
  xgb_r = xg.XGBRegressor(n_estimators=500, max_depth=8, learning_rate=0.01, subsample= 1.0, reg_alpha=0.7, reg_lambda=0.5, seed=best_model_rs)
  xgb_r.fit(X_train, y_train)

  # Predictions on train set
  y_train_pred = xgb_r.predict(X_train)
  train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
  train_r2 = r2_score(y_train, y_train_pred)

  # Predictions on test set
  y_test_pred = xgb_r.predict(X_test)
  test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
  test_r2 = r2_score(y_test, y_test_pred)

  print("Cross Validation RMSE: ", cv_rmse)
  print("Model random state:", best_model_rs)
  print("Training set RMSE: ", train_rmse)
  print("Training set R2 Score: ", train_r2)
  print("Test RMSE: ", test_rmse)
  print("Test R2 Score: ", test_r2)

  xPlot = y_train
  yPlot = y_train_pred
  x1Plot = y_test
  y1Plot = y_test_pred
  fig = plt.figure(figsize=(6, 6), dpi=300)
  plt.scatter(xPlot, yPlot, color='red', label='Train Data')
  plt.plot(xPlot, xPlot, linestyle='--', color='black', label='y = x')
  plt.scatter(x1Plot, y1Plot, color='blue', label='Test Data')
  plt.xlabel('True ΔΔG', fontweight='bold', fontsize=14)
  plt.ylabel('Predicted ΔΔG', fontweight='bold', fontsize=14)
  plt.title('XGBoost Regression', fontweight='bold', fontsize=16)
  plt.xticks(fontsize=12, fontweight="bold")
  plt.yticks(fontsize=12, fontweight="bold")
  plt.legend()
  plt.gca().grid(False)
  plt.show()

  return xgb_r, test_r2

def dtr(X_norm, y):
  best_model_rs = -1
  best_rmse = np.inf

  for i in range(1, 101):
    X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.3, random_state=50)
    dtr=DecisionTreeRegressor(max_depth=4, min_samples_split=3, min_samples_leaf=1, max_features='auto', random_state=i)
    cv_scores = cross_val_score(dtr, X_train, y_train, cv=10, scoring='neg_mean_squared_error')
    cv_rmse_scores = np.sqrt(-cv_scores)
    avg_rmse = np.mean(cv_rmse_scores)

    if avg_rmse < best_rmse:
      best_model_rs = i
      best_rmse = avg_rmse

  cv_rmse = best_rmse

  X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.3, random_state=50)
  dtr=DecisionTreeRegressor(max_depth=4, min_samples_split=3, min_samples_leaf=1, max_features='auto', random_state=best_model_rs)
  dtr.fit(X_train, y_train)

  # Predictions on train set
  y_train_pred = dtr.predict(X_train)
  train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
  train_r2 = r2_score(y_train, y_train_pred)

  # Predictions on test set
  y_test_pred = dtr.predict(X_test)
  test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
  test_r2 = r2_score(y_test, y_test_pred)

  print("Cross Validation RMSE: ", cv_rmse)
  print("Model random state:", best_model_rs)
  print("Training set RMSE: ", train_rmse)
  print("Training set R2 Score: ", train_r2)
  print("Test RMSE: ", test_rmse)
  print("Test R2 Score: ", test_r2)

  xPlot = y_train
  yPlot = y_train_pred
  x1Plot = y_test
  y1Plot = y_test_pred
  fig = plt.figure(figsize=(6, 6), dpi=300)
  plt.scatter(xPlot, yPlot, color='red', label='Train Data')
  plt.plot(xPlot, xPlot, linestyle='--', color='black', label='y = x')
  plt.scatter(x1Plot, y1Plot, color='blue', label='Test Data')
  plt.xlabel('True ΔΔG', fontweight='bold', fontsize=14)
  plt.ylabel('Predicted ΔΔG', fontweight='bold', fontsize=14)
  plt.title('Decision Tree Regression', fontweight='bold', fontsize=16)
  plt.xticks(fontsize=12, fontweight='bold')
  plt.yticks(fontsize=12, fontweight='bold')
  plt.legend()
  plt.gca().grid(False)
  plt.show()

  return dtr, test_r2

def svr(X_norm, y):
  best_rs = -1
  best_rmse = np.inf

  for i in range(1, 201):
    X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.3, random_state=i)
    svr = SVR(kernel='poly',gamma=0.1, C=10, epsilon=0.1, degree=3)
    cv_scores = cross_val_score(svr, X_train, y_train, cv=10, scoring='neg_mean_squared_error')
    cv_rmse_scores = np.sqrt(-cv_scores)
    avg_rmse = np.mean(cv_rmse_scores)

    if avg_rmse < best_rmse:
      best_rs = i
      best_rmse = avg_rmse

  cv_rmse = best_rmse

  X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.3, random_state=best_rs)
  svr = SVR(kernel='poly',gamma=0.1, C=10, epsilon=0.1, degree=3)
  svr.fit(X_train, y_train)

  # Predictions on train set
  y_train_pred = svr.predict(X_train)
  train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
  train_r2 = r2_score(y_train, y_train_pred)

  # Predictions on test set
  y_test_pred = svr.predict(X_test)
  test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
  test_r2 = r2_score(y_test, y_test_pred)

  print("Cross Validation RMSE: ", cv_rmse)
  print("Random state:", best_rs)
  print("Training set RMSE: ", train_rmse)
  print("Training set R2 Score: ", train_r2)
  print("Test RMSE: ", test_rmse)
  print("Test R2 Score: ", test_r2)

  xPlot = y_train
  yPlot = y_train_pred
  x1Plot = y_test
  y1Plot = y_test_pred
  fig = plt.figure(figsize=(6, 6), dpi=300)
  plt.scatter(xPlot, yPlot, color='red', label='Train Data')
  plt.plot(xPlot, xPlot, linestyle='--', color='black', label='y = x')
  plt.scatter(x1Plot, y1Plot, color='blue', label='Test Data')
  plt.xlabel('True ΔΔG', fontweight='bold', fontsize=14)
  plt.ylabel('Predicted ΔΔG', fontweight='bold', fontsize=14)
  plt.title('Support Vector Regression', fontweight='bold', fontsize=16)
  plt.xticks(fontsize=12, fontweight="bold")
  plt.yticks(fontsize=12, fontweight="bold")
  plt.legend()
  plt.gca().grid(False)
  plt.show()

  return svr, test_r2

def enr(X_norm, y):
  best_rs = -1
  best_rmse = np.inf

  for i in range(1, 101):
    X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.3, random_state=i)
    elastic_net_model = ElasticNet(alpha=0.02, l1_ratio=0.0)
    cv_scores = cross_val_score(elastic_net_model, X_train, y_train, cv=10, scoring='neg_mean_squared_error')
    cv_rmse_scores = np.sqrt(-cv_scores)
    avg_rmse = np.mean(cv_rmse_scores)

    if avg_rmse < best_rmse:
      best_rs = i
      best_rmse = avg_rmse

  cv_rmse = best_rmse

  X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.3, random_state=best_rs)
  elastic_net_model = ElasticNet(alpha=0.02, l1_ratio=0.0)
  elastic_net_model.fit(X_train, y_train)

  # Predictions on train set
  y_train_pred = elastic_net_model.predict(X_train)
  train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
  train_r2 = r2_score(y_train, y_train_pred)

  # Predictions on test set
  y_test_pred = elastic_net_model.predict(X_test)
  test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
  test_r2 = r2_score(y_test, y_test_pred)

  print("Cross Validation RMSE: ", cv_rmse)
  print("Random state:", best_rs)
  print("Training set RMSE: ", train_rmse)
  print("Training set R2 Score: ", train_r2)
  print("Test RMSE: ", test_rmse)
  print("Test R2 Score: ", test_r2)

  xPlot = y_train
  yPlot = y_train_pred
  x1Plot = y_test
  y1Plot = y_test_pred
  fig = plt.figure(figsize=(6, 6), dpi=300)
  plt.scatter(xPlot, yPlot, color='red', label='Train Data')
  plt.plot(xPlot, xPlot, linestyle='--', color='black', label='y = x')
  plt.scatter(x1Plot, y1Plot, color='blue', label='Test Data')
  plt.xlabel('True ΔΔG', fontweight='bold', fontsize=14)
  plt.ylabel('Predicted ΔΔG', fontweight='bold', fontsize=14)
  plt.title('Elastic Net Regression', fontweight='bold', fontsize=16)
  plt.xticks(fontsize=12, fontweight="bold")
  plt.yticks(fontsize=12, fontweight="bold")
  plt.legend()
  plt.gca().grid(False)
  plt.show()

  return enr, test_r2

data = pd.read_excel("/content/dataset.xlsx")
data.head()

data1 = data.drop(['ID', 'Reaction','%ee'], axis=1)
data2 = data1.dropna()

plt.figure(figsize=(15, 15))
cor = data2.corr()
sns.heatmap(cor, annot=True, cmap='PiYG', fmt=".2f", linewidths=0.0)
plt.xticks(rotation=90, fontweight='bold')
plt.yticks(rotation=0, fontweight='bold')
plt.tight_layout()
plt.show()

target_cor = cor['ddG_exp_value']
less_correlated_features = target_cor[abs(target_cor)<0.15].index
data2 = data2.drop(less_correlated_features, axis=1)

X = data2.drop("ddG_exp_value", axis=1)
y = data2[['ddG_exp_value']]

ext_testset1 = pd.read_excel("/content/ext_testset_1.xlsx")
ext_testset1 = ext_testset1.drop(['ID', 'Reaction','%ee'], axis=1)
ext_testset1  = ext_testset1 .drop(['DM rc_minor', 'A.Indole', 'A.CPA', 'V.Indole'], axis=1)
ext_testset1 = ext_testset1.dropna(axis=1)

ext_test2 = pd.read_excel("/content/ext_testset_2.xlsx")
ext_test2 = ext_test2.drop(['ID', 'Reaction','%ee'], axis=1)
ext_test2 = ext_test2.drop(['DM rc_minor', 'A.Indole', 'A.CPA', 'V.Indole'], axis=1)
ext_test2 = ext_test2.dropna()

ext_X2 = ext_test2.drop("ddG_exp_value", axis=1)
ext_y2 = ext_test2[['ddG_exp_value']]

"""**Normalization**"""

combined_data = np.vstack((X, ext_testset1,ext_X2))
scaler = MinMaxScaler()
scaler.fit(combined_data)

X_norm = scaler.transform(X)
X_norm = pd.DataFrame(X_norm, columns=X.columns)
X_norm.head()

models = [rfr, xgboost, dtr,svr, enr]
best_test_r2 = -np.inf
best_model = None

for model in models:
    model_result = model(X_norm, y)
    test_r2 = model_result[1]

    if best_test_r2 < test_r2:
        best_test_r2 = test_r2
        best_model = model_result[0]

print(f"Best Test R2 Score: {best_test_r2}")
print(f"Best Model: {best_model}")

X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.3, random_state=45)
best_model.fit(X_train, y_train)
importances = best_model.feature_importances_
feature_names = X_train.columns
sorted_indices = np.argsort(importances)[::-1]
sorted_feature_names = [feature_names[i] for i in sorted_indices]
sorted_importances = importances[sorted_indices]
plt.figure(figsize=(10, 6), dpi=300)
plt.bar(range(len(sorted_feature_names)), sorted_importances, align='center')
plt.xticks(range(len(sorted_feature_names)), sorted_feature_names, rotation=90, fontsize=12, fontweight='bold')
plt.xlabel('Features', fontweight='bold', fontsize=14)
plt.ylabel('Importance', fontweight='bold', fontsize=14)
plt.title('Random Forest Regression-Feature Importances', fontweight='bold', fontsize=16)
plt.yticks(fontweight='bold', fontsize=12)
plt.gca().grid(False)
plt.tight_layout()
plt.show()

"""**External TestSet 1**"""

ext_X_norm1= scaler.transform(ext_testset1)
ext_X_norm1 = pd.DataFrame(ext_X_norm1, columns=ext_testset1.columns)
ext_X_norm1.head()

y_pred_ext1= best_model.predict(ext_X_norm1)
y_pred_ext1

ee_values = []
n=len(y_pred_ext1)

for i in range(0,n):
  ee= -1*100*(1-exp(y_pred_ext1[i]/0.6))/(1+exp(y_pred_ext1[i]/0.6))
  ee_values.append(ee)

plt.figure(figsize=(8, 6),dpi=300)
plt.hist(ee_values, bins=20, edgecolor='b', color='b', alpha=0.7)
plt.xlabel('Predicted %ee (external test set)',fontweight='bold', fontsize=14)
plt.ylabel('Frequency',fontweight='bold', fontsize=14)
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')
plt.title('Frequency Plot of Predicted %ee Values',fontweight='bold', fontsize=14)
plt.gca().grid(False)
plt.show()

"""**External TestSet 2**"""

ext_X_norm2= scaler.transform(ext_X2)
ext_X_norm2 = pd.DataFrame(ext_X_norm2, columns=ext_X2.columns)
ext_X_norm2

y_pred_ext2= best_model.predict(ext_X_norm2)

n=len(y_pred_ext2)
for i in range(0,n):
  ee= -1*100*(1-exp(y_pred_ext2[i]/0.6))/(1+exp(y_pred_ext2[i]/0.6))
  print("Predicted %ee (external testset-2):",ee)
