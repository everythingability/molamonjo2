from django.core.management.base import BaseCommand, CommandError
from rap.models import GTRCategory, HECategory, HEResearchArea

import os
import csv, json

wanted_cats = '''Archaeology of Human Origins
Prehistoric Archaeology
Archaeology of Literate Societies
Archaeological Theory
Science-Based Archaeology
Landscape and Environmental Archaeology
Heritage Management
Architecture HTP
Environmental Planning'''.split("\n")

hecats ='''Adapt	 Climate change	Heritage crime	Land management	Local planning	National planning and infrastructure	Societal change
Conserve	  Buildings and landscapes	Collections and archives	Preserving archaeological remains
Diversity	 Exploring diversity	Workforce diversity
Inform	Information systems and services	New narratives from 'big data'
Innovate	Dating and chronology	Human environment	Materials
Inspire	Audience research	Research media
Skill	Developing the workforce	Working more effectively
Understand	Archaeology of the deeper past	Faith and commemoration	Industrial and infrastructure	Marine and maritime	Military and defence	Rural landscape	Understanding the Historic England Archive	Urban and public realm	Water, wetlands and waterlogged
Value	 Contested values	Economic value	Social value'''.split("\n")

dir_path = os.path.dirname(os.path.realpath(__file__))
class Command(BaseCommand):
    # python manage.py import_he_cats"
    help = 'meant to help me get started, importing a lot of initial data etc'

    def add_arguments(self, parser):
        ''#parser.add_argument('file',  type=str)

    def handle(self, *args, **options):
        #filename  = options['file']
        try:
                      
            for cat in hecats:
                items = cat.split("\t")
                hecategoryname  =  items[0].strip()
                heresearchareas = items[1:len(items)]
                
                print(hecategoryname)
                hec = HECategory(name=hecategoryname)
                hec.save()
                
                try:
                    ''#name = cat
                    for heresearcharea in heresearchareas:
                        he = heresearcharea.strip()
                        if he != '':
                            
                            hera = HEResearchArea(name=he, )
                            hera.save()
                            hera.hecategory = hec
                           
                            hera.save()
                            print( he , hec)

                    print("_" * 80)
                    
                except Exception as err:
                    self.stdout.write( "Error: " + str(err) + " name" )

        except Exception as err:
            raise CommandError( str(err))


        self.stdout.write(self.style.SUCCESS('Done!'))