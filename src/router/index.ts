import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';

import { ContentType } from '@/dto/content';
import NavigationView from '@/views/NavigationView.vue';
import ProductsView from '@/views/ProductsView.vue';
const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        redirect: '/products',
    },
    {
        children: Object.values(ContentType).map((type) => {
            return {
                component: ProductsView,
                path: type,
                props: {
                    content: type,
                },
            };
        }),
        component: NavigationView,
        path: '/'
    },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

export default router;
