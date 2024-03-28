from FlightRadar24 import FlightRadar24API
import pandas as pd
import time
import datetime
from itertools import zip_longest


def fetch_and_append_flights(api,airlines,bounds):
    while True:
        fr_api = FlightRadar24API()
        for airline in airlines:
            try:                
                flights = fr_api.get_flights(airline=airline)
                flight_data = []
                for flight in flights:
                    if flight.destination_airport_iata =="BOM":
                        timen=flight.time
                        timef = datetime.datetime.utcfromtimestamp(timen)

                        flight_data.append({
                            "Flight Callsign": flight.callsign,
                            "Aircraft code": flight.aircraft_code,
                            "regestration":flight.registration, 
                            "id":flight.id,
                            "number":flight.number,  
                            "Airline":flight.airline_iata,
                            "Destination airport":flight.destination_airport_iata,  
                            "Origin airport":flight.origin_airport_iata, 
                            "Altitude":flight.altitude,
                            "Latitude": flight.latitude,
                            "longitude": flight.longitude,             
                            "ground speed":flight.ground_speed,
                            "vertical speed":flight.vertical_speed,
                            "heading":flight.heading,
                            "time":timef,
                            "icao_24bit":flight.icao_24bit,                           
                            "on_ground":flight.on_ground,                        
                                                
                                                
                            })

                        df= pd.DataFrame(flight_data)
                        print (df)
                try:
                    existing_df = pd.read_csv("flight_data.csv")
                except FileNotFoundError:
                    existing_df = pd.DataFrame()

                # Append new data to existing data
                if len(flight_data) > 0:
                    new_df = pd.DataFrame(flight_data)
                    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
                else:
                    updated_df = existing_df

                # Save the updated DataFrame to CSV
                updated_df.to_csv("flight_data.csv", index=False)
                print("Flight data appended to flight_data.csv")

            except Exception as e:
                print("an error occurred", e)
                time.sleep(2)
        time.sleep(5)

        try:
            fr_api = FlightRadar24API()
            flights = fr_api.get_flights(bounds=bounds)
            flight_data = []
            for flight in flights:
                if flight.destination_airport_iata =="BOM":
                    timen=flight.time
                    timef = datetime.datetime.utcfromtimestamp(timen)

                    flight_data.append({
                        "Flight Callsign": flight.callsign,
                        "Aircraft code": flight.aircraft_code,
                        "regestration":flight.registration, 
                        "id":flight.id,
                        "number":flight.number,  
                        "Airline":flight.airline_iata,
                        "Destination airport":flight.destination_airport_iata,  
                        "Origin airport":flight.origin_airport_iata, 
                        "Altitude":flight.altitude,
                        "Latitude": flight.latitude,
                        "longitude": flight.longitude,             
                        "ground speed":flight.ground_speed,
                        "vertical speed":flight.vertical_speed,
                        "heading":flight.heading,
                        "time":timef,
                        "icao_24bit":flight.icao_24bit,                           
                        "on_ground":flight.on_ground,                        
                                            
                                            
                        })

            df= pd.DataFrame(flight_data)
            print (df)
            try:
                existing_df = pd.read_csv("flight_data.csv")
            except FileNotFoundError:
                existing_df = pd.DataFrame()

            # Append new data to existing data
            if len(flight_data) > 0:
                new_df = pd.DataFrame(flight_data)
                updated_df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                updated_df = existing_df

            # Save the updated DataFrame to CSV
            updated_df.to_csv("flight_data.csv", index=False)
            print("bound data to flight_data.csv")

        except Exception as e:
            print("an error occurred", e)
            time.sleep(2)
    
        time.sleep(5)


def main():
    # Initialize FlightRadar24 API
    fr_api = FlightRadar24API()
    
    # Specify airline and CSV filename
    airlines = ["IGO","AIC","SEJ","VTI","AKJ","ETD","UAE","SDG","LLR","BDA","CPA","VIR","BAW","KLM","SIA","IAD","THA","CAL","CSC","MAS","AFR","QTR"]
    bounds = fr_api.get_bounds_by_point(19.09167993529285,72.86293745051911, 222240)
    
    
    # Call function to fetch and append flights
    #fetch_and_append_flights(fr_api,airlines,nonsheds)
    while True:
            try:
                fetch_and_append_flights(fr_api,airlines,bounds)
            except Exception as e:
                print(" Program has stopped")
                print("Restarting again..")
                time.sleep(5)

if __name__ == "__main__":
    main()