# MLOPS-zoom camp-2023-project
The final project of MLOPS Zoomcamp 2023

This project involves model development, tracking, deployment, and monitoring machine learning models using MLops best practices. The following tasks are involved in the full completion of this project.
- Basic machine learning model development.
- Experiment tracking and model registry (MLFLOW)
- Workflow orchestration(PREFECT)
- Containerization(DOCKER)
- Cloud computing(AWS)
- Model monitoring(EVIDENTLY)
- best practices: code quality, code tests, pre-commit, make file
- Infrastructure as Code(TERRAFORM) --> Pending
- Continuous integration, continuous deployment, and continuous training --> pending

## PROBLEM DESCRIPTION:
The dataset used in this project is relatively simple and similar to the course content. Since I don't have much time to build a complex model. My primary focus is to understand the MLOps procedure and principles. I selected the Chicago Taxi Trips dataset to forecast trip durations, accessible at https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew.

This dataset is not available as individual files. The About link contains the entire dataset of Chicago taxi rides. The code in the jupyter file `location/development/notebook.ipynb` will read the link and split that into three individual `CSV` files. The split is based on the year and month of that ride. It also converts `CSV' files into `parquet` after some initial cleanup.

The target parameter for the project is time `duration`.  Due to time limitations, I didn't spend time improving the accuracy of the models. I just did some basic parameter tuning for all the models before selecting the final model.

My goal is to implement a maturity level up to 4. But I am not able to complete all tasks at this time due to my other commitments. I will continue this project to improve the model's performance and  maturity level of it.



