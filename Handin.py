import os
import bs4
import requests
import csv
import numpy as np
import pandas as pd

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


def run():
    file_url = 'http://138.68.86.32/'
    txt_file_name = os.path.basename(file_url)
    txt_path = os.path.join('./', txt_file_name)
    txt_path = txt_path + '.html'
    get_links(file_url, txt_path)
    get_data()
    print('done')


if __name__ == '__main__':
    run()
