from django.shortcuts import render
#from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from django.db.models import Q
from django.db import connection
from .serializer import *
import re
from rest_framework.renderers import JSONRenderer

def recipePageView(request,recipeId):    
    jsonStringOut = {"":""}  

    try:
        recipe = Recipes.objects.filter(id=recipeId)
        #JSONRenderer().render(serializer.data)
        jsonStringOut=recipeSerializer(recipe[0]).data
        #jsonStringOut=serializers.serialize('json', recipe)
        #jsonStringOut = ConstructJSONResponseRecipe(recipe.cooktime,recipe.calories,recipe.servingSize,recipe.carbs,recipe.fats,recipe.proteines,recipe.directions,recipe.imageLink)
    except :
        return JsonResponse(jsonStringOut,safe=False)

    return JsonResponse(jsonStringOut,safe=False)

def recipeView (request):
    if not request.COOKIES.get('ingredients'):
        response = JsonResponse({"":""})
        return response
    else:
        ingredients = request.COOKIES.get("ingredients").split(',')        
        ingrs = ",".join(ingredients)
        Singr = SearchIngridients.objects.raw(f"SELECT MIN(id) as id ,recipes_id, GROUP_CONCAT(ingridient ORDER BY ingridient ASC SEPARATOR ', ') AS all_ingridients FROM recipedj.ingridients_searchingridients WHERE ingridient IN ({ingrs}) GROUP BY recipes_id")        
        jsonStringOut = ""
        concatIngs = ""
        countRes = 1
        for result in Singr:                 
            try:
                allIngredients = SearchIngridients.objects.raw(f"SELECT MIN(id) as id ,recipes_id, GROUP_CONCAT(ingridient ORDER BY ingridient ASC SEPARATOR ', ') AS ingrids FROM recipedj.ingridients_searchingridients WHERE ingridient NOT IN ({ingrs}) AND recipes_id = '{result.recipes_id}' GROUP BY recipes_id LIMIT 1")                       
                concatIngs = allIngredients[0].ingrids
            except:
                concatIngs = ""

            try :
                recipe = Recipes.objects.get(id=result.recipes_id)
                jsonString =ConstructJSONResponse(result.recipes_id,recipe.imageLink,result.all_ingridients,recipe.link,recipe.calories,recipe.proteines,recipe.fats,recipe.carbs,countRes,concatIngs)
                jsonStringOut += jsonString+','
                countRes += 1
            except:
                #print(f"no id {result.recipes_id}")    
                pass

        jsonStringOut = jsonStringOut.rstrip(",")
        jsonStringOut = "{"+jsonStringOut+"}"
        response = JsonResponse(jsonStringOut,safe=False)

        return response

def ConstructJSONResponse(Id,imageLink,tags,url,calories,proteines,fats,carbs,count,ingInside):
    JsonString =  f'"recipe{count}" :'+'{'+f'"recipeId" :"{Id}","title" : "{GetNameFromLink(url)}", "image": "{imageLink}", "ingridients": "{tags}","inginside":"{ingInside}", "link": "{url}", "calories": "{calories}", "proteines": "{proteines}", "fats": "{fats}", "carbs": "{carbs}"'+"}"
    return JsonString

def ConstructJSONResponseRecipe(cooktime,calories,servingSize,carbs,fats,proteines,directions,imageLink):
    JsonString = '{"recipeD" : {'+f'"cooktime" :"{cooktime}", "calories": "{calories}", "servingSize": "{servingSize}", "carbs": "{carbs}", "fats": "{fats}", "proteines": "{proteines}", "directions": "{directions}", "imageLink": "{imageLink}"'+'}}'
    return JsonString

def GetNameFromLink(link):
    try:
        url = link.rstrip("/")
        parts = url.split("/")
        name = parts[len(parts)-1]
        name = name.replace("-"," ")
        return name
    except:
        name = ""
        return name
    