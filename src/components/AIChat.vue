<template>
  <div>
    <div class="ai-chat-icon" @click="toggleChat">
      <i class="fas fa-comment-dots"></i>
    </div>
    
    <div class="ai-chat-modal" :class="{ open: isChatOpen }">
      <div class="chat-header">
        <h3><i class="fas fa-robot"></i> BGarea AI 助手</h3>
        <button class="chat-close-btn" @click="closeChat">&times;</button>
      </div>
      <div class="chat-body" ref="chatBody">
        <div class="message system-message">
          你好！我是 BGarea AI 助手，很高兴为您服务。请问有什么可以帮您的吗？
        </div>
        <div 
          v-for="(message, index) in messages" 
          :key="index"
          :class="['message', message.type === 'user' ? 'user-message' : 'system-message']"
        >
          {{ message.text }}
        </div>
      </div>
      <div class="chat-footer">
        <input 
          type="text" 
          v-model="inputMessage" 
          @keypress.enter="sendMessage"
          placeholder="输入您的问题..." 
          autocomplete="off"
        >
        <button class="btn btn-primary" @click="sendMessage">
          <i class="fas fa-paper-plane"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIChat',
  data() {
    return {
      isChatOpen: false,
      inputMessage: '',
      messages: []
    }
  },
  methods: {
    toggleChat() {
      this.isChatOpen = !this.isChatOpen
    },
    closeChat() {
      this.isChatOpen = false
    },
    sendMessage() {
      if (!this.inputMessage.trim()) return

      const userMessage = {
        type: 'user',
        text: this.inputMessage
      }
      this.messages.push(userMessage)
      
      const userText = this.inputMessage
      this.inputMessage = ''
      
      setTimeout(() => {
        this.generateAIResponse(userText)
      }, 800)
    },
    generateAIResponse(userMessage) {
      const responseMap = {
        '课程信息': '请问您对哪一门课程感兴趣？我们有「机器学习入门」、「Web开发高级技巧」等热门课程。',
        '账户问题': '请描述您的账户问题，例如「修改密码」、「更新资料」或「账户冻结」。',
        '技术支持': '请详细说明您遇到的技术问题，我们会尽快为您转接人工客服。',
        '你好': '你好！我是 EduLearn AI 助手，很高兴为您服务。',
        '谢谢': '不客气！随时为您效劳。',
      }

      let aiResponse = '抱歉，我没有理解您的问题。您可以尝试输入「课程信息」、「账户问题」或「技术支持」。'

      const lowerCaseMessage = userMessage.toLowerCase()
      for (const keyword in responseMap) {
        if (lowerCaseMessage.includes(keyword.toLowerCase())) {
          aiResponse = responseMap[keyword]
          break
        }
      }

      this.messages.push({
        type: 'system',
        text: aiResponse
      })

      this.$nextTick(() => {
        this.scrollToBottom()
      })
    },
    scrollToBottom() {
      const chatBody = this.$refs.chatBody
      if (chatBody) {
        chatBody.scrollTop = chatBody.scrollHeight
      }
    }
  }
}
</script>