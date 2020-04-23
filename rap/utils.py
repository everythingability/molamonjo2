import requests, json
import pandas as pd
import sqlite3

def jprint(j):
    print(json.dumps(j, indent=4, sort_keys=True))

def jget(url):
    #purl = "https://gtr.ukri.org:443/gtr/api/outcomes/artisticandcreativeproducts?q=test&p=1"
    response = requests.get( url, headers={'Accept': 'application/json'} )
    result = response.json()
    return result

def jwrite(fname, data):
    f = open(fname, 'w' )
    f.write(json.dumps(data) )
    f.close()
    print( fname )

def jread(fname):
    f = open(fname )
    d = f.read()
    j = json.loads(d)
    f.close()
    return j


