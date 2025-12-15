<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <Header />
    
    <!-- 分类筛选导航栏 -->
    <nav class="bg-white py-4 px-6 sticky top-[5rem] z-20 border-b border-gray-200 shadow-sm">
      <div class="max-w-7xl mx-auto">
        <!-- 第一行分类 -->
        <div class="grid grid-cols-8 gap-3 mb-3">
          <button 
            v-for="category in firstRowCategories" 
            :key="category.id" 
            :class="[
              'category-tag',
              activeCategory.id === category.id ? 'bg-primary text-white hover:bg-primary' : ''
            ]"
            @click="selectCategory(category)">
            {{ category.name }}
          </button>
        </div>
        <!-- 第二行分类 -->
        <div class="grid grid-cols-8 gap-3">
          <button 
            v-for="category in secondRowCategories" 
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
        <!-- 分类标题和筛选 -->
        <div class="mb-8">
          <h1 class="text-2xl font-bold text-dark mb-2">{{ activeCategory.name }} 相关课程</h1>
          <p class="text-gray-600 mb-6">已为您筛选出 {{ filteredCourses.length }} 个相关课程</p>
          
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
                      <i class="fa fa-play mr-1 text-xs"></i>
                      {{ course.views }}
                    </span>
                    <span class="flex items-center">
                      <i class="fa fa-comment mr-1 text-xs"></i>
                      {{ course.comments }}
                    </span>
                  </div>
                  <span>{{ course.timeAgo }}</span>
                </div>
                <div class="text-xs text-gray-400">{{ course.teacher }}</div>
                <div class="mt-2 flex items-center justify-between">
                  <span class="text-xs px-2 py-1 bg-gray-100 rounded">{{ course.category }}</span>
                  <span class="text-xs font-medium text-primary" v-if="course.price === 'paid'">付费</span>
                  <span class="text-xs font-medium text-green-600" v-else>免费</span>
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
          <div v-if="filteredCourses.length > pageSize" class="flex justify-center items-center gap-2 mt-8">
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
    </main>

    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'CategoryPage',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      // 当前激活的分类
      activeCategory: { id: 1, name: '推荐' },
      
      // 分类数据（与Home页面一致）
      firstRowCategories: [
        { id: 1, name: '推荐' },
        { id: 2, name: '编程开发' },
        { id: 3, name: '人工智能' },
        { id: 4, name: '数据科学' },
        { id: 5, name: '商业管理' },
        { id: 6, name: '设计创意' },
        { id: 7, name: '市场营销' },
        { id: 8, name: '语言学习' }
      ],
      secondRowCategories: [
        { id: 9, name: '职业技能' },
        { id: 10, name: '考研考证' },
        { id: 11, name: '生活兴趣' },
        { id: 12, name: '职场提升' },
        { id: 13, name: '创业指导' },
        { id: 14, name: '教师成长' },
        { id: 15, name: '学生专区' },
        { id: 16, name: '更多分类' }
      ],
      
      // 所有课程数据
      allCourses: [],
      
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
      loading: false
    }
  },
  computed: {
    // 过滤后的课程
    filteredCourses() {
      let filtered = [...this.allCourses]
      
      // 按分类筛选
      if (this.activeCategory.id !== 1) { // 如果不是"推荐"分类
        filtered = filtered.filter(course => 
          course.category === this.activeCategory.name
        )
      }
      
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
      
      // 排序
      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'hot':
            return parseFloat(b.hotScore) - parseFloat(a.hotScore)
          case 'new':
            return new Date(b.createdAt) - new Date(a.createdAt)
          case 'rating':
            return parseFloat(b.rating) - parseFloat(a.rating)
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
      return Math.ceil(this.filteredCourses.length / this.pageSize)
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
      // 返回除当前分类外的其他热门分类
      return this.firstRowCategories
        .filter(cat => cat.id !== this.activeCategory.id)
        .slice(0, 6)
    }
  },
  watch: {
    // 监听路由参数变化
    '$route.params.categoryId': {
      immediate: true,
      handler(newCategoryId) {
        this.handleRouteChange(newCategoryId)
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
      this.resetPagination()
    }
  },
  mounted() {
    // 初始化数据
    this.generateCourses()
    this.handleRouteChange(this.$route.params.categoryId)
  },
  methods: {
    // 处理路由变化
    handleRouteChange(categoryId) {
      if (categoryId) {
        const categoryIdNum = parseInt(categoryId)
        // 从所有分类中查找对应的分类
        const allCategories = [...this.firstRowCategories, ...this.secondRowCategories]
        const category = allCategories.find(cat => cat.id === categoryIdNum)
        
        if (category) {
          this.activeCategory = category
        }
      }
      
      // 重置分页和筛选
      this.resetPagination()
      this.resetFilters()
    },
    
    // 选择分类
    selectCategory(category) {
      this.activeCategory = category
      
      // 更新URL但不刷新页面
      this.$router.replace({
        name: 'Category',
        params: { categoryId: category.id }
      }).catch(() => {})
      
      // 重置分页
      this.resetPagination()
      
      // 滚动到顶部
      window.scrollTo({ top: 0, behavior: 'smooth' })
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
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
        this.jumpPage = this.currentPage
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },
    
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        this.jumpPage = page
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },
    
    // 跳转到指定页
    jumpToPage() {
      if (this.jumpPage >= 1 && this.jumpPage <= this.totalPages) {
        this.currentPage = parseInt(this.jumpPage)
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
    
    // 生成模拟课程数据
    generateCourses() {
      const categories = [
        '编程开发', '人工智能', '数据科学', '商业管理', '设计创意',
        '市场营销', '语言学习', '职业技能', '考研考证', '生活兴趣',
        '职场提升', '创业指导', '教师成长', '学生专区'
      ]
      
      const difficulties = ['beginner', 'intermediate', 'advanced']
      const prices = ['free', 'paid']
      const teachers = ['张老师', '李教授', '王工程师', '刘老师', '陈教授', '赵导师']
      
      // 生成200个课程
      this.allCourses = Array.from({ length: 200 }, (_, index) => {
        const category = categories[Math.floor(Math.random() * categories.length)]
        const difficulty = difficulties[Math.floor(Math.random() * difficulties.length)]
        const price = prices[Math.floor(Math.random() * prices.length)]
        const teacher = teachers[Math.floor(Math.random() * teachers.length)]
        
        return {
          id: index + 1,
          title: this.getCourseTitle(category, difficulty),
          teacher: teacher,
          views: `${(Math.random() * 100 + 5).toFixed(1)}万播放`,
          comments: `${Math.floor(Math.random() * 10000 + 1000)}`,
          duration: `${Math.floor(Math.random() * 60 + 10)}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`,
          timeAgo: `${Math.floor(Math.random() * 30 + 1)}天前`,
          category: category,
          difficulty: difficulty,
          price: price,
          rating: (Math.random() * 2 + 3).toFixed(1), // 3.0-5.0
          hotScore: Math.random() * 100, // 热度分数
          createdAt: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString(), // 30天内
          image: `https://picsum.photos/400/225?random=${index + 1000}`
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
/* 与Home页面一致的样式 */
.category-tag {
  @apply inline-flex items-center justify-center px-3 py-2 text-sm font-medium text-gray-800 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer text-center;
  min-height: 36px;
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
}
.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

/* 视频卡片统一样式 */
.video-card {
  transition: all 0.3s ease;
}

/* 阴影效果 */
.shadow-md {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.shadow-sm {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

/* 视频卡片hover效果 */
.group:hover .group-hover\:scale-105 {
  transform: scale(1.05);
}

/* 播放按钮动画 */
.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}

/* 文字颜色过渡 */
.group:hover .group-hover\:text-primary {
  color: var(--primary-color, #3b82f6);
}

/* 响应式调整 */
@media (max-width: 1024px) {
  .grid-cols-8 {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .grid-cols-8 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  
  .flex-wrap {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>