import urllib.parse, json

from wanted_gtrcats import wanted_cats
from utils import *

p = 1
s =100
totalPages = 0
n = 0

path = "/Users/tomsmith/datadancer/jsonfiles/"
for cat in wanted_cats:
    print( "FIRST PAGE", cat )
    ucat = urllib.parse.quote(cat)
    url = f"https://gtr.ukri.org/gtr/api/projects/?q={ucat}"
    print( url )
    data = jget(url)
    fname = f"{path}{cat}_projects_{p}_{s}.json"
    jwrite(fname, data)

    s = data["size"] 
    totalPages = data["totalPages"]
    print( "size", s)
    print("totalPages", totalPages)

    n = n +1
    for i in range(2,totalPages+1):
        ''
        p = i * s 
        url = f"\thttps://gtr.ukri.org/gtr/api/projects/?q={ucat}&p={i}&s={s}"
        fname = f"projects_{i}_{s}.json"
        print( fname )
        n = n + 1
print ( f"There are {n} projects")



    
#figure out whether to get more...