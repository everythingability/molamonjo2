from django.db import models # https://nesdis.github.io/djongo/get-started/
from django.db.models import Q
#from djongo.models.indexes import TextIndex
#from djongo.models import CheckConstraint, Q
#from djongo.models.indexes import WildcardIndex
from django import forms
from datetime import datetime
from django.utils.safestring import mark_safe
from rap.utils import *
#EmbeddedField

# An alternative to ManyToManyFields
#ArrayField https://nesdis.github.io/djongo/using-django-with-mongodb-array-field/

class SocialTag(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, default='')
    instance_count= models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name_plural = "Social Tags"
        verbose_name = "Calais Social Tag"
        ordering = ('-instance_count', )
    
    def doCount(self):
        instance_count = SocialTagInstance.objects.filter(socialtag=self).count()
        self.instance_count = instance_count
        self.save()
        return instance_count

    

    def __str__(self):
        return str( self.name) 


class SocialTagInstance(models.Model):
    importance = models.IntegerField(null=True, blank=True, default=0)
    socialtag = models.ForeignKey(SocialTag, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="instances")
    def __str__(self):
        return str( self.socialtag) + " > " + str(self.importance)

class Entity(models.Model):
    kind = models.CharField(max_length=255, null=True, blank=True, default='')
    name = models.CharField(max_length=255, null=True, blank=True, default='')
    instance_count= models.IntegerField(null=True, blank=True, default=0)

    def doCount(self):
        instance_count = EntityInstance.objects.filter(entity=self).count()
        self.instance_count = instance_count
        self.save()
        return instance_count


    class Meta:
        verbose_name_plural = "Entities"
        verbose_name = "Calais Entity"

    def __str__(self):
        return str( self.kind) + " > " + str(self.name)


class EntityInstance(models.Model):
    relevance = models.FloatField(null=True, blank=True, default=0.0)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True, blank=True, default=None)
    def __str__(self):
        return str( self.entity) + " > " + str(self.relevance)


class HECategory( models.Model ):

    class Meta:
        verbose_name_plural = "HE Categories"
        verbose_name = "HE Category"

    name = models.CharField(max_length=255)
    #objects = models.DjongoManager()

    def researchareas(self):
        heresearchreas = HEResearchArea.objects.filter(hecategory=self)
        return heresearchreas 

    def research_areas(self):
        heresearchreas = HEResearchArea.objects.filter(hecategory=self)
        s = ''
        for h in heresearchreas:
            s = s + h.name + ", "
        return s


    def __str__(self):
        #str(str(self.id) + "> " +
        return  str(self.name)

class GTRCategory(models.Model):

    class Meta:
        verbose_name_plural = "GtR Categories"
        verbose_name = "GtR Category"

    sid =  models.CharField(max_length=255, null=True, blank=True, default='') 
    name = models.CharField(max_length=255, null=True, blank=True, default='')
    percentage = models.IntegerField(null=True, blank=True, default=0)
    isHECategory = models.BooleanField(null=False,  default=False)

    #objects = models.DjongoManager()

    def project_count(self):
        #https://stackoverflow.com/questions/39677745/how-to-query-django-manytomany-relationship
        #from django.db.models import Count
        #Book.objects.annotate(author_count=Count('authors')).filter(author_count=1)

        projects = Project.objects.filter(gtrs=self)
        return str(projects.count())

    def areas_as_list(self):
        # Reverse lookup
        s = ''
        
        for g in self.gtrs.all():
            s = s + str(g.name) + " , "
        
        return str(    s   )

    def __str__(self):
        if self.name == None:
            return str(self.id)
        return str(self.name)



class HEResearchArea(models.Model):

    class Meta:
        verbose_name_plural = "HE Research Areas"
        verbose_name = "HE Research Area"

    hecategory = models.ForeignKey(HECategory, on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.CharField(max_length=255,null=True, blank=True, default='')
    search_terms = models.TextField(null=True, blank=True, default='',help_text="One per line. Terms will searched for in projects. You don't need to add the name of this category")

    gtrs = models.ManyToManyField(
        to=GTRCategory,
        blank=True, default=None,
       related_name="gtrs"
      
    )
    socialtags = models.ManyToManyField(
        to=SocialTag,
        blank=True, default=None,
       related_name="socialtags"
      
    )
    entities = models.ManyToManyField(
        to=Entity,
        blank=True, default=None,
       related_name="entities"
      
    )

    ######################################### METHODS ##########################################

    def myprojects(self):
        heresearcharea = self
        gtrs = heresearcharea.gtrs.all()
        #entities = heresearcharea.entities.all() #instances 
        socialtags = heresearcharea.socialtags.all() #instances

        ids = []
        for s in socialtags:
            ids.append( s.id)

        mergedprojects = []

        projects = Project.objects.filter( Q(socialtags__socialtag_id__in=ids)|Q(gtrs__in=gtrs)  )
        for p in projects:
            if p in mergedprojects:
                ''
            else:
                mergedprojects.append(p)
        return mergedprojects

    def myprojects_count(self):
        heresearcharea = self
        gtrs = heresearcharea.gtrs.all()
        #entities = heresearcharea.entities.all() #instances 
        socialtags = heresearcharea.socialtags.all() #instances

        ids = []
        for s in socialtags:
            ids.append( s.id)

        mergedprojects = []

        projects = Project.objects.filter( Q(socialtags__socialtag_id__in=ids)|Q(gtrs__in=gtrs)  )
        for p in projects:
            if p in mergedprojects:
                ''
            else:
                mergedprojects.append(p)
                
        return len(mergedprojects)



    def entities_count(self):
        return self.entities.count()

    def socialtags_count(self):
        return self.socialtags.count()
    #objects = models.DjongoManager()

    def gtr_as_list(self):
        # Children query
        s = ''
        for g in self.gtrs.all():
            s = s + str(g.name) + " , "
        return str(    s   )

    def children(self):
        
        return str(    self.gtrs.all().count()    )

    def __str__(self):
        if self.name == None:
            return str(self.id)
        return str(self.name)




class Person(models.Model):

    sid =  models.CharField(max_length=255) 
    name = models.CharField(max_length=255, null=True, blank=True, default='')
    firstName = models.CharField(max_length=50, null=True, blank=True, default='')
    otherNames = models.CharField(max_length=50, null=True, blank=True, default='')
    surname = models.CharField(max_length=50, null=True, blank=True, default='')
    orchidID = models.CharField(max_length=50, null=True, blank=True, default='')

    @mark_safe
    def api_link(self):
        sid = self.sid
        href = f'https://gtr.ukri.org:443/gtr/api/persons/{sid}'
        return '<a href="' + href + '">api</a>'
    #api_link.allow_tags = True

    def project_count(self):
        projects = Project.objects.filter(pi= self)
        return str( projects.count())

    def last_org(self):
        project = Project.objects.filter(pi= self).last()
        return str(project.leadOrganisation.name)


    def getName(self):
        return self.firstName + " " + self.otherNames + " " + self.surname

    def __str__(self):
        return  str(self.getName() )

    

class Organisation(models.Model):

    sid =  models.CharField(max_length=255) 
    name = models.CharField(max_length=255, null=True, blank=True, default='')
    
    class Meta:
        ordering = ('name',)
    
    @mark_safe
    def api_link(self):
        sid = self.sid
        href = f'https://gtr.ukri.org:443/gtr/api/organisations/{sid}'
        return '<a href="' + href + '">api</a>'
    #api_link.allow_tags = True

    def project_count(self):
        projects = Project.objects.filter(leadOrganisation=self)
        return str(projects.count())

    def __str__(self):
        return str(self.name)

class Project(models.Model):

    '''
    'links', 'ext', 'id', 'outcomeid', 'href', 'created', 'updated', 'identifiers',
     'title', 'status', 'grantCategory', 'leadFunder', 'leadOrganisationDepartment', 
     'abstractText', 'techAbstractText', 'potentialImpact', 'healthCategories', 
     'researchActivities', 'researchSubjects', 'researchTopics', 'rcukProgrammes', 
     'start', 'end', 'participantValues'
    '''

    sid =  models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    href = models.CharField(max_length=255, null=True, blank=True, default=None)
    abstractText = models.TextField(null=True, blank=True, default=None)
    start = models.DateField(null=True, blank=True, default=None )
    end = models.DateField(null=True, blank=True, default=None )
    created = models.DateField(null=True, blank=True, default=None )
    updated= models.DateField( null=True, blank=True, default=None)
    projectCategory = models.CharField(max_length=30,null=True, blank=True, default=None)
    leadFunder = models.CharField(max_length=30, null=True, blank=True, default=None)
    status = models.CharField(max_length=12, null=True, blank=True, default=None)
    awardPounds = models.IntegerField(null=True, blank=True, default=0)
    expenditurePounds = models.IntegerField(null=True, blank=True, default=0)
    department = models.CharField(max_length=255, null=True, blank=True, default='')
    GTRProjectUrl = models.CharField(max_length=255, null=True, blank=True, default=None)
    fundingOrgId = models.CharField(max_length=255, null=True, blank=True, default=None)
    pi = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True, default=None)
    json = models.TextField(null=True, blank=True, default=None)

    leadOrganisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, blank=True, default=None)


    gtrs = models.ManyToManyField(to=GTRCategory)
    entities = models.ManyToManyField(to=EntityInstance)
    socialtags = models.ManyToManyField(to=SocialTagInstance)
  
    #objects = models.DjongoManager()


        

    @mark_safe
    def api_link(self):
        sid = self.sid
        href = f'https://gtr.ukri.org:443/gtr/api/projects/{sid}'
        return '<a href="' + href + '">api</a>'
    #api_link.allow_tags = True

    def update_abstract(self):
        sid = self.sid
        href = f'https://gtr.ukri.org:443/gtr/api/projects/{sid}'

    def api_get(self):
        sid = self.sid
        url = f'https://gtr.ukri.org:443/gtr/api/projects/{sid}'

        j = jget(url)
        self.json = j
        self.save()
        print (len(j), self.sid, self.title  )
        try: #update the values we don't have
            self.abstractText = j['abstractText']
            self.leadFunder = j['leadFunder']
            self.save()
        except Exception as err:
            print(err)





    def gtr_as_list(self):
        # Children query
        s = ''
        for g in self.gtrs.all():
            s = s + str(g.name) + " , "
        return str(    s   )

    def __str__(self):
        return str( self.title)



























class Blog(models.Model):
    class Meta:
        ''
        #abstract = True

    name = models.CharField(max_length=100)
    tagline = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        return self.name
    
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = (
            'name', 'tagline'
        )

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True, default='')

    def __str__(self):
        return self.name

class Entry(models.Model):
    #blog = models.EmbeddedField(model_container=Blog)
    #
    #blog = models.EmbeddedField(model_container=Blog,model_form_class=BlogForm)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField( )
    mod_date = models.DateField(default=datetime.now, )
    authors = models.ManyToManyField(
        to=Author,

    )
    n_comments = models.IntegerField(null=True, blank=True)
    n_pingbacks = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    #objects = models.DjongoManager()

    class Meta:
        ''
        #indexes = [TextIndex(fields=['headline', ])]
        #constraints = [CheckConstraint(check=Q(author_age__gte=18), name='age_gte_18')]

    def __str__(self):
        return self.headline