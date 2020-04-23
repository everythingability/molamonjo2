import ijson
import pandas as pd
import numpy as np
import datetime

from wanted_cats import wanted_cats

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

filename = "projects_1_100.json"
# ['links', 'ext', 'id', 'outcomeid', 'href', 'created', 'updated', 'identifiers', 'title', 'status', 'grantCategory', 'leadFunder', 'leadOrganisationDepartment', 'abstractText', 'techAbstractText', 'potentialImpact', 'healthCategories', 'researchActivities', 'researchSubjects', 'researchTopics', 'rcukProgrammes', 'start', 'end', 'participantValues']

good_columns = [
    "href",
    "title",
    "status",
    "start",
    "end",
    "grantCategory",
    'leadFunder',
    'leadOrganisationDepartment',
    'abstractText',
    'researchSubjects', # THIS NEEDS DEEPER GRABBING
    'researchTopics',   # THIS NEEDS DEEPER GRABBING
    ]

data = []
datalinks = []
with open(filename, 'r') as f:
    objects = list( ijson.items(f, 'project'))[0]
    columns = list(objects)[0]
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
            #print( link['rel'] ,  link['href']  ) #
            datalinks.append( {'id':id, 'rel':link['rel'] ,  'href':link['href']}  )
        #print("-" * 80)
        #print(id, row['links'])
        
        
        i = i+1

# FILTER THE ONES WE WANT FROM WHAT WE'VE COLLECTED // DON'T THINK THIS IS OF USE
df = pd.DataFrame(data, columns=good_columns)
print(df["leadFunder"].value_counts())
print(df[df["leadFunder"].isin(["AHRC"])])

for index, row in df.iterrows():
    subjects = row['researchSubjects']['researchSubject']
    for subject in subjects:
        print("RESEARCH_SUBJECT", subject['id'], subject['text'], subject['percentage'])
    #print (r['id'], r['text'], r['percentage'])

print("-" * 80)

for index, row in df.iterrows():
    subjects = row['researchTopics']['researchTopic']
    for subject in subjects:
        print("RESEARCH_TOPIC", subject['id'], subject['text'], subject['percentage'])
    #print (r['id'], r['text'], r['percentage'])



# LET'S FIGURE OUT THE RELATIONSHIPS (BUT WE NEED TO THIS IN THE DF, NOT ON ALL DATALINKS)
print("-" * 80)
print(len(datalinks), "links" )
# let's see what relationships we have
ldf = pd.DataFrame(datalinks, columns=["rel"])
print(ldf["rel"].value_counts())

print("-" * 80)

# ALL LINKS
for index, row in enumerate(datalinks):
    ''
    #print("LINK", row['rel'],  row['href']    )
    #print (r['id'], r['text'], r['percentage'])



