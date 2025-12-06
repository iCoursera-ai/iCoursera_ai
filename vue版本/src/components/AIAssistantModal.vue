<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <div class="assistant-header">
          <div class="assistant-avatar">
            <i class="fas fa-robot"></i>
          </div>
          <div>
            <h3 class="modal-title">AI助手小翔</h3>
            <p class="assistant-subtitle">为您解答学习问题</p>
          </div>
        </div>
        <button class="close-btn" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="modal-body">
        <div class="assistant-intro">
          <p>您好！我是AI学习助手小翔，我可以：</p>
          <ul>
            <li>解答课程相关问题</li>
            <li>生成个性化习题</li>
            <li>规划学习路径</li>
            <li>分析学习难点</li>
          </ul>
        </div>
        
        <div class="quick-questions">
          <div class="section-title">常见问题：</div>
          <button 
            v-for="question in quickQuestions" 
            :key="question"
            class="quick-question-btn"
            @click="askQuestion(question)"
          >
            {{ question }}
          </button>
        </div>
        
        <div class="ask-area">
          <input 
            type="text" 
            v-model="userQuestion"
            placeholder="输入您的问题..."
            @keyup.enter="askQuestion(userQuestion)"
          >
          <button class="send-btn" @click="askQuestion(userQuestion)">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIAssistantModal',
  data() {
    return {
      quickQuestions: [
        '请解释Series和DataFrame的区别',
        '生成关于Pandas数据结构的练习题',
        '我下一步应该学习什么内容？'
      ],
      userQuestion: ''
    }
  },
  methods: {
    askQuestion(question) {
      if (!question.trim()) return
      
      alert(`AI助手正在回答: ${question}`)
      this.userQuestion = ''
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.7);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background-color: white;
  width: 90%;
  max-width: 500px;
  border-radius: 8px;
  padding: 2rem;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.assistant-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.assistant-avatar {
  width: 50px;
  height: 50px;
  background-color: #165DFF;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}

.modal-title {
  font-size: 1.3rem;
  color: #1F2937;
  margin-bottom: 0.2rem;
}

.assistant-subtitle {
  color: #4E5969;
  font-size: 0.9rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #4E5969;
}

.modal-body {
  margin-bottom: 1.5rem;
}

.assistant-intro {
  background-color: #f0f9ff;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.assistant-intro ul {
  margin-top: 0.5rem;
  padding-left: 1.2rem;
}

.assistant-intro li {
  margin-bottom: 0.3rem;
}

.section-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1F2937;
}

.quick-questions {
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

.quick-question-btn {
  text-align: left;
  padding: 0.8rem;
  border: 1px solid #E5E6EB;
  border-radius: 8px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s;
  width: 100%;
  margin-bottom: 0.8rem;
}

.quick-question-btn:hover {
  border-color: #165DFF;
  background-color: #f8fdff;
}

.ask-area {
  display: flex;
  gap: 0.5rem;
}

.ask-area input {
  flex-grow: 1;
  padding: 0.8rem;
  border: 1px solid #E5E6EB;
  border-radius: 8px;
}

.send-btn {
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  border: none;
  background-color: #165DFF;
  color: white;
  font-weight: 600;
  cursor: pointer;
}
</style>