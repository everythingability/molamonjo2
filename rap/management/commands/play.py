from django.core.management.base import BaseCommand, CommandError
from rap.models import Project, GTRCategory, HECategory, HEResearchArea, Person, Organisation
import os, sys
import csv, json

cats =["Archaeological Theory",
"Archaeology Of Human Origins",
"Archaeology of Literate Soc.",
"Architecture HTP",
"Environmental planning",
"Heritage Management",
"Landscape & Environ. Archaeol.",
"Prehistoric Archaeology",
"Science-Based Archaeology"]

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
    # python manage.py import_tools file="tools.csv"
    help = 'meant to help me get started, importing a lot of initial data etc'

    def add_arguments(self, parser):
        ''#parser.add_argument('file',  type=str)

    def handle(self, *args, **options):
        #filename  = options['file']
        try:
            #Project, GTRCategory, HECategory, HEResearchArea, Person, Organisation

            hecategories = HECategory.objects.all()
            gtrs = GTRCategory.objects.all()
            heresearchareas = HEResearchArea.objects.order_by('hecategory')

            previous_category = None
            for n,heresearcharea in enumerate(heresearchareas):

                category = heresearcharea.hecategory ######### MAKE THE HEADER
                if category != previous_category:
                    total = 0
                    print("\n")
                    print(category)
                    print("'" * 80)
               
                c = 0
                these_gtrs = heresearcharea.gtrs.all()
                these_ids = []
                for t in these_gtrs:
                    these_ids.append(t.id)
                #print (these_ids)
                for gtr in these_gtrs:
                
                    c = c + Project.objects.filter( gtrs__in=these_ids ).count()
                #total = total + c
                print( heresearcharea.name, c)


                previous_category = category
                
           


        except Exception as err:
            print(str(err))
            raise CommandError( print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno)))


        self.stdout.write(self.style.SUCCESS('Done!'))