import { Expose, Transform, Type } from 'class-transformer';
import dayjs from 'dayjs';
import flat from 'flat';
import 'reflect-metadata';

enum Language {
    English = 'English',
    Japanese = 'Japanese',
}

export class Item {
    @Expose({ name: 'custitem_rs_spoken_language' })
    @Transform((param) =>
        param.value === undefined ? [] : (param.value as string).split(',').map((language: string) => language.trim() as Language),
    )
    spoken_language: Language[];

    @Expose({ name: 'custitem_rs_subtitle_language' })
    @Transform((param) =>
        param.value === undefined ? [] : (param.value as string).split(',').map((language: string) => language.trim() as Language),
    )
    subtitle_language: Language[];

    @Expose({ name: 'isinstock' })
    in_stock: boolean;

    @Expose()
    internalid: number;

    @Expose({ name: 'custitem_rs_release_date' })
    @Transform((param) => dayjs(param.value as string).toDate())
    release_date: Date;

    @Expose()
    @Transform((param) => parseInt(param.value as string, 10))
    itemid: number;

    @Expose({ name: 'custitem_rs_year_created' })
    @Transform((param) => (param.value === undefined ? null : parseInt(param.value as string, 10)))
    year_created: number | null;

    @Expose({ name: 'custitem_rs_pre_book_date' })
    @Transform((param) => dayjs(param.value as string).toDate())
    pre_book_date: Date;

    @Expose()
    displayname: string;

    @Expose({ name: 'ispurchasable' })
    is_purchasable: boolean;

    @Expose({ name: 'custitem_rs_adult' })
    is_adult: boolean;

    @Expose({ name: 'custitem_rs_availabe_for_purchase' })
    availabe_for_purchase: boolean;

    @Expose()
    @Transform((param) =>
        [param.obj['pricelevel1'], param.obj['pricelevel2'], param.obj['pricelevel3'], param.obj['pricelevel5']].map((value: string) =>
            parseFloat(value),
        ),
    )
    prices: number[];

    @Expose()
    @Transform((param) => param.obj['onlinecustomerprice_detail']['onlinecustomerprice'])
    online_price: number;

    @Expose({ name: 'custitem_rs_run_time' })
    run_time: number;

    @Expose({ name: 'custitem_rs_publisher' })
    publisher: string;

    @Expose({ name: 'itemimages_detail' })
    @Transform((param) => Object.values(flat(param.value) as object).filter((value: string) => value !== ''))
    image_urls: string[];

    get has_english_audio(): boolean {
        return this.spoken_language.includes(Language.English);
    }
}

export class ItemRequest {
    @Expose()
    total: number;

    @Expose()
    @Type(() => Item)
    items: Item[];
}
