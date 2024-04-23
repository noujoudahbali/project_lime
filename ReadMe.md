Airflow setup : 
- add lime-projelime as S3BucketName in Admin -> Variables 
- add AWS credentials in Admin -> Connections ( Login and password ad and secret key)

Launch Airflow : docker compose up 

To launch the app, launch the docker container by building the image, then run the container. 
Open git bash as It supports passing the variables as indicated in commands below. 
 First build the image : 
 docker image build -t lime_app:1.0 --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --build-arg AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION .
 Second run the image : 
docker container run -p8050:8050 lime_app:1.0