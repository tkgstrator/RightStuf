import fs from 'fs';

import axios from 'axios';
import { plainToInstance } from 'class-transformer';
import dayjs from 'dayjs';

import { Item, ItemRequest } from './dto/right.dto';

enum Promotion {
    ThreeDaySale = 'Three-Day-Sale',
    WeeklySpecials = 'Weekly-Specials',
    DailyDeals = 'Daily-Deals',
}

enum OrderType {
    NewRelease = 'New-Release',
    PreOrder = 'Pre-order',
}

export class Client {
    async get_all_products(promotion: Promotion | null, order_type: OrderType | null): Promise<Item[]> {
        const { items, total } = await this.get_products(promotion, order_type, 100, 0);
        if (total <= 100) {
            return items;
        }
        const results: ItemRequest[] = await Promise.all(
            Array.from(Array(Math.ceil((total - 100) / 100)).keys()).map((index: number) =>
                this.get_products(promotion, order_type, 100, index * 100 + 100),
            ),
        );
        return items.concat(results.flatMap((result: ItemRequest) => result.items));
    }

    private async get_products(
        promotion: Promotion | null,
        order_type: OrderType | null,
        limit: number,
        offset: number,
    ): Promise<ItemRequest> {
        const base_url = new URL('https://www.rightstufanime.com/api/items');
        const params: URLSearchParams = new URLSearchParams({
            country: 'US',
            currency: 'USD',
            custitem_rs_web_class: 'Blu-ray',
            fieldset: 'details',
            language: 'en',
            limit: limit.toString(),
            offset: offset.toString(),
        });
        if (promotion !== null) {
            base_url.searchParams.set('custitem_rs_specials_and_promos', promotion.toString());
        }
        if (order_type !== null) {
            base_url.searchParams.set('custitem_rs_new_releases_preorders', order_type.toString());
        }
        params.forEach((value, key) => {
            base_url.searchParams.set(key, value);
        });
        return plainToInstance(ItemRequest, (await axios.get(base_url.href)).data, {
            excludeExtraneousValues: true,
            exposeUnsetFields: true,
        });
    }
}

const client: Client = new Client();
const requests = [
    {
        name: "sales",
        requests:
            [
                { order_type: null, promotion: Promotion.ThreeDaySale },
                { order_type: null, promotion: Promotion.WeeklySpecials },
                { order_type: null, promotion: Promotion.DailyDeals },
            ]
    },
    {
        name: "new-release",
        requests:
            [
                { order_type: OrderType.NewRelease, promotion: null },
            ]
    },
    {
        name: "pre-order",
        requests:
            [
                { order_type: OrderType.PreOrder, promotion: null },
            ]
    },
    {
        name: "products",
        requests:
            [
                { order_type: null, promotion: null },
            ]
    },
];

const current_date: string = dayjs().format('YYYYMMDD');
fs.mkdirSync(`src/assets/${current_date}`, { recursive: true });
requests.forEach(async (request) => {
    const items: Item[] = (await Promise.all(request.requests.map((request) => client.get_all_products(request.promotion, request.order_type))))
        .flat()
        .sort((a, b) => dayjs(b.release_date).unix() - dayjs(a.release_date).unix())
    console.log(request.name, items.length)
    fs.writeFileSync(`src/assets/${current_date}/${request.name}.json`, JSON.stringify(items, null, 2));
});
