<template>
  <div class="management-section">
    <div class="section-header">
      <h2>视频管理</h2>
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
          <div class="stat-number">{{ stats.totalVideos }}</div>
          <div class="stat-label">总视频数</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ stats.totalViews }}</div>
          <div class="stat-label">总观看量</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ stats.totalEarnings }}</div>
          <div class="stat-label">总收入（元）</div>
        </div>
        <div class="stat-item">
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
      return {
        totalVideos: this.videos.length,
        totalViews: this.videos.reduce((sum, video) => sum + video.views, 0),
        totalEarnings: this.videos.reduce((sum, video) => sum + video.earnings, 0),
        averageRating: 4.7 // 可以从视频数据计算
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
    }
  }
}
</script>

<style scoped>
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
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary);
  margin-bottom: 5px;
}

.stat-label {
  color: var(--text-light);
  font-size: 0.9rem;
}
</style>