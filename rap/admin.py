from django.contrib import admin

admin.site.site_header = "RAP Admin"
admin.site.site_title = "RAP Admin Portal"
admin.site.index_title = "Welcome to RAP Portal"

from .models import  Author, Entry, Blog
from .models import Project, GTRCategory, HECategory, HEResearchArea, Person, Organisation
from .models import *

#admin.site.register(EntityInstance)

#admin.site.register(SocialTagInstance)

@admin.register(SocialTag)
class SocialTagAdmin(admin.ModelAdmin):
	model = SocialTag
	ordering = ['-instance_count']
	
	list_display = ('__str__','instance_count',)
	#list_filter = ('kind',)

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
	model = Entity
	ordering = ['-instance_count']
	list_display = ('__str__','instance_count')
	list_filter = ('kind',)


	
@admin.register(Organisation)
class OrganisationPersonAdmin(admin.ModelAdmin):
	model = Organisation
	
	list_display = ('__str__','project_count','api_link')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
	model = Person
	list_display = ('__str__','project_count','api_link', 'last_org')
	#list_filter = ('last_org',)

@admin.register(GTRCategory)
class GTRCategoryAdmin(admin.ModelAdmin):
	model = GTRCategory
	list_display = ('__str__','areas_as_list', 'project_count')

@admin.register(HECategory)
class HEResearchAreaAdmin(admin.ModelAdmin):
	model = HECategory
	list_display = ('__str__','research_areas',		)



@admin.register(HEResearchArea)
class HEResearchAreaAdmin(admin.ModelAdmin):
	model = HEResearchArea
	list_display = ('__str__',
	   'children',
	   'gtr_as_list',
	   'entities_count', 'socialtags_count')
	list_filter = ('hecategory', )
	filter_horizontal = ('socialtags','entities',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	model = Project
	list_display = ('__str__', 'api_link','gtrs_display','end','status')
	search_fields = ['title', "abstractText"]
	list_filter = ('leadFunder','leadOrganisation', 'status' )
	filter_horizontal = ('socialtags','entities',)
	date_hierarchy = 'end'
	readonly_fields = ["json"]

	def gtrs_display(self, obj):
		return ", ".join([
			child.name for child in obj.gtrs.all()
		])
	gtrs_display.short_description = "GtRs"

'''
def save_model(self, request, obj, form, change):
    obj.added_by = request.user
    super().save_model(request, obj, form, change)
'''
	



