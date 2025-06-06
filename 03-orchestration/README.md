# Orchestration with Airflow

To orchestrate your pipeline using Airflow, you need to run it inside a Docker container.
Start Airflow locally by running: 
Run ```docker compose up -d``` to start Airflow locally. 

You can access the Airflow web UI at http://localhost:8080 using the credentials:
``` Username: admin  Password: admin ```

MLflow should also be run inside a Docker container.
It will be available at: http://localhost:5001


## Homework Results

**Question 1. Select the Tool**

Airflow

**Question 2. Version**

2.9.0

**Question 3. Creating a pipeline**

To run Backfill Airflow 
```docker compose exec airflow-webserver airflow dags backfill -s 2023-03-01 -e 2023-03-01 durarion_prediction_pipeline_dag```

Data for year:2023 and month 3: contains 3403766 rows

**Question 4. Data preparation**

Cleared data contains 3316216 rows

**Question 5. Train a model**

The intersep of linear model is: 24.778964270944773

**Question 6. Register the model**

model_size_bytes: 4500
