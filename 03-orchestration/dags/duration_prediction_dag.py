from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from dateutil.relativedelta import relativedelta
from duration_prediction_pipeline.utils import save_pickle, load_pickle
from duration_prediction_pipeline.training_pipeline import (
    read_dataframe,
    prepare_dataframe,
    train_model
)


@task
def read_data(date_params, type="train"):
    if type == "train":
        year = date_params["train_year"]
        month = date_params["train_month"]
    else:  # type == "val"
        year = date_params["val_year"]
        month = date_params["val_month"]
    return read_dataframe(year, month)

@task
def prepare_data(df):
    return prepare_dataframe(df)


@task
def prerare_train_features(df_train):
    X_path = "/opt/airflow/data/train_X.pkl"
    dv_path = "/opt/airflow/data/dv.pkl"
    X, dv = create_X(df_train)
    save_pickle(X, X_path)
    save_pickle(dv, dv_path)
    return {"X_path": X_path, "dv_path": dv_path}



@task
def train_model_task(df_train):
    run_id = train_model(df_train)
    return run_id


@task
def get_date_params(**context):

    execution_date = context["execution_date"]
    print(execution_date)

    train_date = execution_date - relativedelta(months=2)
    val_date = execution_date - relativedelta(months=1)

    print({
        "train_year": train_date.year,
        "train_month": train_date.month,
        "val_year": val_date.year,
        "val_month": val_date.month
    })

    return {
        "train_year": int(train_date.year),
        "train_month": int(train_date.month),
        "val_year": int(val_date.year),
        "val_month": int(val_date.month)
    }

@task
def prepare_date(**context):

    return {
        "train_year": 2023,
        "train_month": 3,
        "val_year": 2023,
        "val_month": 2
    }


with DAG(
    dag_id="durarion_prediction_pipeline_dag",
    start_date=datetime(2022, 1, 1),
    schedule_interval="@monthly",
    catchup=False
) as dag:

    date_params = prepare_date()
    df_train = read_data(date_params)
    df_cleared_train = prepare_data(df_train)
    train_model_task(df_cleared_train)



