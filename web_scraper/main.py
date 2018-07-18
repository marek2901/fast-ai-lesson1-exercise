import requests
import re
import json
import pprint
import time
import pathlib
import urllib

def search(keywords):
    url = 'https://duckduckgo.com/'
    params = { 'q': keywords }

    ## MAKE PATH for incoming images
    pathlib.Path(f"./scrap_data/{keywords}/").mkdir(parents=True, exist_ok=True)
    ##

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=(\d+)\&', res.text, re.M|re.I)

    headers = {
    'dnt': '1',
    'accept-encoding': 'gzip, deflate, sdch, br',
    'x-requested-with': 'XMLHttpRequest',
    'accept-language': 'en-GB,en-USq=0.8,enq=0.6,msq=0.4',
    'user-agent': 'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'accept': 'application/json, text/javascript, */* q=0.01',
    'referer': 'https://duckduckgo.com/',
    'authority': 'duckduckgo.com',
    }

    params = (
    ('l', 'wt-wt'),
    ('o', 'json'),
    ('q', keywords),
    ('vqd', searchObj.group(1)),
    ('f', ',,,'),
    ('p', '2')
    )

    requestUrl = url + "i.js"

    while True:
        res = requests.get(requestUrl, headers=headers, params=params)
        data = json.loads(res.text)
        # printJson(data["results"])
        downloadImages(data["results"], keywords)
        if "next" not in data:
            break
        requestUrl = url + data["next"]
        time.sleep(5)

def downloadImages(objs, dir_name):
    for obj in objs:
        try:
            url = obj["image"]
            filename = re.findall(r"[^\/]*",url)[-2]
            urllib.request.urlretrieve(url, f"./scrap_data/{dir_name}/{filename}")
            print(f"retreived {filename}")
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print('Retriving image error')
            next


def printJson(objs):
    for obj in objs:
        print("Width {0}, Height {1}".format(obj["width"], obj["height"]))
        print("Thumbnail {0}".format(obj["thumbnail"]))
        print("Url {0}".format(obj["url"]))
        print("Title {0}".format(obj["title"].encode('utf-8')))
        print("Image {0}".format(obj["image"]))
        print("__________")

def main():
    search('US Dollar')
    # search('PLN nowe banknoty') ## ZAJEBISTY Keyword
    # search('banknot złoty polski')


if __name__ == '__main__':
    main()
