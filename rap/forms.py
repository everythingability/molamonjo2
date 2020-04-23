from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.contrib.auth.models import User
from .models import Project, GTRCategory, HECategory, HEResearchArea, Person


class ProjectForm(ModelForm):
	class Meta:
		model = Project
		#fields = ['__all__']
		#fields = ['__all__',]
		exclude = ['created']
		widgets = {
			'title': forms.TextInput(
				attrs={
					'class': 'form-control'
					}
				),
			'url': forms.TextInput(
				attrs={
					'class': 'form-control'
					}
				),
			'image_url': forms.TextInput(
				attrs={
					'class': 'form-control'
					}
				),
			'about': forms.Textarea(
				attrs={
					'class': 'form-control'
					}
				),
			}