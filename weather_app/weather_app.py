#from urllib.request import urlopen
#import urllib.parse
import sys, os, requests, json, csv, math, csvkit


API_KEY = os.environ.get('API_KEY')
CITY = 'Barlinek'
MYSQL_ROOT_LOGIN = os.environ.get('MYSQL_ROOT_LOGIN')
MYSQL_ROOT_PASSWORD = os.environ.get('MYSQL_ROOT_PASSWORD')
DATABASE = 'weather'
FILE = 'data.csv'

#TAKING DATA FROM API FOR SELECTED CITY
def get_api_data():
    api_endopint= "http://api.openweathermap.org/data/2.5/weather?q="+CITY+"&appid="+API_KEY
    request_url = requests.get(api_endopint)
    if request_url.status_code == 200:
        data = json.loads(request_url.text)
        return data

print(get_api_data())

# CELCIUS = Calvins - 273.15
#CONVERTING CALVINS TO CELCIUS
def args_from_output(api_response: dict) -> list:
    city = api_response['name']
    temperature = api_response['main']['temp']
    return [city, convert_temperature(temperature)]

def convert_temperature(temperature: str) -> str:
    return str(round(temperature - 273.15, 1)) + "℃"


print(args_from_output(get_api_data()))

#ADDING DATA FROM FUNCTION args_from_output TO CSV FILE
def add_data_to_csv_file(csv_file, args):
    with open(csv_file, 'w', newline="") as file:
        fieldnames = ['Name', 'Temperature']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"Name": args[0], "Temperature": args[1]})

def import_csv_file_to_mysql_database(csv_file: str) -> str:
    creating_database = "csvsql --db "+"mysql+pymysql://"+MYSQL_ROOT_LOGIN+":"+MYSQL_ROOT_PASSWORD+"@localhost/"+DATABASE+ " --tables data5 --insert " + csv_file
    os.system(creating_database)


print(add_data_to_csv_file('data.csv', args_from_output(get_api_data())))
print(import_csv_file_to_mysql_database('data.csv'))