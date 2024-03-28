import pandas as pd
from FlightRadar24 import FlightRadar24API
import datetime
# Initialize FlightRadar24API
fr_api = FlightRadar24API()


bounds = fr_api.get_bounds_by_point(19.09167993529285,72.86293745051911, 222240)
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
            "on_ground":flight.on_ground                        
                                    
                                
                })

df= pd.DataFrame(flight_data)
print (df)