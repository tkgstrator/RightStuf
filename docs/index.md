# 北米版 BD 販売予定リスト

ここは RightStuf で販売または販売が予定されている NIS AMERICA, ANIPLEX OF AMERICA, FUNIMATION, SENTAI FILMWORKS, SHOUT FACTORY の製品の一覧を紹介するページです。

日本の深夜アニメ枠の作品は概ねこの四社からリリースされることが多いですが、まれに別会社からリリースされることもあります。

::: tip 商品リストについて

RightStuf に掲載されていない商品、またはライセンスはされているが製品化の情報がでていない商品については検索することができません。

:::

このページは [@tkgling](https://twitter.com/tkgling)によって運営され、GitHub Actions で毎日自動で更新されています。情報に誤りまたは要望等がありましたらお気軽にご連絡下さい。

## 割引商品一覧

### [Daily Deals](https://www.rightstufanime.com/daily-deals)

毎日更新されている割引商品です。

<table class="table">
    <thead>
        <tr>
            <th v-for="column in columns" :class="column.field" :key="column.title">
                {{ column.title }}
            </th>
        </tr>
    </thead>
    <tbody is="transition-group" name="product-list">
        <tr v-for="product in dailydeals">
            <td class="title"><a :href="'https://www.rightstufanime.com/' + product.ProductId">{{ product.Title }}</a></td>
            <td class="price">${{ product.Price }}</td>
            <td class="release">{{ product.Release }}</td>
            <td class="publisher">{{ product.Publisher }}</td>
        </tr>
    </tbody>
</table>

### [Clearance 3 Day Sale](https://www.rightstufanime.com/sales-and-promos/Three-Day-Sale)

破格な値段で販売されている三日間限定の割引商品です。

<table class="table">
    <thead>
        <tr>
            <th v-for="column in columns" :class="column.field" :key="column.title">
                {{ column.title }}
            </th>
        </tr>
    </thead>
    <tbody is="transition-group" name="product-list">
        <tr v-for="product in clearances">
            <td class="title"><a :href="'https://www.rightstufanime.com/' + product.ProductId">{{ product.Title }}</a></td>
            <td class="price">${{ product.Price }}</td>
            <td class="release">{{ product.Release }}</td>
            <td class="publisher">{{ product.Publisher }}</td>
        </tr>
    </tbody>
</table>

### [Weekly Special](https://www.rightstufanime.com/sales-and-promos/Weekly-Specials)

33%オフで販売されている割引商品です。

<table class="table">
    <thead>
        <tr>
            <th v-for="column in columns" :class="column.field" :key="column.title">
                {{ column.title }}
            </th>
        </tr>
    </thead>
    <tbody is="transition-group" name="product-list">
        <tr v-for="product in weeklyspecials">
            <td class="title"><a :href="'https://www.rightstufanime.com/' + product.ProductId">{{ product.Title }}</a></td>
            <td class="price">${{ product.Price }}</td>
            <td class="release">{{ product.Release }}</td>
            <td class="publisher">{{ product.Publisher }}</td>
        </tr>
    </tbody>
</table>

## 新商品一覧

主に新製品がリストアップされています。

### Pre Order

新規予約が可能な商品一覧です。

<table class="table">
    <thead>
        <tr>
            <th v-for="column in columns" :class="column.field" :key="column.title">
                {{ column.title }}
            </th>
        </tr>
    </thead>
    <tbody is="transition-group" name="product-list">
        <tr v-for="product in preorders">
            <td class="title"><a :href="'https://www.rightstufanime.com/' + product.ProductId">{{ product.Title }}</a></td>
            <td class="price">${{ product.Price }}</td>
            <td class="release">{{ product.Release }}</td>
            <td class="publisher">{{ product.Publisher }}</td>
        </tr>
    </tbody>
</table>

### New Release

最近発売したばかりの商品一覧です。

<table class="table">
    <thead>
        <tr>
            <th v-for="column in columns" :class="column.field" :key="column.title">
                {{ column.title }}
            </th>
        </tr>
    </thead>
    <tbody is="transition-group" name="product-list">
        <tr v-for="product in newreleases">
            <td class="title"><a :href="'https://www.rightstufanime.com/' + product.ProductId">{{ product.Title }}</a></td>
            <td class="price">${{ product.Price }}</td>
            <td class="release">{{ product.Release }}</td>
            <td class="publisher">{{ product.Publisher }}</td>
        </tr>
    </tbody>
</table>

## [全商品一覧](rightstuf.html)

全商品を取得します。{{ itemCounts }} 作品あるので少し重いページになります。

年度別で作品を見たい場合は以下のリンクをご利用ください。

::: warning 年度別リンク

めんどくさいのでまだ実装していません。

:::

### 2022 年販売

### 2021 年販売

### 2020 年販売

### 2019 年販売

### 2018 年販売

### 2017 年販売

### 2016 年販売

<script>
export default {
    // el: "#app",
    data() {
        return {
            columns: [
                {
                    title: "Title",
                    field: "title"
                },
                {
                    title: "Price",
                    field: "price"
                },
                {
                    title: "Release",
                    field: "release"
                },
                {
                    title: "Publisher",
                    field: "publisher"
                }
            ],
            itemCounts: null,
            newreleases: [],
            preorders: [],
            dailydeals: [],
            weeklyspecials: [],
            clearances: [],
            currentTime: new Date().toLocaleDateString()
        }
    },
    mounted() {
        const date = new Date()
        const filePath = `/json/${date.getFullYear()}${(date.getMonth() + 1).toString().padStart(2, "0")}${(date.getDate()).toString().padStart(2, "0")}.json`
        fetch(filePath)
            .then(r => r.json())
            .then(json => {
                const sortedJSON = json.sort((x, y) => new Date(y.Release) - new Date(x.Release))
                this.itemCounts = sortedJSON.length
                this.preorders = sortedJSON.filter(x => x.OrderType === "Pre-order")
                this.newreleases = sortedJSON.filter(x => x.OrderType === "New-Release")
                this.dailydeals = sortedJSON.filter(x => x.Promotion === "Daily-Deals")
                this.weeklyspecials = sortedJSON.filter(x => x.Promotion === "Weekly-Specials")
                this.clearances = sortedJSON.filter(x => x.Promotion === "Three-Day-Sale")
            },
            response => {
                console.log("Error")
            })
    }
}
</script>
