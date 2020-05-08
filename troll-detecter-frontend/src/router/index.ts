import Vue from 'vue'
import Router from 'vue-router'
import HomeComponent from '../views/Home.vue';
import ProfileComponent from '../components/Profile.vue';
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    { path: '/', redirect: { name: 'home' } },
    { path: '/home', name: 'home', component: HomeComponent },
    { path: '/profile/:username', name: 'Profile', component:ProfileComponent},
  ]
});




// import Vue from 'vue'
// import VueRouter, { RouteConfig } from 'vue-router'
// import Home from '../views/Home.vue'

// Vue.use(VueRouter)

//   const routes: Array<RouteConfig> = [
//   {
//     path: '/',
//     name: 'Home',
//     component: Home
//   },
//   {
//     path: '/about',
//     name: 'About',
//     // route level code-splitting
//     // this generates a separate chunk (about.[hash].js) for this route
//     // which is lazy-loaded when the route is visited.
//     component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
//   }
// ]

// const router = new VueRouter({
//   mode: 'history',
//   base: process.env.BASE_URL,
//   routes
// })

// export default router
