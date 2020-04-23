import ijson
import pandas as pd
import numpy as np
import datetime

# https://jsoneditoronline.org/#right=cloud.f5bb8b369ae1469ea4424d139f2a9e37&left=cloud.1c1d051a313b4c79b539db79ea8bdff9
# https://www.dataquest.io/blog/python-json-tutorial/

def parse_float(x):
    try:
        x = float(x)
    except Exception:
        x = 0
    return x

def parse_full_date(row):
    date = datetime.datetime.strptime(row["updated"], "%Y-%m-%dT%H:%M:%S")
    time = row["time_of_stop"].split(":")
    date = date.replace(hour=int(time[0]), minute = int(time[1]), second = int(time[2]))
    return date

filename = "people_1_100.json"

good_columns = [
    "href",
    "firstName",
    "otherNames",
    "surname",
    'updated',
    'email',
    'orcidId',
    ]

data = []

with open(filename, 'r') as f:
    objects = list( ijson.items(f, 'person'))[0]
    #print ("objects", len( objects ))
    columns = list(objects)[0]
  
    #print (columns, len(columns))
    #column_names = list([col["fieldName"] for col in columns])
    column_names = list(columns.keys())
    #print("column_names", column_names)
    i = 1
    for row in objects:
        if i == 1:
            print(column_names)
            print('')


        selected_row = [] # OK SO THIS FISHES OUT THE FLAT DATA
        for item in good_columns:
            
            c = column_names.index(item)
            #print(item, c, row)
            #print (list(row.keys() ))
            r = row[column_names[c]]
            selected_row.append(r)

        # We need to save the id
        id = selected_row[0] 

        data.append(selected_row)

        #print(row['links'])
        links = row['links']['link']
        # Now let's store the links
        for link in links:
            print( link['rel'] ,  link['href']  ) #
        print("-" * 80)
        #print(id, row['links'])

        i = i+1

people = pd.DataFrame(data, columns=good_columns)

print(people["firstName"].value_counts())

people = people[people["firstName"].isin(["James", "Naomi", "Caroline"])]

print ( people )

#print( data )
print("-" * 80)