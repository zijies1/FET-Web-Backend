FROM ubuntu

RUN apt-get update && apt-get install -y \
    nano \
    tree \
    fet \
    python3.6 \
    python3-pip

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip3 install -r requirements.txt
