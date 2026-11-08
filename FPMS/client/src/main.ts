import './main.css'
import './api/axios'

import { createApp } from 'vue'
import { plugin, defaultConfig } from '@formkit/vue'

import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(plugin, defaultConfig)

app.mount('#app')
