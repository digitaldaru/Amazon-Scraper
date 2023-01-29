from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST']) # To render Homepage
def home_page():
    return render_template('index.html')

@app.route('/scrap', methods=['POST'])  # This will be called from UI
def scrap():
    if (request.method=='POST'):
        search= request.form['search-input']

        USER_AGETS = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        ]

        USER_AGENT = random.choice(USER_AGETS)

        HEADERS = {
                "User-Agent": USER_AGENT
            }
        search = search.replace(" ","+")
        url = f"https://www.amazon.in/s?k={search}"
        resp = requests.get(url, headers=HEADERS)
        content = BeautifulSoup(resp.content, 'lxml') 

        item_details = []  

        for item in content.select('.s-result-item.s-asin.sg-col-0-of-12'):         
            #r = requests.get(url="https://www.amazon.in/" + item.select_one("a.a-link-normal")["href"], headers=HEADERS)
            #b = BeautifulSoup(r.content, 'lxml') 
            try:
                Price = int(item.select_one("span.a-price-whole").text.replace(",",""))
            except:
                Price = item.select_one("span.a-price-whole")

               # try:
               #     Discount = b.select_one("span.a-size-large.a-color-price.savingPriceOverride").text
               # except:
               #     Discount = b.select_one("span.a-size-large.a-color-price.savingPriceOverride")

            try:
                Rating = item.select_one("span.a-size-base").text.replace("(","").replace(")","")
            except:
                Rating = item.select_one("span.a-size-base")

            try:
                No_of_People_Rate = item.select_one("span.a-size-base.s-underline-text").text.replace("(","").replace(")","")
            except:
                No_of_People_Rate = item.select_one("span.a-size-base.s-underline-text")
            data = {
               "Name": item.select_one("span.a-size-medium.a-color-base.a-text-normal").text.strip(),
               "Price (Rs)": Price,
                    #"Discount": Discount,
               "Rating": Rating,
               "People Rate": No_of_People_Rate,
               #"Product Image": item.select_one("img.s-image")["src"],
               #"Product Link": "https://www.amazon.in/" + item.select_one("a.a-link-normal")["href"],
                }
            item_details.append(data)
        df = pd.DataFrame(item_details)
        return render_template('results.html',tables=[df.to_html(classes='data')], titles=df.columns.values)


if __name__ == '__main__':
    app.run(debug=True)
