from yelpapi import YelpAPI
import pandas as pd

'''
Some quick helper functions to make record linkage fast.
Max Kramer
'''

# Change to your api key
key = '50G0TnHbhsICvJWfMYhAHwaWs1TVwxf0hDrp0QF3rN1cHVvSH5Lkh0g2y_VysxT1T_H9bIm_t1JultXGfpy2z0ewPCJh9GgOtdgE_wKaNlGY-SDaKDmRuYPJDz4sYHYx'

def setup_client(apikey):
    '''
    generate a client from an api key
    '''
    client = YelpAPI(apikey)
    return client

def import_data(path_to_data):
    '''
    takes in a path to a csv and creates a pd df
    '''
    dataset = pd.read_csv(path_to_data)
    return dataset
    
def gen_params(dataset,rownum):
    '''
    generates query parameters for a business in the df
    '''
    business = dataset.iloc[rownum]
    name = business['DBA Name']
    lat = business['Latitude']
    lon = business['Longitude']
    return (name,lat,lon)

def run(client,name,lat,lon):
    '''
    runs a query to the YELP api with the given parameters
    '''
    resp = client.search_query(name=name,latitude=lat,longitude=lon)['businesses']
    for i in range(len(resp)):
        if resp[i]['name'] == name:
            print("found match")
            return resp[i]
    print("no match")
    return []

def go(apikey,path_to_data):
    '''
    runs the entire df through the querying process, calls all helper functions.
    '''
    client = setup_client(apikey)
    data = import_data(path_to_data)
    result = {} 
    for i in range(len(data)):
        (name,lat,lon) = gen_params(data,i)
        result[name] = run(client,name,lat,lon)

go(key,"after_covid.csv") # Change to whatever csv you want to link