import uuid
from consts import *

class Card:
    def __init__(self):
        self.link = ''
        self.image = ''
        self.cooktime = ''
        self.calories = ''
        self.servingsize = ''
        self.carbs = ''
        self.fats = ''
        self.proteines = ''
        self.description = ''
        self.ingridients = list()
        self.directions = ''
        self.id = uuid.uuid4()
        self.listIngredients =list()
        for category in ingredientsDict.values():
            self.listIngredients.extend(category)

    def setLink(self, link):
        self.link = link
    
    def setImage(self, image):
        self.image = image

    def getImage(self):
        return self.image

    def setCooktime(self,cooktime):
        self.cooktime = cooktime
    
    def setCalories(self, calories):
        self.calories = calories
    
    def setServingsize(self,servingsize):
        self.servingsize = servingsize

    def setCarbs(self, carbs):
        self.carbs = carbs
    
    def setFats(self, fats):
        self.fats = fats
    
    def setProteines(self,proteines):
        self.proteines = proteines

    def setDescription(self,description):    
        self.description = description
    
    def setingridients(self,ingridients):
        self.ingridients = ingridients
    
    def setDirections(self, directions):
        self.directions = directions
    
    def GetLink(self):
        return self.link

    def GetDbInsertRequest(self):
        self.description =  self.description.replace("'","''")        
        return f"insert into ingridients_recipes (id, link, cooktime, calories, servingSize, carbs, fats, proteines, description, directions, insertDate, imageLink) values ('{self.id}','{self.link}','{self.cooktime}','{self.calories}','{self.servingsize}','{self.carbs}','{self.fats}','{self.proteines}','{self.description}','{self.directions}',sysdate(),'{self.image}')"
    
    def GetDbInsertIngridientsRequest(self):        
        insertIng = list()
        for ingr in self.ingridients:
            ingr = ingr.replace("'","''")
            id = uuid.uuid4()
            #print(f"insert into ingridients_ingridient (id, ingridient, idRecipes_id) values ('{id}','{self.id}','{ingr}')")
            insertIng.append(f"insert into ingridients_ingridient (id, ingridient, idRecipes_id) values ('{id}','{ingr}','{self.id}')")
        return insertIng

    def GetDbInsertSearchIngridients(self):        
        insertSearchIng = list()
        listIngInserted = list()
        for ingRecip in self.ingridients:
            for ingr in self.listIngredients:
                if (ingr.lower() in ingRecip.lower()) and (ingr.lower() not in listIngInserted):
                    ingr = ingr.replace("'","''")
                    id = uuid.uuid4()
                    listIngInserted.append(ingr.lower())  
                    #print(f"insert into ingridients_searchingridients (id, ingridient, idRecipes_id) values ('{id}','{self.id}','{ingr}')")                  
                    insertSearchIng.append(f"insert into ingridients_searchingridients (id, ingridient, idRecipes_id) values ('{id}','{ingr}','{self.id}')")
        return insertSearchIng