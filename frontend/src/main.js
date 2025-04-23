import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './style.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// 注册所有ElementPlus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(`ElIcon${key}`, component)
}

app.use(ElementPlus, { size: 'default', zIndex: 3000 })
app.use(router)

app.mount('#app')
