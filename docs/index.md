---
sidebar: false
---

<div id="app" class="container">
    <h1>北米版BD販売予定リスト</h1>
    <p>最終更新日時 {{ currentTime }}</p>
    <!-- <table class="table">
        <thead>
            <tr>
                <th v-for="column in columns" :class="column.field" :key="column.title">
                    {{ column.title }}
                </th>
            </tr>
        </thead>
        <tbody is="transition-group" name="product-list">
            <tr v-for="product in products">
                <td class="title"><a :href="'https://www.rightstufanime.com/' + product.ProductId">{{ product.Title }}</a></td>
                <td class="price">${{ product.Price }}</td>
                <td class="release">{{ product.Release }}</td>
                <td class="publisher">{{ product.Publisher }}</td>
            </tr>
        </tbody>
    </table> -->
</div>

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
            products: [],
            currentTime: new Date().toLocaleDateString()
        }
    },
    mounted() {
        const date = new Date()
        const filePath = `/public/json/${date.getFullYear()}${(date.getMonth() + 1).toString().padStart(2, "0")}${(date.getDate() + 1).toString().padStart(2, "0")}.json`
        console.log(filePath)
        fetch(filePath)
            .then(r => r.json())
            .then(json => {
                this.products = json.sort((x, y) => new Date(y.Release) - new Date(x.Release))
            },
            response => {
                console.log("Error")
            })
    }
}
</script>
