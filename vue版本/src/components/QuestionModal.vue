<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title">提问</h3>
        <button class="close-btn" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="modal-body">
        <div class="form-group">
          <label>问题标题</label>
          <input type="text" v-model="questionTitle" placeholder="请输入问题标题">
        </div>
        
        <div class="form-group">
          <label>详细描述</label>
          <textarea 
            v-model="questionContent" 
            rows="5" 
            placeholder="请详细描述您的问题"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label>是否匿名提问</label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="isAnonymous">
            <span>匿名提问</span>
          </label>
        </div>
        
        <div class="form-group">
          <label>需要AI解答</label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="needsAIAnswer" checked>
            <span>需要AI助手解答</span>
          </label>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn btn-outline" @click="$emit('close')">取消</button>
        <button class="btn btn-primary" @click="submitQuestion">提交问题</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuestionModal',
  data() {
    return {
      questionTitle: '',
      questionContent: '',
      isAnonymous: false,
      needsAIAnswer: true
    }
  },
  methods: {
    submitQuestion() {
      if (!this.questionTitle.trim() || !this.questionContent.trim()) {
        alert('请填写问题标题和内容')
        return
      }
      
      alert('问题已提交，AI助手正在处理...')
      this.$emit('close')
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

.modal-title {
  font-size: 1.3rem;
  color: #1F2937;
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

.form-group {
  margin-bottom: 1.2rem;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #4E5969;
}

.form-group input[type="text"],
.form-group textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #E5E6EB;
  border-radius: 8px;
  font-family: inherit;
}

.form-group textarea {
  resize: vertical;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input {
  width: auto;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn {
  padding: 0.7rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-outline {
  background-color: white;
  color: #165DFF;
  border: 2px solid #165DFF;
}

.btn-primary {
  background-color: #165DFF;
  color: white;
  border: none;
}

.btn:hover {
  opacity: 0.9;
}
</style>