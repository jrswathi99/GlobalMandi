import mysql.connector
from mysql.connector import Error
from FlightRadar24 import FlightRadar24API
import pandas as pd
import time
import datetime
import csv
import os

conn = None
last_db_closed_time = None

def connect_to_database():
    global conn
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='flight details',
            user='root'
        )
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print('Error:', e)
        return None
    



def fetch_and_append_flights(api, airlines,bounds):
    global conn
    if conn is None or not conn.is_connected():
        conn = connect_to_database()

    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
      
        #while True:
        for airline in airlines:
            try:
                fr_api = FlightRadar24API()
                flights = fr_api.get_flights(airline=airline)
                flight_data = []
                for flight in flights:
                    if flight.destination_airport_iata == "BOM":
                        timen = flight.time
                        timef = datetime.datetime.utcfromtimestamp(timen)
                        code=flight.registration
                        form_code= code.replace("-","")
                        flight_data.append({
                            "aircraft_code": flight.aircraft_code,
                            "airline": flight.airline_iata,
                            "altitude": flight.altitude,
                            "destination_airport": flight.destination_airport_iata,
                            "flight_callsign": flight.callsign,
                            "flight_time": timef,
                            "ground_speed": flight.ground_speed,
                            "heading": flight.heading,
                            "icao_24bit": flight.icao_24bit,
                            "flight_id": flight.id,
                            "latitude": flight.latitude,
                            "longitude": flight.longitude,
                            "number": flight.number, 
                            "on_ground": flight.on_ground ,                    
                            "origin_airport": flight.origin_airport_iata,
                            "registration": form_code,  
                            "vertical_speed": flight.vertical_speed,                      
                        })

                for data in flight_data:
                    columns = ', '.join([f"`{col}`" for col in data.keys()])  
                    placeholders = ', '.join(['%s'] * len(data))
                    sql = f"INSERT INTO flights ({columns}) VALUES ({placeholders})"
                    values = tuple(data.values())
                    #print("Executing SQL query:", sql)
                    cursor.execute(sql, values)
                    conn.commit()
                print('Flight data appended to MySQL database')
                
            except Error as e:
                print('Error:', e)
                time.sleep(2)
                continue
            except Exception as e:
                print('An unexpected error occurred:', e)
                time.sleep(2)
                continue
        try:
            fr_api = FlightRadar24API()
            flights = fr_api.get_flights(bounds=bounds)
            flight_data = []
            for flight in flights:
                if flight.destination_airport_iata =="BOM":
                    timen=flight.time
                    timef = datetime.datetime.utcfromtimestamp(timen)
                    code=flight.registration
                    form_code= code.replace("-","")

                    flight_data.append({
                            "aircraft_code": flight.aircraft_code,
                            "airline": flight.airline_iata,
                            "altitude": flight.altitude,
                            "destination_airport": flight.destination_airport_iata,
                            "flight_callsign": flight.callsign,
                            "flight_time": timef,
                            "ground_speed": flight.ground_speed,
                            "heading": flight.heading,
                            "icao_24bit": flight.icao_24bit,
                            "flight_id": flight.id,
                            "latitude": flight.latitude,
                            "longitude": flight.longitude,
                            "number": flight.number, 
                            "on_ground": flight.on_ground ,                    
                            "origin_airport": flight.origin_airport_iata,
                            "registration": form_code,  
                            "vertical_speed": flight.vertical_speed,      
                                        
                        })
            for data in flight_data:
                columns = ', '.join([f"`{col}`" for col in data.keys()])  
                placeholders = ', '.join(['%s'] * len(data))
                sql = f"INSERT INTO flights ({columns}) VALUES ({placeholders})"
                values = tuple(data.values())
                #print("Executing SQL query:", sql)
                cursor.execute(sql, values)
                conn.commit()
            print('bound data appended to MySQL database')
            
        except Error as e:
            print('Error:', e)
            time.sleep(2)
            #continue
        except Exception as e:
            print('An unexpected error occurred:', e)
            time.sleep(2)
            #continue

        #backup_data_to_csv(flight_data)
        time.sleep(5)  

    except Error as e :
        print('error', e)        

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print('Database connection closed')

def main():
    # Initialize FlightRadar24 API
    fr_api = FlightRadar24API()
    
    # Specify airline and CSV filename
    airlines = ["IGO","AIC","SEJ","VTI","AKJ","ETD","UAE","SDG","LLR","BDA","CPA","VIR","BAW","KLM","SIA","IAD","THA","CAL","CSC","MAS","AFR","QTR"]
    bounds = fr_api.get_bounds_by_point(19.09167993529285,72.86293745051911, 222240)
    
    
    # Call function to fetch and append flights
    fetch_and_append_flights(fr_api,airlines,bounds)
    if conn is not None and conn.is_connected():
        conn.close()
        print('Database connection closed')

    

   
if __name__ == "__main__":
    main()
