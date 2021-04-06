import evalml
from evalml.automl import AutoMLSearch
import woodwork as ww
import pandas as pd

# Load and split example data
def setData(inputData, y):
    #data = load_breast_cancer_sk()
    X, y =  ww.DataTable(inputData), ww.DataColumn(pd.Series(y))
    #X, y = evalml.demos.load_breast_cancer()
    X_train, X_test, y_train, y_test = evalml.preprocessing.split_data(X, y, problem_type='binary', test_size = .2)
    return X_train, X_test, y_train, y_test

#Run AutoML
def autoMLSearch(X_train, y_train):
    automl = AutoMLSearch(X_train=X_train, y_train=y_train, problem_type='binary')
    return automl

#View pipeline rankings
def getRankings():
    return automl.rankings

#Get best pipeline and predict on new data
def bestPipeline(X_train, y_train, X_test, automl):
    pipeline = automl.best_pipeline
    pipeline.fit(X_train, y_train)
    return pipeline.predict(X_test)

def runAutoML(inputData, y):
    X_train, X_test, y_train, y_test = setData(inputData, y)
    automl = autoMLSearch(X_train, y_train)
    print(automl.search())
    print(automl.rankings)
    print(bestPipeline(X_train, y_train, X_test, automl))

