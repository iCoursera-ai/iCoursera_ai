<template>
  <div id="app">
    <router-view />
    <!-- 悬浮球组件 -->
    <FloatingChat v-if="shouldShowChat" />
  </div>
</template>

<script>
import FloatingChat from '@/components/FloatingChat.vue'

export default {
  name: 'App',
  components: {
    FloatingChat
  },
  computed: {
    // 判断是否应该显示悬浮球组件
    shouldShowChat() {
      // 获取当前路由
      const currentRoute = this.$route
      if (!currentRoute) return true
      
      // 排除登录和注册页面
      const excludeRoutes = ['/login', '/register']
      return !excludeRoutes.includes(currentRoute.path)
    }
  }
}
</script>