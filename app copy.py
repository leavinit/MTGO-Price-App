from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from urllib.parse import urljoin

# fetch page with requests and scrape it w/ BeautifulSoup4
def scrape():
    url = "https://www.mtgowikiprice.com/card/ISD/78/Snapcaster_Mage"

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    html = driver.page_source
    driver.quit()
    # print (html)
    soup = BeautifulSoup(html)

    card_row = soup.find_all("td",class_="sell_price_round") #Collects rows of sell information 
    # imgs = card_row.find_all("img")
    # print ("Card row:")
    
    # print (card_row)
    print ("\n\n")
    img_list = ""
    for index, i in enumerate(card_row) :
        # print('length of images: ')
        # print(len(i.find_all('img')))
        img_list += "<div id=" + str(index)+ ">"
        for j in i.find_all('img'):
            print(j)
            print ("hi")
            new_img = soup.new_tag('img',src=urljoin(url,j["src"]))
            img_list += str(new_img)
            # print (card_row)
        img_list += "</div>"
    return str(img_list)

# setup Flask App and define routes

# app = Flask(__name__)
imgs = scrape()
print(imgs)
# @app.route('/')
# def index():
# return imgs
