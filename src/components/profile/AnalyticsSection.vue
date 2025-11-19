<template>
  <div class="analytics-section">
    <div class="analytics-header">
      <h2 class="analytics-title">视频数据分析</h2>
      <div class="date-filter">
        <select 
          :value="timeRange" 
          @change="handleTimeRangeChange"
        >
          <option value="7">最近7天</option>
          <option value="30">最近30天</option>
          <option value="90">最近90天</option>
          <option value="365">最近1年</option>
        </select>
      </div>
    </div>

    <div class="video-selector">
      <select v-model="selectedVideo" @change="handleVideoChange">
        <option value="all">所有视频</option>
        <option v-for="video in videos" :key="video.id" :value="video.id">
          {{ video.title }}
        </option>
      </select>
    </div>

    <div class="analytics-overview">
      <div class="stat-card">
        <div class="stat-number">{{ currentVideoStats.totalViews.toLocaleString() }}</div>
        <div class="stat-label">总观看次数</div>
        <div class="stat-change positive">+12% 较上月</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ currentVideoStats.completionRate }}%</div>
        <div class="stat-label">平均完成率</div>
        <div class="stat-change positive">+3% 较上月</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ currentVideoStats.engagementRate }}%</div>
        <div class="stat-label">互动率</div>
        <div class="stat-change positive">+0.8% 较上月</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ currentVideoStats.averageRating }}</div>
        <div class="stat-label">平均评分</div>
        <div class="stat-change positive">+0.2 较上月</div>
      </div>
    </div>

    <!-- 用户行为时间线分析 -->
    <div class="behavior-analysis-section">
      <h3 class="section-title">用户行为时间线分析</h3>
      <div class="behavior-controls">
        <div class="control-group">
          <label>行为类型:</label>
          <select v-model="selectedBehavior" @change="updateBehaviorChart">
            <option value="all">全部行为</option>
            <option value="play">播放</option>
            <option value="pause">暂停</option>
            <option value="seek">跳转</option>
            <option value="speed">变速</option>
            <option value="like">点赞</option>
            <option value="favorite">收藏</option>
            <option value="comment">评论</option>
          </select>
        </div>
        <div class="control-group">
          <label>时间粒度:</label>
          <select v-model="timeGranularity" @change="updateBehaviorChart">
            <option value="second">秒级</option>
            <option value="minute">分钟级</option>
            <option value="segment">片段级</option>
          </select>
        </div>
      </div>
      
      <div class="behavior-chart-container">
        <div class="chart-container">
          <h4 class="chart-subtitle">行为密度热力图</h4>
          <div class="chart-wrapper">
            <canvas ref="behaviorHeatmapChart"></canvas>
          </div>
        </div>
        
        <div class="chart-container">
          <h4 class="chart-subtitle">行为时间分布</h4>
          <div class="chart-wrapper">
            <canvas ref="behaviorTimelineChart"></canvas>
          </div>
        </div>
      </div>

      <!-- 详细行为统计 -->
      <div class="behavior-stats-grid">
        <div class="behavior-stat-card">
          <div class="behavior-icon pause">
            <i class="fas fa-pause"></i>
          </div>
          <div class="behavior-info">
            <div class="behavior-count">{{ currentVideoStats.pauseCount || 0 }}</div>
            <div class="behavior-label">暂停次数</div>
            <div class="behavior-detail">平均每观看者暂停 {{ currentVideoStats.avgPausesPerViewer || 0 }} 次</div>
          </div>
        </div>
        
        <div class="behavior-stat-card">
          <div class="behavior-icon seek">
            <i class="fas fa-redo"></i>
          </div>
          <div class="behavior-info">
            <div class="behavior-count">{{ currentVideoStats.rewindCount || 0 }}</div>
            <div class="behavior-label">回退次数</div>
            <div class="behavior-detail">主要回退点: {{ (currentVideoStats.topRewindPoints || []).join(', ') }}</div>
          </div>
        </div>
        
        <div class="behavior-stat-card">
          <div class="behavior-icon speed">
            <i class="fas fa-tachometer-alt"></i>
          </div>
          <div class="behavior-info">
            <div class="behavior-count">{{ currentVideoStats.speedChangeCount || 0 }}</div>
            <div class="behavior-label">变速次数</div>
            <div class="behavior-detail">{{ (currentVideoStats.speedStats || {}).normal || 0 }}% 正常速度</div>
          </div>
        </div>
        
        <div class="behavior-stat-card">
          <div class="behavior-icon like">
            <i class="fas fa-heart"></i>
          </div>
          <div class="behavior-info">
            <div class="behavior-count">{{ currentVideoStats.likeCount || 0 }}</div>
            <div class="behavior-label">点赞数</div>
            <div class="behavior-detail">点赞率: {{ currentVideoStats.likeRate || 0 }}%</div>
          </div>
        </div>
      </div>

      <!-- 关键时间点分析 -->
      <div class="key-moments-section">
        <h4 class="subsection-title">关键时间点分析</h4>
        <div class="moments-grid">
          <div class="moment-card" v-for="moment in keyMoments" :key="moment.time">
            <div class="moment-time">{{ formatTime(moment.time) }}</div>
            <div class="moment-type" :class="moment.type">{{ getMomentTypeLabel(moment.type) }}</div>
            <div class="moment-intensity">
              <div class="intensity-bar">
                <div class="intensity-fill" :style="{ width: moment.intensity + '%' }"></div>
              </div>
              <span class="intensity-text">{{ moment.intensity }}%</span>
            </div>
            <div class="moment-description">{{ moment.description }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="analytics-charts">
      <div class="chart-container">
        <h3 class="chart-title">观看趋势</h3>
        <div class="chart-wrapper">
          <canvas ref="viewsChart"></canvas>
        </div>
      </div>
      
      <div class="chart-container">
        <h3 class="chart-title">用户互动分布</h3>
        <div class="chart-wrapper">
          <canvas ref="engagementChart"></canvas>
        </div>
      </div>
      
      <div class="chart-container">
        <h3 class="chart-title">观众年龄分布</h3>
        <div class="chart-wrapper">
          <canvas ref="audienceChart"></canvas>
        </div>
      </div>
      
      <div class="chart-container">
        <h3 class="chart-title">收入趋势</h3>
        <div class="chart-wrapper">
          <canvas ref="revenueChart"></canvas>
        </div>
      </div>
    </div>

    <div class="analytics-details">
      <div class="detail-section">
        <h3>关键指标</h3>
        <div class="metrics-grid">
          <div class="metric-item">
            <div class="metric-label">平均观看时长</div>
            <div class="metric-value">{{ currentVideoStats.averageWatchTime || '0分0秒' }}</div>
            <div class="metric-change positive">+45秒</div>
          </div>
          <div class="metric-item">
            <div class="metric-label">互动率</div>
            <div class="metric-value">{{ currentVideoStats.engagementRate || 0 }}%</div>
            <div class="metric-change positive">+0.3%</div>
          </div>
          <div class="metric-item">
            <div class="metric-label">分享率</div>
            <div class="metric-value">2.1%</div>
            <div class="metric-change positive">+0.5%</div>
          </div>
          <div class="metric-item">
            <div class="metric-label">退播率</div>
            <div class="metric-value">{{ currentVideoStats.dropOffRate || 0 }}%</div>
            <div class="metric-change negative">-2%</div>
          </div>
        </div>
      </div>

      <div class="detail-section">
        <h3>热门时段分析</h3>
        <div class="time-distribution">
          <div class="time-slot" v-for="slot in timeSlots" :key="slot.time">
            <div class="time-label">{{ slot.time }}</div>
            <div class="time-bar">
              <div class="time-fill" :style="{ width: slot.percentage + '%' }"></div>
            </div>
            <div class="time-percentage">{{ slot.percentage }}%</div>
          </div>
        </div>
      </div>

      <div class="detail-section">
        <h3>设备分布</h3>
        <div class="device-distribution">
          <div class="device-item" v-for="device in deviceData" :key="device.type">
            <div class="device-info">
              <i :class="device.icon"></i>
              <span class="device-type">{{ device.type }}</span>
            </div>
            <div class="device-stats">
              <span class="device-percentage">{{ device.percentage }}%</span>
              <span class="device-count">{{ device.count }}次观看</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="analytics-actions">
      <button class="btn btn-outline" @click="exportData">
        <i class="fas fa-download"></i> 导出数据
      </button>
      <button class="btn btn-primary" @click="generateReport">
        <i class="fas fa-chart-line"></i> 生成详细报告
      </button>
    </div>
  </div>
</template>

<script>
import { 
  Chart, 
  LineController, 
  BarController, 
  DoughnutController, 
  CategoryScale, 
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'

// 注册所需的组件
Chart.register(
  LineController,
  BarController,
  DoughnutController,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Tooltip,
  Legend
)

export default {
  name: 'AnalyticsSection',
  props: {
    analyticsData: {
      type: Object,
      required: true
    },
    timeRange: {
      type: String,
      default: '30'
    }
  },
  data() {
    return {
      selectedVideo: 'all',
      selectedBehavior: 'all',
      timeGranularity: 'minute',
      videos: [
        { 
          id: 1, 
          title: '机器学习入门教程',
          duration: 930,
          behaviorData: this.generateBehaviorData(930)
        },
        { 
          id: 2, 
          title: 'Python数据分析实战',
          duration: 1545,
          behaviorData: this.generateBehaviorData(1545)
        },
        { 
          id: 3, 
          title: 'Vue 3 高级技巧',
          duration: 1935,
          behaviorData: this.generateBehaviorData(1935)
        }
      ],
      timeSlots: [
        { time: '00-04时', percentage: 5 },
        { time: '04-08时', percentage: 8 },
        { time: '08-12时', percentage: 25 },
        { time: '12-16时', percentage: 22 },
        { time: '16-20时', percentage: 30 },
        { time: '20-24时', percentage: 10 }
      ],
      deviceData: [
        { type: '桌面端', percentage: 45, count: 5604, icon: 'fas fa-desktop' },
        { type: '移动端', percentage: 50, count: 6228, icon: 'fas fa-mobile-alt' },
        { type: '平板', percentage: 5, count: 624, icon: 'fas fa-tablet-alt' }
      ],
      charts: {},
      currentVideoStats: this.getDefaultVideoStats(),
      keyMoments: [],
      isMounted: false // 添加挂载状态标识
    }
  },
  computed: {
    currentVideo() {
      if (this.selectedVideo === 'all') {
        return null
      }
      return this.videos.find(v => v.id === parseInt(this.selectedVideo))
    }
  },
  watch: {
    selectedVideo: {
      immediate: true,
      handler() {
        if (this.isMounted) {
          this.updateVideoStats()
          this.updateBehaviorChart()
        }
      }
    }
  },
  mounted() {
    this.isMounted = true
    this.$nextTick(() => {
      this.initializeCharts()
      this.updateVideoStats()
    })
  },
  beforeUnmount() {
    this.isMounted = false
    this.destroyCharts()
  },
  methods: {
    getDefaultVideoStats() {
      return {
        totalViews: 0,
        completionRate: 0,
        engagementRate: 0,
        averageRating: 0,
        averageWatchTime: '0分0秒',
        dropOffRate: 0,
        pauseCount: 0,
        rewindCount: 0,
        speedChangeCount: 0,
        likeCount: 0,
        favoriteCount: 0,
        commentCount: 0,
        avgPausesPerViewer: 0,
        topRewindPoints: [],
        speedStats: {
          normal: 0,
          fast: 0,
          slow: 0
        },
        likeRate: 0
      }
    },
    
    generateBehaviorData(duration) {
      const behaviors = []
      const behaviorTypes = ['play', 'pause', 'seek', 'speed', 'like', 'favorite', 'comment']
      
      for (let i = 0; i < duration; i += 5) {
        behaviorTypes.forEach(type => {
          if (Math.random() > 0.7) {
            behaviors.push({
              timestamp: i,
              type: type,
              count: Math.floor(Math.random() * 10) + 1,
              intensity: Math.random() * 100
            })
          }
        })
      }
      return behaviors
    },
    
    updateVideoStats() {
      if (!this.currentVideo) {
        this.currentVideoStats = {
          ...this.getDefaultVideoStats(),
          ...this.analyticsData.overview
        }
        return
      }
      
      const behaviorData = this.currentVideo.behaviorData || []
      const totalViews = 12456
      
      this.currentVideoStats = {
        totalViews: totalViews,
        completionRate: 68,
        engagementRate: 4.2,
        averageRating: 4.7,
        averageWatchTime: '8分32秒',
        dropOffRate: 18,
        pauseCount: behaviorData.filter(b => b.type === 'pause').reduce((sum, b) => sum + b.count, 0),
        rewindCount: behaviorData.filter(b => b.type === 'seek' && b.count < 0).reduce((sum, b) => sum + Math.abs(b.count), 0),
        speedChangeCount: behaviorData.filter(b => b.type === 'speed').reduce((sum, b) => sum + b.count, 0),
        likeCount: behaviorData.filter(b => b.type === 'like').reduce((sum, b) => sum + b.count, 0),
        favoriteCount: behaviorData.filter(b => b.type === 'favorite').reduce((sum, b) => sum + b.count, 0),
        commentCount: behaviorData.filter(b => b.type === 'comment').reduce((sum, b) => sum + b.count, 0),
        avgPausesPerViewer: 3.2,
        topRewindPoints: ['2:15', '8:30', '12:45'],
        speedStats: {
          normal: 65,
          fast: 25,
          slow: 10
        },
        likeRate: 8.5
      }
      
      this.updateKeyMoments(behaviorData)
    },
    
    updateKeyMoments(behaviorData) {
      const moments = []
      const timeWindows = {}
      
      behaviorData.forEach(behavior => {
        const windowKey = Math.floor(behavior.timestamp / 30) * 30
        if (!timeWindows[windowKey]) {
          timeWindows[windowKey] = { count: 0, behaviors: [] }
        }
        timeWindows[windowKey].count += behavior.count
        timeWindows[windowKey].behaviors.push(behavior.type)
      })
      
      Object.entries(timeWindows)
        .sort((a, b) => b[1].count - a[1].count)
        .slice(0, 6)
        .forEach(([time, data]) => {
          const dominantBehavior = this.getDominantBehavior(data.behaviors)
          moments.push({
            time: parseInt(time),
            type: dominantBehavior,
            intensity: Math.min(100, (data.count / 50) * 100),
            description: this.getMomentDescription(parseInt(time), dominantBehavior, data.count)
          })
        })
      
      this.keyMoments = moments
    },
    
    getDominantBehavior(behaviors) {
      const counts = {}
      behaviors.forEach(behavior => {
        counts[behavior] = (counts[behavior] || 0) + 1
      })
      return Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b)
    },
    
    getMomentDescription(time, type, count) {
      const timeStr = this.formatTime(time)
      const descriptions = {
        pause: `在 ${timeStr} 有 ${count} 次暂停，可能是难点内容`,
        seek: `在 ${timeStr} 有 ${count} 次回退，观众在重复学习`,
        like: `在 ${timeStr} 获得 ${count} 个点赞，内容受欢迎`,
        comment: `在 ${timeStr} 有 ${count} 条评论，引发讨论`,
        speed: `在 ${timeStr} 有 ${count} 次变速调整`,
        favorite: `在 ${timeStr} 有 ${count} 次收藏，内容价值高`
      }
      return descriptions[type] || `在 ${timeStr} 有显著用户互动`
    },
    
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins}:${secs.toString().padStart(2, '0')}`
    },
    
    getMomentTypeLabel(type) {
      const labels = {
        pause: '暂停',
        seek: '回退',
        like: '点赞',
        comment: '评论',
        speed: '变速',
        favorite: '收藏',
        play: '播放'
      }
      return labels[type] || type
    },
    
    handleVideoChange() {
      this.updateVideoStats()
      this.updateBehaviorChart()
    },
    
    handleTimeRangeChange(event) {
      this.$emit('time-range-change', event.target.value)
    },
    
    updateBehaviorChart() {
      if (!this.isMounted) return
      
      // 安全地销毁图表
      this.safeDestroyChart('behaviorHeatmap')
      this.safeDestroyChart('behaviorTimeline')
      
      this.$nextTick(() => {
        this.createBehaviorCharts()
      })
    },
    
    initializeCharts() {
      if (!this.isMounted) return
      
      this.createViewsChart()
      this.createEngagementChart()
      this.createAudienceChart()
      this.createRevenueChart()
      this.createBehaviorCharts()
    },
    
    createBehaviorCharts() {
      if (!this.isMounted || !this.currentVideo) return
      
      // 行为热力图
      const heatmapCtx = this.$refs.behaviorHeatmapChart?.getContext('2d')
      if (heatmapCtx && this.$refs.behaviorHeatmapChart) {
        this.charts.behaviorHeatmap = new Chart(heatmapCtx, {
          type: 'bar',
          data: this.getHeatmapData(),
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              },
              title: {
                display: true,
                text: '用户行为密度分布'
              }
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: '视频时间（分钟）'
                }
              },
              y: {
                title: {
                  display: true,
                  text: '行为频次'
                },
                beginAtZero: true
              }
            }
          }
        })
      }
      
      // 行为时间线
      const timelineCtx = this.$refs.behaviorTimelineChart?.getContext('2d')
      if (timelineCtx && this.$refs.behaviorTimelineChart) {
        this.charts.behaviorTimeline = new Chart(timelineCtx, {
          type: 'line',
          data: this.getTimelineData(),
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'top'
              }
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: '视频时间'
                }
              },
              y: {
                title: {
                  display: true,
                  text: '行为数量'
                },
                beginAtZero: true
              }
            }
          }
        })
      }
    },
    
    getHeatmapData() {
      const behaviorData = this.currentVideo.behaviorData || []
      const filteredData = this.selectedBehavior === 'all' 
        ? behaviorData 
        : behaviorData.filter(b => b.type === this.selectedBehavior)
      
      const timeWindows = {}
      filteredData.forEach(behavior => {
        const windowKey = Math.floor(behavior.timestamp / 60)
        if (!timeWindows[windowKey]) {
          timeWindows[windowKey] = 0
        }
        timeWindows[windowKey] += behavior.count
      })
      
      const labels = Object.keys(timeWindows).map(t => `${t}分`)
      const data = Object.values(timeWindows)
      
      return {
        labels,
        datasets: [{
          label: '行为频次',
          data,
          backgroundColor: 'rgba(255, 99, 132, 0.6)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }]
      }
    },
    
    getTimelineData() {
      const behaviorTypes = ['pause', 'seek', 'like', 'comment']
      const datasets = []
      
      behaviorTypes.forEach(type => {
        if (this.selectedBehavior !== 'all' && this.selectedBehavior !== type) return
        
        const typeData = (this.currentVideo.behaviorData || [])
          .filter(b => b.type === type)
          .reduce((acc, b) => {
            const timeKey = Math.floor(b.timestamp / 30) * 30
            acc[timeKey] = (acc[timeKey] || 0) + b.count
            return acc
          }, {})
        
        const data = Object.values(typeData)
        
        const colors = {
          pause: { bg: 'rgba(54, 162, 235, 0.2)', border: 'rgba(54, 162, 235, 1)' },
          seek: { bg: 'rgba(255, 206, 86, 0.2)', border: 'rgba(255, 206, 86, 1)' },
          like: { bg: 'rgba(255, 99, 132, 0.2)', border: 'rgba(255, 99, 132, 1)' },
          comment: { bg: 'rgba(75, 192, 192, 0.2)', border: 'rgba(75, 192, 192, 1)' }
        }
        
        datasets.push({
          label: this.getMomentTypeLabel(type),
          data,
          backgroundColor: colors[type].bg,
          borderColor: colors[type].border,
          borderWidth: 2,
          tension: 0.4,
          fill: true
        })
      })
      
      return {
        labels: Array.from({ length: Math.ceil(this.currentVideo.duration / 30) }, (_, i) => 
          this.formatTime(i * 30)
        ),
        datasets
      }
    },
    
    safeDestroyChart(chartName) {
      if (this.charts[chartName] && typeof this.charts[chartName].destroy === 'function') {
        try {
          this.charts[chartName].destroy()
        } catch (error) {
          console.warn(`Error destroying chart ${chartName}:`, error)
        }
        this.charts[chartName] = null
      }
    },
    
    destroyCharts() {
      Object.keys(this.charts).forEach(chartName => {
        this.safeDestroyChart(chartName)
      })
      this.charts = {}
    },
    
    createViewsChart() {
      const ctx = this.$refs.viewsChart?.getContext('2d')
      if (ctx && this.$refs.viewsChart) {
        this.charts.views = new Chart(ctx, {
          type: 'line',
          data: {
            labels: ['0:00', '2:00', '4:00', '6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '24:00'],
            datasets: [{
              label: '观看次数',
              data: [120, 190, 150, 250, 220, 300, 450, 400, 350, 300, 250, 200, 150],
              borderColor: '#0056d2',
              backgroundColor: 'rgba(0, 86, 210, 0.1)',
              borderWidth: 2,
              fill: true,
              tension: 0.4
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              },
              title: {
                display: true,
                text: '观看趋势时间分布'
              },
              tooltip: {
                mode: 'index',
                intersect: false
              }
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: '视频时间轴'
                }
              },
              y: {
                title: {
                  display: true,
                  text: '观看次数'
                },
                beginAtZero: true
              }
            }
          }
        })
      }
    },
    
    createEngagementChart() {
      const ctx = this.$refs.engagementChart?.getContext('2d')
      if (ctx && this.$refs.engagementChart) {
        this.charts.engagement = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: ['点赞', '收藏', '转发', '评论', '分享'],
            datasets: [{
              data: [35, 25, 15, 15, 10],
              backgroundColor: [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(153, 102, 255, 0.7)'
              ],
              borderColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 206, 86)',
                'rgb(75, 192, 192)',
                'rgb(153, 102, 255)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              title: {
                display: true,
                text: '用户互动类型分布'
              },
              legend: {
                position: 'right'
              }
            }
          }
        })
      }
    },
    
    createAudienceChart() {
      const ctx = this.$refs.audienceChart?.getContext('2d')
      if (ctx && this.$refs.audienceChart) {
        this.charts.audience = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['暂停', '加速', '减速', '回退', '快进', '放大', '缩小'],
            datasets: [{
              label: '操作次数',
              data: [45, 30, 15, 28, 22, 12, 8],
              backgroundColor: [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(153, 102, 255, 0.7)',
                'rgba(255, 159, 64, 0.7)',
                'rgba(199, 199, 199, 0.7)'
              ],
              borderColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 206, 86)',
                'rgb(75, 192, 192)',
                'rgb(153, 102, 255)',
                'rgb(255, 159, 64)',
                'rgb(199, 199, 199)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              title: {
                display: true,
                text: '观众播放控制行为统计'
              }
            },
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: '操作次数'
                }
              }
            }
          }
        })
      }
    },
    
    createRevenueChart() {
      const ctx = this.$refs.revenueChart?.getContext('2d')
      if (ctx && this.$refs.revenueChart) {
        this.charts.revenue = new Chart(ctx, {
          type: 'line',
          data: {
            labels: ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],
            datasets: [{
              label: '用户完成率',
              data: [100, 95, 88, 82, 75, 70, 68, 65, 60, 55, 50],
              borderColor: '#4bc0c0',
              backgroundColor: 'rgba(75, 192, 192, 0.1)',
              tension: 0.4,
              fill: true
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              title: {
                display: true,
                text: '视频完成率随播放进度变化'
              }
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: '视频播放进度'
                }
              },
              y: {
                title: {
                  display: true,
                  text: '剩余用户百分比'
                },
                min: 0,
                max: 100
              }
            }
          }
        })
      }
    },
    
    exportData() {
      alert('数据导出功能将在完整版本中实现')
    },
    
    generateReport() {
      alert('详细报告生成功能将在完整版本中实现')
    }
  }
}
</script>

<style scoped>
.behavior-analysis-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 25px;
  margin-bottom: 30px;
}

.section-title {
  font-size: 1.3rem;
  margin-bottom: 20px;
  color: var(--text);
  border-bottom: 2px solid var(--primary);
  padding-bottom: 10px;
}

.subsection-title {
  font-size: 1.1rem;
  margin: 25px 0 15px 0;
  color: var(--text);
}

.behavior-controls {
  display: flex;
  gap: 30px;
  margin-bottom: 25px;
  padding: 15px;
  background: var(--secondary);
  border-radius: 6px;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.control-group label {
  font-weight: 500;
  color: var(--text);
  white-space: nowrap;
}

.control-group select {
  padding: 8px 12px;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: white;
  min-width: 120px;
}

.behavior-chart-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
  margin-bottom: 25px;
}

.chart-subtitle {
  font-size: 1rem;
  margin-bottom: 15px;
  color: var(--text);
  text-align: center;
}

.behavior-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.behavior-stat-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: var(--secondary);
  border-radius: 8px;
  border-left: 4px solid var(--primary);
}

.behavior-icon {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: white;
}

.behavior-icon.pause { background: #ff6b6b; }
.behavior-icon.seek { background: #4ecdc4; }
.behavior-icon.speed { background: #45b7d1; }
.behavior-icon.like { background: #ff6b6b; }
.behavior-icon.favorite { background: #ffa502; }
.behavior-icon.comment { background: #2ed573; }

.behavior-info {
  flex: 1;
}

.behavior-count {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--text);
  margin-bottom: 5px;
}

.behavior-label {
  font-size: 0.9rem;
  color: var(--text-light);
  margin-bottom: 5px;
}

.behavior-detail {
  font-size: 0.8rem;
  color: var(--text-light);
}

.moments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 15px;
}

.moment-card {
  padding: 15px;
  background: var(--secondary);
  border-radius: 6px;
  border: 1px solid var(--border);
}

.moment-time {
  font-size: 1.1rem;
  font-weight: bold;
  color: var(--primary);
  margin-bottom: 8px;
}

.moment-type {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 500;
  margin-bottom: 10px;
}

.moment-type.pause { background: #ffeaa7; color: #e17055; }
.moment-type.seek { background: #81ecec; color: #00cec9; }
.moment-type.like { background: #fab1a0; color: #e84393; }
.moment-type.comment { background: #55efc4; color: #00b894; }
.moment-type.speed { background: #74b9ff; color: #0984e3; }
.moment-type.favorite { background: #fd79a8; color: #e84393; }

.moment-intensity {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.intensity-bar {
  flex: 1;
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  overflow: hidden;
}

.intensity-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff6b6b, #ffa502);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.intensity-text {
  font-size: 0.8rem;
  color: var(--text-light);
  min-width: 35px;
}

.moment-description {
  font-size: 0.85rem;
  color: var(--text);
  line-height: 1.4;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .behavior-chart-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .behavior-controls {
    flex-direction: column;
    gap: 15px;
  }
  
  .behavior-stats-grid {
    grid-template-columns: 1fr;
  }
  
  .moments-grid {
    grid-template-columns: 1fr;
  }
}

/* 保持原有的样式不变 */
.analytics-section {
  padding: 20px 0;
}

.video-selector {
  margin-bottom: 20px;
}

.video-selector select {
  width: 100%;
  max-width: 300px;
  padding: 10px 15px;
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 1rem;
}

.analytics-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 20px;
  text-align: center;
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
  margin-bottom: 5px;
}

.stat-change {
  font-size: 0.8rem;
  font-weight: 500;
}

.stat-change.positive {
  color: var(--success);
}

.stat-change.negative {
  color: var(--danger);
}

.analytics-charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 25px;
  margin-bottom: 30px;
}

.chart-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.chart-title {
  font-size: 1.2rem;
  margin-bottom: 15px;
  font-weight: 600;
  color: var(--text);
}

.chart-wrapper {
  position: relative;
  height: 300px;
}

.analytics-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
  margin-bottom: 30px;
}

.detail-section {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.detail-section h3 {
  margin-bottom: 15px;
  color: var(--text);
  font-size: 1.1rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.metric-item {
  padding: 15px;
  background: var(--secondary);
  border-radius: 6px;
  text-align: center;
}

.metric-label {
  font-size: 0.8rem;
  color: var(--text-light);
  margin-bottom: 5px;
}

.metric-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: var(--text);
  margin-bottom: 3px;
}

.metric-change {
  font-size: 0.7rem;
  font-weight: 500;
}

.time-distribution {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.time-slot {
  display: flex;
  align-items: center;
  gap: 10px;
}

.time-label {
  width: 60px;
  font-size: 0.8rem;
  color: var(--text);
}

.time-bar {
  flex: 1;
  height: 8px;
  background: var(--secondary);
  border-radius: 4px;
  overflow: hidden;
}

.time-fill {
  height: 100%;
  background: var(--primary);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.time-percentage {
  width: 40px;
  font-size: 0.8rem;
  color: var(--text-light);
  text-align: right;
}

.device-distribution {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.device-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: var(--secondary);
  border-radius: 6px;
}

.device-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.device-info i {
  color: var(--primary);
  width: 16px;
}

.device-type {
  font-size: 0.9rem;
  color: var(--text);
}

.device-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.device-percentage {
  font-size: 0.9rem;
  font-weight: bold;
  color: var(--text);
}

.device-count {
  font-size: 0.7rem;
  color: var(--text-light);
}

.analytics-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
}

@media (max-width: 768px) {
  .analytics-charts {
    grid-template-columns: 1fr;
  }
  
  .analytics-details {
    grid-template-columns: 1fr;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
}
</style>