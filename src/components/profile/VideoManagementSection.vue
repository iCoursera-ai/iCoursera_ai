<template>
  <div class="management-section">
    <div class="section-header">
      <h2><i class="fas fa-film"></i> 视频管理</h2>
      <div class="management-actions">
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="搜索视频标题..." 
            class="form-control"
          >
          <i class="fas fa-search"></i>
        </div>
        <select v-model="statusFilter" class="form-control">
          <option value="all">所有状态</option>
          <option value="published">已发布</option>
          <option value="draft">草稿</option>
          <option value="reviewing">审核中</option>
        </select>
      </div>
    </div>

    <div class="videos-grid">
      <VideoCard 
        v-for="video in filteredVideos" 
        :key="video.id"
        :video="video"
        @edit="handleEditVideo"
        @delete="handleDeleteVideo"
        @publish="handlePublishVideo"
        @unpublish="handleUnpublishVideo"
      />
      
      <div v-if="filteredVideos.length === 0" class="empty-state">
        <i class="fas fa-video"></i>
        <h3>暂无视频</h3>
        <p>您还没有上传任何视频，开始上传第一个视频吧！</p>
        <button class="btn btn-primary" @click="$emit('switch-to-upload')">
          <i class="fas fa-upload"></i> 上传视频
        </button>
      </div>
    </div>

    <div class="management-stats" v-if="filteredVideos.length > 0">
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-icon">
            <i class="fas fa-video"></i>
          </div>
          <div class="stat-number">{{ stats.totalVideos }}</div>
          <div class="stat-label">总视频数</div>
        </div>
        <div class="stat-item">
          <div class="stat-icon">
            <i class="fas fa-eye"></i>
          </div>
          <div class="stat-number">{{ formatNumber(stats.totalViews) }}</div>
          <div class="stat-label">总观看量</div>
        </div>
        <div class="stat-item">
          <div class="stat-icon">
            <i class="fas fa-dollar-sign"></i>
          </div>
          <div class="stat-number">{{ stats.totalEarnings }}</div>
          <div class="stat-label">总收入（元）</div>
        </div>
        <div class="stat-item">
          <div class="stat-icon">
            <i class="fas fa-star"></i>
          </div>
          <div class="stat-number">{{ stats.averageRating }}</div>
          <div class="stat-label">平均评分</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VideoCard from './VideoCard.vue'

export default {
  name: 'VideoManagementSection',
  components: {
    VideoCard
  },
  props: {
    videos: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      searchQuery: '',
      statusFilter: 'all'
    }
  },
  computed: {
    filteredVideos() {
      let filtered = this.videos

      // 搜索过滤
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(video => 
          video.title.toLowerCase().includes(query) ||
          video.description.toLowerCase().includes(query)
        )
      }

      // 状态过滤
      if (this.statusFilter !== 'all') {
        filtered = filtered.filter(video => video.status === this.statusFilter)
      }

      return filtered
    },
    stats() {
      const totalViews = this.videos.reduce((sum, video) => sum + video.views, 0)
      const totalEarnings = this.videos.reduce((sum, video) => sum + video.earnings, 0)
      const totalRatings = this.videos.reduce((sum, video) => sum + (video.rating || 0), 0)
      const ratedVideos = this.videos.filter(video => video.rating).length
      
      return {
        totalVideos: this.videos.length,
        totalViews: totalViews,
        totalEarnings: totalEarnings,
        averageRating: ratedVideos > 0 ? (totalRatings / ratedVideos).toFixed(1) : '0.0'
      }
    }
  },
  methods: {
    handleEditVideo(video) {
      this.$emit('edit-video', video)
    },
    handleDeleteVideo(video) {
      this.$emit('delete-video', video)
    },
    handlePublishVideo(video) {
      this.$emit('publish-video', video)
    },
    handleUnpublishVideo(video) {
      this.$emit('unpublish-video', video)
    },
    formatNumber(num) {
      if (num >= 10000) {
        return (num / 10000).toFixed(1) + '万'
      }
      return num.toString()
    }
  }
}
</script>

<style scoped>
.management-section {
  padding: 20px 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 15px;
}

.section-header h2 {
  font-size: 1.8rem;
  color: var(--dark);
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-header h2 i {
  color: var(--primary);
}

.management-actions {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box input {
  padding: 10px 15px 10px 40px;
  border: 1px solid var(--border);
  border-radius: 6px;
  width: 250px;
  font-size: 0.95rem;
  transition: all 0.3s;
}

.search-box input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
}

.search-box i {
  position: absolute;
  left: 15px;
  color: var(--text-light);
}

.form-control {
  padding: 10px 15px;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 0.95rem;
  background-color: white;
  cursor: pointer;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
}

.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
  margin-bottom: 30px;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.empty-state i {
  font-size: 4rem;
  color: var(--primary);
  margin-bottom: 20px;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: var(--dark);
}

.empty-state p {
  color: var(--text-light);
  margin-bottom: 25px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.management-stats {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-item {
  text-align: center;
  padding: 25px 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s;
}

.stat-item:hover {
  transform: translateY(-5px);
}

.stat-icon {
  font-size: 2.5rem;
  color: var(--primary);
  margin-bottom: 15px;
}

.stat-number {
  font-size: 2.2rem;
  font-weight: bold;
  color: var(--primary);
  margin-bottom: 5px;
}

.stat-label {
  color: var(--text-light);
  font-size: 0.95rem;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
}

.btn-primary:hover {
  background-color: var(--primary-dark);
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .management-actions {
    width: 100%;
  }
  
  .search-box input {
    width: 100%;
  }
  
  .videos-grid {
    grid-template-columns: 1fr;
  }
}
</style>