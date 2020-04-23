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

def makedb(fname):
    df = pd.read_json(open(fname))
    print( db )

def dbinsert():
   conn = sqlite3.connect("gtr.db")
   df.to_sql('users', conn)

p = 1
s =100

if __name__ == '__main__':
    url = f"https://gtr.ukri.org:443/gtr/api/persons?p={p}&s={s}" 
    data = jget(url)
    fname = f"people_{p}_{s}.json"
    jwrite(fname, data)

