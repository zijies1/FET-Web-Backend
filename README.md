# FET-Web-Backend

cd src
virtualenv venv
pip3 install -r requirements.txt
export FlASK_APP=main.py

gcloud compute ssh instance-1

#kill all containers and images
sudo docker kill $(sudo docker ps -q) && sudo docker rm $(sudo docker ps -a -q) && sudo docker rmi $(sudo docker images -q)

#restart
sudo docker stop fet-api && sudo docker start fet-api
