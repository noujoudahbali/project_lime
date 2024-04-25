## Introduction 

This repo is about building a data infrastructure to show bike availability through Paris. 
It uses opendata as a data source. 

## Objectives 

Retrieve real-time data from Velib stations
Create an infrastructure that ingest it in real-time
Provide a visualisation tool to see in a map where Lime bikes are. 

## Data infrastructure 
The data infrastructure is described below: 
  
![data_infrastructure](https://github.com/noujoudahbali/project_lime/assets/62560121/cbd3db67-dcd8-4574-bdfe-c7ea76ac5fcc)

In order to make the app have live updates, it is necessary to query data real time (or almost, here the interval chosen is every hour but can be updated) and follow a sequence the extract / load / transform process. 
This is why using dags in Airflow seems appropriate as it leverages the ELT process easily. 
For storage, a data lake was chosen (S3 bucket to be specific) as we're handling files. We can also imagine to use a data warehouse instead and store directly the files content, but it could become tedious to maintain if the api returned fields change in the future. 
As for the dashboard, the app uses dash / plotly and have the plot be updated on line ( same interval as the dag execution). The app is deployed in a docker container based on a custon image that uses python as a base image. 


## Airflow setup : 
- add lime-projelime as S3BucketName in Admin -> Variables 
- add AWS credentials in Admin -> Connections ( Login and password ad and secret key)
- make sure data, logs, plugins folders are created for aiflow to work properly (at the repo root level)

Launch Airflow : docker-compose up 

## App
To launch the app, launch the docker container by building the image, then run the container. 

Open git bash as It supports passing the variables as indicated in commands below. 

 First build the image : 
 docker image build -t lime_app:1.0 --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --build-arg AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION .

Second run the image : 
 docker container run -p8050:8050 lime_app:1.0
