import json, requests, mysql.connector
from time import time, sleep

# WeatherAPI.com Related Variables
api_key = '177fc30f60bc4f49989113612211904' # Add your API Key Here
location_var = 'Manila' # Select Location
run_every_mins = 10 # Interval to Check API in Minutes

# Database Related Variables
db_host_var = 'localhost'
db_user_var = 'root'
db_user_pass = 'dlsu_password'
db_name_var = 'db_weather'
db_table_var = 'raw_data'

def get_data(url_var):
    req = requests.get(url_var)
    input_json = req.json()
    country_var = input_json['location']['country']
    region_var = input_json['location']['region']
    localtime_var = input_json['location']['localtime']
    temp_c_var = input_json['current']['temp_c']
    condition_var = input_json['current']['condition']['text']
    wind_mph_var = input_json['current']['wind_mph']
    pressure_mb_var = input_json['current']['pressure_mb']
    humidity_var = input_json['current']['humidity']
    uv_var = input_json['current']['uv']
    gust_mph_var = input_json['current']['gust_mph']
    return localtime_var, country_var, region_var, temp_c_var, condition_var, wind_mph_var, pressure_mb_var, humidity_var, uv_var, gust_mph_var

def insert_to_db(mydb, output_data):
    try:
        mycursor = mydb.cursor()
        sql_insert_data = "INSERT INTO " + db_name_var + '.' + db_table_var + " (`date`, `country`, `region`, `temp_c`, `condition`, `wind_mph`, `pressure_mb`, `humidity`, `uv`, `gust_mph`) VALUES (STR_TO_DATE(%s,'%Y-%m-%d %H:%i'), %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql_insert_data, output_data)
        mydb.commit()
        print("INFO:", mycursor.rowcount, "record was inserted.", output_data)
    except Exception as ex:
        print("EXCEPTION:", ex)

def setup_db_onstart(mydb):
    try:
        mycursor = mydb.cursor()
        sql_create_schema = 'CREATE SCHEMA IF NOT EXISTS ' + db_name_var + ';'
        mycursor.execute(sql_create_schema)
        print("INFO:", db_name_var, "schema loaded")
        sql_create_table = 'CREATE TABLE IF NOT EXISTS ' + db_name_var + '.' + db_table_var + ' (`date` DATETIME NOT NULL, `country` VARCHAR(45) NULL, `region` VARCHAR(45) NULL, `temp_c` DOUBLE NULL, `condition` VARCHAR(45) NULL, `wind_mph` DOUBLE NULL, `pressure_mb` DOUBLE NULL, `humidity` DOUBLE NULL, `uv` DOUBLE NULL, `gust_mph` DOUBLE NULL, PRIMARY KEY (`date`));'
        mycursor.execute(sql_create_table)
        print("INFO:", db_table_var, "table loaded")
    except Exception as ex:
        print("EXCEPTION:", ex)

url_var = 'http://api.weatherapi.com/v1/current.json?key=' + api_key + '&q=' + location_var + '&aqi=no' # API to be Queried    
mydb = mysql.connector.connect(host=db_host_var, user=db_user_var, passwd=db_user_pass)
setup_db_onstart(mydb)

while True:
    sleep((run_every_mins * 60) - time() % 60)
    output_data = get_data(url_var)
    insert_to_db(mydb, output_data)
    