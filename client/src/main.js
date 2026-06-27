import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import { createPinia } from 'pinia'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.bundle.min.js"

import axios from "axios"
import Cookies from "js-cookie"

axios.defaults.baseURL = "http://localhost:8000"
axios.defaults.withCredentials = true
axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken")

const app = createApp(App)

const pinia = createPinia()

app.use(pinia)      
app.use(router)     

app.mount('#app')