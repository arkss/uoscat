from django import forms
from .models import Cat

class CatPost(forms.Form):
    name = forms.CharField(max_length=20)
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    gender = forms.ChoiceField(choices=[("male","수컷"),
        ("female","암컷"),
        ("null","모름"),]
        
    )
    body = forms.CharField()
    
