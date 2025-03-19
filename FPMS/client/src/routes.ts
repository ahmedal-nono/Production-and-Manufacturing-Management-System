import { createWebHistory, createRouter } from "vue-router";

const routes = [
  // The last route
  // { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
