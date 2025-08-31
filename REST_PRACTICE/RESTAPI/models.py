from django.db import models

# Create your models here.

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class MenuItems(models.Model):
    title= models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory= models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='Category')

    def __str__(self):
        return self.title

class Photo(models.Model):
    title=models.CharField(max_length=255)
    image=models.ImageField(upload_to="avatar/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    