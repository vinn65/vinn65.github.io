from django import forms
from . models import Homework, Notes, ToDo

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