from django import forms
from .models import *

class ishForum(forms.ModelForm):
    class Meta:
        model = ish
        fields = ['nomi','rasmi', 'narxi', 'info']
