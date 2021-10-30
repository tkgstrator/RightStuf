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
    promotion = None
    orderType = None

    def __init__(self, item, promotion=None, orderType=None):
        # 必須情報
        self.title = item["displayname"]
        self.productId = item["urlcomponent"]
        self.release = dt.strptime(item["custitem_rs_release_date"], "%m/%d/%Y").strftime("%Y-%m-%d")
        self.spokenLanguages = [x.replace("'", "").strip() for x in item["custitem_rs_spoken_language"].split(",")]
        self.subtitleLanguages = [x.replace("'", "").strip() for x in item["custitem_rs_subtitle_language"].split(",")]
        self.publisher = item["custitem_rs_publisher"]
        self.price = item["onlinecustomerprice_detail"]["onlinecustomerprice"]
        self.stock = item["isinstock"]
        # プロモーションなどの区分
        self.promotion = promotion
        self.orderType = orderType
        # ないかも知れない情報
        primaryImageURLs = re.findall(r"https://.[^}]*primary.jpg", json.dumps(item["itemimages_detail"]))
        if len(primaryImageURLs) > 0:
            self.productImageURL = primaryImageURLs[0]
        else:
            pass
        try:
            self.created = item["custitem_rs_year_created"]
        except KeyError:
            pass
        try:
            self.runtime = item["custitem_rs_run_time"]
        except KeyError:
            pass


def getProductsData(limit, offset, promotion=None, orderType=None):
    url = "https://www.rightstufanime.com/api/items"
    params = {
        "c": "546372",
        "country": "US",
        "currency": "USD",
        "custitem_rs_specials_and_promos": promotion,
        "custitem_rs_new_releases_preorders": orderType,
        "custitem_rs_web_class": "Blu-ray",
        "language": "en",
        "fieldset": "details",
        "custitem_rs_publisher": "NIS-AMERICA,ANIPLEX-OF-AMERICA,FUNIMATION,SENTAI-FILMWORKS,SHOUT-FACTORY",
        "limit": limit,
        "offset": offset
    }
    return(requests.get(url, params=params, verify=False))


def getAllProductsData():
    # プロモーションの種類で分ける
    parameters = [
        {
            "promotion": None,
            "orderType": None
        },
        {
            "promotion": "Three-Day-Sale",
            "orderType": None
        },
        {
            "promotion": "Weekly-Specials",
            "orderType": None
        },
        {
            "promotion": "Daily-Deals",
            "orderType": None
        },
        {
            "promotion": None,
            "orderType": "New-Release"
        },
        {
            "promotion": None,
            "orderType": "Pre-order"
        }
    ]
    # プロモーションの種類でループ
    items = []
    for parameter in parameters:
        promotion = parameter["promotion"]
        orderType = parameter["orderType"]
        # 総数を取得
        res = getProductsData(0, 0, promotion, orderType)
        if res.status_code == 200:
            try:
                size = int(json.loads(res.text)["total"] / 100) + 1
                for offset in range(0, size):
                    res = getProductsData(100, offset*100, promotion, orderType)
                    # 商品一覧を取得
                    items.extend(map(lambda x: Product(x, promotion, orderType), json.loads(res.text)["items"]))
            except KeyError:
                print("KeyError")
    return items


def saveProductImage(iURL, saveDir):
    res = requests.get(iURL, verify=False)
    if res.status_code == 200:
        file = os.path.basename(iURL)
        path = os.path.dirname(os.path.abspath(
            sys.argv[0])) + "/" + saveDir + "/" + file
        path = path.replace("/", os.sep)
        with open(path, mode="wb") as im:
            im.write(res.content)


def saveCSV(fileName):
    headers = [
        "Title", "ProductId", "Release", "Price", "In stock", "Publisher",
        "Created", "Runtime", "Spoken Languages", "SubTitle Languages", "ImageURL",
        "Promotion", "OrderType"
    ]
    with open(f"{fileName}.csv", mode="w") as f:
        # CSVWriterの設定
        w = csv.writer(f)
        w.writerow(headers)
        items: [Product] = getAllProductsData()
        for item in items:
            w.writerow([item.title, item.productId, item.release, item.price, item.stock, item.publisher, item.created, item.runtime,
                       item.spokenLanguages, item.subtitleLanguages, item.productImageURL, item.promotion, item.orderType])


if __name__ == "__main__":

    # 日付からCSVファイルの名前を決める
    fileName = dt.strftime(dt.utcnow(), "%Y%m%d")
    print("Output FileName:", fileName)
    # CSVファイルを保存
    saveCSV(fileName)
    # CSVをJSONとして保存
    with open(f"{fileName}.csv", mode="r") as f:
        csvfile = []
        for row in csv.DictReader(f):
            csvfile.append(row)
        # JSON書き込み
        with open(f"json/{fileName}.json", mode="w") as w:
            json.dump(csvfile, w, indent=4, sort_keys=True)
