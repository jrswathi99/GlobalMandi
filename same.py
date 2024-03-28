import mysql.connector
from mysql.connector import Error
from FlightRadar24 import FlightRadar24API
import time
import datetime

def connect_to_database():
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

def fetch_and_append_flights(api, airlines):
    conn = connect_to_database()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        while True:
            for airline in airlines:
                try:
                    fr_api = FlightRadar24API()
                    flights = fr_api.get_flights(airline=airline)
                    flight_data = []
                    for flight in flights:
                        if flight.destination_airport_iata == "BOM":
                            timen = flight.time
                            timef = datetime.datetime.utcfromtimestamp(timen)
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
                                "registration": flight.registration,  
                                "vertical_speed": flight.vertical_speed,                      
                            })

                    for data in flight_data:
                        columns = ', '.join([f"`{col}`" for col in data.keys()])  
                        placeholders = ', '.join(['%s'] * len(data))
                        sql = f"INSERT INTO flights ({columns}) VALUES ({placeholders})"
                        values = tuple(data.values())
                        print("Executing SQL query:", sql)
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
            time.sleep(6)  # Adjust sleep time based on data update frequency
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print('Database connection closed')

def main():
    # Specify airline
    airlines = ["IGO","AIC","SEJ","VTI","AKJ","ETD","UAE","SDG","LLR","BDA","CPA","VIR","BAW","KLM","SIA","IAD","THA","CAL","CSC","MAS","AFR","QTR"]
    # Call function to fetch and append flights
    fetch_and_append_flights(FlightRadar24API(), airlines)

if __name__ == "__main__":
    main()
