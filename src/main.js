import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/styles.css'

const app = createApp(App)

// 添加全局通知方法
app.config.globalProperties.$notify = function(options) {
  // 创建通知元素
  const notification = document.createElement('div')
  notification.className = `notification notification-${options.type || 'info'}`
  notification.innerHTML = `
    <div class="notification-content">
      <span class="notification-message">${options.message}</span>
      <button class="notification-close">&times;</button>
    </div>
  `
  
  // 添加到页面
  document.body.appendChild(notification)
  
  // 添加关闭功能
  const closeBtn = notification.querySelector('.notification-close')
  closeBtn.addEventListener('click', () => {
    notification.classList.add('fade-out')
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification)
      }
    }, 300)
  })
  
  // 自动消失
  setTimeout(() => {
    if (notification.parentNode) {
      notification.classList.add('fade-out')
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification)
        }
      }, 300)
    }
  }, options.duration || 5000)
}

app.use(store).use(router).mount('#app')