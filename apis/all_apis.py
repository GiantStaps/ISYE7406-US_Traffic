# DIRECTIONS API 
import requests, polyline
import pandas as pd
from datetime import datetime, timedelta
import pytz 
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# This code does the following: 
# 1. Google Directions API
    # Gets multiple routes from an origin and destination (currently manually put in at the bottom)
    # returns multiple routes with duration, distance, and polyline (used to find bounding box for accident search)
    # finds bounding box for each route
    # function that returns the bounding box for the route with the shortest duration

# 2. Accuweather API
    # gets location key from the latitude and longitude of the mapquest accident
    # gets current conditions from location key **NOTE: current conditions are from ACCIDENT location, not user

# 3. User input (I should really organize this better)
    # origin, destination

# 4. Mapquest API
    # for the bounding box of the route, checks to see if there have been any accidents within a certain time frame
    #NOTE: how to determine time frame? Also - I'm differentiating between incident and accident and only including accidents. 
        # most of the time nothing shows up - considering adding another accident API ()


#1. ####### GOOGLE DIRECTIONS API

# getting multiple routes based on origin and destination
def get_multiple_routes(origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "alternatives": "true", 
        "mode": "driving",       
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None
    
# getting bounding box (FOR ACCIDENT SEARCH LATER)

def get_bounding_box(polyline_str):
    # Decode the polyline string into a list of (latitude, longitude) tuples
    coordinates = polyline.decode(polyline_str)

    # Initialize bounding box values
    min_lat = min(coord[0] for coord in coordinates)  # Minimum latitude
    max_lat = max(coord[0] for coord in coordinates)  # Maximum latitude
    min_lng = min(coord[1] for coord in coordinates)  # Minimum longitude
    max_lng = max(coord[1] for coord in coordinates)  # Maximum longitude

    return min_lat, max_lat, min_lng, max_lng

# convert multiple routes to dataframe
def routes_to_dataframe(routes_data):
    routes_info = []
    for idx, route in enumerate(routes_data.get("routes", [])):
        leg = route["legs"][0]  # Assuming each route has only one leg for simplicity
        polyline_str = route["overview_polyline"]["points"]

        route_info = {
            "Route Number": idx + 1,
            "Start Address": leg["start_address"],
            "End Address": leg["end_address"],
            "Distance": leg["distance"]["text"],
            "Duration": leg["duration"]["text"], 
            "Bounding Box": get_bounding_box(polyline_str)
        }
        routes_info.append(route_info)
    
    return pd.DataFrame(routes_info)

# getting the route with the shortest duration 
def get_bounding_box_of_shortest_duration(routes_df):
    def parse_duration(duration_text):
        # Convert duration text into total minutes
        hours, minutes = 0, 0
        if "hour" in duration_text:
            parts = duration_text.split()
            hours = int(parts[0])
            if "min" in parts:
                minutes = int(parts[2])
        elif "min" in duration_text:
            minutes = int(duration_text.split()[0])
        return hours * 60 + minutes

    # Add a 'Total Duration (min)' column for sorting
    routes_df["Total Duration (min)"] = routes_df["Duration"].apply(parse_duration)

    # Find the route with the shortest duration
    shortest_route = routes_df.loc[routes_df["Total Duration (min)"].idxmin()]

    # Return the bounding box of the shortest route
    return shortest_route["Bounding Box"]


#2. ###### ACCUWEATHER API 

# get location key of accident from latitude and longitude (from mapquest)
def get_location_key(latitude, longitude):
    url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
    params = {
        "apikey": "fnzaoFgUXLiERvRA0Yjvia0xgAAeh5SH",
        "q": f"{latitude},{longitude}"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        location_data = response.json()
        location_info = {
            "Key": location_data.get("Key"),
            "PrimaryPostalCode": location_data.get("PrimaryPostalCode")
        }
        return location_info
    else:
        print("Error:", response.status_code, response.text)
        return None

# getting current conditions (based on accident location)
def get_current_conditions(location_key):
    current_conditions_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
    current_conditions_params = {
        "apikey": "fnzaoFgUXLiERvRA0Yjvia0xgAAeh5SH",
        "language": "en-us",
        "details": True
    }
    current_conditions_response = requests.get(current_conditions_url, params=current_conditions_params)
    
    if current_conditions_response.status_code == 200:
        response_data = current_conditions_response.json()

        data = response_data[0]

        weather_data = {
            "Temperature (F)": data['Temperature']['Imperial']['Value'],
            "Wind Chill (F)": data['WindChillTemperature']['Imperial']['Value'],
            "Humidity (%)": data['RelativeHumidity'],
            "Pressure (inHg)": data['Pressure']['Imperial']['Value'],
            "Visibility (mi)": data['Visibility']['Imperial']['Value'],
            "Wind Speed (mph)": data['Wind']['Speed']['Imperial']['Value'],
            "Precipitation (in)": data['PrecipitationSummary']['Precipitation']['Imperial']['Value'],
            "Day/Night": "Day" if data['IsDayTime'] else "Night"
        }
        return weather_data
    else:
        print("Error:", current_conditions_response.status_code, current_conditions_response.text)
        return None
    
#3. ########## USER INPUT
origin = "33.775799,-84.402481"  # Instructional Center
# IC_Address: "759 Ferst Dr, Atlanta, GA 30318"
destination = "33.640320,-84.439697"  # ATL
# atl_address = "6000 N Terminal Pkwy Suite 4000, Atlanta, GA 30320"

# get route data: 
routes_data = get_multiple_routes(origin, destination)

if routes_data:
    routes_df = routes_to_dataframe(routes_data)
    shortest_route_bbox = get_bounding_box_of_shortest_duration(routes_df)
    mapquest_bbox = f"{shortest_route_bbox[0]},{shortest_route_bbox[2]},{shortest_route_bbox[1]},{shortest_route_bbox[3]}"

#4. ###### MAPQUEST API 
mapquest_url = 'https://www.mapquestapi.com/traffic/v2/incidents'

# uses bounding box from the route with the smallest time in route_df (from Google Directions API)

mapquest_params = {
    'key': '1RVhMpv5zaw4BRrjXEHc099V71owN2sP', 
    'boundingBox': mapquest_bbox,
    'filters': 'incidents'
}

mapquest_response = requests.get(mapquest_url, params=mapquest_params)
mapquest_data = mapquest_response.json()

# Filter for pulling current data (1 day ago)
local_timezone = pytz.timezone('America/New_York')
utc_now = datetime.now(pytz.UTC)
local_now = utc_now.astimezone(local_timezone)
date_filter = local_now - timedelta(hours=10000)

# Storing accident data in dataframe 
mapquest_list = []
for incident in mapquest_data.get('incidents', []):
    if incident.get('shortDesc', '') == 'Accident':
        start_time_str = incident.get('startTime', 'Unknown start time')
        end_time_str = incident.get('endTime')
        
        # Convert start time to datetime object
        if start_time_str != 'Unknown start time':
            # Convert ISO 8601 string to a datetime object in UTC
            start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S%z')  # Handles 'Z' or timezone offsets

            # Convert to local timezone (EST)
            start_time = start_time.astimezone(local_timezone)

            # Similarly handle the end time
            end_time_str = incident.get('endTime')
            if end_time_str:
                end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S%z').astimezone(local_timezone)
            else:
                end_time = None

            # Check if the incident occurred in the time period
            if start_time > date_filter:
                # getting accident information
                accident_info = {
                    'Latitude': incident.get('lat', 'Unknown'),
                    'Longitude': incident.get('lng', 'Unknown'),
                    'Severity': incident.get('severity', 'Unknown'),
                    'Distance': incident.get('distance', 0),
                    'Start Date': start_time.date(),
                    'Start Time': start_time.time(),
                    'Impacting': incident.get('impacting', 'Unknown'),
                    'Day of Week': start_time.strftime('%A'),
                    'Month': start_time.month,
                    'Year': start_time.year, 
                    'Short Description': incident.get('shortDesc', 'Unknown'), 
                    'Full Description': incident.get('fullDesc', 'Unknown') 
                }

                # Handle end time and duration
                if end_time:
                    accident_info['End Date'] = end_time.date()
                    accident_info['End Time'] = end_time.time()
                    duration = (end_time - start_time).total_seconds() / 60  # Duration in minutes
                    accident_info['Duration (min)'] = duration
                else:
                    accident_info['End Date'] = None
                    accident_info['End Time'] = None
                    accident_info['Duration (min)'] = None
                mapquest_list.append(accident_info)

mapquest_df = pd.DataFrame(mapquest_list)
unique_incidents_df = mapquest_df.drop_duplicates(subset=['Start Date', 'Start Time', 'End Date', 'End Time', 'Distance'])

for idx, row in unique_incidents_df.iterrows(): 

    # Get location key using lat and lng
    location_key = get_location_key(row["Latitude"], row["Longitude"])

    # Get current conditions using the location key
    if location_key:
        current_conditions = get_current_conditions(location_key["Key"])
        if current_conditions:
            unique_incidents_df.loc[idx, 'Temperature (F)'] = current_conditions.get('Temperature (F)', 'N/A')
            unique_incidents_df.loc[idx, 'Wind Chill (F)'] = current_conditions.get('Wind Chill (F)', 'N/A')
            unique_incidents_df.loc[idx, 'Humidity (%)'] = current_conditions.get('Humidity (%)', 'N/A')
            unique_incidents_df.loc[idx, 'Pressure (inHg)'] = current_conditions.get('Pressure (inHg)', 'N/A')
            unique_incidents_df.loc[idx, 'Visibility (mi)'] = current_conditions.get('Visibility (mi)', 'N/A')
            unique_incidents_df.loc[idx, 'Wind Speed (mph)'] = current_conditions.get('Wind Speed (mph)', 'N/A')
            unique_incidents_df.loc[idx, 'Precipitation (in)'] = current_conditions.get('Precipitation (in)', 'N/A')
            unique_incidents_df.loc[idx, 'Day/Night'] = current_conditions.get('Day/Night', 'N/A')

print(f"Number of mapquest incidents: {mapquest_df.shape[0]}")
print(f"Number of unique incidents: {unique_incidents_df.shape[0]}")

# Export to Excel
output_file = 'unique_traffic_incidents.csv'
unique_incidents_df.to_csv(output_file, index=False)

all_incidents = pd.DataFrame(mapquest_data.get('incidents', []))

print(f"Total Incidents: {len(all_incidents)}")

all_incidents.to_csv("all_incidents.csv", index=False)


