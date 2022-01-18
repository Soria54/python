from array import array
from xml.etree.ElementInclude import include
from flask import Flask
from flask import render_template
from MySQLdb import _mysql
from bs4 import BeautifulSoup

import controllers.hello as hello
import requests
import cloudscraper
import time
import numpy as np



app = Flask("projetWebToon")

db=_mysql.connect("127.0.0.1","root",  "root","python")
@app.route("/")
def index():

    scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    })
    cookies = {
        'PHPSESSID': 'o4n4anhjrdhdqtlnp1gmidakgv',
        'REMEMBERME': 'QXBwXEVudGl0eVxVc2VyOlFXbHliM009OjE2NzQwMzU2NDY6YzgzM2Y4MzZkMmI1YTY0YWRkNDJjMzA3MGZjMTZhMzUwNjU2MzU4OTI0OWMxYTcyYjA0YmY1ZjZhOGZiZGRmMg%3D%3D'
    }
    testString = ""
    arrayWebToon = []
    stop = False
    i = 1 
    while stop != True:
        time.sleep(1.5)
        japanread = scraper.get("https://www.japanread.cc/notifications?page="+str(i), cookies=cookies).content
        i = i + 1
        soupJapanRead = BeautifulSoup(japanread)

        table = soupJapanRead.find(id='notif-table')

        #and id(table.text.split(' ')) != id("Vous n'avez pas de notification.".split(' '))
        if len(table.text.split(' ')) != 5 :
            testString += table.text
            #arrayWebToon.append(table.find_all('a'))
            arrayWebToon = np.concatenate((arrayWebToon, table.find_all('a')), axis=None)
            #print(table.find_all('a'))
        else:
            stop = True

    #print(japanread)
    #print(arrayWebToon)
    #print(stop)
    #cookie_value, user_agent = cloudscraper.get_cookie_string('https://www.japanread.cc/')

    #print('GET / HTTP/1.1\nCookie: {}\nUser-Agent: {}\n'.format(cookie_value, user_agent))  

    #url = 'https://www.japanread.cc/'
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    #response = requests.get(url, headers=headers)
    #print(response.content)
    newArrayWebToon = []
    #index = 0
    for WebToon in arrayWebToon:
        textChapitre = str(WebToon).split(' - ')
        tempoArray = str(textChapitre[1]).split(' ')
        #print(tempoArray[2])
        #str(tempoArray[1])
        
        #test = np.concatenate((str(WebToon).split(' - ')[0], tempoArray[2]), axis=None)
        #print(test)

        newArrayWebToon.append(np.concatenate((str(WebToon).split(' - ')[0], tempoArray[2]), axis=None))
        #arrayWebToon[index] = str(WebToon).split('-')
        #index = index + 1
    #print(newArrayWebToon)

    arrayTitre = []
    for WebToon in newArrayWebToon:
        if WebToon[0] not in arrayTitre:
            arrayTitre.append(WebToon[0])
    #print(arrayTitre)

    newNewarrayWebToon = []
    for titre in arrayTitre:
        arrayChapitres = []
        for WebToon in newArrayWebToon:
            if titre == WebToon[0]:
                arrayChapitres.append(WebToon[1])
        newNewarrayWebToon.append( [titre, arrayChapitres])
    #print (newNewarrayWebToon)

    for WebToon in newNewarrayWebToon :
        db.query('INSERT INTO `python`.`webToon` (`nom`) VALUES ("' + str(WebToon[0]) + '")')
        print("ici")
        idWebToon = db.insert_id()
        for chapitre in WebToon[1]:
            db.query("INSERT INTO `python`.`chapitre` (`numero`, `id_webToon`) VALUES ('" + str(chapitre) + "', '"+ str(idWebToon) +"')")
    
    #print(db.store_result().fetch_row())

    return  render_template('home.html', newNewarrayWebToon=newNewarrayWebToon)





@app.route("/hello/")
@app.route("/hello/<name>")
def function(name=None):
    return hello.hello(name)


