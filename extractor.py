
from bs4 import BeautifulSoup
import requests
from card import Card
import re
from dbmanager import *

class Extractor:
    def __init__(self) -> None:
        self.cookies = {
    '_ingredients': '1526.1693.1536.1560.1567.1586.1931.1594.1602.1658.1676.1715.1730.1768.1774.1779.1794.1805.1830.1831.1858.1880.1920.1936.1935.1530.1539.1569.1564.1587.1600.1615.1660.1682.1696.1716.1746.1771.1785.1799.1813.1843.1866.1913.1927.1956.1565.1572.1592.1601.1651.1669.1685.1697.1717.1718.1757.1754.1778.1789.1803.1852.1917.1959'
    , 'IngredientPush' : '0'
    , '_deciderIngredients': ''
}
        self.cards = list()
        self.card = None
        self.manager = MysqlDbManager()
        self.manager.connetDb()
    
    def __requestUrl(self, Url , withcookie=False):
        if withcookie :
            response = requests.get(Url, cookies=self.cookies)
        else :
            response = requests.get(Url)
        
        return response.text
    
    def Extarct(self ,url):
        code  = self.__requestUrl(url,True)
        self.__ExtarctCards(code)

    def __ExtarctCards (self,pagecode):
        soup = BeautifulSoup(pagecode, 'html.parser')
        cards = soup.find_all('div',class_= 'line-item')
        for card in cards :
            self.card = Card()
            self.__ExtractCardContent(card)
            self.manager.insertCardIntoDb(self.card)
            self.cards.append(self.card)

        """for c in self.cards :
            print(c.GetLink())
            self.manager.insertCardIntoDb(c)"""

    def __ExtractCardContent(self,card):
        try :
            #extracting image
            image = card.find("img")
            if 'src' in image.attrs:
                self.card.setImage(image.attrs['src'])
        except:
            pass

        #extracting href
        hrefs = card.find_all("div",class_="line-item-body")
        for href in hrefs :
            link = href.find("a").attrs["href"]
            self.card.setLink('https://myfridgefood.com' + link)
        #extarcting Content inside href
        self.__ExtaractHrefContent('https://myfridgefood.com' + link)
            

    def __ExtaractHrefContent (self,Href):
        hrefCode = self.__requestUrl(Href)
        countCardAttrs = 1
        hrefSoup = BeautifulSoup(hrefCode, 'html.parser')
        receipeStats = hrefSoup.find_all("div",class_="recipe-stats")
        for stats in receipeStats :
            separeStat = stats.find_all("div")
            for stat in separeStat :
                try :
                    if countCardAttrs == 1:                    
                        self.card.setCooktime(float('.'.join(re.findall(r'\d+', stat.get_text())))) 
                    elif countCardAttrs == 2:
                        self.card.setCalories(float('.'.join(re.findall(r'\d+', stat.get_text()))))
                    elif countCardAttrs == 3:
                        self.card.setServingsize(float('.'.join(re.findall(r'\d+', stat.get_text()))))              
                    elif countCardAttrs == 4:
                        self.card.setCarbs(float('.'.join(re.findall(r'\d+', stat.get_text()))))
                    elif countCardAttrs == 5:
                        self.card.setFats(float('.'.join(re.findall(r'\d+', stat.get_text()))))
                    elif countCardAttrs == 6:
                        self.card.setProteines(float('.'.join(re.findall(r'\d+', stat.get_text()))))
                except:
                    print("Error while extracting recipe stats")                    
                countCardAttrs = countCardAttrs + 1

        self.card.setLink(Href)
        hrefSections = hrefSoup.find_all("div",class_ = "recipe-text")

        #extaract descr
        try:
            descr = hrefSoup.find('h3', text='description').get_text()
        except:
            descr="no descr"

        #extaract ingredients
        ingredientsHead = hrefSoup.find('h3', text='ingredients')
        listIngredients = list()       
        
        try:  
            ingredientslist = ingredientsHead.find_next('ul')
            ingridients = ingredientslist.find_all("li")
            for ingrident in ingridients:
                if ingridient.get_text().strip() != "":
                    listIngredients.append(ingrident.get_text().strip())
        except:
            try:
                ingredientslist = ingredientsHead.find_next('ol')
                if len(ingredientslist) > 0 :
                    ingridients = ingredientslist.find_all("li")
                    for ingrident in ingridients:
                        if ingridient.get_text().strip() != "":
                            listIngredients.append(ingrident.get_text().strip())
            except:
                parentDiv = ingredientsHead.find_parent('div')
                ingredients = parentDiv.get_text(separator='\n').strip().split('\n')[1:]
                for ingridient in ingredients:
                    if ingridient.strip() != "":
                        listIngredients.append(ingridient.strip())

        self.card.setingridients(listIngredients)

        #extaract directions
        try:
            directionsHead = hrefSoup.find('h3', text='directions')
            directionList = directionsHead.find_parent('div')
            directions_text = directionList.get_text(separator='\n').strip().replace('\n', ' ')
            self.card.setDirections(directions_text)
        except:
            pass
            