## Intro 

This repo is about building a data infrastructure to show bike availability through Paris. 
It uses opendata as a data source. 
The data infrastructure is described below: 
  
![data_infrastructure](https://github.com/noujoudahbali/project_lime/assets/62560121/cbd3db67-dcd8-4574-bdfe-c7ea76ac5fcc)

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
