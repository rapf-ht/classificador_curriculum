import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './routes/index.js'

app.use(router)

createApp(App).mount('#app')
