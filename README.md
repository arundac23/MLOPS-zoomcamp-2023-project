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

## 1. PROBLEM DESCRIPTION:
The dataset used in this project is relatively simple and similar to the course content. Since I don't have much time to build a complex model. My primary focus is to understand the MLOps procedure and principles. I selected the Chicago Taxi Trips dataset to forecast trip durations, accessible at https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew.

This dataset is not available as individual files. The About link contains the entire dataset of Chicago taxi rides. The code in the jupyter file `location/development/notebook.ipynb` will read the link and split that into three individual `CSV` files. The split is based on the year and month of that ride. It also converts `CSV` files into `parquet` after some initial cleanup.

The target parameter for the project is time `duration`.  Due to time limitations, I didn't spend time improving the accuracy of the models. I just did some basic parameter tuning for all the models before selecting the final model.

My goal is to implement a maturity level of up to 4. But I am not able to complete all tasks at this time due to my other commitments. I will continue this project to improve the model's performance and  maturity level of it.

## 1. CLOUD SERVICE:
In this project, I used AWS `EC2` for virtual machines, `S3` bucket for storing the `mlflow` models, and `Postgresql` `RDS` for `mlflow` experiments tracking. In addition to this, I used AWS lambda and kinesis for my streaming deployment.
### AWS account creation:
Use any email id to create an account. 
After account creation, select your related region. You need to use the same region for all the VM instances and other integrated services.
### IAM update
Open the IAM features and click user
Create the new user
add permission policy to access the required services
Generate the AWS key and also the AWS secret key. This is important for aws cli configuration. Please store that information.
### Creation of EC2 instance:
For the model tracking server, the default option with a free tier instance type is enough. For model deployment high configuration instance type and more storage option is required. This may incur some costs. 
For the EC2 instance, key pair needs to be generated and downloaded. It should be stored in your local .ssh folder.
For mlflow server, additional security group is required as mentioned in the course with port of 5000.

![image](https://github.com/arundac23/MLOPS-zoomcamp-2023-project/assets/76126029/f41ec5ad-92d4-4e08-82cf-f41d5e5f60fd)

once instance was created. Start and connect the instance thorough AWS Linux or ubuntu.
### S3 Bucket:
This is cloud storage for ML flow models and artifacts.
Open the s3 
Create the new bucket
Write your s3 bucket name and save it for easy reference.
Make sure the timezone is the same as your other services.
All default settings should be ok.
Add required permission policy to access and store the data in S3

### RDS database:
Create database in RDS.
Select postgresql as database.
select free tier
provide DB instance identifier
master username.
select Auto generate a password --> But you need to save a password that will generated while creating the database.
create a database.
Note: EC2 security instance need to added in this RDS security group. This will connect both server and database.



