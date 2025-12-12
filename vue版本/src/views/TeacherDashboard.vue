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
              <!-- <div class="sidebar-child" @click="goToPage('/article-management')">
                <i class="fa fa-file-text-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">稿件管理</span>
              </div> -->
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
              <div class="text-sm text-secondary mt-1 flex items-center gap-3">
                <button 
                  class="flex items-center gap-1 hover:text-primary transition-colors"
                  @click="syncData"
                >
                  <i class="fa fa-refresh"></i>
                  <span>同步数据</span>
                </button>
                <span>|</span>
                <span>最后同步时间: {{ lastSyncTime }}</span>
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
                  <h3 class="font-medium text-dark">{{ chartTitle }}</h3>
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
                    <div class="stat-card-value">{{ videoStats.totalPlayCount }}</div>
                    <div class="stat-card-change" :class="videoStats.totalPlayCountChange.direction">
                      <i :class="videoStats.totalPlayCountChange.icon"></i>
                      <span>{{ videoStats.totalPlayCountChange.value }}</span>
                    </div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-card-label">粉丝数</div>
                    <div class="stat-card-value">{{ videoStats.fansCount }}</div>
                    <div class="stat-card-change" :class="videoStats.fansCountChange.direction">
                      <i :class="videoStats.fansCountChange.icon"></i>
                      <span>{{ videoStats.fansCountChange.value }}</span>
                    </div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-card-label">总视频数</div>
                    <div class="stat-card-value">{{ videoStats.totalVideos }}</div>
                    <div class="stat-card-change">
                      <span>--</span>
                    </div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-card-label">总评论数</div>
                    <div class="stat-card-value">{{ videoStats.totalComments }}</div>
                    <div class="stat-card-change" :class="videoStats.totalCommentsChange.direction">
                      <i :class="videoStats.totalCommentsChange.icon"></i>
                      <span>{{ videoStats.totalCommentsChange.value }}</span>
                    </div>
                  </div>
                </div>
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mt-4 text-sm">
                  <div class="flex items-center gap-2">
                    <span class="text-secondary">视频类型:</span>
                    <select 
                      v-model="selectedVideoType" 
                      class="border border-gray-200 rounded px-2 py-1 text-sm"
                      @change="updateDataByType"
                    >
                      <option value="all">全部</option>
                      <option value="operating-system">操作系统</option>
                      <option value="iot">物联网</option>
                      <option value="network">计算机网络</option>
                      <option value="data-structure">数据结构</option>
                      <option value="database">数据库原理</option>
                    </select>
                  </div>
                  <div class="flex flex-wrap items-center gap-2">
                    <span class="text-secondary">开始日期</span>
                    <input 
                      type="date" 
                      v-model="startDate" 
                      class="border border-gray-200 rounded px-2 py-1 text-sm"
                      @change="updateDataByDate"
                    >
                    <span class="text-secondary">--</span>
                    <input 
                      type="date" 
                      v-model="endDate" 
                      class="border border-gray-200 rounded px-2 py-1 text-sm"
                      @change="updateDataByDate"
                    >
                  </div>
                </div>
              </div>

              <!-- 课程数据 -->
              <div class="card p-4 card-shadow">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="font-medium text-dark">课程数据</h3>
                  <button 
                    class="text-link flex items-center gap-1"
                    @click="toggleAllCourses"
                  >
                    {{ showAllCourses ? '收起列表' : '视频列表' }}
                    <i :class="showAllCourses ? 'fa fa-angle-down' : 'fa fa-angle-right'"></i>
                  </button>
                </div>

                <!-- 课程列表 -->
                <div class="space-y-2">
                  <!-- 课程项 -->
                  <div 
                    v-for="course in courses" 
                    :key="course.id" 
                    class="course-item cursor-pointer hover:bg-gray-50 transition-colors duration-200" 
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
                          <div class="course-item-stat" :class="course.increaseDirection">
                            <i :class="course.increaseIcon"></i>
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
              <!-- 公告 -->
              <div class="card p-4 card-shadow">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="font-medium text-dark">公告</h3>
                  <button 
                    class="text-xs text-link"
                    @click="toggleAnnouncementExpand"
                  >
                    {{ showFullAnnouncement ? '收起' : '查看更多' }}
                  </button>
                </div>
                <div class="space-y-2 text-xs text-secondary">
                  <div class="line-clamp-1" v-if="!showFullAnnouncement">
                    {{ announcements[0] }}
                  </div>
                  <div v-else class="space-y-2">
                    <div v-for="(announcement, index) in announcements" :key="index">
                      {{ announcement }}
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
import Chart from 'chart.js/auto'

export default {
  name: 'TeacherDashboard',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      activeSubmenu: 'dashboard',
      showFullAnnouncement: false,
      selectedVideoType: 'all',
      startDate: '2023-11-01',
      endDate: '2023-11-07',
      lastSyncTime: '2023-11-01 11:00',
      chartTitle: '总播放量数据(近7日)',
      showAllCourses: false, // 控制是否显示所有课程
      expandedCourses: [],   // 展开后的课程列表
      originalCourses: [],   // 原始课程列表（用于备份）
      announcements: [
        '内容即将审核完成',
        '视频内容一、二审核通过',
        '新功能上线：数据分析模块',
        '系统将于本周五凌晨进行维护',
        '新增视频分类：人工智能入门',
        '教师培训课程已上线',
        '欢迎新教师加入平台'
      ],
      videoStats: {
        totalPlayCount: '1234.5w',
        totalPlayCountChange: {
          value: '1245w',
          direction: 'up',
          icon: 'fa fa-caret-up'
        },
        fansCount: '1234.5w',
        fansCountChange: {
          value: '1245w',
          direction: 'up',
          icon: 'fa fa-caret-up'
        },
        totalVideos: '1234',
        totalComments: '1234.5w',
        totalCommentsChange: {
          value: '1245w',
          direction: 'up',
          icon: 'fa fa-caret-up'
        }
      },
      courses: [
        { 
          id: 1, 
          name: '操作系统课程', 
          avatar: 'https://picsum.photos/32/32?random=1',
          playCount: '1234.5w',
          increase: '1245w',
          increaseIcon: 'fa fa-caret-up text-success',
          increaseDirection: 'text-success',
          viewCount: '1234.5w',
          userCount: '1245w'
        },
        { 
          id: 2, 
          name: '物联网课程', 
          avatar: 'https://picsum.photos/32/32?random=2',
          playCount: '1234.5w',
          increase: '1245w',
          increaseIcon: 'fa fa-caret-up text-success',
          increaseDirection: 'text-success',
          viewCount: '1234.5w',
          userCount: '1245w'
        },
        { 
          id: 3, 
          name: '计算机网络课程', 
          avatar: 'https://picsum.photos/32/32?random=3',
          playCount: '1234.5w',
          increase: '1245w',
          increaseIcon: 'fa fa-caret-up text-success',
          increaseDirection: 'text-success',
          viewCount: '1234.5w',
          userCount: '1245w'
        }
      ],
      chartInstance: null
    }
  },
  mounted() {
    this.initChart()
    this.generateAllCourses() // 生成所有课程数据
  },
  beforeUnmount() {
    try {
      if (this.chartInstance && this.chartInstance.destroy) {
        this.chartInstance.destroy()
      }
    } catch (error) {
      console.warn('图表销毁时出错:', error.message)
    }
    this.chartInstance = null
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

    goToCourseList() {
      this.$router.push('/course-list')
    },

    toggleAnnouncementExpand() {
      this.showFullAnnouncement = !this.showFullAnnouncement
    },

    syncData() {
      this.generateRandomData()
      this.updateLastSyncTime()
    },

    updateLastSyncTime() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const hours = String(now.getHours()).padStart(2, '0')
      const minutes = String(now.getMinutes()).padStart(2, '0')
      this.lastSyncTime = `${year}-${month}-${day} ${hours}:${minutes}`
    },

    updateDataByType() {
      this.generateRandomData()
      this.updateChartTitle()
    },

    updateDataByDate() {
      this.generateRandomData()
      this.updateChartTitle()
    },

    updateChartTitle() {
      const days = this.getDateRangeDays()
      const typeMap = {
        'all': '全部',
        'operating-system': '操作系统',
        'iot': '物联网',
        'network': '计算机网络',
        'data-structure': '数据结构',
        'database': '数据库原理'
      }
      const typeText = typeMap[this.selectedVideoType] || '全部'
      this.chartTitle = `${typeText}播放量数据(近${days}日)`
    },

    getDateRangeDays() {
      const start = new Date(this.startDate)
      const end = new Date(this.endDate)
      const diffTime = Math.abs(end - start)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      return diffDays + 1
    },

    generateRandomData() {
      // 生成随机的图表数据
      const days = this.getDateRangeDays()
      const dates = []
      const playCounts = []
      
      let currentDate = new Date(this.startDate)
      for (let i = 0; i < days; i++) {
        const dateStr = currentDate.toISOString().split('T')[0]
        dates.push(dateStr)
        playCounts.push(Math.floor(Math.random() * 40000) + 5000)
        
        currentDate.setDate(currentDate.getDate() + 1)
      }
      
      // 更新图表
      this.updateChart(dates, playCounts)
      
      // 更新视频统计数据
      this.updateVideoStats()
      
      // 更新课程数据
      this.updateCoursesData()
    },

    updateChart(dates, data) {
      if (this.chartInstance) {
        this.chartInstance.destroy()
      }
      
      const ctx = document.getElementById('playCountChart')
      if (!ctx) return
      
      this.chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: dates,
          datasets: [{
            label: '总播放量',
            data: data,
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
    },

    updateVideoStats() {
      const randomUpDown = () => Math.random() > 0.5 ? 'up' : 'down'
      const randomValue = () => (Math.random() * 1000).toFixed(1) + 'w'
      const randomIcon = (direction) => direction === 'up' ? 'fa fa-caret-up' : 'fa fa-caret-down'
      
      const totalPlayCountChange = {
        direction: randomUpDown(),
        value: randomValue()
      }
      totalPlayCountChange.icon = randomIcon(totalPlayCountChange.direction)
      
      const fansCountChange = {
        direction: randomUpDown(),
        value: randomValue()
      }
      fansCountChange.icon = randomIcon(fansCountChange.direction)
      
      const totalCommentsChange = {
        direction: randomUpDown(),
        value: randomValue()
      }
      totalCommentsChange.icon = randomIcon(totalCommentsChange.direction)
      
      this.videoStats = {
        totalPlayCount: (Math.random() * 2000 + 1000).toFixed(1) + 'w',
        totalPlayCountChange,
        fansCount: (Math.random() * 2000 + 1000).toFixed(1) + 'w',
        fansCountChange,
        totalVideos: Math.floor(Math.random() * 1000 + 500).toString(),
        totalComments: (Math.random() * 2000 + 1000).toFixed(1) + 'w',
        totalCommentsChange
      }
    },

    generateAllCourses() {
      const courseTypes = [
        '操作系统', '物联网', '计算机网络', '数据结构', '数据库原理',
        '人工智能', '软件工程', '编译原理', '计算机组成原理', '算法设计',
        '机器学习', '深度学习', 'Web开发', '移动开发', '网络安全'
      ]

      this.expandedCourses = Array.from({ length: 12 }, (_, i) => {
        const randomUpDown = Math.random() > 0.5 ? 'up' : 'down'
        const increaseValue = (Math.random() * 500).toFixed(1) + 'w'

        return {
          id: i + 1,
          name: `${courseTypes[i % courseTypes.length]}课程`,
          avatar: `https://picsum.photos/32/32?random=${i + 1}`,
          playCount: (Math.random() * 2000 + 1000).toFixed(1) + 'w',
          increase: increaseValue,
          increaseIcon: randomUpDown === 'up' ? 'fa fa-caret-up text-success' : 'fa fa-caret-down text-error',
          increaseDirection: randomUpDown === 'up' ? 'text-success' : 'text-error',
          viewCount: (Math.random() * 2000 + 1000).toFixed(1) + 'w',
          userCount: (Math.random() * 2000 + 1000).toFixed(1) + 'w'
        }
      })

      // 初始只显示前3个
      this.courses = this.expandedCourses.slice(0, 3)
      this.originalCourses = [...this.courses]
    },

    // 修改 updateCoursesData 方法
    updateCoursesData() {
      if (this.showAllCourses) {
        this.courses = [...this.expandedCourses]
      } else {
        this.courses = this.expandedCourses.slice(0, 3)
      }
    },
    
    toggleAllCourses() {
      this.showAllCourses = !this.showAllCourses
      this.updateCoursesData()
    },

    initChart() {
      this.generateRandomData()
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
  @apply text-error;
}
.text-error {
  color: #F53F3F;
}

/* 课程项 */
.course-item {
  @apply flex items-center justify-between py-3 border-b border-gray-100;
}
.course-item:hover {
  @apply bg-gray-50;
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

/* 图表工具提示 */
.chart-tooltip {
  @apply absolute bg-white p-2 rounded shadow-md border border-gray-200 text-sm z-50 whitespace-nowrap;
}
.chart-highlight {
  @apply bg-primary/5 absolute top-0 bottom-0 w-[12.5%] border-x border-primary/20 pointer-events-none;
}
</style>