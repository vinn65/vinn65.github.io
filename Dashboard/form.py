from dataclasses import fields
from django import forms
from . models import Homework, Notes, ToDo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']

class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject','title','description','due','is_finished'] 


class DashboardForm(forms.Form):
    text = forms.CharField(label='Enter a search parameter..')


class TodoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'is_finished']

class ConversionForm(forms.Form):
    CHOICES = [('length','Length'),('mass','Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES = [('yard','Yard'),('foot','Foot')]
    input1 = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter a value to convert'}
        ))
    measure1 = forms.CharField(
        label = '',widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label = '',widget=forms.Select(choices = CHOICES)
    )

class ConversionMassForm(forms.Form):
    CHOICES = [('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField(required=False, label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter a value to convert'}
        ))
    measure1 = forms.CharField(
        label = '',widget=forms.Select(choices = CHOICES)
    )
    measure2 = forms.CharField(
        label = '',widget=forms.Select(choices = CHOICES)
    )

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']


