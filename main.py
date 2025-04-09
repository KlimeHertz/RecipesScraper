from extractor import Extractor

Ex = Extractor()
maxpages = 148
for i in range(135,maxpages):
# URL of the web page
    url = 'https://myfridgefood.com/search-by-ingredients?page='+str(i)+""
    print("Extarcting page"+ str(i))
    Ex.Extarct(url)