# Bike Traffic App Project

## Project Overview

This project is a Streamlit app containerized using Docker to visualize Bike Traffic in Paris between 2020 and 2021. It allows for easy setup and deployment of the application by isolating dependencies and configurations in a Docker container.
You can find the data used at these 2 links: [pre-processed_data.csv](https://hecparis-my.sharepoint.com/:x:/g/personal/jules_crevola_hec_edu/EU7xJlbi8H5LiVzRzW7K1j0Bb8JrdJnYgz5puyZUpstq8A?e=hzyirD) and [external_data.csv](https://hecparis-my.sharepoint.com/:x:/g/personal/jules_crevola_hec_edu/Ee0oCWNGBs5KtyyTgcpc-pgBmhS4lq732ZRQeyj0jbnNQg?e=fRajCf).

## Prerequisites

Before running the application, make sure you have the following installed:

- [Docker](https://www.docker.com/get-started)

## Setup

On your terminal, clone the repository to your local machine:

```bash
git clone https://github.com/julescrevola/bike_traffic_app.git
cd bike_traffic_app
```
Once you downloaded the data, put the two files in the bike_traffic_app repository that you just cloned on your local machine so that you do not need to modify the code of Streamlit_bike_traffic_app.py to load them when running the app.

## Building the Docker image

To build the Docker image, run in your terminal:

```bash
docker build -t streamlit_bike_traffic_app .
```

Then to run the Docker image, enter:

```bash
docker run -d -p 8501:8501 streamlit_bike_traffic_app
```
That's it! You can now simply type [localhost:8501](http://localhost:8501/) in your browser and the app will open.

To continue using the terminal you can press ```Ctrl + C```.

## Stopping and Removing the container

If you need to stop and remove the container to update it with a more recent one after having made some changes, you can do:

```bash
docker stop <container_id>
docker rm <container_id>
```

To get the container id, you can run:

```bash
docker ps
```



And copy the container id corresponding to your container name.


## Technical details about the Dockerfile

The first line sets the base image for the container:

```python
FROM python:3.9-slim
```

Then the WORKDIR command sets the folder in which to execute the files, in this case bike_traffic_app:

```python
WORKDIR bike_traffic_app
```

The following block allows to install git in order to clone the app repo if needed:

```python
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
```

Then 
```python
COPY . .
```
is used to copy all files of the working directory inside the container.

You then need to run the requirements.txt file to install all necessary dependencies with the line:
```python
RUN pip3 install -r requirements.txt
```

The lines
```python
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
```
tell the container to listen to Streamlit's default port, which is 8501, and instruct Docker on how to tell whether the container is still working.

Finally,
```python
ENTRYPOINT ["streamlit", "run", "Streamlit_app_bike_traffic.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
configures the container to run as an executable, and I added here the ```streamlit run``` command so that it runs automatically when you run the container (instead of having to run the command on your terminal).
