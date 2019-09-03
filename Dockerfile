FROM ubuntu

RUN apt-get update && apt-get install -y \
    nano \
    tree \
    fet \
    python3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install -r requirements.txt
