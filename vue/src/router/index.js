import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from "../views/Index";
import App from "../App";
import login from "../views/login"
import realtime from "../views/realtime"
import history from "../views/history"
import account from "../views/account"


Vue.use(VueRouter)

const routes = [
	{
		path: '/',
		name: 'login',
		component: login
	},
	{
		path: '/stock',
		name: 'Stock',
		component: Index,
		children:[
			{
				path: '/realtime',
				name: 'RealTime',
				component: realtime
			},
			{
				path: '/history',
				name: 'History',
				component: history
			}
		]
	},
	{
		path: '/setting',
		name: 'Setting',
		component: Index,
		children:[
			{
				path: '/account',
				name: 'Account',
				component: account
			}
		]
	}
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
