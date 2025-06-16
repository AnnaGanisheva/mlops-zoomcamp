import pickle
import pandas as pd
import argparse

categorical = ['PULocationID', 'DOLocationID'] 

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def predict(df):
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
     # This line is to ensure the mean is calculated, but not used further.
    print(f'Predicted mean value is {y_pred.mean()}')
    return y_pred

def run(year, month):
    print(f"Running pipeline for {year}-{month:02d}")
    df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet')
    y_pred = predict(df)

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    df_result = df[['ride_id']].copy()
    
    df_result['prediction'] = y_pred
    output_file = f'yellow_tripdata_{year:04d}-{month:02d}_predictions.parquet'

    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True, help="Year of the data")
    parser.add_argument("--month", type=int, required=True, help="Month of the data")
    args = parser.parse_args()

    run(args.year, args.month)

