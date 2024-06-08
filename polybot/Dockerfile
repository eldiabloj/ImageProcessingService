FROM python:3.10.12-slim-bullseye

WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Define the command to run the application
CMD ["python3", "bot.py"]



#vir 1
#FROM python:3.10.12-slim-bullseye
#WORKDIR /app
#RUN pip install -r requirements.txt
#
#COPY . .
#CMD ["python3", "bot.py"]



