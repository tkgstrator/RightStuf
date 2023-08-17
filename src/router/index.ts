import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import NavigationView from '@/views/NavigationView.vue';

const routes: Array<RouteRecordRaw> = [
    // {
    //     path: '/',
    //     // redirect: '/',
    // },
    {
        path: '/',
        component: NavigationView,
        children: [
            // {
            //     path: '/',
            //     redirect: '/pre-order',
            // },
            {
                path: '/',
                component: () => import('@/views/HomeView.vue'),
            },
            {
                path: 'pre-order',
                component: () => import('@/views/PreorderView.vue'),
            },
            {
                path: 'new-release',
                component: () => import('@/views/NewReleaseView.vue'),
            },
            {
                path: 'sales',
                component: () => import('@/views/SalesView.vue'),
            },
            // {
            //     path: 'tab2',
            //     component: () => import('@/views/Tab2Page.vue'),
            // },
            // {
            //     path: 'tab3',
            //     component: () => import('@/views/Tab3Page.vue'),
            // },
        ],
    },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

export default router;
