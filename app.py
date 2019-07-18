from flask import Flask
from bs4 import BeautifulSoup
import requests
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
    img_name_filter=[
        ["/digits/42676c5e4de751dac38d2ca66e5fc04c.png", "0"],
        ["/digits/a340f607cd31805c33804c68a49a2132.png", "1"],
        ["/digits/aedbf92de88685fc9c65b05805afe072.png", "2"],         
        ["/digits/095a265f47b7984233276a07d45ba4b7.png", "3"],
        ["/digits/7e07524d29908dbb7755a829e90e6cbd.png", "4"],
        ["/digits/e236e29a9df241f931d0634688bc6841.png", "5"],
        ["/digits/b759e0bb9fc7efb52de84758b8533354.png", "6"],
        ["/digits/adbfb8a239250963192ff13c1dfbc563.png", "7"],
        ["/digits/e0288fb443cf533ca706213b4437c21c.png", "8"],
        ["/digits/bced19340a9edc1a3b2aaa00c3cd40b8.png", "9"],
        ["/digits/13e544f95e9be31f4db121d189439a69.png", "."]
    ] 
            
    print ("\n\n")
    img_list = ""
    for index1, i in enumerate(card_row) :
        # print('length of images: ')
        # print(len(i.find_all('img')))
        
        img_list += "<div id=" + str(index1)+ ">"
        for j in i.find_all('img'):
            # print(j)
            # print ("hi")
            # img_list += '<span>'
            for k in img_name_filter:
                if j["src"] == k[0] :
                    img_list += k[1]
            # img_list += '</span>'
            # new_img = soup.new_tag('img',src=urljoin(url,j["src"]))
            # img_list += str(new_img)
            # print (card_row)
        img_list += "</div>"
    return str(img_list)
# setup Flask App and define routes

app = Flask(__name__)
imgs = scrape()
@app.route('/')
def index():
    return imgs
