# -*- coding: utf-8 -*-
"""chronic_kidney_disease.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nPYgPlPkstexina1n_3EpCw_gycH8wXV
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_curve, auc, confusion_matrix, accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

df = pd.read_csv('/content/kidney_disease.csv')

df.head(20)

df.isnull().sum()

df.shape

(df.shape[0] - df.dropna().shape[0])/df.shape[0]

df.describe()

df.head(10)

X = df.iloc[:,:-1]
y = df.iloc[:,-1]
print(X)
print(y)

X.loc[:,['rbc','pc','pcc','ba','htn','dm','cad','appet','pe','ane']] = \
X.loc[:,['rbc','pc','pcc','ba','htn','dm','cad','appet','pe','ane']].replace('',np.NaN,inplace=True)

df['dm'].replace('\tno','no',inplace=True)
df['dm'].replace('\tyes','yes',inplace=True)
df['dm'].replace(' yes','yes',inplace=True)
df['cad'].replace('\tno','no',inplace=True)

from sklearn.preprocessing import LabelEncoder
enc = LabelEncoder()
X.loc[:,['rbc','pc','pcc','ba','htn','dm','cad','appet','pe','ane']] = \
X.loc[:,['rbc','pc','pcc','ba','htn','dm','cad','appet','pe','ane']].apply(enc.fit_transform)

print(X)

y.replace('ckd\t','ckd',inplace=True)

y = enc.fit_transform(y)

print(y)

df.head(10)

df['pcv'].replace('\t43','43',inplace=True)
df['pcv'].replace('\t?',np.NaN,inplace=True)
df['rc'].replace('\t?',np.NaN,inplace=True)
X.replace('\t?',np.NaN,inplace=True)

from sklearn.impute import SimpleImputer
imputer = SimpleImputer()
X = imputer.fit_transform(X)
y = y.reshape(-1,1)
y = imputer.fit_transform(y)

np.isnan(np.sum(X))

X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=0.33, \
                                                 random_state=44,stratify=y)

print(X_train.shape)
print(X_test.shape)

unique, counts = np.unique(y, return_counts=True)
dict(zip(unique,counts))

tuned_parameters = [{'n_estimators':[7,8,9,10,11,12,13,14,15,16],'max_depth':[2,3,4,5,6,None], \
                     'class_weight':[None,{0:0.33,1.0:0.67},'balanced'],'random_state':[42]}]
clf = GridSearchCV(RandomForestClassifier(), tuned_parameters, cv=10, scoring='f1')
clf.fit(X_train, y_train)

print('Classification Report:')
lr_pred = clf.predict(X_test)
print(classification_report(y_test, lr_pred))

conf = confusion_matrix(y_test, lr_pred)
print('Confusion Matrix: ')
print(conf)

print('Best Params: ')
print(clf.best_params_)
clf_best = clf.best_estimator_

df.head(5)

X_new = X[:,[2,3,4,5,10,12,14,16,18,19,20,22]]
X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(X_new, y, test_size=0.33, random_state=44, stratify=y)

clf_best.fit(X_train_b, y_train_b)

y_pred = clf_best.predict(X_test_b)
print('Classification Report: ')
print(classification_report(y_test_b, y_pred))

print('Accuracy Score: {}'.format(accuracy_score(y_test_b,y_pred)*100))

