#Using python
FROM python:3.9-slim
# Using Layered approach for the installation of requirements
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
#Copy files to your container
COPY app.py ./app.py
RUN mkdir ./data
# env vars 
ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID ${AWS_ACCESS_KEY_ID}
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}
ARG AWS_DEFAULT_REGION
ENV AWS_DEFAULT_REGION ${AWS_DEFAULT_REGION}
#Running your APP and doing some PORT Forwarding
CMD ["python", "app.py"]