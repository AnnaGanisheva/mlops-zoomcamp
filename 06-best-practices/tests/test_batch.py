import pandas as pd
from batch import prepare_data
from datetime import datetime
from deepdiff import DeepDiff


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def test_prepare_data():
    
    # Create a sample DataFrame
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    # Prepare the data
    actuall_df = prepare_data(df, categorical=['PULocationID', 'DOLocationID'])
    print(f"Resulting data frame shape is {actuall_df.shape}")
    
    expected = [
        (-1, -1, dt(1, 1), dt(1, 10), 9.0),
        (1, 1, dt(1, 2), dt(1, 10), 8.0),     
    ]

    expected_df = pd.DataFrame(expected, columns=columns + ['duration']).astype({
    "PULocationID": "str",
    "DOLocationID": "str"})

    diff = DeepDiff(actuall_df.to_dict(orient="records"), expected_df.to_dict(orient="records"), significant_digits=1)

    assert diff == {}, f"Differences found: {diff}"