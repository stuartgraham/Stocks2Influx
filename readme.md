
# Stock price scaper to InfluxDB
Grabs stock data from alphavantage and publishes to InfluxDB on periodic basis

### settings.py
Create settings.py from settings.py.example
| Settings | Description | Inputs |
| :----: | --- | --- |
| `LIVE_CONN` | Enables live lookups on website | `True` |
| `INFLUX_HOST` | InfluxDB host | `influx.test.local` |
| `INFLUX_HOST_PORT` | InfluxDB port  | `8086` |
| `INFLUX_DATABASE` | InfluxDB databse  | `test` |
| `RUNMINS` | Run every x mins | `720` |
| `APIKEY` | API key for stock lookups | `SOMEAPIKEY` |
| `STOCKS` | Comma seperated stock list | `IBM,F` |

### Requirements
```sh
pip install -p requirements.txt
```

### Execution 
```sh
python3 .\main.py
```

### Docker Compose
```sh 
  stocks2influx:
    image: ghcr.io/stuartgraham/stocks2influx:latest
    restart: always
    container_name: stocks2influx
    environment:
      - LIVE_CONN=True
      - INFLUX_HOST=influx.test.local
      - INFLUX_HOST_PORT=8086
      - INFLUX_DATABASE=stockprice
      - APIKEY=SOMEKEY
      - STOCKS=IBM,F
      - RUNMINS=100
```