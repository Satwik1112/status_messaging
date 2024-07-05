This is status managing project only for  client-server script using fast api

setup
  - add required configuration in config.py file for mqtt connection
  - add reqiured configuration for mongoDB connection, default seto to localhost(edit mongo_url if needed)

config.py 
  - configuration for connection to mqtt client and time format

mongoDB_connection.py
  - configuration for connection to mongoDB client

mongoDB_config.py
  - all connections for mongoDB client

mqtt_server.py
  - all connections for mqtt_client

main.py
  - fast api application which generates status for each second
  - endpoint "/" with query string "?start_time=12:57:37&end_time=12:57:52" gives number of states
  - endpoint "/delete_records" delete all records in database
