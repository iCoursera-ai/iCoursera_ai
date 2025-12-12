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
          <div class="course-section-title flex justify-between items-center cursor-pointer" @click="toggleSection('section1')">
            <span>第一章</span>
            <i class="fa" :class="section1Open ? 'fa-angle-down' : 'fa-angle-right'"></i>
          </div>
          <div class="pl-2" v-show="section1Open">
            <div class="course-item" @click="goToVideoAnalysis()">
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
            <div class="course-item active" @click="goToExerciseAnalysis()">
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

      <!-- 主内容区域：习题详情分析 -->
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
          <span class="text-dark font-medium">习题1.1 - 数据分析</span>
        </div>

        <!-- 页面内容容器 -->
        <div class="space-y-6">
          <!-- 数据分析概览 -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="text-xs text-secondary mb-1">参与人数</div>
              <div class="flex items-center justify-between">
                <div class="text-xl font-bold text-dark">12,568</div>
                <div class="text-success text-xs flex items-center">
                  <i class="fa fa-caret-up mr-1"></i> 156
                </div>
              </div>
              <div class="mt-2 h-10">
                <canvas :ref="el => chartRefs.participantsChart = el"></canvas>
              </div>
            </div>
            
            <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="text-xs text-secondary mb-1">平均正确率</div>
              <div class="flex items-center justify-between">
                <div class="text-xl font-bold text-dark">68%</div>
                <div class="text-danger text-xs flex items-center">
                  <i class="fa fa-caret-down mr-1"></i> 4%
                </div>
              </div>
              <div class="mt-2 h-10">
                <canvas :ref="el => chartRefs.accuracyChart = el"></canvas>
              </div>
            </div>
            
            <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="text-xs text-secondary mb-1">平均用时</div>
              <div class="flex items-center justify-between">
                <div class="text-xl font-bold text-dark">8分25秒</div>
                <div class="text-success text-xs flex items-center">
                  <i class="fa fa-caret-up mr-1"></i> 12秒
                </div>
              </div>
              <div class="mt-2 h-10">
                <canvas :ref="el => chartRefs.timeSpentChart = el"></canvas>
              </div>
            </div>
            
            <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="text-xs text-secondary mb-1">错题提交率</div>
              <div class="flex items-center justify-between">
                <div class="text-xl font-bold text-dark">32%</div>
                <div class="text-success text-xs flex items-center">
                  <i class="fa fa-caret-up mr-1"></i> 2%
                </div>
              </div>
              <div class="mt-2 h-10">
                <canvas :ref="el => chartRefs.errorRateChart = el"></canvas>
              </div>
            </div>
          </div>

          <!-- 习题分析、习题内容和习题建议并排显示 -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- 习题数据分析 -->
            <div class="lg:col-span-2 bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="flex justify-between items-center mb-4">
                <h3 class="font-medium text-dark">习题数据分析</h3>
                <!-- <button class="text-primary text-sm hover:bg-primary/10 px-3 py-1 rounded transition-colors">查看历史数据</button> -->
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- 内容分析饼图 -->
                <div>
                  <h4 class="text-sm font-medium text-gray-600 mb-3">内容分析</h4>
                  <div class="h-48 flex items-center justify-center">
                    <canvas :ref="el => chartRefs.contentAnalysisChart = el"></canvas>
                  </div>
                  <div class="flex justify-center gap-4 mt-2 text-xs text-gray-500">
                    <div class="flex items-center gap-1">
                      <span class="w-3 h-3 rounded-full bg-primary"></span>
                      <span>正确 74%</span>
                    </div>
                    <div class="flex items-center gap-1">
                      <span class="w-3 h-3 rounded-full bg-gray-300"></span>
                      <span>错误 24%</span>
                    </div>
                    <div class="flex items-center gap-1">
                      <span class="w-3 h-3 rounded-full bg-warning"></span>
                      <span>未答 2%</span>
                    </div>
                  </div>
                </div>
                
                <!-- 用时分析柱状图 -->
                <div>
                  <h4 class="text-sm font-medium text-gray-600 mb-3">习题用时分析</h4>
                  <div class="h-48">
                    <canvas :ref="el => chartRefs.timeAnalysisChart = el"></canvas>
                  </div>
                </div>
              </div>
            </div>

            <!-- 习题建议 -->
            <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <h3 class="font-medium text-dark mb-4">习题建议</h3>
              <div class="text-sm text-gray-600 space-y-3">
                <div class="p-3 bg-primary/5 rounded-lg">
                  <p class="font-medium text-primary mb-1">正确率分析</p>
                  <p class="text-xs">所有习题正确率偏低，题目内容难度较高且题目数量不足</p>
                </div>
                <div class="p-3 bg-warning/5 rounded-lg">
                  <p class="font-medium text-warning mb-1">题目问题</p>
                  <p class="text-xs">题目2的正确率偏低，可能题目本身存在问题</p>
                </div>
                <div class="p-3 bg-success/5 rounded-lg">
                  <p class="font-medium text-success mb-1">改进建议</p>
                  <p class="text-xs">建议增加同类题型练习，提高学生对知识点的掌握程度</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 习题内容 - 占满宽度 -->
          <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
            <div class="flex justify-between items-center mb-6">
              <h3 class="font-medium text-dark">习题内容</h3>
              <!-- <button class="bg-primary/10 text-primary text-sm px-3 py-1 rounded hover:bg-primary/20 transition-colors">
                修改题目
              </button> -->
            </div>
            
            <div class="mb-4">
              <h4 class="text-base font-medium text-dark mb-4">01. 单元测验 <span class="text-xs text-primary bg-primary/10 px-2 py-0.5 rounded ml-2">查看帮助</span></h4>
              
              <!-- 题目列表 -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div v-for="question in questions" :key="question.id" class="question-item">
                  <div class="question-header">
                    <span class="w-5 h-5 rounded-full bg-primary/10 text-primary flex items-center justify-center text-xs">{{ question.id }}</span>
                    <span class="text-sm">{{ question.title }}</span>
                  </div>
                  <div class="space-y-1 mt-3">
                    <div v-for="option in question.options" :key="option.id" 
                         class="option-item" 
                         :class="{ 'correct': option.correct }">
                      <div class="flex items-start gap-2">
                        <span class="w-5 h-5 rounded-full flex items-center justify-center text-xs mt-0.5"
                              :class="option.correct ? 'bg-success/10 text-success' : 'bg-gray-100 text-gray-500'">
                          {{ option.letter }}
                        </span>
                        <div class="flex-1">
                          <div class="flex justify-between items-start">
                            <div>
                              <span class="text-sm">{{ option.text }}</span>
                              <span v-if="option.correct" class="ml-2 text-xs text-success bg-success/10 px-1.5 py-0.25 rounded">正确答案</span>
                            </div>
                            <span class="text-xs font-medium ml-2"
                                  :class="option.correct ? 'text-success' : 'text-secondary'">
                              {{ option.percentage }}
                            </span>
                          </div>
                          <!-- 人数比例进度条 -->
                          <div class="mt-1 w-full bg-gray-200 rounded-full h-1.5">
                            <div class="h-1.5 rounded-full"
                                 :class="option.correct ? 'bg-success' : 'bg-primary'"
                                 :style="`width: ${option.percentageValue}%`"></div>
                          </div>
                          <!-- 详细人数信息 -->
                          <div class="flex justify-between mt-1">
                            <span class="text-xs text-gray-500">选择人数: {{ option.peopleCount }}</span>
                            <span class="text-xs text-gray-500">占总人数: {{ option.percentage }}</span>
                          </div>
                        </div>
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
import { Chart } from 'chart.js/auto'

export default {
  name: 'ExerciseAnalysis',
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
      questions: [
        {
          id: 1,
          title: '(2分) 计算机之父是指：',
          options: [
            { 
              id: 1, 
              letter: 'A', 
              text: '艾伦·图灵', 
              correct: true,
              percentage: '65%',
              percentageValue: 65,
              peopleCount: '8,168人'
            },
            { 
              id: 2, 
              letter: 'B', 
              text: '赫尔曼·豪瑟', 
              correct: false,
              percentage: '12%',
              percentageValue: 12,
              peopleCount: '1,508人'
            },
            { 
              id: 3, 
              letter: 'C', 
              text: '蒂姆·伯纳斯-李', 
              correct: false,
              percentage: '18%',
              percentageValue: 18,
              peopleCount: '2,262人'
            },
            { 
              id: 4, 
              letter: 'D', 
              text: '马克·安德森', 
              correct: false,
              percentage: '5%',
              percentageValue: 5,
              peopleCount: '628人'
            }
          ]
        },
        {
          id: 2,
          title: '(2分) 下列属于比较新的人工智能的研究方向：',
          options: [
            { 
              id: 5, 
              letter: 'A', 
              text: '人工神经元网络', 
              correct: false,
              percentage: '28%',
              percentageValue: 28,
              peopleCount: '3,519人'
            },
            { 
              id: 6, 
              letter: 'B', 
              text: '类脑人工智能', 
              correct: true,
              percentage: '45%',
              percentageValue: 45,
              peopleCount: '5,655人'
            },
            { 
              id: 7, 
              letter: 'C', 
              text: '深度学习', 
              correct: false,
              percentage: '22%',
              percentageValue: 22,
              peopleCount: '2,765人'
            },
            { 
              id: 8, 
              letter: 'D', 
              text: '贝叶斯网络', 
              correct: false,
              percentage: '5%',
              percentageValue: 5,
              peopleCount: '629人'
            }
          ]
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
      this.$nextTick(() => {
        this.initSmallCharts()
        this.initAnalysisCharts()
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
      
      // 参与人数小图表
      if (this.chartRefs.participantsChart) {
        this.chartInstances.participantsChart = new Chart(this.chartRefs.participantsChart, {
          type: 'line',
          data: { labels: [1,2,3,4,5,6,7], datasets: [{ data: [5,3,4,6,5,7,9], borderColor: '#165DFF', tension: 0.4 }] },
          options: smallChartConfig
        })
      }
      
      // 正确率小图表
      if (this.chartRefs.accuracyChart) {
        this.chartInstances.accuracyChart = new Chart(this.chartRefs.accuracyChart, {
          type: 'line',
          data: { labels: [1,2,3,4,5,6,7], datasets: [{ data: [72,75,73,70,69,68,68], borderColor: '#F53F3F', tension: 0.4 }] },
          options: smallChartConfig
        })
      }
      
      // 用时小图表
      if (this.chartRefs.timeSpentChart) {
        this.chartInstances.timeSpentChart = new Chart(this.chartRefs.timeSpentChart, {
          type: 'bar',
          data: { labels: [1,2,3,4,5], datasets: [{ data: [6,7,8,8,8.5], backgroundColor: '#10B981' }] },
          options: smallChartConfig
        })
      }
      
      // 错题率小图表
      if (this.chartRefs.errorRateChart) {
        this.chartInstances.errorRateChart = new Chart(this.chartRefs.errorRateChart, {
          type: 'doughnut',
          data: { labels: ['错题', '正确'], datasets: [{ data: [32,68], backgroundColor: ['#F53F3F', '#E5E6EB'] }] },
          options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
        })
      }
    },
    
    initAnalysisCharts() {
      // 内容分析饼图
      if (this.chartRefs.contentAnalysisChart) {
        this.chartInstances.contentAnalysisChart = new Chart(this.chartRefs.contentAnalysisChart, {
          type: 'doughnut',
          data: { 
            labels: ['正确', '错误', '未答'], 
            datasets: [{ 
              data: [74,24,2], 
              backgroundColor: ['#165DFF', '#E5E6EB', '#FF9F43'],
              borderWidth: 0
            }] 
          },
          options: { 
            responsive: true, 
            maintainAspectRatio: false, 
            plugins: { legend: { display: false } },
            cutout: '70%'
          }
        })
      }
      
      // 用时分析柱状图
      if (this.chartRefs.timeAnalysisChart) {
        this.chartInstances.timeAnalysisChart = new Chart(this.chartRefs.timeAnalysisChart, {
          type: 'bar',
          data: {
            labels: ['10分钟', '20分钟', '30分钟', '40分钟', '50分钟'],
            datasets: [{ 
              label: '人数分布', 
              data: [120, 350, 420, 280, 150], 
              backgroundColor: '#165DFF' 
            }]
          },
          options: { 
            responsive: true, 
            maintainAspectRatio: false, 
            plugins: { legend: { display: false } },
            scales: {
              y: { beginAtZero: true, ticks: { display: false } },
              x: { grid: { display: false } }
            }
          }
        })
      }
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

/* 习题样式 */
.question-item {
  @apply border border-gray-200 rounded-lg p-4 bg-white;
}
.question-header {
  @apply font-medium text-dark mb-3 flex items-center gap-2;
}
.option-item {
  @apply pl-6 py-3 hover:bg-gray-50 transition-colors cursor-pointer border-b border-gray-100 last:border-b-0;
}
.option-item.correct {
  @apply bg-success/5 border-l-4 border-success pl-4;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .question-header {
    @apply flex-col items-start;
  }
  
  .question-header span:last-child {
    @apply mt-1 ml-7;
  }
}
</style>