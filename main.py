from bs4 import BeautifulSoup #for scraping
import requests               #required for reading the file
import pandas as pd           #(optional) Pandas for dataframes 
import json                   #(optional) If you want to export json
import os
import re
import traceback
import urllib
import random
from progress.bar import Bar

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def get_content(count,content_soup):
    vidId = []
    content_tr = content_soup.find_all('tr', class_ = "pl-video yt-uix-tile")
    if content_tr:
        with Bar('Processing', max=len(content_tr)) as bar:
            for tr in content_tr:
                time = tr.find('div', class_='timestamp').find('span').text
                time = int(time.split(":")[0])
                if time < 5:
                    vidId.append(tr['data-video-id'])
                bar.next()
    return vidId        
         
reload_val = "/browse_ajax?action_continuation=1&amp;continuation=4qmFsgIqEhpWTFVVZml3ekx5LTh5S3pJYnNtWlR6eERndxoMZWdkUVZEcERUMmRJ&itct=CAAQhGciEwjT6MWyzJvnAhUVemgKHR0_BiGCARoIABCEZyITCPmskabLm-cCFUdBaAodCacNig=="
url = "https://www.youtube.com"
count = 0
iteration = 0    
if __name__ == "__main__":
    while count < 50000 or iteration <10000:
        link = url + reload_val
        try:
            print("getting the value")
            source= json.loads(requests.get(link, proxies=urllib.request.getproxies()).text)
            content_soup=BeautifulSoup(escape_ansi(source["content_html"]),'html.parser')
            tracking_param=BeautifulSoup(escape_ansi(source["tracking_params"]),'html.parser')
            page_soup=BeautifulSoup(escape_ansi(source["load_more_widget_html"]),'html.parser')
            continuation = page_soup.find('button', class_ = "yt-uix-button yt-uix-button-size-default yt-uix-button-default load-more-button yt-uix-load-more browse-items-load-more-button")['data-uix-load-more-href']
            reload_val = str(continuation)+"&itct="+ str(tracking_param)
            vid =  get_content(count,content_soup)
            iteration = iteration+1
            if vid:
                count = count + len(vid)
                with open("videoid/data_{}.json".format(count), "w+") as f:
                    f.write(json.dumps(vid))   
        except:
            traceback.print_exc()
            print("exception in network")
   




