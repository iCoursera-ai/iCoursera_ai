<template>
  <div class="video-card">
    <div class="video-card-thumbnail">
      <img :src="video.thumbnail" :alt="video.title" class="thumbnail-image">
      <div class="video-status" :class="video.status">
        {{ getStatusText(video.status) }}
      </div>
      <div class="video-overlay">
        <button class="btn-play" @click="previewVideo">
          <i class="fas fa-play"></i>
        </button>
      </div>
    </div>
    
    <div class="video-card-content">
      <h3 class="video-title">{{ video.title }}</h3>
      <p class="video-description">{{ video.description }}</p>
      
      <div class="video-meta">
        <span class="video-category">{{ getCategoryText(video.category) }}</span>
        <span class="video-level" :class="video.level">{{ getLevelText(video.level) }}</span>
        <span class="video-duration">{{ video.duration }}</span>
      </div>
      
      <div class="video-stats">
        <span class="stat">
          <i class="fas fa-eye"></i> {{ video.views }}
        </span>
        <span class="stat">
          <i class="fas fa-heart"></i> {{ video.likes }}
        </span>
        <span class="stat">
          <i class="fas fa-comment"></i> {{ video.comments }}
        </span>
        <span class="stat" v-if="video.earnings > 0">
          <i class="fas fa-dollar-sign"></i> {{ video.earnings }}
        </span>
      </div>
      
      <div class="video-date">
        <small>创建于: {{ formatDate(video.createdAt) }}</small>
        <small v-if="video.publishedAt">发布于: {{ formatDate(video.publishedAt) }}</small>
      </div>
    </div>
    
    <div class="video-card-actions">
      <button class="btn-action btn-edit" @click="$emit('edit', video)" title="编辑">
        <i class="fas fa-edit"></i>
      </button>
      
      <button 
        v-if="video.status === 'published'"
        class="btn-action btn-unpublish" 
        @click="$emit('unpublish', video)"
        title="下架"
      >
        <i class="fas fa-eye-slash"></i>
      </button>
      
      <button 
        v-else
        class="btn-action btn-publish" 
        @click="$emit('publish', video)"
        title="发布"
      >
        <i class="fas fa-eye"></i>
      </button>
      
      <button class="btn-action btn-analytics" @click="viewAnalytics" title="数据分析">
        <i class="fas fa-chart-bar"></i>
      </button>
      
      <button class="btn-action btn-delete" @click="$emit('delete', video)" title="删除">
        <i class="fas fa-trash"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VideoCard',
  props: {
    video: {
      type: Object,
      required: true
    }
  },
  methods: {
    getStatusText(status) {
      const statusMap = {
        'published': '已发布',
        'draft': '草稿',
        'reviewing': '审核中',
        'rejected': '未通过'
      }
      return statusMap[status] || status
    },
    getCategoryText(category) {
      const categoryMap = {
        'technology': '技术',
        'data-science': '数据科学',
        'business': '商业',
        'design': '设计',
        'marketing': '市场营销',
        'personal-development': '个人发展'
      }
      return categoryMap[category] || category
    },
    getLevelText(level) {
      const levelMap = {
        'beginner': '初级',
        'intermediate': '中级',
        'advanced': '高级'
      }
      return levelMap[level] || level
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('zh-CN')
    },
    previewVideo() {
      alert(`预览视频: ${this.video.title}`)
    },
    viewAnalytics() {
      alert(`查看视频分析: ${this.video.title}`)
    }
  }
}
</script>

<style scoped>
.video-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.video-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.video-card-thumbnail {
  position: relative;
  height: 160px;
  overflow: hidden;
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-status {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 500;
  text-transform: uppercase;
}

.video-status.published {
  background: var(--success);
  color: white;
}

.video-status.draft {
  background: var(--warning);
  color: white;
}

.video-status.reviewing {
  background: var(--primary);
  color: white;
}

.video-status.rejected {
  background: var(--danger);
  color: white;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.video-card:hover .video-overlay {
  opacity: 1;
}

.btn-play {
  background: rgba(255, 255, 255, 0.9);
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.3s;
}

.btn-play:hover {
  transform: scale(1.1);
}

.btn-play i {
  color: var(--primary);
  font-size: 1.2rem;
}

.video-card-content {
  padding: 20px;
}

.video-title {
  font-size: 1.1rem;
  margin-bottom: 8px;
  color: var(--text);
  line-height: 1.4;
}

.video-description {
  color: var(--text-light);
  font-size: 0.9rem;
  margin-bottom: 12px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.video-category, .video-level, .video-duration {
  padding: 4px 8px;
  background: var(--secondary);
  border-radius: 4px;
  font-size: 0.8rem;
  color: var(--text-light);
}

.video-level.beginner {
  background: #e8f5e8;
  color: var(--success);
}

.video-level.intermediate {
  background: #fff3cd;
  color: var(--warning);
}

.video-level.advanced {
  background: #f8d7da;
  color: var(--danger);
}

.video-stats {
  display: flex;
  gap: 15px;
  margin-bottom: 12px;
  font-size: 0.8rem;
  color: var(--text-light);
}

.video-stats .stat i {
  margin-right: 4px;
}

.video-date {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.video-date small {
  color: var(--text-light);
  font-size: 0.7rem;
}

.video-card-actions {
  display: flex;
  border-top: 1px solid var(--border);
  padding: 15px;
  gap: 8px;
}

.btn-action {
  flex: 1;
  padding: 8px;
  border: 1px solid var(--border);
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  color: var(--text-light);
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-action:hover {
  background: var(--secondary);
}

.btn-edit:hover {
  color: var(--primary);
  border-color: var(--primary);
}

.btn-publish:hover {
  color: var(--success);
  border-color: var(--success);
}

.btn-unpublish:hover {
  color: var(--warning);
  border-color: var(--warning);
}

.btn-analytics:hover {
  color: var(--info);
  border-color: var(--info);
}

.btn-delete:hover {
  color: var(--danger);
  border-color: var(--danger);
}
</style>