from django import forms
 
from .models import Character, Equipement
 
class MoveForm(forms.ModelForm):
 
    class Meta:
        model = Character
        fields = ('lieu',)