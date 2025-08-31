from django import forms
from RESTAPI.models import MenuItems, Category, Photo

class DemoForm(forms.Form):
    slug = forms.SlugField()
    title = forms.CharField(max_length=255)

class ModelForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = '__all__'

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = "__all__"