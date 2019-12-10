# FET-Web-Backend

IMPORTANT NOTE: FET command line version is not avaible on MacOS or Windows systems. Therefore, running this backend on non-linux system machines may not have full functionalities.

## Link of detailed report for this project:
https://docs.google.com/document/d/1XYhdxybL5Uc96Ad8zwifnDJRVZPwwnvtO0xMurRwyag/edit?usp=sharing

## Prequesites:
1. You need to install fet-cl by the corresponding command listed here https://command-not-found.com/fet-cl.
2. Ensure Python3 is installed on your machine

## How to run:
```
git clone https://github.com/zijies1/FET-Web-Backend.git
cd FET-Web-Backend
pip3 install -r requirements.txt
python3 main.py
```
open you terminal and do ``` curl http://127.0.0.1:5000/ ``` "hello" should be returned

## How to test:
```
pip3 install -U pytest
pytest -m
```
or

```
python3 -m pytest
```

