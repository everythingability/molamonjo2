import requests
import os

from django.http import HttpResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators  import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib import messages
#
from rap.models import Project, GTRCategory, HECategory, HEResearchArea, Person
from .forms import ProjectForm

def home(request):
    return render(request, "home.html", {} )

# Create your views here.
@login_required
def dashboard(request):

    projects =     Project.objects.all()
    hecategories = HECategory.objects.all()
    herearchareas = HEResearchArea.objects.all()
    gtrCategories  = GTRCategory.objects.all()


    context = {'hecategories':hecategories,
               'herearchareas':herearchareas,
               'gtrCategories':gtrCategories,
               'projects':projects
                }


    return render(request, "projects/dashboard.html", context )

@login_required
def projects(request):

    projects = Project.objects.all()
   
    return render(request, "projects/projects.html", {'projects': projects} )

@login_required
def project(request, id):

    project = Project.objects.get(id=id)
    form = ProjectForm(instance = project)
    return render(request, "projects/project.html", {'project': project, 'form':form, 'request':request} )

@login_required
def heresearcharea(request, id):

    heresearcharea = HEResearchArea.objects.get(id=id)
    gtrs = heresearcharea.gtrs.all()
    entities = heresearcharea.entities.all() #instances 
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

    return render(request, "projects/heresearcharea.html", {'heresearcharea': heresearcharea, 'request':request, 'projects':mergedprojects} )


def logout_view(request):
    logout(request)
    return redirect("/")

def polls_list(request):
    MAX_OBJECTS = 20
    polls = Poll.objects.all()[:MAX_OBJECTS]
    data = {"results": list(polls.values("question", "created_by__username", "pub_date"))}
    return JsonResponse(data)


