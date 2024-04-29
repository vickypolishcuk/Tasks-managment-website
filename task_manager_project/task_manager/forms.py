from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    final_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
    )
    class Meta:
        model = Task
        fields = ['title', 'description', 'final_date', 'executor']
