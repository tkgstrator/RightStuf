import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import NavigationView from '@/views/NavigationView.vue';
import ProductsView from '@/views/ProductsView.vue';
import { ContentType } from '@/dto/content';
const routes: Array<RouteRecordRaw> = [
    // {
    //     path: '/',
    //     // redirect: '/',
    // },
    {
        path: '/',
        component: NavigationView,
        children: Object.values(ContentType).map((type) => {
            return {
                path: type,
                component: ProductsView,
                props: {
                    content: type,
                },
            };
        })
    },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

export default router;
