<template>
  <div class="font-inter bg-gray-50 min-h-screen flex flex-col">
    <Header />
    
    <div class="flex flex-1">
      <!-- 左侧课程列表导航 -->
      <aside class="w-64 bg-white border-r border-gray-200 flex-shrink-0 h-[calc(100vh-5rem)] sticky top-[5rem] overflow-y-auto z-30">
        <!-- 课程章节标题 -->
        <div class="course-section-title">
          操作系统课程
        </div>
        
        <!-- 第一章 -->
        <div class="border-b border-gray-200">
          <div class="course-section-title flex justify-between items-center cursor-pointer" @click="toggleSection('section1')">
            <span>第一章</span>
            <i class="fa" :class="section1Open ? 'fa-angle-down' : 'fa-angle-right'"></i>
          </div>
          <div class="pl-2" v-show="section1Open">
            <div class="course-item active" @click="goToVideoAnalysis()">
              <div class="course-item-icon course-item-video">
                <i class="fa fa-play text-xs"></i>
              </div>
              <span>视频1.1</span>
            </div>
            <div class="course-item" @click="goToVideoAnalysis()">
              <div class="course-item-icon course-item-video">
                <i class="fa fa-play text-xs"></i>
              </div>
              <span>视频1.2</span>
            </div>
            <div class="course-item" @click="goToExerciseAnalysis()">
              <div class="course-item-icon course-item-exercise">
                <i class="fa fa-pencil text-xs"></i>
              </div>
              <span>习题1.1</span>
            </div>
          </div>
        </div>
        
        <!-- 第二章 -->
        <div class="border-b border-gray-200">
          <div class="course-section-title flex justify-between items-center cursor-pointer" @click="toggleSection('section2')">
            <span>第二章</span>
            <i class="fa" :class="section2Open ? 'fa-angle-down' : 'fa-angle-right'"></i>
          </div>
          <div class="pl-2" v-show="section2Open">
            <div class="course-item" @click="goToVideoAnalysis()">
              <div class="course-item-icon course-item-video">
                <i class="fa fa-play text-xs"></i>
              </div>
              <span>视频2.1</span>
            </div>
            <div class="course-item" @click="goToVideoAnalysis()">
              <div class="course-item-icon course-item-video">
                <i class="fa fa-play text-xs"></i>
              </div>
              <span>视频2.2</span>
            </div>
            <div class="course-item" @click="goToExerciseAnalysis()">
              <div class="course-item-icon course-item-exercise">
                <i class="fa fa-pencil text-xs"></i>
              </div>
              <span>习题2.1</span>
            </div>
            <div class="course-item" @click="goToExerciseAnalysis()">
              <div class="course-item-icon course-item-exercise">
                <i class="fa fa-pencil text-xs"></i>
              </div>
              <span>习题2.2</span>
            </div>
          </div>
        </div>
        
        <!-- 其他章节 -->
        <div v-for="chapter in otherChapters" :key="chapter.id" class="border-b border-gray-200">
          <div class="course-section-title flex justify-between items-center cursor-pointer" @click="toggleOtherSection(chapter.id)">
            <span>{{ chapter.name }}</span>
            <i class="fa" :class="openSections[chapter.id] ? 'fa-angle-down' : 'fa-angle-right'"></i>
          </div>
        </div>
      </aside>

      <!-- 主内容区域：视频详情分析 -->
      <main class="flex-1 overflow-y-auto p-6">
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
          <span class="text-dark font-medium">视频1.1 - 数据分析</span>
        </div>

        <!-- 页面内容容器 -->
        <div class="space-y-6">
          <!-- 数据分析概览 -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="text-xs text-secondary mb-1">观看总人数</div>
              <div class="flex items-center justify-between">
                <div class="text-xl font-bold text-dark">12,256</div>
                <div class="text-success text-xs flex items-center">
                  <i class="fa fa-caret-up mr-1"></i> 206
                </div>
              </div>
              <div class="mt-2 h-10">
                <canvas :ref="el => chartRefs.viewersChart = el"></canvas>
              </div>
            </div>
            
            <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="text-xs text-secondary mb-1">平均观看时长</div>
              <div class="flex items-center justify-between">
                <div class="text-xl font-bold text-dark">8分12秒</div>
                <div class="text-success text-xs flex items-center">
                  <i class="fa fa-caret-up mr-1"></i> 14秒
                </div>
              </div>
              <div class="mt-2 h-10">
                <canvas :ref="el => chartRefs.durationChart = el"></canvas>
              </div>
            </div>
            
            <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="text-xs text-secondary mb-1">评论总量</div>
              <div class="flex items-center justify-between">
                <div class="text-xl font-bold text-dark">4,592</div>
                <div class="text-success text-xs flex items-center">
                  <i class="fa fa-caret-up mr-1"></i> 112
                </div>
              </div>
              <div class="mt-2 h-10">
                <canvas :ref="el => chartRefs.commentsChart = el"></canvas>
              </div>
            </div>
            
            <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="text-xs text-secondary mb-1">点赞总量</div>
              <div class="flex items-center justify-between">
                <div class="text-xl font-bold text-dark">3,256</div>
                <div class="text-success text-xs flex items-center">
                  <i class="fa fa-caret-up mr-1"></i> 366
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
                  <h3 class="font-medium text-dark">视频播放</h3>
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
                <h3 class="font-medium text-dark mb-4">内容时段分析</h3>
                <div class="h-64 bg-gray-50 rounded-lg relative w-full">
                  <canvas :ref="el => chartRefs.contentChart = el" class="w-full h-full"></canvas>
                </div>
              </div>

              <!-- 底部分析区域 -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <!-- 完成率分析 -->
                <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                  <h3 class="font-medium text-dark mb-4 text-sm">完成率分析</h3>
                  <div class="h-40 bg-gray-50 rounded-lg relative w-full">
                    <canvas :ref="el => chartRefs.completionChart = el" class="w-full h-full"></canvas>
                  </div>
                </div>
                
                <!-- 热门时段分析 -->
                <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                  <h3 class="font-medium text-dark mb-4 text-sm">热门时段分析</h3>
                  <div class="h-40 bg-gray-50 rounded-lg relative w-full">
                    <canvas :ref="el => chartRefs.hotTimeChart = el" class="w-full h-full"></canvas>
                  </div>
                </div>
                
                <!-- 今日互动统计 -->
                <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                  <h3 class="font-medium text-dark mb-4 text-sm">今日互动统计</h3>
                  <div class="h-40 bg-gray-50 rounded-lg relative w-full">
                    <canvas :ref="el => chartRefs.todayInteractionChart = el" class="w-full h-full"></canvas>
                  </div>
                </div>
              </div>
            </div>

            <!-- 右侧辅助数据 -->
            <div class="w-full lg:w-80 space-y-6">
              <!-- 课程视频列表 -->
              <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="font-medium text-dark">课程视频榜单</h3>
                  <span class="text-xs text-primary cursor-pointer" @click="goToDashboard()">查看全部</span>
                </div>
                <div class="overflow-x-auto">
                  <table class="w-full text-sm">
                    <thead>
                      <tr class="border-b border-gray-200">
                        <th class="text-left py-2 text-secondary text-xs">排名</th>
                        <th class="text-left py-2 text-secondary text-xs">视频名</th>
                        <th class="text-left py-2 text-secondary text-xs">时长/min</th>
                        <th class="text-left py-2 text-secondary text-xs">点击量</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="video in videoRanking" :key="video.id" class="border-b border-gray-100">
                        <td class="py-2 text-xs">{{ video.rank }}</td>
                        <td class="py-2 text-xs">{{ video.name }}</td>
                        <td class="py-2 text-xs">{{ video.duration }}</td>
                        <td class="py-2 text-xs">{{ video.clicks }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- 关键时间节点分析 -->
              <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                <h3 class="font-medium text-dark mb-4">关键时间节点分析</h3>
                <div class="space-y-4">
                  <div v-for="node in keyTimeNodes" :key="node.time">
                    <div class="flex justify-between items-center mb-1">
                      <span class="text-xs font-medium">{{ node.time }}</span>
                      <span class="text-xs px-1.5 py-0.5 rounded" :class="node.colorClass">
                        {{ node.count }}
                      </span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2 mb-1">
                      <div class="h-2 rounded-full" :style="`width: ${node.percentage}%`" :class="node.bgColorClass"></div>
                    </div>
                    <p class="text-xs" :class="node.textColorClass">{{ node.description }}</p>
                  </div>
                </div>
              </div>

              <!-- 课程建议 -->
              <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                <h3 class="font-medium text-dark mb-4">课程建议</h3>
                <div class="text-sm text-secondary space-y-2">
                  <p>1. 视频时间3分30秒前内容时长较长，视频内容较为困难，可以适当延长</p>
                  <p>2. 23分30秒后，多方面描述，视频内容较为简单</p>
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
      section1Open: true,
      section2Open: true,
      openSections: {},
      otherChapters: [
        { id: 'section3', name: '第三章' },
        { id: 'section4', name: '第四章' },
        { id: 'section5', name: '第五章' },
        { id: 'section6', name: '第六章' },
        { id: 'section7', name: '第七章' },
        { id: 'section8', name: '第八章' }
      ],
      videoRanking: [
        { id: 1, rank: 1, name: '视频1.1', duration: 15, clicks: '32,214' },
        { id: 2, rank: 2, name: '视频1.2', duration: 21, clicks: '22,145' },
        { id: 3, rank: 3, name: '视频2.1', duration: 18, clicks: '21,567' },
        { id: 4, rank: 4, name: '视频2.2', duration: 17, clicks: '12,356' },
        { id: 5, rank: 5, name: '视频3.1', duration: 21, clicks: '12,356' }
      ],
      keyTimeNodes: [
        { 
          time: '9:00', 
          count: '115条', 
          percentage: 80,
          colorClass: 'text-warning bg-warning/10',
          bgColorClass: 'bg-warning',
          textColorClass: 'text-warning',
          description: '在9:00有115条评论，可能是难点内容'
        },
        { 
          time: '4:00', 
          count: '110个', 
          percentage: 75,
          colorClass: 'text-danger bg-danger/10',
          bgColorClass: 'bg-danger',
          textColorClass: 'text-danger',
          description: '在4:00有110个点赞，内容受欢迎'
        },
        { 
          time: '0:30', 
          count: '33条', 
          percentage: 30,
          colorClass: 'text-success bg-success/10',
          bgColorClass: 'bg-success',
          textColorClass: 'text-success',
          description: '在0:30有33条评论，引发讨论'
        },
        { 
          time: '23:00', 
          count: '52条', 
          percentage: 45,
          colorClass: 'text-primary bg-primary/10',
          bgColorClass: 'bg-primary',
          textColorClass: 'text-primary',
          description: '在23:00有52条变速调整'
        }
      ],
      chartRefs: {},
      chartInstances: {}
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
    toggleSection(section) {
      this[section + 'Open'] = !this[section + 'Open']
    },
    
    toggleOtherSection(sectionId) {
      this.openSections[sectionId] = !this.openSections[sectionId]
      this.$set(this.openSections, sectionId, this.openSections[sectionId])
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
        this.initCompletionChart()
        this.initHotTimeChart()
        this.initInteractionChart()
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
    },
    
    initCompletionChart() {
      if (!this.chartRefs.completionChart) return
      
      this.chartInstances.completionChart = new Chart(this.chartRefs.completionChart, {
        type: 'line',
        data: {
          labels: ['0%', '20%', '40%', '60%', '80%', '100%'],
          datasets: [{ 
            label: '完成率', 
            data: [90, 85, 70, 50, 30, 20], 
            borderColor: '#165DFF', 
            fill: true, 
            backgroundColor: 'rgba(22, 93, 255, 0.1)' 
          }]
        },
        options: { 
          responsive: true, 
          maintainAspectRatio: false, 
          plugins: { 
            legend: { display: false },
            title: { display: false }
          },
          scales: { 
            x: { 
              ticks: { callback: v => v },
              title: { 
                display: true, 
                text: '视频播放进度',
                font: { size: 10 },
                color: '#4E5969'
              }
            },
            y: { 
              ticks: { callback: v => v + '%' },
              title: { 
                display: true, 
                text: '剩余用户百分比',
                font: { size: 10 },
                color: '#4E5969'
              }
            }
          }
        }
      })
    },
    
    initHotTimeChart() {
      if (!this.chartRefs.hotTimeChart) return
      
      this.chartInstances.hotTimeChart = new Chart(this.chartRefs.hotTimeChart, {
        type: 'bar',
        data: {
          labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
          datasets: [{ 
            label: '观看量', 
            data: [120, 80, 200, 350, 280, 420], 
            backgroundColor: '#165DFF' 
          }]
        },
        options: { 
          responsive: true, 
          maintainAspectRatio: false, 
          plugins: { legend: { display: false } },
          indexAxis: 'y'
        }
      })
    },
    
    initInteractionChart() {
      if (!this.chartRefs.todayInteractionChart) return
      
      this.chartInstances.todayInteractionChart = new Chart(this.chartRefs.todayInteractionChart, {
        type: 'bar',
        data: {
          labels: ['转发', '评论', '点赞'],
          datasets: [{
            label: '今日统计',
            data: [326, 542, 896],
            backgroundColor: [
              '#FF9F43',
              '#165DFF',
              '#10B981'
            ],
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return ` ${context.raw} 次`
                }
              }
            }
          },
          scales: {
            x: {
              beginAtZero: true,
              grid: { display: false },
              ticks: { font: { size: 10 }, color: '#4E5969' }
            },
            y: {
              grid: { display: false },
              ticks: { font: { size: 11 }, color: '#4E5969' }
            }
          },
          indexAxis: 'y'
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