import http.client
import json
import time
from datetime import datetime, timedelta
import os
import requests
from influxdb import InfluxDBClient
import schedule
from pprint import pprint

# .ENV FILE FOR TESTING
# if os.path.exists('.env'):
#     from dotenv import load_dotenv
#     load_dotenv()

# GLOBALS
LIVE_CONN = bool(os.environ['LIVE_CONN'])
INFLUX_HOST = os.environ['INFLUX_HOST']
INFLUX_HOST_PORT = int(os.environ['INFLUX_HOST_PORT'])
INFLUX_DATABASE = os.environ['INFLUX_DATABASE']
APIKEY = os.environ['APIKEY']
STOCKS = os.environ['STOCKS']
RUNMINS =  int(os.environ['RUNMINS'])

JSON_OUTPUT = 'output.json'

INFLUX_CLIENT = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_HOST_PORT, database=INFLUX_DATABASE)

def construct_url(*args):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + args[0] + '&outputsize=compact&interval=60min&apikey=' + APIKEY
    return url

# Get json data
def get_json(*args):
    resp = requests.get(args[0])
    payload_data = resp.json()
    with open(JSON_OUTPUT, 'w') as outfile:
        json.dump(payload_data, outfile)

def get_saved_data(*args):
    if LIVE_CONN == True:
        get_json(args[0])

    with open(JSON_OUTPUT) as json_file:
        working_data = json.load(json_file)
    return working_data

def write_to_influx(data_payload):
    INFLUX_CLIENT.write_points(data_payload)
    pass    

def sort_json(working_data):
    # Interate over payload and pull out data points
    
    insert_symbol = working_data['Meta Data']['2. Symbol']

    # Fields logic for insert
    data_points = working_data['Time Series (Daily)']
    for k,v in data_points.items():
        # Skip if older than 3 days
        out_time = datetime.strptime(k, '%Y-%m-%d')
        if datetime.now() - out_time > timedelta(days=3):
            continue
        
        base_dict = {'measurement' : insert_symbol, 'tags' : {'name': 'stockprice'}}
        base_dict.update({'time': k})
        fields_data = {'price' : float(v['4. close']), 'volume' : int(v['5. volume']), 'low' : float(v['3. low']), 'high' : float(v['2. high'])}
        base_dict.update({'fields' : fields_data})
        data_payload = [base_dict]
        print("SUBMIT:" + str(data_payload))
        print('#'*30)
        write_to_influx(data_payload)

def do_it(*args):
    working_data = get_saved_data(args[0])
    sort_json(working_data)

def main():
    ''' Main entry point of the app '''
    stocks = STOCKS.split(',')
    for stock in stocks:
        url = construct_url(stock)
        do_it(url)
        schedule.every(RUNMINS).minutes.do(do_it, url)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    ''' This is executed when run from the command line '''
    main()