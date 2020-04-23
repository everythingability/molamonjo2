from django.core.management.base import BaseCommand, CommandError
from rap.models import Project, Person, Organisation, GTRCategory
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
    # python manage.py import_projects"
    help = 'meant to help me get started, importing a lot of initial data etc'

    def add_arguments(self, parser):
        ''#parser.add_argument('file',  type=str)

    def handle(self, *args, **options):
        #filename  = options['file']
        try:
            #self.stdout.write(dir_path)
            #self.stdout.write(filename)
            filename = "all_projects.csv"#filename.replace("file=", "") 
            fullpath = dir_path + "/" + filename
            self.stdout.write(fullpath)

            taxonomy_dicts = []
            file = open(fullpath, 'r')
            reader = csv.DictReader(file)
            # Title	StartDate	EndDate	AwardPounds	ExpenditurePounds	Region	Status
            # FundingOrgName	ProjectReference	LeadROName	Department	ProjectCategory	
            # PISurname	PIFirstName	PIOtherNames	PI ORCID iD	StudentSurname	
            # StudentFirstName	StudentOtherNames	Student ORCID iD	
            	
            # #Classifications 1	Classifications 2	Classifications 3	Classifications 4	Classifications 5	Other Classifications	
            # GTRProjectUrl	ProjectId	FundingOrgId	LeadROId	PIId	

            n = 1	
            for i, rec in enumerate(reader):
              
                sid = rec['ProjectId']
                title = rec["Title"]
                start = rec["StartDate"]
                end = rec['EndDate']
                #abstractText = rec['']
                print(start, end)
                start = fixDate(start)
                end = fixDate(end)

                awardPounds = rec['AwardPounds']
                expenditurePounds = rec['ExpenditurePounds']
                #print(awardPounds,  expenditurePounds)

                if awardPounds=='':awardPounds = int(0)
                if expenditurePounds=='':expenditurePounds = int(0)

                Region = rec['Region']
                status = rec['Status']
                fundingOrgId = rec['FundingOrgId']
                projectCategory  = rec['ProjectCategory'] #Research Grant, Feasibility Study
                GTRProjectUrl =  rec['GTRProjectUrl']

                LeadROId = rec['LeadROId']
                LeadROName = rec['LeadROName']
                Department = rec['Department']

                
                PIId = rec['PIId']
                PIFirstName = rec['PIFirstName']
                PIOtherNames = rec['PIOtherNames']
                PISurname = rec['PISurname']
                PIORCIDiD = rec['PI ORCID iD']

                # Classifications
                c_1 = str(rec['Classifications 1'])
                c_2 = str(rec['Classifications 2'])
                c_3 = str(rec['Classifications 3'])
                c_4 = str(rec['Classifications 4'])
                c_5 = str(rec['Classifications 5'])
               
                match = False
                new_cats = []
                other_cats =[]
                if c_1 in cats:
                    match = True
                    new_cats.append(c_1)
                else:
                    other_cats.append(c_1)
                if c_2 in cats :
                    match = True
                    new_cats.append(c_2)
                else:
                    other_cats.append(c_2)
                if c_3 in cats :
                    match = True
                    new_cats.append(c_3)
                else:
                    other_cats.append(c_3)
                if c_4 in cats :
                    match = True
                    new_cats.append(c_4)
                else:
                    other_cats.append(c_4)
                if c_5 in cats :
                    match = True
                    new_cats.append(c_5)
                else:
                    other_cats.append(c_5)

                if match == True: #It's in one of the selected categories

                    #get or create the project
                    
                    project, created = Project.objects.get_or_create(sid=sid)
                    if created:
                        project.title = title
                        project.start = start
                        project.end = end
                        project.awardPounds = awardPounds
                        project.expenditurePounds = expenditurePounds
                        #project.leadFunder = leadFunder
                        
                        project.status = status
                        project.projectCategory = projectCategory
                        project.GTRProjectUrl = GTRProjectUrl
                        project.fundingOrgId = fundingOrgId
                        print (start, end)
                        project.save()


            
                    #get or create the organisation, add to project
                    org, created = Organisation.objects.get_or_create(sid=LeadROId)
                    if created:
                        org.name = LeadROName
                        org.save()
                    project.leadOrganisation = org
                    project.save()

                    #get or create the PI, add to project
                    person, created = Person.objects.get_or_create(sid=PIId)
                    if created:
                        person.firstName = PIFirstName
                        person.otherNames = PIOtherNames
                        person.surname = PISurname
                        person.orchidID = PIORCIDiD
                        person.save()
                    project.pi = person
                    project.save()

                    #for each of the categories, get/create and add to project
                    for cat in new_cats:
                        print("CAT", cat)
                        if cat != '':
                            catObj = GTRCategory.objects.filter(name=cat).first()
                            if catObj != None:
                                catObj.isHECategory = True
                                catObj.save()
                                project.gtrs.add(catObj)

                    for cat in other_cats:
                        if cat != '':
                            catObj = GTRCategory.objects.filter(name=cat).first()
                            if catObj != None:
                                catObj.isHECategory = False
                                catObj.save()
                                project.gtrs.add(catObj)
                    project.save()





                    print (n, i, new_cats , other_cats)
                    print(PIId)
                    print ( PIFirstName, PIOtherNames,PISurname)
                    print (title)
                    #print ( c_1, c_2, c_3, c_4, c_5)
                    print( GTRProjectUrl)
                    
                    n = n + 1
                    print("-" * 80)

                   
               


        except Exception as err:
            print(str(err))
            raise CommandError( print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno)))


        self.stdout.write(self.style.SUCCESS('Done!'))