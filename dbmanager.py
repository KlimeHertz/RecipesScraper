import mysql.connector
from card import Card
import requests



class MysqlDbManager():
    def __init__(self):
        self.columns = str()
        self.columnsName = None
        self.sqlDb = None
        self.cursor = None
        self.card = Card()        

    def connetDb(self):
        self.sqlDb = mysql.connector.connect(host = "localhost", user = "root", password = "Kimimarooto123+-", database="recipedj")
        if (self.sqlDb):
            print("Sql database connected.")
        else:
            print("Error while connecting sql database.")

    def insertInto(self,sqlReq,data) -> bool:
        self.cursor = self.sqlDb.cursor()
        
        if self.cursor:
            #print("Database ready.")
            try :
                self.executeSql(sqlReq,data)
            except:
                self.sqlDb.commit            

    def update(self, objectName, columns : tuple, data : tuple) -> bool:
        return False
    def delete(self, objectName, rowsId : tuple, coloumns : tuple, deleteAll  : bool = False) -> bool:
        return False
    def selectData(self,objectName,colums : tuple = ())-> tuple:
        return ()

    def closeConnexion(self):
        self.sqlDb.close()

    def executeSql(self,sqlRequest, bindValues : tuple = (), isFetch = False) -> tuple:
        if isFetch:
            self.cursor.execute(sqlRequest,bindValues)
            retvals = self.cursor.fetchall()
        else:
            retvals = self.cursor.execute(sqlRequest,bindValues)   

        self.sqlDb.commit()    
        return retvals

    def insertCardIntoDb(self, card : Card) -> bool:
        insertCard = card.GetDbInsertRequest()
        self.insertInto(insertCard,())
        #print(insertCard)

        ListReqOfIng = card.GetDbInsertIngridientsRequest()
        for ingRq in ListReqOfIng:
            #print(ingRq)
            self.insertInto(ingRq,())
        
        ListReqOfSearchIng = card.GetDbInsertSearchIngridients()
        for ingSrchRq in ListReqOfSearchIng:
            #print(ingSrchRq)
            self.insertInto(ingSrchRq,())