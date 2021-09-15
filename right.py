import os
import re
from statistics import mode
import sys
import csv
import json
import requests
import urllib3
from datetime import datetime as dt
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


class Product():
    title = None
    productId = None
    price = None
    release = None
    spokenLanguages = None
    subtitleLanguages = None
    productImageURL = None
    publisher = None
    created = None
    runtime = None

    def __init__(self, json):
        self.title = json["Title"]
        self.productId = json["ProductId"]
        self.release = json["Release"]
        self.price = json["Price"]
        self.stock = json["In stock"]
        self.spokenLanguages = [x.replace("'", "").replace("[", "").replace("]", "").strip() for x in json["Spoken Languages"].split(",")]
        self.subtitleLanguages = [x.replace("'", "").replace("[", "").replace("]", "").strip() for x in json["SubTitle Languages"].split(",")]
        self.productImageURL = json["ImageURL"]
        self.publisher = json["Publisher"]
        self.created = json["Created"]
        self.runtime = json["Runtime"]


def getProductsData(limit, offset):
    url = "https://www.rightstufanime.com/api/items"
    params = {
        "c": "546372",
        "country": "US",
        "currency": "USD",
        # "custitem_rs_spoken_language": "English",
        # "custitem_rs_specials_and_promos" : "Weekly-Specials",
        "custitem_rs_web_class": "Blu-ray",
        "language": "en",
        "fieldset": "details",
        "custitem_rs_publisher": "NIS-AMERICA,ANIPLEX-OF-AMERICA,FUNIMATION,SENTAI-FILMWORKS,SHOUT-FACTORY",
        "limit": limit,
        "offset": offset
    }
    return(requests.get(url, params=params, verify=False))


def saveProductImage(iURL, saveDir):
    res = requests.get(iURL, verify=False)
    if res.status_code == 200:
        file = os.path.basename(iURL)
        path = os.path.dirname(os.path.abspath(
            sys.argv[0])) + "/" + saveDir + "/" + file
        path = path.replace("/", os.sep)
        with open(path, mode="wb") as im:
            im.write(res.content)


if __name__ == "__main__":
    # CSVとして保存
    with open("product.csv", mode="w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Title", "ProductId", "Release", "Price", "In stock", "Publisher",
                   "Created", "Runtime", "Spoken Languages", "SubTitle Languages", "ImageURL"])
        res = getProductsData(0, 0)
        if res.status_code == 200:
            size = int(json.loads(res.text)["total"] / 100) + 1
            for offset in range(0, size):
                res = getProductsData(100, offset*100)
                items = json.loads(res.text)["items"]
                for item in items:
                    name = item["displayname"]
                    productId = item["urlcomponent"]
                    date = dt.strptime(item["custitem_rs_release_date"], "%m/%d/%Y").strftime("%Y/%m/%d")
                    spokenLanguages = [x.replace("'", "").strip() for x in item["custitem_rs_spoken_language"].split(",")]
                    subtitleLanguages = [x.replace("'", "").strip() for x in item["custitem_rs_subtitle_language"].split(",")]
                    publisher = item["custitem_rs_publisher"]
                    try:
                        created = item["custitem_rs_year_created"]
                    except KeyError:
                        created = ""
                    try:
                        runtime = item["custitem_rs_run_time"]
                    except KeyError:
                        runtime = ""
                    price = item["onlinecustomerprice_detail"]["onlinecustomerprice"]
                    stock = item["isinstock"]

                    primaryImageURLs = re.findall(r"https://.[^}]*primary.jpg", json.dumps(item["itemimages_detail"]))
                    if len(primaryImageURLs) > 0:
                        primaryImageURL = primaryImageURLs[0]
                    else:
                        primaryImageURL = ""
                    w.writerow([name, productId, date, price, stock, publisher, created,
                               runtime, spokenLanguages, subtitleLanguages, primaryImageURL])

    # CSVをJSONとして保存
    with open("product.csv", mode="r") as f:
        csvfile = []
        for row in csv.DictReader(f):
            csvfile.append(row)
        # JSON書き込み
        with open(dt.strftime(dt.now(), "json/%Y%m%d%H%M.json"), mode="w") as w:
            json.dump(csvfile, w, indent=4, sort_keys=True)
