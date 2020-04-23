from django.core.management.base import BaseCommand, CommandError
from rap.models import GTRCategory, HECategory, HEResearchArea

import pprint
import os
import csv, json
from datetime import datetime

import pymongo
from pymongo import MongoClient
client = MongoClient()

dir_path = os.path.dirname(os.path.realpath(__file__))
class Command(BaseCommand):
    # python manage.py import_tools file="tools.csv"
    help = 'meant to help me get started, importing a lot of initial data etc'

    def add_arguments(self, parser):
        ''#parser.add_argument('file',  type=str)

    def handle(self, *args, **options):
        #filename  = options['file']
        try:
            print( client )
            db = client.monjo
            projectstable = db.rap_project

            project = {
                "id": "317494312946123467",
                "title": "Hello There",
                "abstractText": "Let's see if this works",
                "status": "Open",
                "whathappens": 42
                }
            project_id = projectstable.insert_one(project).inserted_id
            print( project_id )
            pprint.pprint(projectstable.find_one())


                      
            
        except Exception as err:
            raise CommandError( str(err))


        self.stdout.write(self.style.SUCCESS('Done!'))