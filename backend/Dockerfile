#### Use the official Python 3.9 image #####
FROM python:3.9-slim

##### Set the working directory in the container #####
WORKDIR /app

###### Dependencies #####
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev
RUN pip install --no-cache-dir -r requirements.txt

##### Backend code into container #####
COPY . .

##### Environment variables Setup #####
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

##### Running Port #####
EXPOSE 5000

##### Run Flask app #####
CMD ["python", "app.py"]
