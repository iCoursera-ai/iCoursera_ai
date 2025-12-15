import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/tailwind.css'  // 确保路径正确

const app = createApp(App)
app.use(router)
app.mount('#app')