import os
import bs4
import requests
import numpy as np
import pandas as pd
import re
import urllib.request, json


titles = []
dates = []
price = []
location = []
links = []
dataset = []


def get_links(url, save_path='./downloaded'):
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    soup = bs4.BeautifulSoup(open('./.html'))
    for each_a in soup.findAll('a'):
        if ".html" in each_a.text:
            links.append(each_a.text)


def get_data():
    for page in links:
        r = requests.get('http://138.68.86.32/' + page)
        soup = bs4.BeautifulSoup(r.content)

        for each_div in soup.findAll("table", {"class": "printbredde"}):

            for each_h3 in each_div.findAll("h3"):
                data = []
                for each_b in each_h3.findAll("b"):
                    # titles.append(each_b.text)
                    data.append(each_b.text)
                    # print(each_b.text)
                    spans = []

                for each_span in (each_h3.previousSibling.previous).findAll("span"):
                    spans.append(each_span.text)
                # dates.append(spans[0])
                # location.append(spans[1])
                if "DKK" or "free" not in spans[0]:
                    data.append(spans[0] + "(nan)")
                else:
                    data.append(spans[0])
                data.append(spans[1])
                # print(data)
                dataset.append(data)
            print(np.array(dataset))
            df = pd.DataFrame(np.array(dataset))
            df.to_csv("scraped_events.csv", sep=',')

def load_correct_csv():
    df = pd.read_csv('scraped_events_correct.csv')

    df['How_Much'] = get_price(str(df['How_Much']))
    df['coordinates'] = geo_loc(str(df)['where'])
    print(df)

def get_price(price_str):
    price_regexp = r"(?P<price>\d+)"
    if 'Free admission' in price_str:
        price = 0
    elif 'ratis' in price_str:
        price = 0
    else:
        m = re.search(price_regexp, price_str)
        try:
            price = int(m.group('price'))
        except:
            price = None
    return price

def geo_loc(input_string):
    with urllib.request.urlopen("http://138.68.86.32/locs2.json") as url:
        data = json.loads(url.read().decode())
    locs = json.loads(data)[0]
    lat, lon = locs.get(input_string)
    print(data)
    return lat, lon;

def run():
    file_url = 'http://138.68.86.32/'
    txt_file_name = os.path.basename(file_url)
    txt_path = os.path.join('./', txt_file_name)
    txt_path = txt_path + '.html'
    get_links(file_url, txt_path)
    get_data()
    load_correct_csv()
    print('done')


if __name__ == '__main__':
    run()
