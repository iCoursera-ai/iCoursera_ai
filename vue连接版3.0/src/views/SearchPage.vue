<template>
  <div class="min-h-screen flex flex-col">
    <Header />
    
    <div class="flex-1 bg-gray-50">
      <div class="container mx-auto p-6 md:p-8">
        <!-- 搜索框区域 -->
        <div class="mb-8">
          <h1 class="text-2xl font-semibold text-gray-800 mb-6">搜索课程</h1>
          
          <!-- 搜索框 -->
          <div class="relative max-w-3xl mx-auto">
            <input 
              type="text" 
              id="mainSearchInput"
              v-model="searchQuery"
              placeholder="输入课程名称、描述或领域..." 
              class="w-full px-6 py-4 pl-14 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30 focus:outline-none transition-all duration-300 text-base shadow-sm"
              @keypress.enter="performSearch"
            >
            <i class="fa fa-search absolute left-5 top-1/2 transform -translate-y-1/2 text-gray-400 text-lg"></i>
            <button 
              @click="performSearch" 
              :disabled="isLoading"
              class="absolute right-3 top-1/2 transform -translate-y-1/2 px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <i v-if="isLoading" class="fa fa-spinner fa-spin mr-2"></i>
              搜索
            </button>
          </div>
          
          <!-- 热门搜索推荐 -->
          <div class="mt-6">
            <p class="text-sm text-gray-500 mb-3">热门搜索：</p>
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="keyword in hotKeywords" 
                :key="keyword"
                @click="setSearchQuery(keyword)" 
                class="px-4 py-2 bg-white border border-gray-200 rounded-full text-sm hover:bg-blue-500 hover:text-white hover:border-blue-500 transition-all duration-200"
              >
                {{ keyword }}
              </button>
            </div>
          </div>
        </div>

        <!-- 筛选区域 -->
        <div v-if="searchTerm" class="mb-8">
          <div class="flex flex-wrap items-center justify-between gap-4 mb-4">
            <div>
              <h2 class="text-lg font-semibold text-gray-800 mb-1">
                搜索结果："{{ searchTerm }}"
                <span class="text-sm font-normal text-gray-500 ml-2">
                  {{ sortDirectionText }}
                </span>
              </h2>
              <p class="text-sm text-gray-500">
                找到 {{ pagination.total }} 个相关课程
              </p>
            </div>
            
            <div class="flex items-center gap-4">
              <select 
                v-model="sortBy" 
                @change="applyFilters"
                class="px-4 py-2 border border-gray-300 rounded-md focus:border-blue-500 focus:outline-none text-sm"
              >
                <option v-for="option in sortOptions" :key="option.value" :value="option.value">
                  {{ option.label }}
                </option>
              </select>
              
              <select 
                v-model="selectedDomain" 
                @change="applyFilters"
                class="px-4 py-2 border border-gray-300 rounded-md focus:border-blue-500 focus:outline-none text-sm"
              >
                <option value="all">全部分类</option>
                <option v-for="domain in domains" :key="domain" :value="domain">
                  {{ domain }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="isLoading" class="text-center py-12">
          <i class="fa fa-spinner fa-spin text-4xl text-blue-500 mb-4"></i>
          <p class="text-gray-600">正在搜索...</p>
        </div>

        <!-- 错误状态 -->
        <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 mb-8">
          <div class="flex items-center">
            <i class="fa fa-exclamation-triangle text-red-500 text-2xl mr-3"></i>
            <div>
              <h3 class="text-red-800 font-semibold">搜索失败</h3>
              <p class="text-red-600 mt-1">{{ error }}</p>
              <button @click="performSearch" class="mt-3 px-4 py-2 bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors">
                <i class="fa fa-redo mr-2"></i>重新搜索
              </button>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else-if="!isLoading && searchTerm && courses.length === 0" class="text-center py-16">
          <i class="fa fa-search text-5xl text-gray-300 mb-4"></i>
          <h4 class="text-gray-500 font-medium mb-2">没有找到相关课程</h4>
          <p class="text-gray-400 text-sm mb-4">请尝试其他关键词或简化搜索词</p>
          <div class="flex justify-center gap-2">
            <button @click="clearSearch" class="px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors">
              清空搜索
            </button>
            <button 
              v-for="keyword in hotKeywords.slice(0, 3)"
              :key="keyword"
              @click="setSearchQuery(keyword)" 
              class="px-4 py-2 bg-blue-50 text-blue-600 rounded hover:bg-blue-100 transition-colors"
            >
              {{ keyword }}
            </button>
          </div>
        </div>

        <!-- 搜索结果区域 -->
        <div v-else-if="!isLoading && courses.length > 0">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- 课程卡片 -->
            <div 
              v-for="course in paginatedCourses" 
              :key="course.course_id"
              class="bg-white rounded-lg overflow-hidden border border-gray-200 hover:shadow-lg transition-all duration-300 cursor-pointer group"
              @click="goToCourse(course)"
            >
              <!-- 课程封面 -->
              <div class="relative h-48 bg-gradient-to-br from-blue-50 to-gray-100 overflow-hidden">
                <img 
                  v-if="course.thumbnail_url"
                  :src="course.thumbnail_url" 
                  :alt="course.course_name"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                >
                <div v-else class="w-full h-full flex items-center justify-center">
                  <i class="fa fa-book-open text-4xl text-blue-300"></i>
                </div>
                
                <!-- 课程时长 -->
                <div class="absolute bottom-3 right-3 px-2 py-1 bg-black/60 text-white text-xs rounded flex items-center">
                  <i class="fa fa-clock mr-1"></i>
                  {{ formatDurationHours(course.duration_hours) }}
                </div>
                
                <!-- 难度标签 -->
                <div class="absolute top-3 left-3 px-2 py-1 bg-black/60 text-white text-xs rounded">
                  {{ getDifficultyText(course.difficulty) }}
                </div>
              </div>
              
              <!-- 课程信息 -->
              <div class="p-4">
                <div class="flex items-start justify-between mb-2">
                  <h4 class="text-sm font-semibold text-gray-800 line-clamp-2 hover:text-blue-600 flex-1">
                    {{ course.course_name }}
                  </h4>
                  <span v-if="course.rating" class="ml-2 px-2 py-1 bg-yellow-50 text-yellow-700 text-xs rounded flex items-center whitespace-nowrap">
                    <i class="fa fa-star text-yellow-500 mr-1"></i>
                    {{ formatRating(course.rating) }}
                  </span>
                </div>
                
                <div class="text-xs text-gray-500 mb-3">{{ course.domain }}</div>
                
                <p class="text-xs text-gray-600 line-clamp-2 mb-4">
                  {{ course.description || '暂无课程描述' }}
                </p>
                
                <div class="flex items-center justify-between text-xs">
                  <div class="flex items-center text-gray-500">
                    <i class="fa fa-user-graduate mr-1"></i>
                    <span>{{ formatStudentCount(course.enrolled_count) }}人学习</span>
                  </div>
                  <div class="flex items-center text-gray-500">
                    <i class="fa fa-layer-group mr-1"></i>
                    <span>{{ course.chapter_count || 0 }}章节</span>
                  </div>
                  <div class="text-xs text-gray-400">
                    {{ course.created_at ? new Date(course.created_at).toLocaleDateString() : '' }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 分页 -->
          <div v-if="pagination.total_pages > 1" class="mt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div class="text-sm text-gray-500">
              显示第 {{ ((pagination.page - 1) * pagination.page_size) + 1 }} - 
              {{ Math.min(pagination.page * pagination.page_size, pagination.total) }} 条，
              共 {{ pagination.total }} 条结果
            </div>
            
            <nav class="flex items-center space-x-2">
              <button
                @click="loadPage(pagination.page - 1)"
                :disabled="pagination.page === 1"
                class="w-10 h-10 flex items-center justify-center rounded-md border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <i class="fa fa-angle-left text-gray-500"></i>
              </button>
              
              <button
                v-for="pageNum in visiblePages"
                :key="pageNum"
                @click="loadPage(pageNum)"
                class="w-10 h-10 flex items-center justify-center rounded-md border transition-colors"
                :class="{
                  'bg-blue-500 text-white border-blue-500': pagination.page === pageNum,
                  'border-gray-200 hover:bg-gray-50': pagination.page !== pageNum
                }"
              >
                {{ pageNum }}
              </button>
              
              <button
                @click="loadPage(pagination.page + 1)"
                :disabled="pagination.page === pagination.total_pages"
                class="w-10 h-10 flex items-center justify-center rounded-md border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <i class="fa fa-angle-right text-gray-500"></i>
              </button>
            </nav>
          </div>
        </div>

        <!-- 热门推荐（搜索前显示） -->
        <div v-else-if="!isLoading && !searchTerm">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
            <div 
              v-for="(category, index) in domains" 
              :key="index"
              @click="setSearchQuery(category)"
              class="bg-white p-6 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all duration-300 cursor-pointer"
            >
              <div class="flex items-center mb-4">
                <div class="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center mr-3">
                  <i class="fa fa-book text-blue-500"></i>
                </div>
                <h3 class="font-semibold text-gray-800">{{ category }}</h3>
              </div>
              <p class="text-sm text-gray-500">探索{{ category }}相关课程</p>
            </div>
          </div>
          
          <h2 class="text-xl font-bold text-gray-800 mb-4">热门搜索</h2>
          <div class="flex flex-wrap gap-3">
            <button 
              v-for="keyword in hotKeywords" 
              :key="keyword"
              @click="setSearchQuery(keyword)" 
              class="px-5 py-3 bg-white border border-gray-200 rounded-lg hover:bg-blue-50 hover:border-blue-300 hover:text-blue-600 transition-all duration-200 flex items-center"
            >
              <i class="fa fa-search text-sm mr-2 text-gray-400 group-hover:text-blue-500"></i>
              {{ keyword }}
            </button>
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
import courseService from '@/service/course.js'

export default {
  name: 'SearchPage',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      searchQuery: '',
      searchTerm: '',
      hotKeywords: ['Python编程', '人工智能', '机器学习', '数据分析', '金融投资', '医学基础'],
      courses: [],
      
      // 筛选条件
      sortBy: 'enrolled_count',  // 默认按热度排序
      sortOptions: [  // 修改排序选项
        { value: 'enrolled_count', label: '按热度排序', icon: 'fa fa-fire' },
        { value: 'duration_hours', label: '按时长排序', icon: 'fa fa-clock' },
        { value: 'rating', label: '按评分排序', icon: 'fa fa-star' }
      ],
      selectedDomain: 'all',
      domains: ['编程开发', '人工智能', '数据科学', '商业管理', '医学健康'],
      
      // 加载状态
      isLoading: false,
      error: '',
      
      // 分页
      pagination: {
        page: 1,
        page_size: 12,
        total: 0,
        total_pages: 0
      }
    }
  },
  computed: {
    paginatedCourses() {
      // 确保每个课程都有封面图片
      return this.courses.map(course => ({
        ...course,
        thumbnail_url: this.getCourseThumbnail(course)
      }))
    },
    
    totalPages() {
      return this.pagination.total_pages || 0
    },
    
    visiblePages() {
      const pages = []
      const maxVisible = 5
      
      if (this.totalPages <= maxVisible) {
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i)
        }
      } else {
        let start = Math.max(1, this.pagination.page - 2)
        let end = Math.min(this.totalPages, start + maxVisible - 1)
        
        if (end - start + 1 < maxVisible) {
          start = Math.max(1, end - maxVisible + 1)
        }
        
        for (let i = start; i <= end; i++) {
          pages.push(i)
        }
      }
      
      return pages
    },
    
    // 显示当前排序方式的文本
    currentSortLabel() {
      const option = this.sortOptions.find(opt => opt.value === this.sortBy)
      return option ? option.label : '按热度排序'
    },
    
    // 显示当前排序的图标
    sortIcon() {
      const option = this.sortOptions.find(opt => opt.value === this.sortBy)
      return option ? option.icon : 'fa fa-sort'
    },
    
    // 获取排序方向的描述
    sortDirectionText() {
      switch(this.sortBy) {
        case 'enrolled_count':
          return '（学习人数从高到低）'
        case 'duration_hours':
          return '（课程时长从长到短）'
        case 'rating':
          return '（评分从高到低）'
        default:
          return ''
      }
    }
  },
  mounted() {
    // 从URL参数中获取搜索词和排序方式
    const query = this.$route.query.q
    const sortByFromUrl = this.$route.query.sort_by || this.$route.query.sort  // 尝试读取 sort_by 或 sort
    
    if (query) {
      this.searchQuery = query
      this.searchTerm = query
    }
    
    if (sortByFromUrl) {
      this.sortBy = sortByFromUrl
    }
    
    if (query) {
      this.performSearch()
    }
    
    // 页面加载时聚焦到搜索框
    const searchInput = document.getElementById('mainSearchInput')
    if (searchInput) {
      searchInput.focus()
    }
  },
  methods: {
    getCourseThumbnail(course) {
      // 如果有封面图片，直接返回
      if (course.thumbnail_url && course.thumbnail_url.trim() !== '') {
        return course.thumbnail_url
      }
      
      // 根据课程ID生成随机封面
      const courseId = course.course_id || course.id || 'default'
      
      // 使用稳定的随机种子，确保同一课程的封面不变
      const seed = this.hashString(courseId)
      
      // 根据领域选择不同的图片主题
      const domainThemes = {
        '编程开发': ['code', 'computer', 'laptop', 'programming', 'software'],
        '人工智能': ['ai', 'robot', 'neural', 'brain', 'future'],
        '数据科学': ['data', 'chart', 'analytics', 'statistics', 'graph'],
        '商业管理': ['business', 'meeting', 'office', 'strategy', 'finance'],
        '医学健康': ['medical', 'health', 'doctor', 'hospital', 'science'],
        'default': ['education', 'learning', 'study', 'knowledge', 'book']
      }
      
      const theme = domainThemes[course.domain] || domainThemes['default']
      const themeIndex = seed % theme.length
      const selectedTheme = theme[themeIndex]
      
      // 生成Picsum随机图片URL，使用课程ID作为随机种子
      return `https://picsum.photos/seed/${courseId}_${selectedTheme}/400/225`
    },
    hashString(str) {
      let hash = 0
      for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i)
        hash = ((hash << 5) - hash) + char
        hash = hash & hash // 转换为32位整数
      }
      return Math.abs(hash)
    },
    setSearchQuery(query) {
      this.searchQuery = query
      this.performSearch()
    },
    
    async performSearch() {
      if (!this.searchQuery.trim()) {
        this.error = '请输入搜索关键词'
        return
      }
      
      this.isLoading = true
      this.error = ''
      this.searchTerm = this.searchQuery.trim()
      this.pagination.page = 1
      
      try {
        const response = await courseService.searchCoursesByName(
          this.searchTerm,
          this.pagination.page,
          this.pagination.page_size,
          this.sortBy,  // 这个会作为 sort_by 参数传递给API
          this.selectedDomain !== 'all' ? this.selectedDomain : null
        )
        
        if (response.code === 200) {
          this.courses = response.data.courses || []
          this.pagination = {
            ...this.pagination,
            ...response.data.pagination
          }
          
          // 关键修改：URL参数名改为 sort_by
          this.$router.replace({
            query: { 
              q: this.searchTerm,
              sort_by: this.sortBy  // 改为 sort_by
            }
          })
          
          console.log(`按${this.currentSortLabel}搜索成功，找到${this.courses.length}个课程`)
        } else {
          this.error = response.msg || '搜索失败'
        }
      } catch (err) {
        console.error('搜索错误:', err)
        this.error = '网络错误，请稍后重试'
        
        // API失败时使用模拟数据
        if (!this.courses.length) {
          this.useMockData()
        }
      } finally {
        this.isLoading = false
      }
    },
    
    async loadPage(page) {
      if (page === this.pagination.page) return
      
      this.pagination.page = page
      this.isLoading = true
      
      try {
        const response = await courseService.searchCoursesByName(
          this.searchTerm,
          page,
          this.pagination.page_size,
          this.sortBy,  // 传递 sort_by 参数
          this.selectedDomain !== 'all' ? this.selectedDomain : null
        )
        
        if (response.code === 200) {
          this.courses = response.data.courses || []
          this.pagination = {
            ...this.pagination,
            ...response.data.pagination
          }
          
          window.scrollTo({ top: 0, behavior: 'smooth' })
          
          // 更新URL时也使用正确的参数名
          this.$router.replace({
            query: { 
              q: this.searchTerm,
              sort_by: this.sortBy  // 改为 sort_by
            }
          })
        }
      } catch (err) {
        console.error('加载分页错误:', err)
        this.error = '加载失败'
      } finally {
        this.isLoading = false
      }
    },
    
    async applyFilters() {
      if (!this.searchTerm) return
      
      this.pagination.page = 1
      await this.performSearch()
    },
    
    // 切换排序方式
    changeSort(sortValue) {
      this.sortBy = sortValue
      this.applyFilters()
    },
    
    clearSearch() {
      this.searchQuery = ''
      this.searchTerm = ''
      this.courses = []
      this.error = ''
      this.$router.replace({ query: {} })
    },
    
    goToCourse(course) {
      const courseId = course.course_id || course.id
      if (!courseId) {
        console.error('课程ID不存在:', course)
        return
      }
      
      localStorage.setItem('currentCourseInfo', JSON.stringify({
        course_id: courseId,
        course_name: course.course_name || course.title,
        teacher_id: course.user_id || course.teacher_id,
        thumbnail_url: course.thumbnail_url ||  this.getCourseThumbnail(course),
        from: 'search'
      }))
      
      this.$router.push({
        name: 'VideoPlayer',
        params: {
          courseId: courseId
        },
        query: {
          courseId: courseId,
          courseName: course.course_name || course.title,
          teacherId: course.user_id || course.teacher_id,
          from: 'search',
          searchTerm: this.searchTerm,
          sortBy: this.sortBy
        }
      })
    },
    
    getDifficultyText(difficulty) {
      const difficultyMap = {
        1: '入门',
        2: '初级',
        3: '中级',
        4: '高级',
        5: '专家'
      }
      return difficultyMap[difficulty] || '未知'
    },
    
    // 格式化时长显示
    formatDurationHours(hours) {
      if (!hours && hours !== 0) return '0小时'
      
      const totalHours = Math.floor(hours)
      const minutes = Math.round((hours - totalHours) * 60)
      
      if (totalHours > 0 && minutes > 0) {
        return `${totalHours}小时${minutes}分钟`
      } else if (totalHours > 0) {
        return `${totalHours}小时`
      } else {
        return `${minutes}分钟`
      }
    },
    
    // 格式化评分
    formatRating(rating) {
      if (!rating && rating !== 0) return '未评分'
      return rating.toFixed(1)
    },
    
    // 格式化学生人数
    formatStudentCount(count) {
      if (!count) return '0'
      if (count >= 10000) {
        return (count / 10000).toFixed(1) + '万'
      }
      return count.toString()
    },
    
    // 模拟数据（按不同排序方式演示）
    useMockData() {
      // 模拟按热度排序的数据
      if (this.sortBy === 'enrolled_count') {
        this.courses = [
          { 
            course_id: 'C001',
            course_name: '深度学习实战：从零搭建AI模型', 
            thumbnail_url: 'https://picsum.photos/400/225?random=101',
            difficulty: 3,
            rating: 4.8,
            enrolled_count: 25600,  // 最多人学习
            duration_hours: 24.5,
            chapter_count: 12,
            domain: '人工智能',
            created_at: '2024-01-15 10:00:00',
            user_id: 'T001'
          },
          { 
            course_id: 'C004',
            course_name: 'Python数据分析实战：从数据处理到可视化', 
            thumbnail_url: 'https://picsum.photos/400/225?random=104',
            difficulty: 3,
            rating: 4.9,
            enrolled_count: 22400,  // 第二多
            duration_hours: 18,
            chapter_count: 8,
            domain: '数据科学',
            created_at: '2024-02-10 14:30:00',
            user_id: 'T004'
          },
          { 
            course_id: 'C002',
            course_name: '机器学习基础：理论与Python实践', 
            thumbnail_url: 'https://picsum.photos/400/225?random=102',
            difficulty: 2,
            rating: 4.6,
            enrolled_count: 18300,  // 第三多
            duration_hours: 20,
            chapter_count: 10,
            domain: '人工智能',
            created_at: '2024-01-25 09:15:00',
            user_id: 'T002'
          }
        ]
      }
      // 模拟按时长排序的数据
      else if (this.sortBy === 'duration_hours') {
        this.courses = [
          { 
            course_id: 'C003',
            course_name: '深度学习进阶：神经网络优化与应用', 
            thumbnail_url: 'https://picsum.photos/400/225?random=103',
            difficulty: 4,
            rating: 4.8,
            enrolled_count: 12700,
            duration_hours: 48.5,  // 最长
            chapter_count: 15,
            domain: '人工智能',
            created_at: '2024-02-05 11:20:00',
            user_id: 'T003'
          },
          { 
            course_id: 'C001',
            course_name: '深度学习实战：从零搭建AI模型', 
            thumbnail_url: 'https://picsum.photos/400/225?random=101',
            difficulty: 3,
            rating: 4.8,
            enrolled_count: 25600,
            duration_hours: 36,  // 第二长
            chapter_count: 12,
            domain: '人工智能',
            created_at: '2024-01-15 10:00:00',
            user_id: 'T001'
          },
          { 
            course_id: 'C006',
            course_name: 'Java高级编程与系统架构', 
            thumbnail_url: 'https://picsum.photos/400/225?random=106',
            difficulty: 4,
            rating: 4.7,
            enrolled_count: 9800,
            duration_hours: 30.5,  // 第三长
            chapter_count: 14,
            domain: '编程开发',
            created_at: '2024-01-20 13:45:00',
            user_id: 'T006'
          }
        ]
      }
      // 模拟按评分排序的数据
      else if (this.sortBy === 'rating') {
        this.courses = [
          { 
            course_id: 'C004',
            course_name: 'Python数据分析实战：从数据处理到可视化', 
            thumbnail_url: 'https://picsum.photos/400/225?random=104',
            difficulty: 3,
            rating: 4.9,  // 最高分
            enrolled_count: 22400,
            duration_hours: 18,
            chapter_count: 8,
            domain: '数据科学',
            created_at: '2024-02-10 14:30:00',
            user_id: 'T004'
          },
          { 
            course_id: 'C001',
            course_name: '深度学习实战：从零搭建AI模型', 
            thumbnail_url: 'https://picsum.photos/400/225?random=101',
            difficulty: 3,
            rating: 4.8,  // 第二高分
            enrolled_count: 25600,
            duration_hours: 24.5,
            chapter_count: 12,
            domain: '人工智能',
            created_at: '2024-01-15 10:00:00',
            user_id: 'T001'
          },
          { 
            course_id: 'C003',
            course_name: '深度学习进阶：神经网络优化与应用', 
            thumbnail_url: 'https://picsum.photos/400/225?random=103',
            difficulty: 4,
            rating: 4.8,  // 并列第二
            enrolled_count: 12700,
            duration_hours: 30,
            chapter_count: 15,
            domain: '人工智能',
            created_at: '2024-02-05 11:20:00',
            user_id: 'T003'
          }
        ]
      }
      
      this.pagination = {
        page: 1,
        page_size: 12,
        total: this.courses.length,
        total_pages: 1
      }
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