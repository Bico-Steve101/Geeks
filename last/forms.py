from django import forms
from .models import Hackathons, Projects, Contacts, Grade
from last.models import User  # Import your custom User model
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'bio', 'tag', 'project_description', 'avatar')


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class HackathonForm(forms.ModelForm):  # creating a new form for the Space
    class Meta:
        model = Hackathons  # the name of the Space specified
        fields = '__all__'  # list of fields to include in the form fields, they are required(the founder, name and
        # others under space that are editable)
        exclude = ['founder', 'participants']  # the list of items to exclude from the entry field


class ProjectForm(forms.ModelForm):  # creating a new form for the Space
    class Meta:
        model = Projects  # the name of the Space specified
        fields = '__all__'  # list of fields to include in the form fields, they are required(the founder, name and
        # others under space that are editable
        exclude = ['user']  # the list of items to exclude from the entry field


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = '__all__'

        exclude = ['user']


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade']

        # To provide a custom display in the form
        labels = {
            'grade': 'Participant Grade',
        }

        # You can add widgets or customize input types here if needed
        widgets = {
            'grade': forms.NumberInput(attrs={'step': '0.1'}),  # Example for decimal places
        }


GradeFormSet = forms.modelformset_factory(Grade, form=GradeForm, extra=0)


class GradeFormAll(forms.Form):
    participant = forms.IntegerField(widget=forms.HiddenInput())
    grade = forms.IntegerField()
