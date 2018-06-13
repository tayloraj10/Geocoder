import csv
import requests

''' 
Geocodes a csv file and saves goecoded file in same directory

address_columns - put in index of columns that contain the address to geocode
address_csv_in - file pathway to file to be geocoded
iter_num = the number of rows within the csv to geocode, leave at 0 if you want all rows to be geocoded
'''

# Zero based index of columns in input file that contain address components
address_columns = [0, 1, 2]

# File pathway to file to be geocoded
address_csv_in = r""

# Number of rows to Geocode. Leave 0 if you'd like all rows geocoded.
iter_num = 0





csvfile_out = address_csv_in.split('.csv')[0] + '_geocoded.csv'

gmap_url = "https://maps.googleapis.com/maps/api/geocode/json?"
api_key = "AIzaSyDpa9FUmUBcVQwg37VRDoOs3W3JVUjaD00"


address_list = []
geocoded_address_list = []
row_address = []
        

def read_addresses(ungeocoded_addresses_file):
    global address_list
    global zip_present
    global sc_present
    global site
    with open(ungeocoded_addresses_file, 'r') as csv_in:        
        reader = csv.reader(csv_in)
        reader = list(reader)
        
        for row in reader[1:]:
            row_address = []
            for col in address_columns:
                row_address.append(row[col].strip())
            address_list.append(row_address)
       
def google_maps_geocode(address):
    address2 = ", ".join(address)
    address3 = address2.replace(" ", "%20")
    #print(address2)
    #print(address3)
    r = requests.get(gmap_url + "address=" + address3 + "&key=" + api_key)
    #print(gmap_url + "address=" + address3 + "&key=" + api_key)
    rj = r.json()
    #print(rj)
    #street_address = city = state = zip_code = ""
    
    
    try:
        full_address = rj['results'][0]['formatted_address']
        full = full_address.rsplit(',', 1)[0]
        lat = rj['results'][0]['geometry']['location']['lat']
        lng = rj['results'][0]['geometry']['location']['lng']
        accuracy = rj['results'][0]['geometry']['location_type']
        
        results = [full, lat, lng, accuracy]
    except:
        results = ["FAILED", "FAILED", "FAILED", "FAILED"]
        print(address2)
        print(rj['status'])
        
    
    #print(results, '\n')
    geocoded_address_list.append(results)
    
def write_to_file(geocoded_addresses):
    global sc_present
    global zip_present
    #with open(ungeocoded_addresses_file, 'r') as csv_in:   
        #with open(csvfile_out, 'w', newline='') as outcsv:  
            
    with open(address_csv_in, 'r') as csv_in:   
        with open(csvfile_out, 'w', newline='') as outcsv:                 
            reader = csv.reader(csv_in)
            writer = csv.writer(outcsv, delimiter=',')
            
            all_rows = []
            row = next(reader)
            row.append('Geocode Address')
            row.append('Latitude')
            row.append('Longitude')
            row.append('Accuracy')
            
            all_rows.append(row)
            
            
            for count, row in enumerate(reader):
                
                if iter_num > 0 and count == iter_num:
                    break
                    
                row.append(geocoded_addresses[count][0])
                row.append(geocoded_addresses[count][1])
                row.append(geocoded_addresses[count][2])
                row.append(geocoded_addresses[count][3])
                
                
                all_rows.append(row)
                
            #print(all_rows)
            
            writer.writerows(all_rows)
            
            
            #for item in geocoded_addresses:
                #writer.writerows(item)
            
def run(number=0):
    global address_list
    if number == 0:
        read_addresses(address_csv_in)
        for item in address_list:
            google_maps_geocode(item)
        write_to_file(geocoded_address_list)
    else:
        read_addresses(address_csv_in)
        for item in address_list[:number]:
            google_maps_geocode(item)
        write_to_file(geocoded_address_list)
        
        
if __name__ == '__main__':
    run(iter_num)
