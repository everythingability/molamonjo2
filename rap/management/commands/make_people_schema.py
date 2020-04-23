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


def makedb(fname):
    global df

    #take the links oute
    j = jread( fname )
    #links = j['links']
    #del j['links']
    obj = j['person']
    df = pd.read_json(j)
    print(df)

    print( pd.build_table_schema(df) )

    ###
    #conn = sqlite3.connect("gtr.db")
    #df.to_sql('users', conn)
    #print( df )

def dbinsert():
    global df
    conn = sqlite3.connect("gtr.db")
    df.to_sql('users', conn)

p = 1
s =100

if __name__ == '__main__':
    global df
    fname = "people_1_100.json"
    makedb( fname )
    #dbinsert(  )

