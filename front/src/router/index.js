import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,

  },
  {
    path: '/list',
    name: 'list',
    component: () => import(/* webpackChunkName: "about" */ '../views/VideoList')
  },
  {
    path: '/play',
    name: 'play',
    component: () => import(/* webpackChunkName: "about" */ '../views/Play')
  },
  {
    path: '/test',
    name: 'test',
    component: () => import(/* webpackChunkName: "about" */ '../views/Test')
  },
  {
    path: '/share',
    name: 'share',
    component: () => import(/* webpackChunkName: "about" */ '../views/ShareScreen')
  },
  {
    path: '/admin/Collect',
    name: 'collect',
    component: () => import(/* webpackChunkName: "about" */ '../views/admin/Collect')
  }
]

const router = new VueRouter({
  // mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
