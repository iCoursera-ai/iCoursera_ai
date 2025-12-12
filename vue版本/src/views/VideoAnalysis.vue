<template>
  <div class="font-inter bg-gray-50 min-h-screen flex flex-col">
    <Header />
    
    <div class="flex flex-1">
      <!-- 左侧课程列表导航 -->
<aside class="w-64 bg-white border-r border-gray-200 flex-shrink-0 fixed top-[5rem] left-0 h-[calc(100vh-5rem)] overflow-y-auto z-30">
        <!-- 课程章节标题 -->
        <div class="course-section-title">
          操作系统课程
        </div>
        
        <!-- 第一章 -->
        <div class="border-b border-gray-200">
          <div class="course-section-title flex justify-between items-center cursor-pointer" @click="toggleSection('section1', true)">
            <span>第一章</span>
            <i class="fa" :class="section1Open ? 'fa-angle-down' : 'fa-angle-right'"></i>
          </div>
          <div class="pl-2" v-show="section1Open">
            <div class="course-item" :class="{ 'active': currentItem === 'video1.1' }" @click="selectItem('video1.1', 'video', 'section1')">
              <div class="course-item-icon course-item-video">
                <i class="fa fa-play text-xs"></i>
              </div>
              <span>视频1.1</span>
            </div>
            <div class="course-item" :class="{ 'active': currentItem === 'video1.2' }" @click="selectItem('video1.2', 'video', 'section1')">
              <div class="course-item-icon course-item-video">
                <i class="fa fa-play text-xs"></i>
              </div>
              <span>视频1.2</span>
            </div>
            <div class="course-item" :class="{ 'active': currentItem === 'exercise1.1' }" @click="selectItem('exercise1.1', 'exercise', 'section1')">
              <div class="course-item-icon course-item-exercise">
                <i class="fa fa-pencil text-xs"></i>
              </div>
              <span>习题1.1</span>
            </div>
            <div class="course-item" :class="{ 'active': currentItem === 'exercise1.2' }" @click="selectItem('exercise1.2', 'exercise', 'section1')">
              <div class="course-item-icon course-item-exercise">
                <i class="fa fa-pencil text-xs"></i>
              </div>
              <span>习题1.2</span>
            </div>
          </div>
        </div>
        
        <!-- 第二章 -->
        <div class="border-b border-gray-200">
          <div class="course-section-title flex justify-between items-center cursor-pointer" @click="toggleSection('section2', true)">
            <span>第二章</span>
            <i class="fa" :class="section2Open ? 'fa-angle-down' : 'fa-angle-right'"></i>
          </div>
          <div class="pl-2" v-show="section2Open">
            <div class="course-item" :class="{ 'active': currentItem === 'video2.1' }" @click="selectItem('video2.1', 'video', 'section2')">
              <div class="course-item-icon course-item-video">
                <i class="fa fa-play text-xs"></i>
              </div>
              <span>视频2.1</span>
            </div>
            <div class="course-item" :class="{ 'active': currentItem === 'video2.2' }" @click="selectItem('video2.2', 'video', 'section2')">
              <div class="course-item-icon course-item-video">
                <i class="fa fa-play text-xs"></i>
              </div>
              <span>视频2.2</span>
            </div>
            <div class="course-item" :class="{ 'active': currentItem === 'exercise2.1' }" @click="selectItem('exercise2.1', 'exercise', 'section2')">
              <div class="course-item-icon course-item-exercise">
                <i class="fa fa-pencil text-xs"></i>
              </div>
              <span>习题2.1</span>
            </div>
            <div class="course-item" :class="{ 'active': currentItem === 'exercise2.2' }" @click="selectItem('exercise2.2', 'exercise', 'section2')">
              <div class="course-item-icon course-item-exercise">
                <i class="fa fa-pencil text-xs"></i>
              </div>
              <span>习题2.2</span>
            </div>
          </div>
        </div>
        
        <!-- 其他章节 -->
        <div v-for="chapter in otherChapters" :key="chapter.id" class="border-b border-gray-200">
          <div class="course-section-title flex justify-between items-center cursor-pointer" @click="toggleOtherSection(chapter.id, true)">
            <span>{{ chapter.name }}</span>
            <i class="fa" :class="openSections[chapter.id] ? 'fa-angle-down' : 'fa-angle-right'"></i>
          </div>
          <div class="pl-2" v-show="openSections[chapter.id]">
            <div class="course-item" :class="{ 'active': currentItem === `video${chapter.id.replace('section', '')}.1` }" @click="selectItem(`video${chapter.id.replace('section', '')}.1`, 'video', chapter.id)">
              <div class="course-item-icon course-item-video">
                <i class="fa fa-play text-xs"></i>
              </div>
              <span>视频{{ chapter.id.replace('section', '') }}.1</span>
            </div>
            <div class="course-item" :class="{ 'active': currentItem === `video${chapter.id.replace('section', '')}.2` }" @click="selectItem(`video${chapter.id.replace('section', '')}.2`, 'video', chapter.id)">
              <div class="course-item-icon course-item-video">
                <i class="fa fa-play text-xs"></i>
              </div>
              <span>视频{{ chapter.id.replace('section', '') }}.2</span>
            </div>
            <div class="course-item" :class="{ 'active': currentItem === `exercise${chapter.id.replace('section', '')}.1` }" @click="selectItem(`exercise${chapter.id.replace('section', '')}.1`, 'exercise', chapter.id)">
              <div class="course-item-icon course-item-exercise">
                <i class="fa fa-pencil text-xs"></i>
              </div>
              <span>习题{{ chapter.id.replace('section', '') }}.1</span>
            </div>
            <div class="course-item" :class="{ 'active': currentItem === `exercise${chapter.id.replace('section', '')}.2` }" @click="selectItem(`exercise${chapter.id.replace('section', '')}.2`, 'exercise', chapter.id)">
              <div class="course-item-icon course-item-exercise">
                <i class="fa fa-pencil text-xs"></i>
              </div>
              <span>习题{{ chapter.id.replace('section', '') }}.2</span>
            </div>
          </div>
        </div>
      </aside>

      <!-- 主内容区域：视频详情分析 -->
      <main class="flex-1 overflow-y-auto p-6 ml-64" style="height: calc(100vh - 5rem);">
        <!-- 面包屑导航 -->
        <div class="text-sm text-secondary mb-6">
          <span @click="goToDashboard()" class="cursor-pointer hover:text-primary">用户中心</span>
          <i class="fa fa-angle-right mx-1 text-gray-400"></i>
          <span @click="goToDashboard()" class="cursor-pointer hover:text-primary">教师管理</span>
          <i class="fa fa-angle-right mx-1 text-gray-400"></i>
          <span @click="goToDashboard()" class="cursor-pointer hover:text-primary">工作台</span>
          <i class="fa fa-angle-right mx-1 text-gray-400"></i>
          <span>操作系统课程</span>
          <i class="fa fa-angle-right mx-1 text-gray-400"></i>
          <span class="text-dark font-medium">{{ currentItemDisplay }} - 数据分析</span>
        </div>

        <!-- 页面内容容器 -->
        <div class="space-y-6">
          <!-- 数据分析概览 -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="text-xs text-secondary mb-1">观看总人数</div>
              <div class="flex items-center justify-between">
                <div class="text-xl font-bold text-dark">{{ currentStats.viewers }}</div>
                <div class="text-success text-xs flex items-center">
                  <i class="fa fa-caret-up mr-1"></i> {{ currentStats.viewersIncrease }}
                </div>
              </div>
              <div class="mt-2 h-10">
                <canvas :ref="el => chartRefs.viewersChart = el"></canvas>
              </div>
            </div>
            
            <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="text-xs text-secondary mb-1">平均观看时长</div>
              <div class="flex items-center justify-between">
                <div class="text-xl font-bold text-dark">{{ currentStats.avgDuration }}</div>
                <div class="text-success text-xs flex items-center">
                  <i class="fa fa-caret-up mr-1"></i> {{ currentStats.durationIncrease }}
                </div>
              </div>
              <div class="mt-2 h-10">
                <canvas :ref="el => chartRefs.durationChart = el"></canvas>
              </div>
            </div>
            
            <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="text-xs text-secondary mb-1">评论总量</div>
              <div class="flex items-center justify-between">
                <div class="text-xl font-bold text-dark">{{ currentStats.comments }}</div>
                <div class="text-success text-xs flex items-center">
                  <i class="fa fa-caret-up mr-1"></i> {{ currentStats.commentsIncrease }}
                </div>
              </div>
              <div class="mt-2 h-10">
                <canvas :ref="el => chartRefs.commentsChart = el"></canvas>
              </div>
            </div>
            
            <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="text-xs text-secondary mb-1">点赞总量</div>
              <div class="flex items-center justify-between">
                <div class="text-xl font-bold text-dark">{{ currentStats.likes }}</div>
                <div class="text-success text-xs flex items-center">
                  <i class="fa fa-caret-up mr-1"></i> {{ currentStats.likesIncrease }}
                </div>
              </div>
              <div class="mt-2 h-10">
                <canvas :ref="el => chartRefs.likesChart = el"></canvas>
              </div>
            </div>
          </div>

          <!-- 视频播放区域 + 数据 -->
          <div class="flex flex-col lg:flex-row gap-6">
            <!-- 视频播放 + 核心分析 -->
            <div class="flex-1 space-y-6">
              <!-- 视频播放 -->
              <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="font-medium text-dark">{{ currentItemDisplay }} 播放</h3>
                  <button class="text-primary text-sm hover:bg-primary/10 px-3 py-1 rounded transition-colors">更换视频</button>
                </div>
                <div class="aspect-video bg-gray-100 rounded-lg flex items-center justify-center">
                  <div class="w-20 h-20 rounded-full bg-black/10 flex items-center justify-center cursor-pointer hover:bg-black/20 transition-colors">
                    <i class="fa fa-play text-3xl text-dark"></i>
                  </div>
                </div>
              </div>

              <!-- 内容时段分析 -->
              <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                <h3 class="font-medium text-dark mb-4">{{ currentItemDisplay }} 内容时段分析</h3>
                <div class="h-64 bg-gray-50 rounded-lg relative w-full">
                  <canvas :ref="el => chartRefs.contentChart = el" class="w-full h-full"></canvas>
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
import { Chart } from 'chart.js/auto'

export default {
  name: 'VideoAnalysis',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      section1Open: true, // 初始状态：第一章展开
      section2Open: false, // 初始状态：第二章闭合
      openSections: {},
      currentItem: 'video1.1', // 默认选中视频1.1
      lastOpenedSection: 'section1', // 记录上次打开的章节
      otherChapters: [
        { id: 'section3', name: '第三章' },
        { id: 'section4', name: '第四章' },
        { id: 'section5', name: '第五章' },
        { id: 'section6', name: '第六章' },
        { id: 'section7', name: '第七章' },
        { id: 'section8', name: '第八章' }
      ],
      chartRefs: {},
      chartInstances: {},
      // 不同视频的统计数据
      videoStats: {
        'video1.1': {
          viewers: '12,256',
          viewersIncrease: '206',
          avgDuration: '8分12秒',
          durationIncrease: '14秒',
          comments: '4,592',
          commentsIncrease: '112',
          likes: '3,256',
          likesIncrease: '366'
        },
        'video1.2': {
          viewers: '10,856',
          viewersIncrease: '156',
          avgDuration: '7分45秒',
          durationIncrease: '8秒',
          comments: '3,245',
          commentsIncrease: '89',
          likes: '2,856',
          likesIncrease: '245'
        },
        'video2.1': {
          viewers: '11,500',
          viewersIncrease: '180',
          avgDuration: '9分05秒',
          durationIncrease: '20秒',
          comments: '3,800',
          commentsIncrease: '95',
          likes: '3,100',
          likesIncrease: '300'
        },
        'video2.2': {
          viewers: '9,800',
          viewersIncrease: '120',
          avgDuration: '8分30秒',
          durationIncrease: '15秒',
          comments: '2,950',
          commentsIncrease: '75',
          likes: '2,600',
          likesIncrease: '200'
        },
        // 其他章节视频的数据
        'video3.1': {
          viewers: '8,200',
          viewersIncrease: '90',
          avgDuration: '7分50秒',
          durationIncrease: '10秒',
          comments: '2,400',
          commentsIncrease: '60',
          likes: '2,100',
          likesIncrease: '150'
        },
        'video3.2': {
          viewers: '7,500',
          viewersIncrease: '80',
          avgDuration: '8分15秒',
          durationIncrease: '12秒',
          comments: '2,100',
          commentsIncrease: '50',
          likes: '1,900',
          likesIncrease: '120'
        },
        'video4.1': {
          viewers: '6,800',
          viewersIncrease: '70',
          avgDuration: '7分30秒',
          durationIncrease: '8秒',
          comments: '1,800',
          commentsIncrease: '40',
          likes: '1,600',
          likesIncrease: '100'
        }
      }
    }
  },
  computed: {
    currentItemDisplay() {
      // 将 video1.1 转换为 "视频1.1"
      if (this.currentItem.startsWith('video')) {
        const num = this.currentItem.replace('video', '')
        return `视频${num}`
      } else if (this.currentItem.startsWith('exercise')) {
        const num = this.currentItem.replace('exercise', '')
        return `习题${num}`
      }
      return this.currentItem
    },
    currentStats() {
      // 返回当前选中项目的统计数据
      return this.videoStats[this.currentItem] || this.videoStats['video1.1']
    }
  },
  created() {
    // 从路由参数中获取要选中的项目
    if (this.$route.params.item) {
      this.currentItem = this.$route.params.item
      // 根据选中的项目自动展开对应的章节
      this.autoOpenSection(this.currentItem)
      
      // 如果有传递的展开章节信息，关闭其他章节
      if (this.$route.params.openedSection) {
        this.closeOtherSections(this.$route.params.openedSection)
      }
    }
  },
  mounted() {
    this.initCharts()
  },
  beforeUnmount() {
    // 销毁所有图表实例
    Object.values(this.chartInstances).forEach(chart => {
      if (chart) chart.destroy()
    })
  },
  methods: {
    toggleSection(section, closeOthers = false) {
      if (closeOthers) {
        // 关闭其他章节
        this.closeOtherSections(section)
      }
      this[section + 'Open'] = !this[section + 'Open']
      if (this[section + 'Open']) {
        this.lastOpenedSection = section
      }
    },
    
    toggleOtherSection(sectionId, closeOthers = false) {
      if (closeOthers) {
        // 关闭其他章节
        this.closeOtherSections(sectionId)
      }
      this.openSections[sectionId] = !this.openSections[sectionId]
      if (this.openSections[sectionId]) {
        this.lastOpenedSection = sectionId
      }
    },
    
    closeOtherSections(currentSection) {
      // 关闭除了当前章节之外的所有章节
      if (currentSection !== 'section1') {
        this.section1Open = false
      }
      if (currentSection !== 'section2') {
        this.section2Open = false
      }
      
      // 关闭其他章节
      for (const sectionId in this.openSections) {
        if (sectionId !== currentSection) {
          this.openSections[sectionId] = false
        }
      }
    },
    
    autoOpenSection(item) {
      // 根据项目ID自动展开对应的章节
      if (item.includes('1.')) {
        this.section1Open = true
        this.lastOpenedSection = 'section1'
      } else if (item.includes('2.')) {
        this.section2Open = true
        this.lastOpenedSection = 'section2'
      } else if (item.includes('3.')) {
        this.openSections['section3'] = true
        this.lastOpenedSection = 'section3'
      } else if (item.includes('4.')) {
        this.openSections['section4'] = true
        this.lastOpenedSection = 'section4'
      } else if (item.includes('5.')) {
        this.openSections['section5'] = true
        this.lastOpenedSection = 'section5'
      } else if (item.includes('6.')) {
        this.openSections['section6'] = true
        this.lastOpenedSection = 'section6'
      } else if (item.includes('7.')) {
        this.openSections['section7'] = true
        this.lastOpenedSection = 'section7'
      } else if (item.includes('8.')) {
        this.openSections['section8'] = true
        this.lastOpenedSection = 'section8'
      }
    },
    
    selectItem(item, type, sectionId) {
      if (type === 'exercise') {
        // 跳转到习题分析页面，并传递当前选中的项目和当前展开的章节
        this.$router.push({ 
          name: 'ExerciseAnalysis', 
          params: { 
            item: item,
            openedSection: sectionId
          } 
        })
      } else {
        // 在当前页面更新选中的视频
        this.currentItem = item
        
        // 自动展开对应的章节
        this.autoOpenSection(item)
        
        this.updateVideoData(item)
      }
    },
    
    updateVideoData(item) {
      // 这里可以添加根据item更新视频数据的逻辑
      // 例如从API获取不同视频的数据
      console.log(`更新视频数据: ${item}`)
      
      // 销毁旧图表
      Object.values(this.chartInstances).forEach(chart => {
        if (chart) chart.destroy()
      })
      
      // 重新初始化图表
      this.$nextTick(() => {
        this.initCharts()
      })
    },
    
    goToDashboard() {
      this.$router.push('/teacher-dashboard')
    },
    
    goToVideoAnalysis() {
      this.$router.push('/video-analysis')
    },
    
    goToExerciseAnalysis() {
      this.$router.push('/exercise-analysis')
    },
    
    initCharts() {
      // 等待DOM渲染完成
      this.$nextTick(() => {
        this.initSmallCharts()
        this.initContentChart()
      })
    },
    
    initSmallCharts() {
      const smallChartConfig = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { x: { display: false }, y: { display: false } },
        elements: { point: { radius: 0 } }
      }
      
      // 观看人数小图表
      if (this.chartRefs.viewersChart) {
        this.chartInstances.viewersChart = new Chart(this.chartRefs.viewersChart, {
          type: 'line',
          data: { labels: [1,2,3,4,5,6,7], datasets: [{ data: [5,3,4,6,5,7,6], borderColor: '#165DFF', tension: 0.4 }] },
          options: smallChartConfig
        })
      }
      
      // 时长小图表
      if (this.chartRefs.durationChart) {
        this.chartInstances.durationChart = new Chart(this.chartRefs.durationChart, {
          type: 'bar',
          data: { labels: [1,2,3,4,5], datasets: [{ data: [3,5,4,6,5], backgroundColor: '#10B981' }] },
          options: smallChartConfig
        })
      }
      
      // 评论小图表
      if (this.chartRefs.commentsChart) {
        this.chartInstances.commentsChart = new Chart(this.chartRefs.commentsChart, {
          type: 'line',
          data: { labels: [1,2,3,4,5,6,7], datasets: [{ data: [2,4,3,5,4,6,5], borderColor: '#165DFF', tension: 0.4 }] },
          options: smallChartConfig
        })
      }
      
      // 点赞小图表
      if (this.chartRefs.likesChart) {
        this.chartInstances.likesChart = new Chart(this.chartRefs.likesChart, {
          type: 'doughnut',
          data: { labels: ['已赞', '未赞'], datasets: [{ data: [3256, 6744], backgroundColor: ['#165DFF', '#E5E6EB'] }] },
          options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
        })
      }
    },
    
    initContentChart() {
      if (!this.chartRefs.contentChart) return
      
      this.chartInstances.contentChart = new Chart(this.chartRefs.contentChart, {
        type: 'line',
        data: {
          labels: ['0', '100', '200', '300', '400', '500', '6', '7', '8', '9', '10', '11'],
          datasets: [
            { label: '暂停', data: [200, 150, 250, 180, 220, 200, 190, 160, 180, 200, 220, 250], borderColor: '#FF9F43', tension: 0.4 },
            { label: '减速播放', data: [150, 200, 180, 220, 150, 180, 200, 170, 190, 180, 200, 220], borderColor: '#165DFF', tension: 0.4 },
            { label: '倍速播放', data: [100, 120, 150, 100, 130, 120, 140, 110, 130, 120, 140, 150], borderColor: '#10B981', tension: 0.4 }
          ]
        },
        options: { 
          responsive: true, 
          maintainAspectRatio: false, 
          plugins: { legend: { position: 'top' } },
          scales: {
            y: { beginAtZero: true },
            x: { title: { display: true, text: '时间/分' } }
          }
        }
      })
    }
  }
}
</script>

<style scoped>
/* 课程样式 */
.course-section-title {
  @apply font-medium text-gray-600 py-2 px-4 border-b border-gray-200;
}
.course-item {
  @apply flex items-center gap-3 px-4 py-2.5 hover:bg-primary/5 cursor-pointer transition-colors text-sm;
}
.course-item.active {
  @apply bg-primary/10 text-primary;
}
.course-item-icon {
  @apply w-5 h-5 flex items-center justify-center rounded;
}
.course-item-video {
  @apply bg-primary/10 text-primary;
}
.course-item-exercise {
  @apply bg-success/10 text-success;
}
</style>