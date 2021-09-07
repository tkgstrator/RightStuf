import os
import re
import sys
import csv
import json
import requests
import urllib3
import datetime
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


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
        "custitem_rs_publisher": "NIS-AMERICA,ANIPLEX-OF-AMERICA,FUNIMATION,SENTAI-FILMWORKS",
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
    with open("product.csv", mode="w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Title", "ProductId", "Release", "Price", "In stock", "Publisher", "Created", "Runtime", "Spoken Languages", "SubTitle Languages", "ImageURL"])
        res = getProductsData(0, 0)
        if res.status_code == 200:
            size = int(json.loads(res.text)["total"] / 100) + 1
            for offset in range(0, size):
                res = getProductsData(100, offset*100)
                items = json.loads(res.text)["items"]
                for item in items:
                    name = item["displayname"]
                    productId = item["urlcomponent"]
                    date = datetime.datetime.strptime(item["custitem_rs_release_date"], "%m/%d/%Y").strftime("%Y/%m/%d")
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
                    # print("Getting " + name + " information.")
                    w.writerow([name, productId, date, price, stock, publisher, created, runtime, spokenLanguages, subtitleLanguages, primaryImageURL])

                # image = json.dumps(item["itemimages_detail"])
                # count = re.findall(r"https://.[^}]*primary.jpg", image)
                # for iURL in count:
                #     saveProductImage(iURL, "weekly")
