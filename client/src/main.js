import './assets/main.css'

import { createApp } from 'vue'
import TDesign from 'tdesign-vue-next'
import axios from 'axios'

import App from './App.vue'
import router from './router'
import pinia from './stores'

// imports global style variables from tdesign
import 'tdesign-vue-next/es/style/index.css'

const app = createApp(App)

app.config.globalProperties.$http = axios

app.use(pinia)
app.use(router)
app.use(TDesign)

app.mount('#app')
