<template>
  <div class="min-h-screen flex flex-col">
    <Header />
    
    <!-- 主内容容器 -->
    <div class="flex-1 bg-gray-50">
      <div class="container mx-auto p-6 md:p-8">
        <!-- 搜索框区域（固定在顶部） -->
        <div class="mb-8">
          <h1 class="text-2xl font-semibold text-dark mb-6">搜索课程</h1>
          
          <!-- 大型搜索框 -->
          <div class="relative max-w-3xl mx-auto">
            <input 
              type="text" 
              id="mainSearchInput"
              v-model="searchQuery"
              placeholder="输入课程名、讲师名或关键词进行搜索..." 
              class="w-full px-6 py-4 pl-14 rounded-lg border border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/30 focus:outline-none transition-all duration-300 text-base shadow-sm"
              @keypress.enter="performSearch"
            >
            <i class="fa fa-search absolute left-5 top-1/2 transform -translate-y-1/2 text-gray-400 text-lg"></i>
            <button @click="performSearch" class="absolute right-3 top-1/2 transform -translate-y-1/2 px-6 py-2 bg-primary text-white rounded-md hover:bg-primary/90 transition-colors">
              搜索
            </button>
          </div>
          
          <!-- 热门搜索推荐 -->
          <div class="mt-6">
            <p class="text-sm text-gray-500 mb-3">热门搜索：</p>
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="hotKeyword in hotKeywords" 
                :key="hotKeyword"
                @click="setSearchQuery(hotKeyword)" 
                class="px-4 py-2 bg-white border border-gray-200 rounded-full text-sm hover:bg-primary hover:text-white hover:border-primary transition-all duration-200"
              >
                {{ hotKeyword }}
              </button>
            </div>
          </div>
        </div>

        <!-- 筛选区域 -->
        <div class="mb-8">
          <div class="flex flex-wrap items-center justify-between gap-4 mb-4">
            <h2 class="text-lg font-semibold text-dark">搜索结果：<span id="resultCount">{{ filteredCourses.length }}</span> 个相关课程</h2>
            <div class="flex items-center gap-4">
              <select v-model="sortBy" class="px-4 py-2 border border-gray-300 rounded-md focus:border-primary focus:outline-none text-sm">
                <option value="default">综合排序</option>
                <option value="hot">按热度排序</option>
                <option value="time">按时间排序</option>
                <option value="rating">按评分排序</option>
              </select>
              <select v-model="selectedCategory" class="px-4 py-2 border border-gray-300 rounded-md focus:border-primary focus:outline-none text-sm">
                <option value="all">全部分类</option>
                <option v-for="category in categories" :key="category.value" :value="category.value">
                  {{ category.label }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <!-- 搜索结果区域 -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- 左侧课程列表 -->
          <div class="lg:col-span-2">
            <div class="space-y-6">
              <!-- 搜索结果卡片 -->
              <div 
                v-for="course in paginatedCourses" 
                :key="course.id"
                class="card p-4 hover:shadow-md transition-shadow duration-200 cursor-pointer" 
                @click="goToCourseDetail(course.id)"
              >
                <div class="flex flex-col md:flex-row gap-4">
                  <div class="relative w-full md:w-48 h-32 rounded-lg overflow-hidden flex-shrink-0">
                    <img :src="course.image" :alt="course.title" class="w-full h-full object-cover">
                    <span :class="course.badgeClass">{{ course.badgeText }}</span>
                    <span class="video-time">{{ formatDuration(course.duration) }}</span>
                  </div>
                  <div class="flex-1">
                    <h3 class="text-lg font-semibold text-dark mb-2 hover:text-primary transition-colors">{{ course.title }}</h3>
                    <p class="text-sm text-gray-600 mb-3 line-clamp-2">
                      {{ course.description }}
                    </p>
                    <div class="flex flex-wrap items-center gap-4 text-sm text-gray-500">
                      <span class="flex items-center gap-1"><i class="fa fa-user text-gray-400"></i> {{ course.teacher }}</span>
                      <span class="flex items-center gap-1"><i class="fa fa-eye text-gray-400"></i> {{ course.views }}</span>
                      <span class="flex items-center gap-1"><i class="fa fa-thumbs-up text-gray-400"></i> {{ course.rating }}</span>
                      <span class="text-xs px-2 py-1 bg-gray-100 rounded">{{ course.category }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 分页 -->
            <div class="flex justify-center items-center gap-2 mt-8">
              <button 
                @click="prevPage" 
                :disabled="currentPage === 1"
                class="w-10 h-10 flex items-center justify-center rounded-md border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <i class="fa fa-angle-left text-gray-500"></i>
              </button>
              
              <button 
                v-for="page in visiblePages" 
                :key="page"
                @click="goToPage(page)"
                class="w-10 h-10 flex items-center justify-center rounded-md border"
                :class="currentPage === page ? 'bg-primary text-white border-primary' : 'border-gray-200 hover:bg-gray-50'"
              >
                {{ page }}
              </button>
              
              <button 
                @click="nextPage" 
                :disabled="currentPage === totalPages"
                class="w-10 h-10 flex items-center justify-center rounded-md border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <i class="fa fa-angle-right text-gray-500"></i>
              </button>
            </div>
          </div>

          <!-- 右侧筛选和推荐 -->
          <div class="space-y-6">
            <!-- 高级筛选 -->
            <div class="card p-5">
              <h3 class="text-lg font-semibold text-dark mb-4">高级筛选</h3>
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">难度等级</label>
                  <div class="space-y-2">
                    <label v-for="level in difficultyLevels" :key="level.value" class="flex items-center">
                      <input 
                        type="checkbox" 
                        v-model="selectedDifficulty"
                        :value="level.value"
                        class="rounded text-primary focus:ring-primary"
                      >
                      <span class="ml-2 text-sm text-gray-600">{{ level.label }}</span>
                    </label>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">课程时长</label>
                  <div class="space-y-2">
                    <label v-for="duration in durationFilters" :key="duration.value" class="flex items-center">
                      <input 
                        type="checkbox" 
                        v-model="selectedDuration"
                        :value="duration.value"
                        class="rounded text-primary focus:ring-primary"
                      >
                      <span class="ml-2 text-sm text-gray-600">{{ duration.label }}</span>
                    </label>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">课程价格</label>
                  <div class="space-y-2">
                    <label class="flex items-center">
                      <input type="checkbox" v-model="isFree" class="rounded text-primary focus:ring-primary">
                      <span class="ml-2 text-sm text-gray-600">免费</span>
                    </label>
                    <label class="flex items-center">
                      <input type="checkbox" v-model="isPaid" class="rounded text-primary focus:ring-primary">
                      <span class="ml-2 text-sm text-gray-600">付费</span>
                    </label>
                  </div>
                </div>
                
                <button @click="applyFilters" class="w-full mt-4 px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90 transition-colors">
                  应用筛选
                </button>
              </div>
            </div>

            <!-- 相关讲师推荐 -->
            <div class="card p-5">
              <h3 class="text-lg font-semibold text-dark mb-4">相关讲师</h3>
              <div class="space-y-4">
                <div 
                  v-for="teacher in relatedTeachers" 
                  :key="teacher.id"
                  class="flex items-center gap-3 p-3 hover:bg-gray-50 rounded-md cursor-pointer"
                  @click="goToTeacherProfile(teacher.id)"
                >
                  <div class="w-12 h-12 rounded-full bg-gray-200 overflow-hidden">
                    <img :src="teacher.avatar" class="w-full h-full object-cover">
                  </div>
                  <div>
                    <h4 class="text-sm font-medium text-dark">{{ teacher.name }}</h4>
                    <p class="text-xs text-gray-500">{{ teacher.expertise }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- 相关分类 -->
            <div class="card p-5">
              <h3 class="text-lg font-semibold text-dark mb-4">相关分类</h3>
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="category in relatedCategories" 
                  :key="category"
                  class="px-3 py-1 bg-blue-50 text-primary rounded-full text-sm cursor-pointer hover:bg-blue-100"
                  @click="setSearchQuery(category)"
                >
                  {{ category }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'SearchPage',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      searchQuery: '深度学习',
      hotKeywords: ['Python编程', '人工智能', '机器学习', '数据分析', '金融投资', '医学基础'],
      courses: [
        { 
          id: 1, 
          title: '深度学习实战：从零搭建AI模型', 
          description: '本课程将带你从零开始学习深度学习，掌握TensorFlow和PyTorch框架，构建各种AI模型，包括图像识别、自然语言处理等实际应用案例。',
          teacher: '李明教授', 
          views: '25.6万播放', 
          rating: '98%好评',
          category: '人工智能',
          duration: 46540, // seconds
          image: 'https://picsum.photos/300/200?random=101',
          badgeClass: 'badge-blue',
          badgeText: '新品',
          difficulty: 'intermediate',
          price: 'free'
        },
        { 
          id: 2, 
          title: '机器学习基础：理论与Python实践', 
          description: '系统学习机器学习核心算法，包括线性回归、逻辑回归、决策树、支持向量机等，结合Python代码实践，掌握模型训练与评估方法。',
          teacher: '王静教授', 
          views: '18.3万播放', 
          rating: '96%好评',
          category: '人工智能',
          duration: 30015,
          image: 'https://picsum.photos/300/200?random=102',
          badgeClass: 'badge-green',
          badgeText: '精讲',
          difficulty: 'beginner',
          price: 'free'
        },
        { 
          id: 3, 
          title: '深度学习进阶：神经网络优化与应用', 
          description: '深入学习卷积神经网络、循环神经网络、注意力机制等高级深度学习模型，探索在计算机视觉、自然语言处理等领域的实际应用。',
          teacher: '陈明教授', 
          views: '12.7万播放', 
          rating: '95%好评',
          category: '人工智能',
          duration: 55845,
          image: 'https://picsum.photos/300/200?random=103',
          badgeClass: 'badge-orange',
          badgeText: '新课',
          difficulty: 'advanced',
          price: 'paid'
        },
        { 
          id: 4, 
          title: 'Python数据分析实战：从数据处理到可视化', 
          description: '掌握Pandas、NumPy、Matplotlib等数据分析核心库，学习数据清洗、统计分析、可视化展示等技能，应用于实际业务场景。',
          teacher: '张伟教授', 
          views: '22.4万播放', 
          rating: '97%好评',
          category: '数据科学',
          duration: 36930,
          image: 'https://picsum.photos/300/200?random=104',
          badgeClass: 'badge-blue',
          badgeText: '新品',
          difficulty: 'intermediate',
          price: 'free'
        },
        { 
          id: 5, 
          title: '人工智能在医疗健康领域的应用', 
          description: '探索人工智能在医学影像分析、疾病诊断、药物研发等医疗健康领域的创新应用，学习相关算法模型和技术实现。',
          teacher: '刘芳教授', 
          views: '14.8万播放', 
          rating: '94%好评',
          category: '医学健康',
          duration: 35120,
          image: 'https://picsum.photos/300/200?random=105',
          badgeClass: 'badge-green',
          badgeText: '精讲',
          difficulty: 'intermediate',
          price: 'paid'
        }
      ],
      categories: [
        { value: 'programming', label: '编程开发' },
        { value: 'ai', label: '人工智能' },
        { value: 'data-science', label: '数据科学' },
        { value: 'business', label: '商业管理' },
        { value: 'medical', label: '医学健康' }
      ],
      selectedCategory: 'all',
      sortBy: 'default',
      difficultyLevels: [
        { value: 'beginner', label: '入门' },
        { value: 'intermediate', label: '中级' },
        { value: 'advanced', label: '高级' }
      ],
      selectedDifficulty: [],
      durationFilters: [
        { value: 'short', label: '0-5小时' },
        { value: 'medium', label: '5-15小时' },
        { value: 'long', label: '15小时以上' }
      ],
      selectedDuration: [],
      isFree: true,
      isPaid: false,
      relatedTeachers: [
        { id: 1, name: '李明教授', expertise: '人工智能专家', avatar: 'https://picsum.photos/100/100?random=201' },
        { id: 2, name: '王静教授', expertise: '机器学习专家', avatar: 'https://picsum.photos/100/100?random=202' },
        { id: 3, name: '陈明教授', expertise: '深度学习专家', avatar: 'https://picsum.photos/100/100?random=203' }
      ],
      relatedCategories: ['人工智能', '机器学习', '深度学习', '神经网络', '计算机视觉', '自然语言处理'],
      currentPage: 1,
      pageSize: 5
    }
  },
  computed: {
    filteredCourses() {
      let filtered = [...this.courses]
      
      // 搜索关键词过滤
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(course => 
          course.title.toLowerCase().includes(query) ||
          course.description.toLowerCase().includes(query) ||
          course.teacher.toLowerCase().includes(query) ||
          course.category.toLowerCase().includes(query)
        )
      }
      
      // 分类过滤
      if (this.selectedCategory !== 'all') {
        const categoryMap = {
          'programming': '编程开发',
          'ai': '人工智能',
          'data-science': '数据科学',
          'business': '商业管理',
          'medical': '医学健康'
        }
        const targetCategory = categoryMap[this.selectedCategory] || this.selectedCategory
        filtered = filtered.filter(course => course.category === targetCategory)
      }
      
      // 难度过滤
      if (this.selectedDifficulty.length > 0) {
        filtered = filtered.filter(course => this.selectedDifficulty.includes(course.difficulty))
      }
      
      // 时长过滤
      if (this.selectedDuration.length > 0) {
        filtered = filtered.filter(course => {
          const hours = course.duration / 3600
          if (this.selectedDuration.includes('short')) return hours <= 5
          if (this.selectedDuration.includes('medium')) return hours > 5 && hours <= 15
          if (this.selectedDuration.includes('long')) return hours > 15
          return true
        })
      }
      
      // 价格过滤
      const priceFilters = []
      if (this.isFree) priceFilters.push('free')
      if (this.isPaid) priceFilters.push('paid')
      if (priceFilters.length > 0) {
        filtered = filtered.filter(course => priceFilters.includes(course.price))
      }
      
      // 排序
      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'hot':
            return parseInt(b.views.replace(/[^\d]/g, '')) - parseInt(a.views.replace(/[^\d]/g, ''))
          case 'time':
            return b.id - a.id // 假设ID越大越新
          case 'rating':
            return parseFloat(b.rating) - parseFloat(a.rating)
          default:
            return 0
        }
      })
      
      return filtered
    },
    totalPages() {
      return Math.ceil(this.filteredCourses.length / this.pageSize)
    },
    paginatedCourses() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredCourses.slice(start, end)
    },
    visiblePages() {
      const pages = []
      const maxVisible = 5
      
      if (this.totalPages <= maxVisible) {
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i)
        }
      } else {
        let start = Math.max(1, this.currentPage - 2)
        let end = Math.min(this.totalPages, start + maxVisible - 1)
        
        if (end - start + 1 < maxVisible) {
          start = Math.max(1, end - maxVisible + 1)
        }
        
        for (let i = start; i <= end; i++) {
          pages.push(i)
        }
      }
      
      return pages
    }
  },
  mounted() {
    // 页面加载时聚焦到搜索框
    const searchInput = document.getElementById('mainSearchInput')
    if (searchInput) {
      searchInput.focus()
    }
  },
  methods: {
    setSearchQuery(query) {
      this.searchQuery = query
      this.performSearch()
    },
    
    performSearch() {
      if (this.searchQuery.trim()) {
        // 在实际应用中，这里可以发送搜索请求到后端
        console.log(`正在搜索: ${this.searchQuery}`)
        this.currentPage = 1 // 重置到第一页
      }
    },
    
    formatDuration(seconds) {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const secs = seconds % 60
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    },
    
    applyFilters() {
      this.currentPage = 1 // 重置到第一页
    },
    
    goToCourseDetail(courseId) {
      this.$router.push({ 
        name: 'CourseDetail', 
        params: { id: courseId },
        query: { from: 'search' }
      })
    },
    
    goToTeacherProfile(teacherId) {
      this.$router.push({ 
        name: 'TeacherProfile', 
        params: { id: teacherId }
      })
    },
    
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
      }
    },
    
    goToPage(page) {
      this.currentPage = page
    }
  }
}
</script>

<style scoped>
/* 引入Tailwind中的自定义工具类 */
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* 卡片hover效果优化 */
.card {
  transition: all 0.3s ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
}

/* 限制行数 */
.line-clamp-1 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
}
.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}
.line-clamp-3 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}

/* 视频相关工具类 */
.badge-hot {
  @apply absolute top-2 left-2 bg-red-500 text-white text-xs px-2 py-0.5 rounded z-10;
}
.badge-blue {
  @apply absolute top-2 left-2 bg-primary text-white text-xs px-2 py-0.5 rounded z-10;
}
.badge-green {
  @apply absolute top-2 left-2 bg-success text-white text-xs px-2 py-0.5 rounded z-10;
}
.badge-orange {
  @apply absolute top-2 left-2 bg-orange-500 text-white text-xs px-2 py-0.5 rounded z-10;
}
.video-time {
  @apply absolute bottom-2 right-2 bg-black/70 text-white text-xs px-1.5 py-0.5 rounded z-10;
}
.video-card-hover {
  @apply hover:shadow-md transition-shadow duration-200 cursor-pointer;
}

/* 确保所有课程卡片都有手型光标 */
.cursor-pointer {
  cursor: pointer;
}
</style>