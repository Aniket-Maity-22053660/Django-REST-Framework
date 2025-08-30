from django import forms
from RESTAPI.models import MenuItems

class DemoForm(forms.Form):
    name = forms.CharField(widget=forms.Textarea(attrs= {'rows':5}))
    email = forms.EmailField(label="Enter an email address")

class ModelForm(forms.ModelForm):
    class Meta:
        model=MenuItems
        fields = '__all__'