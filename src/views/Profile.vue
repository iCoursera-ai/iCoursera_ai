<template>
  <section class="user-profile" v-if="user">
    <div class="container">
      <div class="profile-header">
        <div class="profile-avatar">
          <i class="fas fa-user"></i>
          <button class="avatar-edit" @click="editAvatar">
            <i class="fas fa-camera"></i>
          </button>
        </div>
        <div class="profile-info">
          <h1 id="userName">{{ user.firstName }} {{ user.lastName }}</h1>
          <p>{{ user.membership }} · 加入时间: <span id="joinDate">{{ joinDate }}</span></p>
          <p><i class="fas fa-map-marker-alt"></i> <span id="userLocation">{{ user.location || '未设置' }}</span></p>
          <div class="profile-stats">
            <div class="stat">
              <strong>{{ userStats.uploadedVideos }}</strong>
              <span>上传视频</span>
            </div>
            <div class="stat">
              <strong>{{ userStats.totalViews }}</strong>
              <span>总观看</span>
            </div>
            <div class="stat">
              <strong>{{ userStats.subscribers }}</strong>
              <span>订阅者</span>
            </div>
          </div>
        </div>
        <div class="profile-actions">
          <button class="btn btn-info" @click="openAdaptiveLearningModal">
            <i class="fas fa-flask"></i> 教学优化洞察
          </button>
          <button class="btn btn-outline" @click="editProfile">
            <i class="fas fa-edit"></i> 编辑资料
          </button>
        </div>
      </div>

      <div class="profile-tabs">
        <div 
          class="tab" 
          :class="{ active: activeTab === 'upload' }"
          @click="activeTab = 'upload'"
        >
          上传视频
        </div>
        <div 
          class="tab" 
          :class="{ active: activeTab === 'manage' }"
          @click="activeTab = 'manage'"
        >
          视频管理
        </div>
        <div 
          class="tab" 
          :class="{ active: activeTab === 'analytics' }"
          @click="activeTab = 'analytics'"
        >
          数据分析
        </div>
        <div 
          class="tab" 
          :class="{ active: activeTab === 'settings' }"
          @click="activeTab = 'settings'"
        >
          账户设置
        </div>
      </div>

      <!-- 上传视频标签页 -->
      <div class="tab-content" :class="{ active: activeTab === 'upload' }">
        <UploadVideoSection />
      </div>

      <!-- 视频管理标签页 -->
      <div class="tab-content" :class="{ active: activeTab === 'manage' }">
        <VideoManagementSection 
          :videos="userVideos"
          @edit-video="editVideo"
          @delete-video="deleteVideo"
          @publish-video="publishVideo"
          @unpublish-video="unpublishVideo"
        />
      </div>

      <!-- 数据分析标签页 -->
      <div class="tab-content" :class="{ active: activeTab === 'analytics' }">
        <AnalyticsSection 
          :analyticsData="analyticsData"
          :timeRange="analyticsTimeRange"
          @time-range-change="handleTimeRangeChange"
        />
      </div>

      <!-- 账户设置标签页 -->
      <div class="tab-content" :class="{ active: activeTab === 'settings' }">
        <AccountSettingsSection 
          :user="user"
          @update-profile="updateProfile"
          @update-password="updatePassword"
          @update-notifications="updateNotifications"
        />
      </div>
    </div>

    <!-- 自适应学习模态框 -->
    <AdaptiveLearningModal 
      :show="showAdaptiveLearningModal"
      @close="closeAdaptiveLearningModal"
      @export-report="exportReport"
    />

    <!-- 删除确认模态框 -->
    <ConfirmModal 
      :show="showDeleteModal"
      title="确认删除"
      :message="'您确定要删除视频 ' + deleteVideoTitle + ' 吗？此操作无法撤销。'"
      confirm-text="确认删除"
      cancel-text="取消"
      type="danger"
      @confirm="confirmDeleteVideo"
      @cancel="cancelDeleteVideo"
    />

    <!-- 下架确认模态框 -->
    <ConfirmModal 
      :show="showUnpublishModal"
      title="确认下架"
      :message="'您确定要下架视频 ' + unpublishVideoTitle + ' 吗？视频将不再对学习者可见。'"
      confirm-text="确认下架"
      cancel-text="取消"
      type="warning"
      @confirm="confirmUnpublishVideo"
      @cancel="cancelUnpublishVideo"
    />
  </section>
</template>

<script>
import { mapState } from 'vuex'
import UploadVideoSection from '../components/profile/UploadVideoSection.vue'
import VideoManagementSection from '../components/profile/VideoManagementSection.vue'
import AnalyticsSection from '../components/profile/AnalyticsSection.vue'
import AccountSettingsSection from '../components/profile/AccountSettingsSection.vue'
import AdaptiveLearningModal from '../components/profile/AdaptiveLearningModal.vue'
import ConfirmModal from '../components/common/ConfirmModal.vue'

export default {
  name: 'Profile',
  components: {
    UploadVideoSection,
    VideoManagementSection,
    AnalyticsSection,
    AccountSettingsSection,
    AdaptiveLearningModal,
    ConfirmModal
  },
  data() {
    return {
      activeTab: 'analytics',
      analyticsTimeRange: '30',
      showAdaptiveLearningModal: false,
      showDeleteModal: false,
      showUnpublishModal: false,
      deleteVideoTitle: '',
      unpublishVideoTitle: '',
      videoToDelete: null,
      videoToUnpublish: null,
      userStats: {
        uploadedVideos: 15,
        totalViews: 12456,
        subscribers: 1234,
        totalEarnings: 2450,
        averageRating: 4.7
      },
      userVideos: [],
      analyticsData: {}
    }
  },
  computed: {
    ...mapState(['user']),
    joinDate() {
      return this.user.joinDate || '2022年3月'
    }
  },
  created() {
    this.loadUserVideos()
    this.loadAnalyticsData()
  },
  methods: {
    editAvatar() {
      this.showAlert('编辑头像', '头像编辑功能将在完整版本中实现', 'info')
    },
    editProfile() {
      this.activeTab = 'settings'
    },
    openAdaptiveLearningModal() {
      this.showAdaptiveLearningModal = true
    },
    closeAdaptiveLearningModal() {
      this.showAdaptiveLearningModal = false
    },
    exportReport() {
      this.showAlert('报告导出', '完整报告已发送至您的邮箱', 'success')
    },
    loadUserVideos() {
      // 模拟用户视频数据
      this.userVideos = [
        {
          id: 1,
          title: '机器学习入门教程',
          description: '从零开始学习机器学习基础概念和算法',
          thumbnail: 'https://via.placeholder.com/300x160/0056d2/ffffff?text=Machine+Learning',
          category: 'technology',
          level: 'beginner',
          duration: '15:30',
          status: 'published',
          views: 12456,
          likes: 1234,
          comments: 89,
          earnings: 245,
          createdAt: '2023-10-15',
          publishedAt: '2023-10-16'
        },
        {
          id: 2,
          title: 'Python数据分析实战',
          description: '使用Python进行数据清洗、分析和可视化',
          thumbnail: 'https://via.placeholder.com/300x160/28a745/ffffff?text=Python+Data',
          category: 'data-science',
          level: 'intermediate',
          duration: '25:45',
          status: 'published',
          views: 8765,
          likes: 765,
          comments: 45,
          earnings: 189,
          createdAt: '2023-09-20',
          publishedAt: '2023-09-21'
        },
        {
          id: 3,
          title: 'Vue 3 高级技巧',
          description: '深入学习Vue 3的组合式API和性能优化',
          thumbnail: 'https://via.placeholder.com/300x160/dc3545/ffffff?text=Vue+3',
          category: 'technology',
          level: 'advanced',
          duration: '32:15',
          status: 'draft',
          views: 0,
          likes: 0,
          comments: 0,
          earnings: 0,
          createdAt: '2023-11-01',
          publishedAt: null
        },
        {
          id: 4,
          title: 'React Hooks 深入理解',
          description: '掌握React Hooks的使用场景和最佳实践',
          thumbnail: 'https://via.placeholder.com/300x160/ffc107/333333?text=React+Hooks',
          category: 'technology',
          level: 'intermediate',
          duration: '28:30',
          status: 'reviewing',
          views: 0,
          likes: 0,
          comments: 0,
          earnings: 0,
          createdAt: '2023-10-25',
          publishedAt: null
        }
      ]
    },
    loadAnalyticsData() {
      // 模拟分析数据
      this.analyticsData = {
        overview: {
          totalViews: 12456,
          subscribers: 1234,
          completionRate: 68,
          averageRating: 4.7
        },
        viewsData: {
          labels: ['10月15日', '10月16日', '10月17日', '10月18日', '10月19日', '10月20日', '10月21日'],
          data: [1200, 1900, 1500, 2100, 1800, 2200, 2000]
        },
        engagementData: {
          labels: ['播放', '点赞', '收藏', '分享', '评论'],
          data: [100, 85, 60, 45, 30]
        },
        audienceData: {
          labels: ['18-24岁', '25-34岁', '35-44岁', '45岁以上'],
          data: [35, 45, 15, 5]
        },
        revenueData: {
          labels: ['9月', '10月', '11月'],
          data: [1890, 2450, 1500]
        }
      }
    },
    handleTimeRangeChange(range) {
      this.analyticsTimeRange = range
      // 在实际应用中，这里会根据时间范围重新加载数据
      this.showAlert('时间范围已更新', `已切换到最近${range}天的数据`, 'info')
    },
    editVideo(video) {
      this.showAlert('编辑视频', `编辑视频: ${video.title}`, 'info')
      // 在实际应用中，这里会跳转到视频编辑页面
    },
    deleteVideo(video) {
      this.videoToDelete = video
      this.deleteVideoTitle = video.title
      this.showDeleteModal = true
    },
    publishVideo(video) {
      video.status = 'published'
      video.publishedAt = new Date().toISOString().split('T')[0]
      this.showAlert('发布成功', `视频 "${video.title}" 已发布`, 'success')
    },
    unpublishVideo(video) {
      this.videoToUnpublish = video
      this.unpublishVideoTitle = video.title
      this.showUnpublishModal = true
    },
    confirmDeleteVideo() {
      if (this.videoToDelete) {
        this.userVideos = this.userVideos.filter(v => v.id !== this.videoToDelete.id)
        this.showAlert('删除成功', `视频 "${this.videoToDelete.title}" 已删除`, 'success')
      }
      this.cancelDeleteVideo()
    },
    cancelDeleteVideo() {
      this.showDeleteModal = false
      this.videoToDelete = null
      this.deleteVideoTitle = ''
    },
    confirmUnpublishVideo() {
      if (this.videoToUnpublish) {
        this.videoToUnpublish.status = 'draft'
        this.videoToUnpublish.publishedAt = null
        this.showAlert('下架成功', `视频 "${this.videoToUnpublish.title}" 已下架`, 'success')
      }
      this.cancelUnpublishVideo()
    },
    cancelUnpublishVideo() {
      this.showUnpublishModal = false
      this.videoToUnpublish = null
      this.unpublishVideoTitle = ''
    },
    updateProfile(profileData) {
      // 在实际应用中，这里会调用API更新用户资料
      Object.assign(this.user, profileData)
      this.showAlert('更新成功', '个人资料已更新', 'success')
    },
    updatePassword(passwordData) {
      // 在实际应用中，这里会调用API更新密码
      this.showAlert('更新成功', '密码已更新', 'success')
    },
    updateNotifications(notificationSettings) {
      // 在实际应用中，这里会调用API更新通知设置
      this.showAlert('更新成功', '通知设置已更新', 'success')
    },
    showAlert(title, message, type = 'info') {
      alert(`${title}: ${message}`)
    }
  }
}
</script>