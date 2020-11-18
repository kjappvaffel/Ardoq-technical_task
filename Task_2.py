import requests
import json
from tabulate import tabulate


def get_station_status():
    url="https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json"
    headers={'Client-Identifier':'ardoq-technical_task'}
    response=requests.get(url, headers=headers)
    return json.loads(response.text)

def get_station_information():
    url="https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json"
    headers={'Client-Identifier':'ardoq-technical_task'}
    response=requests.get(url, headers=headers)
    return json.loads(response.text)
            
#organizes the information from the station_status.json file into a dictionary with the unique ids as keys
def organize_station_status():
    #retrieves the status information
    stations=get_station_status()["data"]["stations"]

    #declares variables for later use
    available_bikes=0
    available_spots=0
    station_id=""
    station_installed=""

    #creates a dictionary to organize variables
    stations_dict={}
    
    #iterates through all stations, and declares installation, possibility of rental and returnal, and potentially number of spots and bikes. 
    for station in stations:
        station_id=station["station_id"]
        if station["is_installed"]==1:
            station_installed="Yes"
            if station["is_renting"]==1:
                available_bikes=station['num_bikes_available']
            #if the station is not renting, it is stated in the column    
            else:
                available_bikes="Not renting"
            if station["is_returning"]==1:
                available_spots=station=station["num_docks_available"]

            #if the station is not returning, it is stated
            else:
                available_spots="Not returning"
        #if station is not installed, it is stated
        else:
            station_installed+="No"
        
        #uses the unique id to store the relevant information from status. 
        stations_dict[station_id]=[station_installed, available_bikes, available_spots]
        
    return stations_dict

#adds adress and name from the station_information.json file by using the id. 
def add_address_to_dictionary(stations_dict):
    stations=get_station_information()["data"]["stations"]

    for station in stations:
        id=station["station_id"]
        address=station["address"]
        name=station["name"]
        if stations_dict[id]!=None:
            #adds name and adress in the first element in the array for formating reasons
            stations_dict[id].insert(0,address)
            stations_dict[id].insert(0,name)
    return stations_dict



        
def print_info(dict_info):
    template = '{:<5} {:<30} {:<40} {:<10} {:<15} {:<15}'
    table_headers=['id','Station name', 'Adress', 'Installed','Available bikes','Available spots']
    print(template.format(*table_headers))
    
    for item in dict_info.items():
        
        print(template.format(*[item[0],item[1][0],item[1][1],item[1][2],item[1][3],item[1][4]]))
    
    


status_dict=organize_station_status()
status_dict_with_info=add_address_to_dictionary(status_dict)
print_info(status_dict_with_info)



