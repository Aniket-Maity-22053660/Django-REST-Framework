from django import forms
from RESTAPI.models import MenuItems, Category

class DemoForm(forms.Form):
    slug = forms.SlugField()
    title = forms.CharField(max_length=255)

class ModelForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = '__all__'