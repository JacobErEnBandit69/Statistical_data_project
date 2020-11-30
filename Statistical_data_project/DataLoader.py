import psycopg2
import pandas as pd
def get_data_from_uplink_db():
   try:
      connection = psycopg2.connect(user="chirpstack_as_events",
                                    password="dbpassword",
                                    host="0.0.0.0",
                                    port="5432",
                                    database="chirpstack_as_events")
      cursor = connection.cursor()

      postgreSQL_select_Query = "SELECT application_name, rx_info, dr, received_at, object  FROM device_up WHERE application_name='OTAA_test_app'"

      cursor.execute(postgreSQL_select_Query)
      db_data = cursor.fetchall()
      df = pd.DataFrame()
      for row in db_data:
         gps_dict = row[4]["gpsLocation"]["1"]
         rx_info = row[1][0]
         tx_timestamp = pd.to_datetime(row[3]).tz_convert('Europe/Copenhagen')
         rx_timestamp = pd.to_datetime(rx_info["time"]).tz_convert('Europe/Copenhagen')

         df.loc[tx_timestamp, "application_name"] = row[0]
         df.loc[tx_timestamp, "loRaSNR"] = rx_info["loRaSNR"]
         df.loc[tx_timestamp, "rssi"] = rx_info["rssi"]
         df.loc[tx_timestamp, "datarate"]= row[2]
         df.loc[tx_timestamp, 'gateway_name'] = rx_info["name"]
         df.loc[tx_timestamp, "rx_gateway_latitude"] = rx_info["location"]["latitude"]
         df.loc[tx_timestamp, "rx_gateway_longitude"] = rx_info["location"]["longitude"]
         df.loc[tx_timestamp, "tx_latitude"] = gps_dict["latitude"]
         df.loc[tx_timestamp, "tx_longitude"] = gps_dict["longitude"]
         df.loc[tx_timestamp, "rx_timestamp"] = rx_timestamp
         df.loc[tx_timestamp, "tx_timestamp"] = tx_timestamp

      return df

   except (Exception, psycopg2.Error) as error :
      print ("Error while fetching data from PostgreSQL", error)

   finally:
      #closing database connection.
      if(connection):
         cursor.close()
         connection.close()
         print("PostgreSQL connection is closed")

