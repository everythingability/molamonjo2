from django.core.management.base import BaseCommand, CommandError
#from rap.models import Project, Person, Organisation, GTRCategory
from rap.models import *
import os, sys
import csv, json, requests
from pprint import pprint
from random import randint
from time import sleep

from calais import CalaisResponse

CALAIS_API_KEY = 'sCp2wutebF2mJBAjm3LgUUUQUTvtOzEq'

def print_summary(jobj):

    for k,v in list(jobj.items()):
        print("\t%d %s" % (len(v), k))
    

def print_entities(self):
    if not hasattr(self, "entities"):
        return None
    for item in self.entities:
        print("%s: %s (%.2f)" % (item['_type'], item['name'], item['relevance']))

def print_topics(self):
    if not hasattr(self, "topics"):
        return None
    for topic in self.topics:
        print(topic['categoryName'])

def print_relations(self):
    if not hasattr(self, "relations"):
        return None
    for relation in self.relations:
        print(relation['_type'])
        for k,v in relation.items():
            if not k.startswith("_"):
                if isinstance(v, unicode):
                    print("\t%s:%s" % (k,v))
                elif isinstance(v, dict) and v.has_key('name'):
                    print("\t%s:%s" % (k, v['name']))

def print_social_tags(jobj):
    objs =[]
    for socialTag in jobj:
        tags = jobj[socialTag]
        #print("socialTag", socialTag)
       
        if socialTag == "language" :
            ''
        elif socialTag == "socialTag":

            for tag in tags:
                obj = {}
                for t in tag:
                    if t == 'name': obj['name']= tag[t]
                    if t == 'importance': obj['importance']= tag[t]
                objs.append(obj)
            #print(objs)
    return objs
            
        
#


def analyze(text):
  

    url = 'https://api-eit.refinitiv.com/permid/calais'
    body = {'content': text}
    headers = {    'x-ag-access-token': CALAIS_API_KEY,
                   "http.useragent":"Calais Rest Client",
                   "Accept" :"application/json",
                   "enableMetadataType":"GenericRelations,SocialTags", 
                   'Content-Type' : 'text/html',
                   'outputformat' : 'application/json'}
                
    # Don't use calais.py because it uses old urllib calls
    response = requests.post(url, data=json.dumps(body), headers=headers)
    result = response.json()
    return result
    
def _simplify_json(json):
    result = {}
    # First, resolve references
    for element in json.values():
        for k,v in element.items():
            if isinstance(v, str) and v.startswith("http://") and v in json:
                element[k] = json[v]
    for k, v in json.items():
        if "_typeGroup" in v:
            group = v["_typeGroup"]
            if not group in result:
                result[group]=[]
            del v["_typeGroup"]
            v["__reference"] = k
            result[group].append(v)
    return result

dir_path = os.path.dirname(os.path.realpath(__file__))
class Command(BaseCommand):
    # python manage.py export_projects_as_csv
    help = 'Create a csv of data, luke...'

    def add_arguments(self, parser):
        ''#parser.add_argument('file',  type=str)

    def handle(self, *args, **options):
        #filename  = options['file']
        try:
            #id = randint(2228, 2228+500)
            projects = Project.objects.all()
            n = projects.count()
            i = 0

            EntityInstance.objects.all().delete()
            Entity.objects.all().delete()
           
            SocialTagInstance.objects.all().delete()
            SocialTag.objects.all().delete()

            for project in projects:
                #project = Project.objects.get(id=2235)
                print( project.title)
                
                sid = str(project.sid)
                fname =f'{sid}_calais.json'
            
                # UNDERSTAND
                try:
                    result = analyze(project.abstractText)
                except Exception as err:
                    print(err)
                    continue # something has gone wrong...

                #SAVE TO FILE
                f = open(fname, "w")
                f.write(json.dumps(result))
                f.close()

                ## SAVE TO DATABASE
                simplejson = _simplify_json(result) # cleans up stupidly complex json into just a studipdly complex json. 
                
                # ENTITIES
                if 'entities' not in simplejson:
                    print( simplejson)
                else:

                    for entity in simplejson['entities']:
                        print (entity['_type'], entity['name'], entity['relevance'] )
                        kind = entity['_type']
                        name = entity['name']
                        relevance = entity['relevance']

                        # ADD ENTITIES
                        e, created = Entity.objects.get_or_create( name = name)
                        e.kind = kind
                        if created:
                            e.save()

                        ei = EntityInstance.objects.create( relevance=relevance, entity=e )
                        ei.save()

                        project.entities.add( ei )


                # SOCIAL TAGS
                objs = print_social_tags( simplejson)
                for o in objs:
                    name = o['name']
                    importance = o['importance']
                    # ADD SOCIAL TAGS
                    st, created = SocialTag.objects.get_or_create(name = name)
                    if created:
                        st.save()

                    sti = SocialTagInstance.objects.create(importance=importance, socialtag=st)
                    sti.save()
                    
                    project.socialtags.add( sti )
                    project.save()
                sleep(randint(0,4))
                msg = "%s of %s" % (str(i), str(n))
                i = i +1
                print( msg  )

        except Exception as err:
            print(str(err))
            pass
            #raise CommandError( print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno)))

        self.stdout.write(self.style.SUCCESS('Done!'))