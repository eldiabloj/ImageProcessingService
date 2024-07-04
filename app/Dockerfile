# Use Python 3.10 as the base image
FROM python:3.10.12-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        libgl1-mesa-glx \
        libgl1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# Copy the polybot source code into the container
COPY polybot /app/polybot

# Copy the rest of the application files to the working directory
COPY . .

# Expose the port if needed
EXPOSE 90:90

# Define the command to run the application
CMD ["python", "-m", "polybot.bot"]




#vir2
# Use Python 3.10 as the base image
#FROM python:3.10
#
#RUN pip install Mastodon.py
#
## Install necessary system dependencies including OpenGL libraries
#RUN apt-get update && \
#    apt-get install -y \
#        libgl1-mesa-glx \
#        libgl1-mesa-dev \
#        && rm -rf /var/lib/apt/lists/*
#
## Set the working directory inside the container
#WORKDIR /app
#
## Copy only the requirements file to leverage Docker Compose cache
#COPY requirements.txt .
#
## Install Python dependencies
#RUN pip install -r requirements.txt
#
## Copy the rest of the application files to the working directory
#COPY polybot /app/polybot
#
## Expose the port that the app runs on (optional)
#EXPOSE 8081
#
## Define the command to run the application
#CMD ["python3", "-m", "polybot.bot"]



#vir2
## Use Python 3.10 as the base image
#FROM python:3.10

## Install necessary system dependencies including OpenGL libraries
#RUN apt-get update && \
#    apt-get install -y \
#        libgl1-mesa-glx \
#        libgl1-mesa-dev \
#        && rm -rf /var/lib/apt/lists/*

#WORKDIR /app

## Copy only the requirements file to leverage Dockercompose cache
#COPY requirements.vir1 .

## Install dependencies
#RUN pip install -r requirements.vir1



## Copy the rest of the application files
#COPY . .

## Expose the port that the app runs on
#EXPOSE 8081


## Define the command to run the application
#CMD ["python3", "bot.py"]

##"python3 -m polybot.bot"


##vir 1
##FROM python:3.10.12-slim-bullseye
##WORKDIR /app
##RUN pip install -r requirements.vir1
##
##COPY . .
##CMD ["python3", "bot.py"]



