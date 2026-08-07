import { createRouter, createWebHistory } from 'vue-router';
import Main from '../views/main.vue';

const routes = [
    {
        path: '/',
        name: 'Main',
        component: Main
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