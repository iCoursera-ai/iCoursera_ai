<template>
  <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
    <div class="adaptive-learning-modal">
      <div class="modal-header">
        <h2>教学优化洞察</h2>
        <button class="close-btn" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="modal-content">
        <div class="insight-section">
          <h3>学习行为分析</h3>
          <div class="insight-grid">
            <div class="insight-card">
              <div class="insight-icon">
                <i class="fas fa-chart-line"></i>
              </div>
              <div class="insight-content">
                <h4>完成率趋势</h4>
                <p>您的课程平均完成率为 <strong>68%</strong>，高于平台平均 52%</p>
              </div>
            </div>
            
            <div class="insight-card">
              <div class="insight-icon">
                <i class="fas fa-clock"></i>
              </div>
              <div class="insight-content">
                <h4>最佳观看时长</h4>
                <p>观众在 <strong>8-12分钟</strong> 的视频中完成率最高</p>
              </div>
            </div>
            
            <div class="insight-card">
              <div class="insight-icon">
                <i class="fas fa-users"></i>
              </div>
              <div class="insight-content">
                <h4>受众特征</h4>
                <p>主要观众年龄在 <strong>25-34岁</strong>，偏好实践性内容</p>
              </div>
            </div>
            
            <div class="insight-card">
              <div class="insight-icon">
                <i class="fas fa-lightbulb"></i>
              </div>
              <div class="insight-content">
                <h4>优化建议</h4>
                <p>增加实战案例和代码演示可提升学习效果</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="recommendation-section">
          <h3>个性化建议</h3>
          <div class="recommendation-list">
            <div class="recommendation-item">
              <i class="fas fa-check-circle"></i>
              <span>考虑制作更多关于 <strong>Vue 3 实战项目</strong> 的内容</span>
            </div>
            <div class="recommendation-item">
              <i class="fas fa-check-circle"></i>
              <span>在视频中加入 <strong>互动问答</strong> 环节提高参与度</span>
            </div>
            <div class="recommendation-item">
              <i class="fas fa-check-circle"></i>
              <span>优化视频缩略图设计以提升点击率</span>
            </div>
          </div>
        </div>
        
        <div class="action-section">
          <button class="btn btn-outline" @click="$emit('close')">
            关闭
          </button>
          <button class="btn btn-primary" @click="$emit('export-report')">
            <i class="fas fa-download"></i> 导出详细报告
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdaptiveLearningModal',
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'export-report']
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.adaptive-learning-modal {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  border-bottom: 1px solid var(--border);
}

.modal-header h2 {
  margin: 0;
  color: var(--text);
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: var(--text-light);
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
  transition: all 0.3s;
}

.close-btn:hover {
  background: var(--secondary);
  color: var(--text);
}

.modal-content {
  padding: 30px;
}

.insight-section {
  margin-bottom: 30px;
}

.insight-section h3 {
  margin-bottom: 20px;
  color: var(--text);
  font-size: 1.2rem;
}

.insight-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.insight-card {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 20px;
  background: var(--secondary);
  border-radius: 8px;
  border-left: 4px solid var(--primary);
}

.insight-icon {
  background: var(--primary);
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.insight-content h4 {
  margin: 0 0 8px 0;
  color: var(--text);
  font-size: 1rem;
}

.insight-content p {
  margin: 0;
  color: var(--text-light);
  font-size: 0.9rem;
  line-height: 1.4;
}

.recommendation-section {
  margin-bottom: 30px;
}

.recommendation-section h3 {
  margin-bottom: 15px;
  color: var(--text);
  font-size: 1.2rem;
}

.recommendation-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recommendation-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid var(--border);
}

.recommendation-item i {
  color: var(--success);
  flex-shrink: 0;
}

.recommendation-item span {
  color: var(--text);
  font-size: 0.95rem;
}

.action-section {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid var(--border);
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover {
  background: #0046b8;
  transform: translateY(-1px);
}

.btn-outline {
  background: transparent;
  color: var(--primary);
  border: 1px solid var(--primary);
}

.btn-outline:hover {
  background: var(--primary);
  color: white;
}

@media (max-width: 768px) {
  .modal-content {
    padding: 20px;
  }
  
  .insight-grid {
    grid-template-columns: 1fr;
  }
  
  .action-section {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>