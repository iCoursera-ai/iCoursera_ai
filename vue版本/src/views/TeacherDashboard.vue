<template>
  <div class="font-inter bg-gray-50 min-h-screen flex flex-col">
    <Header />
    
    <div class="flex flex-1">
      <!-- 侧边栏导航 -->
      <aside class="w-64 bg-white border-r border-gray-200 flex-shrink-0 h-[calc(100vh-5rem)] sticky top-[5rem] overflow-y-auto z-30">
        <nav class="py-4 space-y-1">
          <!-- 教师管理 -->
          <div class="sidebar-group">
            <div class="sidebar-parent active" @click="toggleSubmenu('dashboard')">
              <div class="sidebar-parent-content">
                <i class="fa fa-tachometer sidebar-icon"></i>
                <span>教师管理</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200" :class="{'rotate-icon': activeSubmenu === 'dashboard'}"></i>
            </div>
            <div id="submenu-dashboard" class="bg-gray-50" :class="{'hidden': activeSubmenu !== 'dashboard'}">
              <div class="sidebar-child active">
                <i class="fa fa-circle-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">工作台</span>
              </div>
            </div>
          </div>

          <!-- 管理员管理 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" @click="toggleSubmenu('admin')">
              <div class="sidebar-parent-content">
                <i class="fa fa-user-secret sidebar-icon"></i>
                <span>管理员管理</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200" :class="{'rotate-icon': activeSubmenu === 'admin'}"></i>
            </div>
            <div id="submenu-admin" class="bg-gray-50" :class="{'hidden': activeSubmenu !== 'admin'}">
              <div class="sidebar-child" @click="goToPage('/course-management')">
                <i class="fa fa-circle-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">课程管理</span>
              </div>
              <div class="sidebar-child" @click="goToPage('/user-management')">
                <i class="fa fa-circle-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">用户管理</span>
              </div>
            </div>
          </div>
             
          <!-- 收藏管理 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" @click="toggleSubmenu('favorites')">
              <div class="sidebar-parent-content">
                <i class="fa fa-heart sidebar-icon"></i>
                <span>收藏管理</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200" :class="{'rotate-icon': activeSubmenu === 'favorites'}"></i>
            </div>
            <div id="submenu-favorites" class="bg-gray-50" :class="{'hidden': activeSubmenu !== 'favorites'}">
              <div class="sidebar-child" @click="goToFavorites('my-collection')">
                <i class="fa fa-book text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">我的收藏</span>
              </div>
              <div class="sidebar-child" @click="goToFavorites('likes')">
                <i class="fa fa-thumbs-up text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">点赞</span>
              </div>
              <div class="sidebar-child" @click="goToFavorites('history')">
                <i class="fa fa-history text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">历史记录</span>
              </div>
            </div>
          </div>

          <!-- 个人中心 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" @click="toggleSubmenu('user-center')">
              <div class="sidebar-parent-content">
                <i class="fa fa-user-circle-o sidebar-icon"></i>
                <span>个人中心</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200" :class="{'rotate-icon': activeSubmenu === 'user-center'}"></i>
            </div>
            <div id="submenu-user-center" class="bg-gray-50" :class="{'hidden': activeSubmenu !== 'user-center'}">
              <div 
                class="sidebar-child" 
                @click="goToPersonalCenter('user-info')"
              >
                <i class="fa fa-id-card-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">用户信息</span>
              </div>
              <div 
                class="sidebar-child" 
                @click="goToPersonalCenter('user-settings')"
              >
                <i class="fa fa-cog text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">用户设置</span>
              </div>
            </div>
          </div>
        </nav>
      </aside>

      <!-- 主内容区域 -->
      <main class="flex-1 overflow-y-auto p-6" style="max-height: calc(100vh - 5rem);">
        <!-- 面包屑导航 -->
        <div class="text-sm text-secondary mb-6">
          <span>用户中心</span>
          <i class="fa fa-angle-right mx-1 text-gray-400"></i>
          <span>教师管理</span>
          <i class="fa fa-angle-right mx-1 text-gray-400"></i>
          <span class="text-dark font-medium">工作台</span>
        </div>

        <!-- 页面内容容器 -->
        <div class="space-y-6">
          <!-- 工作台头部 -->
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <h2 class="text-xl font-bold text-dark">欢迎回来, 奥利翔</h2>
              <div class="text-sm text-secondary mt-1 flex items-center gap-3">
                <button class="flex items-center gap-1 hover:text-primary transition-colors">
                  <i class="fa fa-refresh"></i>
                  <span>同步数据</span>
                </button>
                <span>|</span>
                <span>最后同步时间: 2023-11-01 11:00</span>
              </div>
            </div>
          </div>

          <!-- 调整图表卡片的外层容器 -->
          <div class="flex flex-col lg:flex-row gap-6">
            <!-- 左侧主体区域 -->
            <div class="flex-1 space-y-6">
              <!-- 总播放量图表 -->
              <div class="card p-4 card-shadow">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="font-medium text-dark">总播放量数据(近7日)</h3>
                  <div class="flex gap-2">
                    <button class="text-xs text-secondary hover:text-primary px-2 py-1">日</button>
                    <button class="text-xs text-secondary hover:text-primary px-2 py-1">周</button>
                    <button class="text-xs text-primary bg-primary/10 px-2 py-1 rounded">月</button>
                  </div>
                </div>
                
                <!-- 图表容器 -->
                <div class="h-64 bg-gray-50 rounded-lg relative w-full">
                  <canvas id="playCountChart" class="w-full h-full"></canvas>
                  <div id="chartHighlight" class="chart-highlight hidden"></div>
                  <div id="chartTooltip" class="chart-tooltip hidden"></div>
                </div>
              </div>

              <!-- 视频播放数据 -->
              <div class="card p-4 card-shadow">
                <h3 class="font-medium text-dark mb-4">视频播放数据</h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
                  <div class="stat-card">
                    <div class="stat-card-label">总播放量</div>
                    <div class="stat-card-value">1234.5w</div>
                    <div class="stat-card-change up">
                      <i class="fa fa-caret-up"></i>
                      <span>1245w</span>
                    </div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-card-label">粉丝数</div>
                    <div class="stat-card-value">1234.5w</div>
                    <div class="stat-card-change up">
                      <i class="fa fa-caret-up"></i>
                      <span>1245w</span>
                    </div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-card-label">总视频数</div>
                    <div class="stat-card-value">1234</div>
                    <div class="stat-card-change">
                      <span>--</span>
                    </div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-card-label">总评论数</div>
                    <div class="stat-card-value">1234.5w</div>
                    <div class="stat-card-change up">
                      <i class="fa fa-caret-up"></i>
                      <span>1245w</span>
                    </div>
                  </div>
                </div>
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mt-4 text-sm">
                  <div class="flex items-center gap-2">
                    <span class="text-secondary">视频类型:</span>
                    <select class="border border-gray-200 rounded px-2 py-1 text-sm">
                      <option>全部</option>
                    </select>
                  </div>
                  <div class="flex flex-wrap items-center gap-2">
                    <span class="text-secondary">开始日期</span>
                    <input type="date" class="border border-gray-200 rounded px-2 py-1 text-sm">
                    <span class="text-secondary">--</span>
                    <input type="date" class="border border-gray-200 rounded px-2 py-1 text-sm">
                  </div>
                </div>
              </div>

              <!-- 课程数据 -->
              <div class="card p-4 card-shadow">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="font-medium text-dark">课程数据</h3>
                  <button class="text-link">视频列表 ></button>
                </div>
                <div class="space-y-2">
                  <!-- 课程项 -->
                  <div 
                    v-for="course in courses" 
                    :key="course.id" 
                    class="course-item cursor-pointer" 
                    @click="goToVideoAnalysis(course.id)"
                  >
                    <div class="course-item-info">
                      <div class="course-item-avatar">
                        <img :src="course.avatar" alt="课程" class="w-full h-full object-cover">
                      </div>
                      <div>
                        <div class="course-item-name">{{ course.name }}</div>
                        <div class="course-item-stats">
                          <div class="course-item-stat">
                            <i class="fa fa-play-circle-o"></i>
                            <span>{{ course.playCount }}</span>
                          </div>
                          <div class="course-item-stat">
                            <i class="fa fa-caret-up text-success"></i>
                            <span>{{ course.increase }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="course-item-stats">
                      <div class="course-item-stat">
                        <i class="fa fa-eye"></i>
                        <span>{{ course.viewCount }}</span>
                      </div>
                      <div class="course-item-stat">
                        <i class="fa fa-user"></i>
                        <span>{{ course.userCount }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 我的课程 -->
              <div class="card p-4 card-shadow">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="font-medium text-dark">我的课程</h3>
                  <button class="text-link">
                    <i class="fa fa-search"></i>
                  </button>
                </div>
                <div class="h-32 bg-gray-50 rounded-lg flex items-center justify-center text-secondary">
                  暂无课程数据
                </div>
              </div>
            </div>

            <!-- 右侧功能栏 -->
            <div class="w-full lg:w-64 space-y-6">
              <!-- 热门功能 -->
              <div class="card p-4 card-shadow">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="font-medium text-dark">热门功能</h3>
                  <span class="text-xs text-secondary">更多</span>
                </div>
                <div class="grid grid-cols-2 gap-3">
                  <button class="flex flex-col items-center p-2 hover:bg-gray-50 rounded">
                    <i class="fa fa-play-circle-o text-primary text-xl mb-1"></i>
                    <span class="text-xs">视频管理</span>
                  </button>
                  <button class="flex flex-col items-center p-2 hover:bg-gray-50 rounded">
                    <i class="fa fa-line-chart text-primary text-xl mb-1"></i>
                    <span class="text-xs">内容统计</span>
                  </button>
                  <button class="flex flex-col items-center p-2 hover:bg-gray-50 rounded">
                    <i class="fa fa-bar-chart text-primary text-xl mb-1"></i>
                    <span class="text-xs">流量管理</span>
                  </button>
                  <button class="flex flex-col items-center p-2 hover:bg-gray-50 rounded">
                    <i class="fa fa-upload text-primary text-xl mb-1"></i>
                    <span class="text-xs">线上推广</span>
                  </button>
                  <button class="flex flex-col items-center p-2 hover:bg-gray-50 rounded">
                    <i class="fa fa-bell text-warning text-xl mb-1"></i>
                    <span class="text-xs">内容违规</span>
                  </button>
                </div>
              </div>

              <!-- 后台提问 -->
              <div class="card p-4 card-shadow">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="font-medium text-dark">后台提问</h3>
                  <span class="text-xs text-link">全部 ></span>
                </div>
                <div class="space-y-3 text-sm">
                  <div class="flex gap-2">
                    <span class="text-secondary">学生1:</span>
                    <span>老师我这么做对吗？</span>
                  </div>
                  <div class="flex gap-2">
                    <span class="text-secondary">学生2:</span>
                    <span>老师，这个知识点不太懂</span>
                  </div>
                  <div class="flex gap-2">
                    <span class="text-secondary">学生3:</span>
                    <span>怎么破解这个问题？</span>
                  </div>
                </div>
              </div>

              <!-- 公告 -->
              <div class="card p-4 card-shadow">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="font-medium text-dark">公告</h3>
                  <span class="text-xs text-link">查看更多</span>
                </div>
                <div class="space-y-2 text-xs text-secondary">
                  <div class="line-clamp-1">内容即将审核完成</div>
                  <div class="line-clamp-1">视频内容一、二审核通过</div>
                  <div class="line-clamp-1">新功能上线：数据分析模块</div>
                </div>
              </div>

              <!-- 视频TOP -->
              <div class="card p-4 card-shadow">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="font-medium text-dark">视频TOP</h3>
                  <select class="text-xs border border-gray-200 rounded px-1 py-0.5">
                    <option>近7天</option>
                  </select>
                </div>
                
                <!-- 视频TOP标签按钮 -->
                <div class="video-top-tabs">
                  <div 
                    v-for="tab in videoTopTabs" 
                    :key="tab.type"
                    class="video-top-tab" 
                    :class="{ 'active': activeVideoTab === tab.type }"
                    @click="switchVideoTab(tab.type)"
                  >
                    {{ tab.label }}
                  </div>
                </div>
                
                <!-- 视频TOP内容 -->
                <div class="video-top-content">
                  <div v-for="tab in videoTopTabs" :key="tab.type" class="video-top-list" :class="{ 'hidden': activeVideoTab !== tab.type }">
                    <div class="space-y-3">
                      <div 
                        v-for="(item, index) in videoTopData[tab.type]" 
                        :key="item.id"
                        class="flex justify-between items-center"
                      >
                        <div class="flex items-center gap-2">
                          <span class="w-5 h-5 rounded-full flex items-center justify-center text-xs" :class="getRankClass(index)">
                            {{ index + 1 }}
                          </span>
                          <span class="text-sm">{{ item.name }}</span>
                        </div>
                        <span class="text-sm">{{ item.value }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'TeacherDashboard',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      activeSubmenu: 'dashboard',
      activeVideoTab: 'play',
      courses: [
        { 
          id: 1, 
          name: '操作系统课程', 
          avatar: 'https://picsum.photos/32/32?random=1',
          playCount: '1234.5w',
          increase: '1245w',
          viewCount: '1234.5w',
          userCount: '1245w'
        },
        { 
          id: 2, 
          name: '物联网课程', 
          avatar: 'https://picsum.photos/32/32?random=2',
          playCount: '1234.5w',
          increase: '1245w',
          viewCount: '1234.5w',
          userCount: '1245w'
        },
        { 
          id: 3, 
          name: '计算机网络课程', 
          avatar: 'https://picsum.photos/32/32?random=3',
          playCount: '1234.5w',
          increase: '1245w',
          viewCount: '1234.5w',
          userCount: '1245w'
        }
      ],
      videoTopTabs: [
        { type: 'play', label: '播放' },
        { type: 'like', label: '点赞' },
        { type: 'comment', label: '评论' },
        { type: 'share', label: '分享' },
        { type: 'collect', label: '收藏' }
      ],
      videoTopData: {
        play: [
          { id: 1, name: '操作系统', value: '1234.5w' },
          { id: 2, name: '物联网', value: '1200.0w' },
          { id: 3, name: '数据结构', value: '1100.0w' }
        ],
        like: [
          { id: 4, name: '计算机网络', value: '876.2w' },
          { id: 5, name: '操作系统', value: '765.1w' },
          { id: 6, name: '数据库原理', value: '654.0w' }
        ],
        comment: [
          { id: 7, name: '物联网', value: '123.4w' },
          { id: 8, name: '计算机网络', value: '112.3w' },
          { id: 9, name: '操作系统', value: '101.2w' }
        ],
        share: [
          { id: 10, name: '数据结构', value: '98.7w' },
          { id: 11, name: '物联网', value: '87.6w' },
          { id: 12, name: '计算机网络', value: '76.5w' }
        ],
        collect: [
          { id: 13, name: '操作系统', value: '156.7w' },
          { id: 14, name: '数据结构', value: '145.6w' },
          { id: 15, name: '数据库原理', value: '134.5w' }
        ]
      },
      chartInstance: null
    }
  },
  mounted() {
    this.initChart()
  },
  beforeUnmount() {
    if (this.chartInstance) {
      this.chartInstance.destroy()
    }
  },
  methods: {
    toggleSubmenu(submenu) {
      this.activeSubmenu = this.activeSubmenu === submenu ? null : submenu
    },

    goToPage(path) {
      this.$router.push(path)
    },
    
    goToFavorites(tab) {
      this.$router.push({
        path: '/favorites-management',
        query: { tab }
      })
    },
    
    toggleSubmenu(submenu) {
      this.activeSubmenu = this.activeSubmenu === submenu ? null : submenu
    },

    goToPersonalCenter(page = 'user-info') {
      this.$router.push({ 
        path: '/personal-information',
        query: { page }
      })
    },

    goToVideoAnalysis(videoId) {
      this.$router.push({ 
        path: '/video-analysis',
        query: { videoId }
      })
    },

    switchVideoTab(tabType) {
      this.activeVideoTab = tabType
    },

    goToWorkEngine() {
      this.$router.push('/work-engine')
    },
    
    goToCourseManagement() {
      this.$router.push('/course-management')
    },
    
    goToUserManagement() {
      this.$router.push('/user-management')
    },
    

    getRankClass(index) {
      if (index === 0) return 'bg-primary text-white'
      if (index === 1) return 'bg-gray-300 text-white'
      if (index === 2) return 'bg-warning/30 text-warning'
      return 'bg-gray-200 text-gray-700'
    },

    initChart() {
      const dates = ['2023-11-01', '2023-11-02', '2023-11-03', '2023-11-04', '2023-11-05', '2023-11-06', '2023-11-07', '2023-11-08']
      const playCounts = [8000, 15000, 39068, 35000, 20000, 32000, 25000, 12000]
      
      const ctx = document.getElementById('playCountChart')
      if (!ctx) return
      
      if (this.chartInstance) {
        this.chartInstance.destroy()
      }
      
      this.chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: dates,
          datasets: [{
            label: '总播放量',
            data: playCounts,
            borderColor: '#165DFF',
            backgroundColor: 'rgba(22, 93, 255, 0.05)',
            borderWidth: 2.5,
            pointBackgroundColor: '#FFFFFF',
            pointBorderColor: '#165DFF',
            pointBorderWidth: 2,
            pointRadius: 5,
            pointHoverRadius: 7,
            tension: 0.4,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: {
            duration: 1000,
            easing: 'easeOutQuart'
          },
          interaction: {
            mode: 'index',
            intersect: false,
          },
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            x: {
              grid: {
                display: false
              },
              ticks: {
                maxRotation: 0,
                color: '#6B7280'
              }
            },
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
              },
              ticks: {
                callback: function(value) {
                  if (value >= 1000) {
                    return (value / 1000) + 'k'
                  }
                  return value
                },
                color: '#6B7280'
              }
            }
          }
        }
      })
    }
  }
}
</script>

<style scoped>
/* 侧边栏样式 */
.sidebar-parent {
  @apply flex items-center justify-between px-4 py-3 text-gray-500 hover:bg-primary/5 hover:text-primary transition-all duration-200 cursor-pointer;
}
.sidebar-parent.active {
  @apply bg-primary/10 text-primary font-medium;
}
.sidebar-parent-content {
  @apply flex items-center gap-2;
}
.sidebar-child {
  @apply flex items-center px-6 py-2 text-gray-500 hover:bg-primary/5 hover:text-primary transition-all duration-200 cursor-pointer text-sm;
}
.sidebar-child.active {
  @apply bg-primary/10 text-primary font-medium;
}
.sidebar-child-text {
  @apply ml-3;
}
.sidebar-icon {
  @apply w-4 text-center;
}
.rotate-icon {
  @apply transform transition-transform duration-200 rotate-90;
}

/* 卡片样式 */
.card {
  @apply bg-white rounded-lg border border-gray-200 shadow-sm;
}
.card-shadow {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.02);
}

/* 链接样式 */
.text-link {
  @apply text-primary hover:text-primary/80 transition-colors duration-200 cursor-pointer;
}

/* 统计卡片 */
.stat-card {
  @apply bg-white rounded-lg border border-gray-200 p-3 flex flex-col justify-between;
}
.stat-card-value {
  @apply text-xl font-bold text-dark;
}
.stat-card-label {
  @apply text-xs text-secondary mb-1;
}
.stat-card-change {
  @apply text-xs flex items-center gap-1 mt-1;
}
.stat-card-change.up {
  @apply text-success;
}
.stat-card-change.down {
  color: #F53F3F;
}

/* 课程项 */
.course-item {
  @apply flex items-center justify-between py-3 border-b border-gray-100;
}
.course-item-info {
  @apply flex items-center gap-3;
}
.course-item-avatar {
  @apply w-8 h-8 rounded-full overflow-hidden;
}
.course-item-name {
  @apply font-medium text-dark;
}
.course-item-stats {
  @apply flex gap-4 text-xs text-secondary;
}
.course-item-stat {
  @apply flex items-center gap-1;
}

/* 视频TOP标签 */
.video-top-tabs {
  @apply flex border-b border-gray-200 mb-3;
}
.video-top-tab {
  @apply px-2 py-1 text-xs cursor-pointer hover:text-primary transition-colors;
}
.video-top-tab.active {
  @apply text-primary border-b-2 border-primary font-medium;
}

/* 图表工具提示 */
.chart-tooltip {
  @apply absolute bg-white p-2 rounded shadow-md border border-gray-200 text-sm z-50 whitespace-nowrap;
}
.chart-highlight {
  @apply bg-primary/5 absolute top-0 bottom-0 w-[12.5%] border-x border-primary/20 pointer-events-none;
}
</style>