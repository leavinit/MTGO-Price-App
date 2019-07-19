from flask import Flask, render_template, request, Markup
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys   # For keyboard keys 
import time                                       # Waiting function  
from urllib.parse import urljoin
from forms import CardForm
from mtgsdk import Card



# fetch page with selenium and scrape it w/ BeautifulSoup4
def scrape(card):
    # url = "https://www.mtgowikiprice.com/card/ISD/78/Snapcaster_Mage"
    # card = "Snapcaster Mage"
    url = "https://www.mtgowikiprice.com/"

    options = Options()
    options.headless = True
    prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('detach', True)
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--incognito")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    search = driver.find_elements_by_id('_cardskeyword_home')[0]
    # print(search)
    time.sleep(1)
    search.send_keys(card)
    time.sleep(1.0)
    search.send_keys(Keys.ENTER) 
    time.sleep(1.0)
    html = driver.page_source
    # driver.quit()
    # print (html)
    soup = BeautifulSoup(html, features="html.parser")

    card_sell_row = soup.find_all("td",class_="sell_price_round") #Collects rows of sell information
    card_buy_row = soup.find_all("td",class_="buy_price_round") #Collects row of buy information
    # imgs = card_buy_row.find_all("img")
    if (card_sell_row and card_buy_row):
        print ("--Buy and Sell prices loaded with success--")
    
    # print (card_buy_row)
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
            
    # print ("\n\n")
    buy_list = "<div id='buyList'>"
    for index1, i in enumerate(card_buy_row) :
        buy_list += "<div class='buy_prices' id=" + str(index1)+ ">"
        for j in i.find_all('img'):
            for k in img_name_filter:
                if j["src"] == k[0] :
                    buy_list += k[1]
        buy_list += "</div>"
    buy_list += "</div>"

    sell_list = "<div id='sellList'>"
    for index2, i2 in enumerate(card_sell_row) :
        sell_list += "<div class='sell_prices' id=" + str(index2)+ ">"
        for j2 in i2.find_all('img'):
            for k2 in img_name_filter:
                if j2["src"] == k2[0] :
                    sell_list += k2[1]
        sell_list += "</div>"
    sell_list += "</div>"

    return (buy_list, sell_list)


# setup Flask 'App and define routes

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'you-will-never-guess'

# imgs = scrape(card="Wasteland Strangler")
# imgs = "randomImages here"
# print (Markup(imgs))
# if imgs:
    # print ("---imgs loaded--")
@app.route('/',methods=["GET","POST"])
def index():
    form = CardForm()
    if request.method == "GET":
        return render_template('/cardForm.html', form=form)
    if request.method == "POST":
        card = request.form.get('card_name')  #gets card entered on form
        card_image_url = Card.where(name=card).all()[0].image_url #gets card image from scryfall via api

        buy_prices, sell_prices = scrape(card=card) #scrape returns two lists of prices
        
        return render_template('/index.html', buy_prices=buy_prices, sell_prices=sell_prices, card_name=card, card_image_url=card_image_url)
