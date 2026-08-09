import { createRouter, createWebHistory } from 'vue-router';
import Main from '../views/Main.vue';
import Loading from '../views/Loading.vue';

const routes = [
    {
        path: '/',
        name: 'main',
        component: Main
    },
    {
        path: '/loading',
        name: 'loading',
        component: Loading
    },

    // Path de erro deve ser o último
    /*{
        path: '/:pathMatch(.*)*',
        name: 'not-found',
        component: () => import('../views/NotFoundView.vue')
    }*/
];

const router = createRouter({
    history: createWebHistory(), 
    routes
});

export default router;