<template>
  <div id="app">
    <router-view />
    <!-- 悬浮球组件 -->
    <FloatingChat />
  </div>
</template>

<script>
import FloatingChat from '@/components/FloatingChat.vue'

export default {
  name: 'App',
  components: {
    FloatingChat
  }
}
</script>