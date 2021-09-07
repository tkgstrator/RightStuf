# -*- coding: utf-8 -*-
import csv
import json
from datetime import datetime as dt


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


with open("product.csv", mode="r") as f:
    csvfile = []
    products = []
    for row in csv.DictReader(f):
        csvfile.append(row)
    for product in json.loads(json.dumps(csvfile)):
        products.append(Product(product))
    products = list(filter(lambda x: dt.strptime(x.release, "%Y/%m/%d") > dt.now(), products))
    release = map(lambda x: x.release, products)

    with open("docs/index.md", mode="w") as f:
        f.write(f"# 北米版BD販売予定リスト({dt.strftime(dt.now(), '%Y/%m/%d')})\n\n")
        for date in sorted(set(release), reverse=False):
            f.write(f"## {date}\n\n")
            releaseProducts = filter(lambda x: x.release == date, products)
            for product in releaseProducts:
                f.write(f"### [{product.title}](https://www.rightstufanime.com/{product.productId})\n\n")
                f.write(f"![]({product.productImageURL})\n\n")
                f.write(f"| 製品情報 | 内容 |\n")
                f.write(f"| :------: | :--: |\n")
                f.write(f"| 言語     | {', '.join(product.spokenLanguages)} |\n")
                f.write(f"| 字幕     | {', '.join(product.subtitleLanguages)} |\n")
                f.write(f"| 収録時間 | {product.runtime}mins |\n")
                f.write(f"| 放送年   | {product.created} |\n")
                f.write(f"| 販売元   | {product.publisher} |\n")
                f.write(f"| 価格     | ${product.price} |\n\n")
