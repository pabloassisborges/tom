from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests, lxml
import csv
from random import randint
from time import sleep

app = Flask(__name__)

headers = {
  "User-Agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

query = []
header = ['Search Phrase', 'URL', 'Headline', 'Destiny_URL']
d = []

@app.before_request
def clear_trailing():
    from flask import redirect, request
    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

@app.errorhandler(404)
def route_not_found(e):
    return "The resource could not be found.", 404

@app.route('/', methods=['GET'])
def home():
    return "Google Search API. The server is up!", 200

@app.route('/csv', methods=['GET'])
def index():

    with open('c.txt', encoding='utf-8') as f:
        for line in f:
            query.append(line)
    
    with open('tom.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    for q in query:
        #print(str(q))
        sleep(randint(1,3))
        html = requests.get('https://www.google.com/search?q='+q, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        print(str(soup))
        for ads in soup.select('.uEierd'):
            print("this one have ads")
            title = ads.select_one('.v0nnCb').text
            if ads.select_one('.WZ8Tjf span'):
                phone = ads.select_one('.WZ8Tjf span').text
            else:
                phone = None
            link = ads.select_one('.Krnil')['href']
            displayed_link = ads.select_one('.abuKkc .qzEoUe').text
            tracking_link = ads.select_one('.Krnil')['data-rw']
            #snippet = ads.select_one('.uUPGi div:nth-child(3) .lyLwlc').text

            if ads.select_one('.aLF0Z'):
                inline_ads = ads.select_one('.aLF0Z').text.replace(" · ", "\n")
                inline_ads_link = ads.select_one('.aLF0Z a')['href']
            else:
                inline_ads = None
                inline_ads_link = None

            print(f'{title}\n')
            d = [q, displayed_link, title, link]

            with open('tom.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(d)

    return "done",200

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")