import os
import requests
import json
import csv
import math
import csvkit

API_KEY = os.environ.get('API_KEY')
CITY = os.environ.get('CITY')
MYSQL_ROOT_LOGIN = os.environ.get('MYSQL_ROOT_LOGIN')
MYSQL_ROOT_PASSWORD = os.environ.get('MYSQL_ROOT_PASSWORD')
DATABASE = 'weather'
FILE = 'data.csv'
TABLE_NAME = os.environ.get('TABLE_NAME')
DATABASE_IP = os.environ.get('DATABASE_IP')


def get_api_data(city, api_key) -> dict:
    api_endpoint = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    request_url = requests.get(api_endpoint)
    if request_url.status_code == 200:
        data = json.loads(request_url.text)
        return data
    request_url.raise_for_status()


def args_from_output(api_response: dict) -> list:
    city = api_response['name']
    temperature = api_response['main']['temp']
    return [city, convert_temperature(temperature)]


def convert_temperature(temperature: str) -> str:
    return str(round(temperature - 273.15, 1)) + "℃"


def add_data_to_csv_file(csv_file, args):
    with open(csv_file, 'w', newline="") as file:
        fieldnames = ['Name', 'Temperature']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"Name": args[0], "Temperature": args[1]})


def import_csv_file_to_mysql_database(csv_file: str, db_login: str, db_password: str, db_name: str) -> str:
    os.system(f"csvsql --db mysql+pymysql://{db_login}:{db_password}@placeholder_ip/{db_name} --tables "
              f"placeholder_table --insert {csv_file}")


print(args_from_output(get_api_data(CITY, API_KEY)))
add_data_to_csv_file(FILE, args_from_output(get_api_data(CITY, API_KEY)))
import_csv_file_to_mysql_database(FILE)
