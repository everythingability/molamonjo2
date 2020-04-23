from django.core.management.base import BaseCommand, CommandError
from rap.models import Project, Person, Organisation, GTRCategory
import os, sys
import csv, json, requests

from random import randint
from time import sleep

def fixDate(s): # 01/02/2020 to YYYY-MM-DD
    try:
        if s !=None:
            dItems = s.split("/")
            year = dItems[2]
            month = dItems[1]
            day = dItems[0]
            d = f"{year}-{month}-{day}" 
            return d
        else:
            return None
    except:
        return None

dir_path = os.path.dirname(os.path.realpath(__file__))
class Command(BaseCommand):
    # python manage.py update_abstracts"
    help = 'Use the API luke...'

    def add_arguments(self, parser):
        ''#parser.add_argument('file',  type=str)

    def handle(self, *args, **options):
        #filename  = options['file']
        try:
            projects = Project.objects.all()
            pcount = projects.count()
            for i, project in enumerate(projects):
                try:
                    project.api_get()
                    print( f'{i} of {pcount}...')
                    sleep(randint(0,4))
                except Exception as err:
                    print(err)

        except Exception as err:
            print(str(err))
            raise CommandError( print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno)))


        self.stdout.write(self.style.SUCCESS('Done!'))