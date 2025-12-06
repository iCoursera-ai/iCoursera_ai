<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title">AI生成习题</h3>
        <button class="close-btn" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="modal-body">
        <div class="exercise-section">
          <div class="exercise-title">选择题</div>
          <div class="exercise-item">
            <p>Pandas中，用于创建一维数组的数据结构是？</p>
            <div class="options">
              <label v-for="option in mcqOptions" :key="option.value" class="option-label">
                <input type="radio" :name="'q1'" :value="option.value" v-model="selectedMCQ">
                <span>{{ option.text }}</span>
              </label>
            </div>
          </div>
        </div>
        
        <div class="exercise-section">
          <div class="exercise-title">判断题</div>
          <div class="exercise-item">
            <p>DataFrame可以看作是多个Series的集合。</p>
            <div class="options">
              <label class="option-label">
                <input type="radio" name="q2" value="true" v-model="selectedTF">
                <span>正确</span>
              </label>
              <label class="option-label">
                <input type="radio" name="q2" value="false" v-model="selectedTF">
                <span>错误</span>
              </label>
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn btn-outline" @click="resetAnswers">重置</button>
        <button class="btn btn-primary" @click="submitAnswers">提交答案</button>
        <button class="btn btn-success" @click="aiGrade">AI批改</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExerciseModal',
  props: {
    lesson: Object
  },
  data() {
    return {
      mcqOptions: [
        { value: 'A', text: 'DataFrame' },
        { value: 'B', text: 'Series' },
        { value: 'C', text: 'Array' },
        { value: 'D', text: 'Matrix' }
      ],
      selectedMCQ: null,
      selectedTF: null
    }
  },
  methods: {
    resetAnswers() {
      this.selectedMCQ = null
      this.selectedTF = null
    },
    submitAnswers() {
      // 提交答案逻辑
      this.$emit('close')
      alert('答案已提交，正在批改中...')
    },
    aiGrade() {
      // AI批改逻辑
      this.$emit('close')
      alert('AI批改完成！')
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
  max-width: 600px;
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

.exercise-section {
  margin-bottom: 1.5rem;
}

.exercise-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.exercise-item {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.exercise-item p {
  margin-bottom: 1rem;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.option-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
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

.btn-success {
  background-color: #10B981;
  color: white;
  border: none;
}

.btn:hover {
  opacity: 0.9;
}
</style>