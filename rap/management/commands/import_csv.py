from django.core.management.base import BaseCommand, CommandError
from rap.models import Project
import os
import csv, json

dir_path = os.path.dirname(os.path.realpath(__file__))
class Command(BaseCommand):
    # python manage.py import_tools file="tools.csv"
    help = 'meant to help me get started, importing a lot of initial data etc'

    def add_arguments(self, parser):
        parser.add_argument('file',  type=str)

    def handle(self, *args, **options):
        filename  = options['file']
        try:
            #self.stdout.write(dir_path)
            #self.stdout.write(filename)
            filename = filename.replace("file=", "") 
            fullpath = dir_path + "/" + filename
            self.stdout.write(fullpath)

            taxonomy_dicts = []
            file = open(fullpath, 'r')
            reader = csv.DictReader(file)
            for rec in reader:
                #print(rec) # Category	Subcategory	URL	Description	Image
                #self.stdout.write( rec["Name"] )
                try:
                    name = rec["Name"]
                    url = rec["URL"]
                    image_url = rec["Image"]
                    cat = rec["Category"]
                    altcat = rec["Subcategory"]
                    about = rec["Description"]
                    # Does the Category exits
                    catObj, created = Category.objects.get_or_create(name=cat,)
                    if created:
                        catObj.save()

                    altcatObj, created = Category.objects.get_or_create(name=altcat,)
                    if created:
                        altcatObj.save()

                    obj, created = Tool.objects.get_or_create(name=name,)
                    if created:
                        obj.url = url
                        obj.image_url = image_url
                        obj.category = catObj
                        obj.altcategory = altcatObj
                        obj.about = about
                        obj.save()
                        self.stdout.write( "Saved: " + rec["Name"] )
                except Exception as err:
                    self.stdout.write( "Error: " + str(err) + " name" )







        except Exception as err:
            raise CommandError( str(err))


        self.stdout.write(self.style.SUCCESS('Done!'))