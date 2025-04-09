from rest_framework import serializers 
from  .models import *

class ingredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingridient
        fields = "__all__"

class recipeSerializer(serializers.ModelSerializer):
    recipe_ing = ingredientsSerializer(many=True)
    class Meta:
        model = Recipes
        fields = "__all__"
