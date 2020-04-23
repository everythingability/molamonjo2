from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # THE SITE HOME
   

    #path('bio/<username>/', views.bio, name='bio'),
    #path('articles/<slug:title>/', views.article, name='article-detail'),
    path('projects/', views.projects, name='projects'),
    path('project/<str:id>/', views.project, name='project'),
    path('heresearcharea/<str:id>/', views.heresearcharea, name='heresearcharea'),
    #path('weblog/', include('blog.urls')),
    
]