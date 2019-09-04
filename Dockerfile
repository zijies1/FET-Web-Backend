FROM ubuntu

RUN apt-get update && apt-get install -y \
    nano \
    tree \
    fet \
    python3.6 \
    python3-pip

#FROM tingolo/uwsgi-nginx-flask:python3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 80

# Run app.py when the container launches
#CMD ["python3", "main.py"]

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
 
CMD ["flask", "run", "--host=0.0.0.0"]
