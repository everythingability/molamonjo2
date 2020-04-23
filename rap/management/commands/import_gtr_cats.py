from django.core.management.base import BaseCommand, CommandError
from rap.models import GTRCategory

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

dir_path = os.path.dirname(os.path.realpath(__file__))
class Command(BaseCommand):
    # python manage.py import_gtr_cats"
    help = ''

    def add_arguments(self, parser):
        ''#parser.add_argument('file',  type=str)

    def handle(self, *args, **options):
        #filename  = options['file']
        try:
            #self.stdout.write(dir_path)
            #self.stdout.write(filename)
            
            for cat in wanted_cats:
                #print(rec) # Category	Subcategory	URL	Description	Image
                #self.stdout.write( rec["Name"] )
                try:
                    name = cat

                    catObj, created = GTRCategory.objects.get_or_create(name=cat,)
                    if created:
                        
                        catObj.save()
                    print(created, catObj.name)
                except Exception as err:
                    self.stdout.write( "Error: " + str(err) + " name" )







        except Exception as err:
            raise CommandError( str(err))


        self.stdout.write(self.style.SUCCESS('Done!'))