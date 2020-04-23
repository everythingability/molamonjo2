"""monjo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import rap
import rap.views

urlpatterns = [
    path("", rap.views.home, name="home"),  # THE SITE HOME, no login required.
    path('logout/', rap.views.logout_view, name='logout'),  # THE SITE HOME


   
    path('rap/', include('rap.urls')),  # THE SITE FUNCTIONALITY @login_required
    path('admin/', admin.site.urls),
]
urlpatterns += staticfiles_urlpatterns()
print( urlpatterns)
