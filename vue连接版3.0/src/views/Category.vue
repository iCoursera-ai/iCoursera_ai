<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <Header />
    
    <!-- 分类筛选导航栏 -->
    <nav class="bg-white py-4 px-6 sticky top-[5rem] z-20 border-b border-gray-200 shadow-sm">
      <div class="max-w-7xl mx-auto">
        <!-- 第一行分类 -->
        <div class="grid grid-cols-7 gap-3">
          <button 
            v-for="category in categories" 
            :key="category.id" 
            :class="[
              'category-tag',
              activeCategory.id === category.id ? 'bg-primary text-white hover:bg-primary' : ''
            ]"
            @click="selectCategory(category)">
            {{ category.name }}
          </button>
        </div>
      </div>
    </nav>

    <main class="flex-1">
      <!-- 主内容区域 -->
      <div class="max-w-7xl mx-auto px-4 py-6">
        <!-- 加载状态 -->
        <div v-if="loading" class="text-center py-16">
          <div class="inline-flex items-center justify-center space-x-2">
            <div class="w-3 h-3 bg-primary rounded-full animate-pulse"></div>
            <div class="w-3 h-3 bg-primary rounded-full animate-pulse" style="animation-delay: 0.2s"></div>
            <div class="w-3 h-3 bg-primary rounded-full animate-pulse" style="animation-delay: 0.4s"></div>
          </div>
          <div class="text-gray-500 text-sm mt-2">正在加载课程...</div>
        </div>
        
        <!-- 内容区域 -->
        <div v-else>
          <!-- 分类标题和筛选 -->
          <div class="mb-8">
            <h1 class="text-2xl font-bold text-dark mb-2">{{ activeCategory.name }} 相关课程</h1>
            <p class="text-gray-600 mb-6">已为您筛选出 {{ totalCount }} 个相关课程</p>
            
            <!-- 排序和筛选选项 -->
            <div class="flex flex-wrap items-center justify-between gap-4 bg-white p-4 rounded-lg shadow-sm">
              <div class="flex items-center space-x-4">
                <button 
                  v-for="sortOption in sortOptions" 
                  :key="sortOption.value"
                  :class="[
                    'px-4 py-2 rounded-md text-sm font-medium transition-colors',
                    sortBy === sortOption.value 
                      ? 'bg-primary text-white' 
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                  @click="changeSort(sortOption.value)">
                  {{ sortOption.label }}
                </button>
              </div>
              
              <div class="flex items-center space-x-4">
                <!-- 难度筛选 -->
                <div class="relative">
                  <button 
                    @click="toggleDifficultyMenu"
                    class="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-200">
                    <span>难度: {{ getDifficultyLabel }}</span>
                    <i class="fa fa-chevron-down text-xs"></i>
                  </button>
                  
                  <!-- 难度下拉菜单 -->
                  <div 
                    v-if="showDifficultyMenu"
                    class="absolute top-full right-0 mt-2 w-40 bg-white rounded-md shadow-lg py-2 z-50 border border-gray-200">
                    <button 
                      v-for="difficulty in difficultyOptions" 
                      :key="difficulty.value"
                      @click="selectDifficulty(difficulty.value)"
                      class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                      {{ difficulty.label }}
                    </button>
                  </div>
                </div>
                
                <!-- 价格筛选 -->
                <div class="relative">
                  <button 
                    @click="togglePriceMenu"
                    class="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-200">
                    <span>价格: {{ getPriceLabel }}</span>
                    <i class="fa fa-chevron-down text-xs"></i>
                  </button>
                  
                  <!-- 价格下拉菜单 -->
                  <div 
                    v-if="showPriceMenu"
                    class="absolute top-full right-0 mt-2 w-32 bg-white rounded-md shadow-lg py-2 z-50 border border-gray-200">
                    <button 
                      v-for="price in priceOptions" 
                      :key="price.value"
                      @click="selectPrice(price.value)"
                      class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                      {{ price.label }}
                    </button>
                  </div>
                </div>
                
                <!-- 重置筛选 -->
                <button 
                  @click="resetFilters"
                  class="px-4 py-2 text-sm font-medium text-gray-600 hover:text-primary transition-colors">
                  重置筛选
                </button>
              </div>
            </div>
          </div>

          <!-- 视频推荐区域 -->
          <div class="mb-8">
            <!-- 视频网格 - 一行5个 -->
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
              <div 
                v-for="course in paginatedCourses" 
                :key="course.id" 
                class="bg-white rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow group video-card"
                @click="goToCourseDetail(course)">
                <!-- 视频封面 - 16:9比例 -->
                <div class="relative" style="aspect-ratio: 16/9;">
                  <img :src="course.image" :alt="course.title" 
                       class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                  <span class="absolute bottom-2 right-2 bg-black/70 text-white text-xs px-1.5 py-0.5 rounded">
                    {{ course.duration }}
                  </span>
                  <!-- 难度标签 -->
                  <div v-if="course.difficultyLabel" class="absolute top-2 left-2">
                    <span :class="[
                      'text-xs px-2 py-0.5 rounded-full text-white',
                      course.difficulty === 'beginner' ? 'bg-green-500' : 
                      course.difficulty === 'intermediate' ? 'bg-yellow-500' : 'bg-red-500'
                    ]">
                      {{ course.difficultyLabel }}
                    </span>
                  </div>
                  <!-- 播放按钮 -->
                  <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/20">
                    <div class="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                      <i class="fa fa-play text-white text-lg"></i>
                    </div>
                  </div>
                </div>
                <!-- 视频信息 -->
                <div class="p-3">
                  <h4 class="text-sm font-medium line-clamp-2 mb-2 group-hover:text-primary transition-colors">{{ course.title }}</h4>
                  <div class="flex items-center justify-between text-xs text-gray-500 mb-1">
                    <div class="flex items-center space-x-3">
                      <span class="flex items-center">
                        <i class="fa fa-user mr-1 text-xs"></i>
                        {{ course.enrolledCountText }}
                      </span>
                      <span class="flex items-center">
                        <i class="fa fa-comment mr-1 text-xs"></i>
                        {{ course.chapter_count || '0' }}章
                      </span>
                    </div>
                    <span>{{ course.timeAgo }}</span>
                  </div>
                  <div class="text-xs text-gray-400 mb-2">{{ course.teacher }}</div>
                  <div class="flex items-center justify-between">
                    <span class="text-xs px-2 py-1 bg-gray-100 rounded">{{ course.category }}</span>
                    <div class="flex items-center">
                      <span v-if="course.rating" class="flex items-center text-yellow-500 text-xs mr-2">
                        <i class="fa fa-star mr-0.5"></i>
                        {{ course.rating }}
                      </span>
                      <span class="text-xs font-medium text-primary" v-if="course.price === 'paid'">付费</span>
                      <span class="text-xs font-medium text-green-600" v-else>免费</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 如果没有课程 -->
            <div v-if="filteredCourses.length === 0 && !loading" class="text-center py-16">
              <div class="flex flex-col items-center justify-center">
                <i class="fa fa-search text-gray-400 text-4xl mb-4"></i>
                <h3 class="text-lg font-medium text-gray-600 mb-2">暂无相关课程</h3>
                <p class="text-gray-500 mb-6">试试其他分类或调整筛选条件</p>
                <button @click="resetFilters" class="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary/90 transition-colors">
                  重置筛选条件
                </button>
              </div>
            </div>
            
            <!-- 分页 -->
            <div v-if="totalPages > 1 && filteredCourses.length > 0" class="flex justify-center items-center gap-2 mt-8">
              <button 
                @click="prevPage" 
                :disabled="currentPage === 1"
                class="w-10 h-10 flex items-center justify-center rounded-md border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                <i class="fa fa-angle-left text-gray-500"></i>
              </button>
              
              <button 
                v-for="page in visiblePages" 
                :key="page"
                @click="goToPage(page)"
                class="w-10 h-10 flex items-center justify-center rounded-md border"
                :class="currentPage === page ? 'bg-primary text-white border-primary' : 'border-gray-200 hover:bg-gray-50'">
                {{ page }}
              </button>
              
              <button 
                @click="nextPage" 
                :disabled="currentPage === totalPages"
                class="w-10 h-10 flex items-center justify-center rounded-md border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                <i class="fa fa-angle-right text-gray-500"></i>
              </button>
              
              <!-- 跳转到指定页 -->
              <div class="ml-4 flex items-center text-sm text-gray-600">
                <span class="mr-2">跳转到</span>
                <input 
                  type="number" 
                  v-model="jumpPage"
                  min="1"
                  :max="totalPages"
                  class="w-16 px-2 py-1 border border-gray-300 rounded text-center focus:outline-none focus:border-primary"
                  @keypress.enter="jumpToPage">
                <span class="ml-2">页</span>
              </div>
            </div>
          </div>
          
          <!-- 热门分类推荐 -->
          <div v-if="!loading && filteredCourses.length > 0" class="mt-12">
            <h2 class="text-xl font-bold text-dark mb-6">其他热门分类</h2>
            <div class="flex flex-wrap gap-3">
              <button 
                v-for="category in relatedCategories" 
                :key="category.id"
                @click="selectCategory(category)"
                class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-primary hover:text-white transition-colors">
                {{ category.name }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { courseService } from '@/service/course.js'

export default {
  name: 'CategoryPage',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      // 当前激活的分类
      activeCategory: { id: 1, name: '编程开发', domain: '编程开发' },
      
      // 分类数据
      categories: [
        { id: 1, name: '编程开发', domain: '编程开发' },
        { id: 2, name: '人工智能', domain: '人工智能' },
        { id: 3, name: '数据科学', domain: '数据科学' },
        { id: 4, name: '商业管理', domain: '商业管理' },
        { id: 5, name: '设计创意', domain: '设计创意' },
        { id: 6, name: '市场营销', domain: '市场营销' },
        { id: 7, name: '语言学习', domain: '语言学习' }
      ],
      
      // 所有课程数据
      allCourses: [],
      
      // API返回的总课程数和分页信息
      paginationInfo: {
        total: 0,
        page: 1,
        page_size: 20,
        total_pages: 0
      },
      
      // 排序选项
      sortOptions: [
        { value: 'hot', label: '按热度' },
        { value: 'new', label: '按时间' },
        { value: 'rating', label: '按评分' }
      ],
      sortBy: 'hot',
      
      // 难度筛选
      difficultyOptions: [
        { value: 'all', label: '全部难度' },
        { value: 'beginner', label: '入门' },
        { value: 'intermediate', label: '中级' },
        { value: 'advanced', label: '高级' }
      ],
      selectedDifficulty: 'all',
      showDifficultyMenu: false,
      
      // 价格筛选
      priceOptions: [
        { value: 'all', label: '全部价格' },
        { value: 'free', label: '免费' },
        { value: 'paid', label: '付费' }
      ],
      selectedPrice: 'all',
      showPriceMenu: false,
      
      // 分页相关
      currentPage: 1,
      jumpPage: 1,
      pageSize: 20,
      
      // 加载状态
      loading: false
    }
  },
  computed: {
    // 过滤后的课程
    filteredCourses() {
      let filtered = [...this.allCourses]
      
      // 按难度筛选
      if (this.selectedDifficulty !== 'all') {
        filtered = filtered.filter(course => 
          course.difficulty === this.selectedDifficulty
        )
      }
      
      // 按价格筛选
      if (this.selectedPrice !== 'all') {
        filtered = filtered.filter(course => 
          course.price === this.selectedPrice
        )
      }
      
      // 前端排序（注意：API已经根据sortBy参数进行了排序，这里主要是处理前端的筛选后排序）
      // 如果需要完全依赖API排序，可以注释掉这段代码
      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'hot':
            return (b.enrolled_count || 0) - (a.enrolled_count || 0)
          case 'new':
            return new Date(b.created_at || b.createdAt) - new Date(a.created_at || a.createdAt)
          case 'rating':
            return (b.rating || 0) - (a.rating || 0)
          default:
            return 0
        }
      })
      
      return filtered
    },
    
    // 分页数据
    paginatedCourses() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredCourses.slice(start, end)
    },
    
    // 总页数
    totalPages() {
      // 优先使用API返回的分页信息
      if (this.paginationInfo.total_pages > 0) {
        return this.paginationInfo.total_pages
      }
      // 如果没有API分页信息，使用本地计算
      return Math.ceil(this.filteredCourses.length / this.pageSize)
    },
    
    // 总课程数
    totalCount() {
      // 优先使用API返回的总数
      if (this.paginationInfo.total > 0) {
        return this.paginationInfo.total
      }
      return this.filteredCourses.length
    },
    
    // 可见的页码
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
    },
    
    // 难度标签显示
    getDifficultyLabel() {
      const option = this.difficultyOptions.find(opt => opt.value === this.selectedDifficulty)
      return option ? option.label : '全部难度'
    },
    
    // 价格标签显示
    getPriceLabel() {
      const option = this.priceOptions.find(opt => opt.value === this.selectedPrice)
      return option ? option.label : '全部价格'
    },
    
    // 相关分类推荐
    relatedCategories() {
      return this.categories
        .filter(cat => cat.id !== this.activeCategory.id)
        .slice(0, 6)
    }
  },
  watch: {
    // 监听路由domain参数变化
    '$route.query.domain': {
      immediate: true,
      handler(newDomain) {
        if (newDomain) {
          this.handleDomainChange(newDomain)
        }
      }
    },
    
    // 监听筛选条件变化，重置分页
    selectedDifficulty() {
      this.resetPagination()
    },
    selectedPrice() {
      this.resetPagination()
    },
    sortBy() {
      // 当排序方式改变时，重新调用API获取排序后的数据
      this.currentPage = 1
      this.jumpPage = 1
      this.loadCourses()
    }
  },
  mounted() {
    // 初始化数据
    this.initData()
  },
  methods: {
    // 初始化数据
    async initData() {
      // 检查是否有domain参数
      if (this.$route.query.domain) {
        this.handleDomainChange(this.$route.query.domain)
      } else {
        // 如果没有参数，使用第一个分类
        this.activeCategory = this.categories[0]
        // 加载课程
        await this.loadCourses()
      }
    },
    
    // 处理domain参数变化
    handleDomainChange(domain) {
      // 查找对应的分类
      const category = this.categories.find(cat => cat.domain === domain)
      
      if (category) {
        this.activeCategory = category
      } else {
        // 如果没有找到，使用第一个分类
        this.activeCategory = this.categories[0]
      }
      
      // 重置分页和筛选
      this.resetPagination()
      this.resetFilters()
      
      // 加载课程
      this.loadCourses()
    },
    
    // 选择分类
    // 在category.vue的selectCategory方法中
    selectCategory(category) {
      this.activeCategory = category
      
      // 方案1：使用简单的push而不是replace
      this.$router.push({
        path: '/category',
        query: { domain: category.domain || category.name }
      }).catch(err => {
        console.log('路由跳转被阻止:', err)
      })
      
      // 或者方案2：直接更新query参数而不改变路由
      // this.$router.push({ query: { domain: category.domain || category.name } })
      
      // 重置分页
      this.resetPagination()
      
      // 重新加载课程
      this.loadCourses()
      
      // 滚动到顶部
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },

    // 加载课程数据
    async loadCourses() {
      this.loading = true
      try {
        const domain = this.$route.query.domain || this.activeCategory.domain || this.activeCategory.name
        
        // 根据排序方式构建API请求参数
        let orderBy = 'enrolled_count'
        if (this.sortBy === 'new') {
          orderBy = 'created_at'
        } else if (this.sortBy === 'rating') {
          orderBy = 'rating'
        }
        
        const response = await courseService.getCoursesByDomain(
          domain, 
          this.currentPage, 
          this.pageSize
        )
        
        if (response.code === 200) {
          // 保存分页信息
          if (response.data.pagination) {
            this.paginationInfo = response.data.pagination
            // 更新当前页数
            this.currentPage = this.paginationInfo.page
            this.jumpPage = this.currentPage
          }
          
          // 转换API数据格式
          this.allCourses = this.transformApiData(response.data.courses || [])
        } else {
          console.error('获取课程失败:', response.msg)
          // 如果API失败，使用模拟数据
          this.useMockData()
        }
      } catch (error) {
        console.error('加载课程数据失败:', error)
        // 如果API失败，使用模拟数据
        this.useMockData()
      } finally {
        this.loading = false
      }
    },
    
    // 转换API数据为前端格式
    transformApiData(courses) {
      return courses.map(course => {
        // 处理难度映射
        let difficulty = 'beginner'
        let difficultyLabel = '入门'
        if (course.difficulty === 1) {
          difficulty = 'beginner'
          difficultyLabel = '入门'
        } else if (course.difficulty === 2) {
          difficulty = 'intermediate'
          difficultyLabel = '中级'
        } else if (course.difficulty >= 3) {
          difficulty = 'advanced'
          difficultyLabel = '高级'
        }
        
        return {
          id: course.course_id,
          title: course.course_name,
          teacher: this.getTeacherName(course),
          enrolledCountText: this.formatEnrolledCount(course.enrolled_count),
          enrolled_count: course.enrolled_count,
          comments: course.chapter_count ? `${course.chapter_count}章` : '0章',
          chapter_count: course.chapter_count,
          duration: `${course.duration_hours || 0}小时`,
          timeAgo: this.formatTimeAgo(course.created_at),
          category: course.domain,
          domain: course.domain,
          difficulty: difficulty,
          difficultyLabel: difficultyLabel,
          price: this.determinePrice(course),
          rating: parseFloat(course.rating) || 0,
          createdAt: course.created_at,
          created_at: course.created_at,
          image: course.thumbnail_url || this.getRandomImage(course.course_id),
          description: course.description
        }
      })
    },
    
    // 使用模拟数据（降级方案）
    useMockData() {
      this.allCourses = this.generateCourses()
      this.paginationInfo = {
        page: this.currentPage,
        page_size: this.pageSize,
        total: this.allCourses.length,
        total_pages: Math.ceil(this.allCourses.length / this.pageSize)
      }
    },
    
    // 获取教师名称
    getTeacherName(course) {
      // 这里可以根据teacher_id调用API获取教师信息
      // 暂时使用默认值
      const teacherNames = ['张老师', '李教授', '王工程师', '刘老师', '陈教授', '赵导师']
      return course.teacher_id ? `教师${course.teacher_id}` : teacherNames[Math.floor(Math.random() * teacherNames.length)]
    },
    
    // 格式化报名人数
    formatEnrolledCount(count) {
      if (!count) return '0 人学习'
      if (count < 10000) return `${count} 人学习`
      if (count < 100000) return `${(count / 10000).toFixed(1)}万 人学习`
      return `${Math.floor(count / 10000)}万+ 人学习`
    },
    
    // 格式化时间
    formatTimeAgo(dateStr) {
      if (!dateStr) return '未知时间'
      
      try {
        const date = new Date(dateStr)
        const now = new Date()
        const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
        
        if (diffDays === 0) return '今天'
        if (diffDays === 1) return '昨天'
        if (diffDays < 7) return `${diffDays}天前`
        if (diffDays < 30) return `${Math.floor(diffDays / 7)}周前`
        if (diffDays < 365) return `${Math.floor(diffDays / 30)}个月前`
        return `${Math.floor(diffDays / 365)}年前`
      } catch (e) {
        return '未知时间'
      }
    },
    
    // 辅助方法：确定价格
    determinePrice(course) {
      // 这里可以根据课程的其他属性判断是否是免费
      // 暂时随机分配
      return Math.random() > 0.5 ? 'free' : 'paid'
    },
    
    // 获取随机图片
    getRandomImage(courseId) {
      const imageUrls = [
        'https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80',
        'https://images.unsplash.com/photo-1555099962-4199c345e5dd?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80',
        'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80',
        'https://images.unsplash.com/photo-1542831371-29b0f74f9713?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80',
        'https://images.unsplash.com/photo-1517697471339-4aa32003c11a?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
      ]
      
      // 确保courseId是字符串
      const idStr = String(courseId || '0')
      return imageUrls[idStr.charCodeAt(0) % imageUrls.length]
    },
    
    // 切换排序
    changeSort(sortType) {
      this.sortBy = sortType
    },
    
    // 切换难度菜单
    toggleDifficultyMenu() {
      this.showDifficultyMenu = !this.showDifficultyMenu
      if (this.showDifficultyMenu) {
        this.showPriceMenu = false
      }
    },
    
    // 选择难度
    selectDifficulty(difficulty) {
      this.selectedDifficulty = difficulty
      this.showDifficultyMenu = false
    },
    
    // 切换价格菜单
    togglePriceMenu() {
      this.showPriceMenu = !this.showPriceMenu
      if (this.showPriceMenu) {
        this.showDifficultyMenu = false
      }
    },
    
    // 选择价格
    selectPrice(price) {
      this.selectedPrice = price
      this.showPriceMenu = false
    },
    
    // 重置筛选
    resetFilters() {
      this.selectedDifficulty = 'all'
      this.selectedPrice = 'all'
      this.sortBy = 'hot'
      this.showDifficultyMenu = false
      this.showPriceMenu = false
      this.resetPagination()
    },
    
    // 重置分页
    resetPagination() {
      this.currentPage = 1
      this.jumpPage = 1
    },
    
    // 分页方法
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
        this.jumpPage = this.currentPage
        this.loadCourses()
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
        this.jumpPage = this.currentPage
        this.loadCourses()
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },
    
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        this.jumpPage = page
        this.loadCourses()
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },
    
    // 跳转到指定页
    jumpToPage() {
      if (this.jumpPage >= 1 && this.jumpPage <= this.totalPages) {
        this.currentPage = parseInt(this.jumpPage)
        this.loadCourses()
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } else {
        // 如果输入超出范围，重置为当前页
        this.jumpPage = this.currentPage
      }
    },
    
    // 跳转到课程详情
    goToCourseDetail(course) {
      this.$router.push({
        name: 'VideoPlayer',
        params: { courseId: course.id }
      })
    },
    
    // 生成模拟课程数据（备选方案）
    generateCourses() {
      const categories = [
        { name: '编程开发', domain: '编程开发' },
        { name: '人工智能', domain: '人工智能' },
        { name: '数据科学', domain: '数据科学' },
        { name: '商业管理', domain: '商业管理' },
        { name: '设计创意', domain: '设计创意' },
        { name: '市场营销', domain: '市场营销' },
        { name: '语言学习', domain: '语言学习' }
      ]
      
      const difficulties = ['beginner', 'intermediate', 'advanced']
      const difficultyLabels = ['入门', '中级', '高级']
      const prices = ['free', 'paid']
      const teachers = ['张老师', '李教授', '王工程师', '刘老师', '陈教授', '赵导师']
      
      const domain = this.$route.query.domain || this.activeCategory.domain || this.activeCategory.name
      
      // 生成与当前domain相关的课程
      return Array.from({ length: 30 }, (_, index) => {
        const difficultyIndex = Math.floor(Math.random() * difficulties.length)
        const difficulty = difficulties[difficultyIndex]
        const difficultyLabel = difficultyLabels[difficultyIndex]
        const price = prices[Math.floor(Math.random() * prices.length)]
        const teacher = teachers[Math.floor(Math.random() * teachers.length)]
        const enrolledCount = Math.floor(Math.random() * 50000) + 1000
        const rating = (Math.random() * 2 + 3).toFixed(1)
        const daysAgo = Math.floor(Math.random() * 365)
        const createdAt = new Date(Date.now() - daysAgo * 24 * 60 * 60 * 1000).toISOString()
        
        return {
          id: `MOCK-${domain.substring(0, 2)}-${index + 1}`,
          title: `${domain}课程 - ${this.getCourseTitle(domain, difficulty)}`,
          teacher: teacher,
          enrolledCountText: this.formatEnrolledCount(enrolledCount),
          enrolled_count: enrolledCount,
          comments: `${Math.floor(Math.random() * 10) + 1}章`,
          chapter_count: Math.floor(Math.random() * 10) + 1,
          duration: `${Math.floor(Math.random() * 50) + 5}小时`,
          timeAgo: this.formatTimeAgo(createdAt),
          category: domain,
          domain: domain,
          difficulty: difficulty,
          difficultyLabel: difficultyLabel,
          price: price,
          rating: parseFloat(rating),
          createdAt: createdAt,
          created_at: createdAt,
          image: this.getRandomImage(index),
          description: `${domain}相关课程描述`
        }
      })
    },
    
    // 根据分类和难度生成课程标题
    getCourseTitle(category, difficulty) {
      const titles = {
        '编程开发': {
          beginner: ['Python入门教程', 'Java基础编程', 'HTML/CSS网页设计'],
          intermediate: ['Spring Boot实战', 'React高级应用', 'Docker容器化'],
          advanced: ['微服务架构设计', '分布式系统原理', '高性能网络编程']
        },
        '人工智能': {
          beginner: ['AI基础入门', '机器学习概览', 'Python数据科学'],
          intermediate: ['深度学习实战', '神经网络原理', 'TensorFlow应用'],
          advanced: ['强化学习进阶', '计算机视觉算法', '自然语言处理']
        },
        '数据科学': {
          beginner: ['数据分析基础', 'Excel数据分析', 'SQL查询入门'],
          intermediate: ['Python数据分析', '数据可视化实战', '统计建模'],
          advanced: ['大数据处理', '机器学习算法', '商业智能分析']
        },
        '商业管理': {
          beginner: ['管理学基础', '市场营销入门', '财务管理基础'],
          intermediate: ['战略管理', '组织行为学', '人力资源管理'],
          advanced: ['企业战略规划', '领导力发展', '商业创新管理']
        },
        '设计创意': {
          beginner: ['PS基础入门', 'UI设计基础', '平面设计原理'],
          intermediate: ['UI动效设计', '插画设计', '品牌视觉设计'],
          advanced: ['产品设计思维', '用户体验设计', '设计系统构建']
        },
        '市场营销': {
          beginner: ['营销基础', '社交媒体营销', '内容营销入门'],
          intermediate: ['数字营销策略', '品牌建设', '电商运营'],
          advanced: ['营销数据分析', '增长黑客', '品牌战略规划']
        },
        '语言学习': {
          beginner: ['英语入门', '日语基础', '商务英语'],
          intermediate: ['英语口语强化', '日语进阶', '商务沟通技巧'],
          advanced: ['高级口译', '专业日语', '跨文化沟通']
        }
      }
      
      const categoryTitles = titles[category] || titles['编程开发']
      const difficultyTitles = categoryTitles[difficulty] || categoryTitles.beginner
      return difficultyTitles[Math.floor(Math.random() * difficultyTitles.length)]
    }
  }
}
</script>

<style scoped>
/* 重置和基础样式 */
* {
  box-sizing: border-box;
}

/* 与Home页面一致的样式 */
.category-tag {
  @apply inline-flex items-center justify-center px-3 py-2 text-sm font-medium text-gray-800 bg-gray-100 rounded-lg hover:bg-gray-200 transition-all duration-300 cursor-pointer text-center;
  min-height: 36px;
  border: 1px solid transparent;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.category-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.category-tag.active {
  background-color: #3b82f6;
  color: white;
  border-color: #3b82f6;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

/* 隐藏滚动条 */
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}

.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* 限制行数 */
.line-clamp-1 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
  line-clamp: 1;
}

.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
}

.line-clamp-3 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  line-clamp: 3;
}

/* 视频卡片统一样式 */
.video-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
}

.video-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent 0%, rgba(0, 0, 0, 0.1) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.video-card:hover::before {
  opacity: 1;
}

/* 卡片图片容器 */
.video-card-image {
  position: relative;
  overflow: hidden;
  aspect-ratio: 16/9;
}

.video-card-image img {
  transition: transform 0.5s ease;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-card:hover .video-card-image img {
  transform: scale(1.05);
}

/* 播放按钮覆盖层 */
.video-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.video-card:hover .video-overlay {
  opacity: 1;
}

.play-button {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
  font-size: 24px;
  transition: all 0.3s ease;
  backdrop-filter: blur(4px);
}

.play-button:hover {
  background: white;
  transform: scale(1.1);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

/* 卡片内容 */
.video-card-content {
  padding: 1rem;
  background: white;
}

.video-title {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
  transition: color 0.2s ease;
}

.video-card:hover .video-title {
  color: #3b82f6;
}

.video-info {
  color: #6b7280;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.video-info span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.video-duration {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-weight: 500;
}

/* 阴影效果 */
.shadow-md {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.shadow-lg {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 
              0 8px 10px -6px rgba(0, 0, 0, 0.1);
}

.shadow-sm {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 
              0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

/* 悬停效果增强 */
.video-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

/* 渐变边框效果 */
.gradient-border {
  position: relative;
  border-radius: 12px;
}

.gradient-border::after {
  content: '';
  position: absolute;
  inset: -1px;
  background: linear-gradient(45deg, #3b82f6, #8b5cf6, #10b981);
  border-radius: 13px;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.gradient-border:hover::after {
  opacity: 1;
}

/* 类别标签容器 */
.category-tags-container {
  display: flex;
  gap: 0.75rem;
  padding: 1rem 0;
  margin-bottom: 1.5rem;
  position: relative;
}

.category-tags-container::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(to right, transparent, #e5e7eb, transparent);
}

/* 加载动画 */
.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 骨架屏动画 */
.skeleton {
  background: linear-gradient(90deg, #f3f4f6 25%, #e5e7eb 50%, #f3f4f6 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 8px;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* 空状态样式 */
.empty-state {
  text-align: center;
  padding: 4rem 1rem;
  color: #6b7280;
}

.empty-state-icon {
  font-size: 3rem;
  color: #d1d5db;
  margin-bottom: 1rem;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.page-button {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: white;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-button:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  transform: translateY(-2px);
}

.page-button.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.page-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* 筛选器样式 */
.filter-container {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 12px;
}

.filter-select {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* 响应式调整 */
@media (max-width: 1024px) {
  .grid-cols-4 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  
  .video-card-content {
    padding: 0.75rem;
  }
}

@media (max-width: 768px) {
  .grid-cols-4 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  
  .category-tags-container {
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }
  
  .filter-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-select {
    width: 100%;
  }
}

@media (max-width: 640px) {
  .grid-cols-4 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
  
  .flex-wrap {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .play-button {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
  
  .video-title {
    font-size: 1rem;
  }
  
  .video-info {
    font-size: 0.75rem;
  }
}

/* 暗色模式支持 */
@media (prefers-color-scheme: dark) {
  .video-card {
    background: #1f2937;
  }
  
  .video-card-content {
    background: #1f2937;
  }
  
  .video-title {
    color: #f9fafb;
  }
  
  .video-info {
    color: #9ca3af;
  }
  
  .category-tag {
    background: #374151;
    color: #e5e7eb;
  }
  
  .category-tag:hover {
    background: #4b5563;
  }
  
  .filter-container {
    background: #374151;
  }
  
  .filter-select {
    background: #4b5563;
    border-color: #6b7280;
    color: #f9fafb;
  }
}

/* 平滑滚动 */
html {
  scroll-behavior: smooth;
}

/* 焦点样式优化 */
*:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
  border-radius: 4px;
}

/* 工具类 */
.text-primary {
  color: #3b82f6;
}

.bg-primary {
  background-color: #3b82f6;
}

.border-primary {
  border-color: #3b82f6;
}

.fill-primary {
  fill: #3b82f6;
}

.stroke-primary {
  stroke: #3b82f6;
}

/* 悬停动画类 */
.hover-lift:hover {
  transform: translateY(-4px);
  transition: transform 0.3s ease;
}

.hover-glow:hover {
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.2);
  transition: box-shadow 0.3s ease;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 网格动画 */
.grid-item {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s ease forwards;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 交错动画延迟 */
.grid-item:nth-child(2) { animation-delay: 0.1s; }
.grid-item:nth-child(3) { animation-delay: 0.2s; }
.grid-item:nth-child(4) { animation-delay: 0.3s; }
.grid-item:nth-child(5) { animation-delay: 0.4s; }
.grid-item:nth-child(6) { animation-delay: 0.5s; }
</style>