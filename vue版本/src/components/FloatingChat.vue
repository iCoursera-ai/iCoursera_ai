<template>
  <!-- 只在登录状态下显示AI助手 -->
  <div v-if="isLoggedIn" class="floating-chat-container">
    <!-- 悬浮球 -->
    <div 
      v-if="!isChatOpen"
      class="floating-button"
      @click="openChat"
      :style="{
        bottom: position.bottom + 'px',
        right: position.right + 'px'
      }"
    >
      <i class="fa fa-comment"></i>
    </div>

    <!-- 聊天对话框 -->
    <div v-if="isChatOpen" class="chat-dialog" :style="{ 
      bottom: position.bottom + 'px', 
      right: position.right + 'px',
      width: '390px',
      height: '600px'
    }">
      <!-- 对话框标题栏 -->
      <div class="chat-header">
        <div class="chat-title">AI小翔</div>
        <div class="chat-actions">
          <button class="chat-action-btn" @click="toggleMinimize">
            <i class="fa" :class="isMinimized ? 'fa-window-maximize' : 'fa-window-minimize'"></i>
          </button>
          <button class="chat-action-btn" @click="closeChat">
            <i class="fa fa-times"></i>
          </button>
        </div>
      </div>

      <!-- 聊天内容区域 -->
      <div v-if="!isMinimized" class="chat-content">
        <iframe
          ref="chatIframe"
          :src="chatIframeUrl"
          style="width: 100%; height: 100%; border: none;"
          title="AI小翔"
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FloatingChat',
  data() {
    return {
      isChatOpen: false,
      isMinimized: false,
      position: {
        bottom: 20,
        right: 20
      },
      cozeClient: null,
      chatIframeUrl: '',
      isLoggedIn: false,
      checkInterval: null
    }
  },
  mounted() {
    // 初始化时检查登录状态
    this.checkLoginStatus()
    // 设置定期检查登录状态
    this.checkInterval = setInterval(this.checkLoginStatus, 2000)
    
    // 监听登录状态变化
    window.addEventListener('storage', this.handleStorageChange)
    window.addEventListener('user-auth-change', this.checkLoginStatus)
  },
  beforeUnmount() {
    this.cleanup()
    // 清除定时器
    if (this.checkInterval) {
      clearInterval(this.checkInterval)
    }
    // 移除事件监听
    window.removeEventListener('storage', this.handleStorageChange)
    window.removeEventListener('user-auth-change', this.checkLoginStatus)
  },
  methods: {
    checkLoginStatus() {
      // 检查用户是否登录
      const user = localStorage.getItem('bgareaCurrentUser') || 
                  sessionStorage.getItem('bgareaCurrentUser')
      const wasLoggedIn = this.isLoggedIn
      this.isLoggedIn = !!user
      
      // 如果从登录状态变为未登录状态，关闭聊天框
      if (wasLoggedIn && !this.isLoggedIn) {
        this.isChatOpen = false
        this.isMinimized = false
      }
      
      // 只有登录状态下才初始化Coze聊天
      if (this.isLoggedIn) {
        this.initializeCozeChat()
      }
    },
    
    handleStorageChange(event) {
      // 监听localStorage的变化（主要是用户登录状态的变化）
      if (event.key === 'bgareaCurrentUser' || event.key === null) {
        this.checkLoginStatus()
      }
    },
    
    initializeCozeChat() {
      // 如果已初始化，则跳过
      if (this.chatIframeUrl) return
      
      // 动态加载 Coze SDK
      if (!window.CozeWebSDK) {
        this.loadCozeSDK()
      } else {
        this.setupChatIframeUrl()
      }
    },

    loadCozeSDK() {
      const script = document.createElement('script')
      script.src = 'https://lf-cdn.coze.cn/obj/unpkg/flow-platform/chat-app-sdk/1.2.0-beta.19/libs/cn/index.js'
      script.onload = () => {
        this.setupChatIframeUrl()
      }
      document.head.appendChild(script)
    },

    setupChatIframeUrl() {
      // 从存储中获取当前用户信息
      const userData = localStorage.getItem('bgareaCurrentUser') || 
                      sessionStorage.getItem('bgareaCurrentUser')
      
      let userInfo = {
        id: 'user',
        name: 'User',
        avatar: 'https://s3.bmp.ovh/imgs/2025/08/23/6e917ea67f79b68d.png'
      }
      
      if (userData) {
        try {
          const user = JSON.parse(userData)
          userInfo = {
            id: user.id || 'user',
            name: user.username || 'User',
            avatar: user.avatar || 'https://s3.bmp.ovh/imgs/2025/08/23/6e917ea67f79b68d.png'
          }
        } catch (e) {
          console.error('解析用户信息失败:', e)
        }
      }

      // 创建 iframe URL 参数
      const params = new URLSearchParams({
        bot_id: '7537973732451860514',
        user_id: userInfo.id,
        user_name: userInfo.name,
        user_avatar: userInfo.avatar,
        bot_avatar: 'https://s3.bmp.ovh/imgs/2025/09/11/33babec17951a20c.png',
        token: 'cztei_qy8OgftMLBMQmyV81OchH3PHs8AHCd0noLV7XxpLBGvCGxwXCaQV0vlntpJ6DbmK3',
        lang: 'zh-CN',
        layout: 'pc'
      })

      this.chatIframeUrl = `https://www.coze.cn/standalone/iframe?${params.toString()}`
    },

    openChat() {
      // 检查是否登录
      if (!this.isLoggedIn) {
        // 未登录时跳转到登录页
        this.$router.push('/login')
        return
      }
      
      this.isChatOpen = true
      this.isMinimized = false
    },

    closeChat() {
      this.isChatOpen = false
      this.isMinimized = false
    },

    toggleMinimize() {
      this.isMinimized = !this.isMinimized
    },

    cleanup() {
      if (this.cozeClient) {
        // 清理 Coze 客户端资源
        this.cozeClient = null
      }
    }
  }
}
</script>

<style scoped>
.floating-chat-container {
  position: fixed;
  z-index: 9999;
}

.floating-button {
  position: fixed;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5);
  transition: all 0.3s ease;
  font-size: 24px;
}

.floating-button:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
}

.chat-dialog {
  position: fixed;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  z-index: 10000;
}

.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: move;
  user-select: none;
}

.chat-title {
  font-weight: 600;
  font-size: 16px;
}

.chat-actions {
  display: flex;
  gap: 8px;
}

.chat-action-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.chat-action-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.chat-content {
  flex: 1;
  min-height: 0;
}
</style>