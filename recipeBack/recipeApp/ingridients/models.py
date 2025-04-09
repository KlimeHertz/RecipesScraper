from django.db import models
from datetime import datetime

# Create your models here.
class Recipes (models.Model):
    id = models.CharField(primary_key=True, null=False, unique=True,max_length=80)
    link = models.URLField(blank=True,null=True)
    cooktime = models.CharField(max_length=45,null=True)
    calories = models.CharField(max_length=20,null=True)
    servingSize = models.CharField(max_length=20,null=True)
    carbs = models.CharField(max_length=45,null=True)
    fats = models.CharField(max_length=45,null=True)
    proteines = models.CharField(max_length=45,null=True)
    description = models.TextField(blank=True,null=True)
    directions = models.TextField(blank=True,null=True)
    insertDate = models.DateField(blank=True,null=True)
    imageLink = models.URLField(blank=True,null=True)
    
    def save(self,**kwargs):
        self.insertDate = datetime.now()
        super().save(**kwargs)


class Ingridient(models.Model):
    id = models.CharField(primary_key=True, null=False, unique=True,max_length=80)
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE,related_name='recipe_ing')
    ingridient = models.CharField(max_length=80)

class SearchIngridients(models.Model):
    id = models.CharField(primary_key=True, null=False, unique=True,max_length=80)
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingridient = models.CharField(max_length=80)
