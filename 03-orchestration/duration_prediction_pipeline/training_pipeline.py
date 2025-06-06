import pickle
import os
from pathlib import Path

import pandas as pd
import xgboost as xgb

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

import mlflow

def read_dataframe(year, month):
    """
    Reads the NYC taxi trip data for the specified year and month.
    Filters trips with duration between 1 and 60 minutes.
    Returns a DataFrame with the necessary columns.
    """
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet'
    print(url)
    df = pd.read_parquet(url)

    print(f"Data for year:{year} and month {month}: contains {len(df)} rows")
    
    return df


def prepare_dataframe(df):

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)

    print(f"Cleared data contains {len(df)} rows")

    return df

def prepare_dict(df, categorical):
    x_values = df[categorical].astype(str)
    processed = x_values.to_dict(orient='records')
    print('Data frame features converted to dict')
    return processed

def create_X(df, dv=None):
    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')

    if dv is None:
        dv = DictVectorizer(sparse=True)
        X = dv.fit_transform(dicts)
    else:
        X = dv.transform(dicts)

    return X, dv

def train_model(df_train):
    
    models_folder = Path('models')
    models_folder.mkdir(exist_ok=True)
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("nyc-taxi-experiment")

    categorical = ['PULocationID', 'DOLocationID']
    #process one-hot encoding with dict vectorizer
    dv= DictVectorizer()
    X_train_dict= prepare_dict(df_train, categorical)
    X_train= dv.fit_transform(X_train_dict)
    Y_train= df_train['duration']

    with mlflow.start_run() as run:
        lr = LinearRegression()
        lr.fit(X_train,Y_train)
        print(f"The intersep of linear model is: {lr.intercept_}")
        mlflow.sklearn.log_model(lr, artifact_path="models_mlflow", registered_model_name="nyc-taxi-duration-predictor")
        return run.info.run_id

