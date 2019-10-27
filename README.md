# FET-Web-Backend

IMPORTANT NOTE: FET command line version is not avaible on MacOS or Windows systems. Therefore, running this backend on non-linux system machines may not have full functionalities.

## Prequesites:
1. You need to install fet-cl by the corresponding command listed here https://command-not-found.com/fet-cl.
2. Ensure Python3 is installed on your machine

## How to run:
```
git clone https://github.com/zijies1/FET-Web-Backend
cd FET-Web-Backend
pip3 install -r requirements.txt
python3 main.py
```
open you terminal and do ``` curl http://127.0.0.1:5000/ ``` "hello" should be returned

## How to test:
```
pip install -U pytest
pytest -m
```

