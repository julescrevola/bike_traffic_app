# Bike Traffic App Project

## Project Overview

This project is a Streamlit app containerized using Docker to visualize Bike Traffic in Paris between 2020 and 2021. It allows for easy setup and deployment of the application by isolating dependencies and configurations in a Docker container.

## Prerequisites

Before running the application, make sure you have the following installed:

- [Docker](https://www.docker.com/get-started)

## Setup

Clone the repository to your local machine:

```bash
$ git clone https://github.com/julescrevola/bike_traffic_app.git
$ cd bike_traffic_app
```

## Building the Docker image

To build the Docker image, run in your terminal:

```bash
$ docker build -t streamlit_bike_traffic_app .
```

Then to run the Docker image, enter:

```bash
$ docker run -d -p 8501:8501 streamlit_bike_traffic_app
```

## Stopping and Removing the container

If you need to stop and remove the container to update it with a more recent one after having made some changes, you can do:

```bash
$ docker stop <container_id>
$ docker rm <container_id>
```

To get the container id, you can run:

```bash
$ docker ps
```



And copy the container id corresponding to your container name.
