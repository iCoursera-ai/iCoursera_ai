<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <Header />
    
    <!-- 搜索页面主内容 -->
    <div class="flex-1">
      <div class="max-w-7xl mx-auto px-4 py-6">
        <!-- 搜索框区域 -->
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
            <h2 class="text-lg font-semibold text-dark">
              搜索结果：<span class="text-primary">{{ searchResults.length }}</span> 个相关课程
            </h2>
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
          
          <!-- 已选筛选标签 -->
          <div v-if="hasActiveFilters" class="flex flex-wrap gap-2 mb-4">
            <span v-if="selectedCategory !== 'all'" class="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
              {{ getCategoryLabel(selectedCategory) }}
              <button @click="selectedCategory = 'all'" class="ml-1.5 hover:text-blue-900">
                <i class="fa fa-times text-xs"></i>
              </button>
            </span>
            
            <span v-for="level in selectedDifficulty" :key="level" class="inline-flex items-center px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
              {{ getDifficultyLabel(level) }}
              <button @click="removeDifficulty(level)" class="ml-1.5 hover:text-green-900">
                <i class="fa fa-times text-xs"></i>
              </button>
            </span>
            
            <span v-for="duration in selectedDuration" :key="duration" class="inline-flex items-center px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
              {{ getDurationLabel(duration) }}
              <button @click="removeDuration(duration)" class="ml-1.5 hover:text-purple-900">
                <i class="fa fa-times text-xs"></i>
              </button>
            </span>
            
            <span v-if="isFree || isPaid" class="inline-flex items-center px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm">
              {{ getPriceLabel() }}
              <button @click="clearPriceFilter" class="ml-1.5 hover:text-orange-900">
                <i class="fa fa-times text-xs"></i>
              </button>
            </span>
            
            <button @click="clearAllFilters" class="text-sm text-gray-500 hover:text-primary">
              清除所有筛选
            </button>
          </div>
        </div>

        <!-- 搜索结果区域 -->
        <div class="flex flex-col lg:flex-row gap-6">
          <!-- 左侧课程列表 -->
          <div class="lg:w-3/4">
            <!-- 没有搜索结果时的提示 -->
            <div v-if="searchResults.length === 0 && searchQuery.trim()" class="text-center py-12">
              <i class="fa fa-search text-gray-300 text-4xl mb-4"></i>
              <h3 class="text-lg font-medium text-gray-700 mb-2">未找到相关课程</h3>
              <p class="text-gray-500">建议您尝试其他关键词或调整筛选条件</p>
            </div>
            
            <!-- 视频网格布局（与主页保持一致） -->
            <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              <div 
                v-for="course in paginatedCourses" 
                :key="course.id"
                class="bg-white rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow group video-card"
                @click="goToCourseDetail(course)"
              >
                <!-- 视频封面 - 16:9比例 -->
                <div class="relative" style="aspect-ratio: 16/9;">
                  <img :src="course.image" :alt="course.title" 
                      class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                  <!-- 课程标签 -->
                  <span v-if="course.badgeText" :class="course.badgeClass">
                    {{ course.badgeText }}
                  </span>
                  <!-- 视频时长 -->
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
                  <h4 class="text-sm font-medium line-clamp-2 mb-2 group-hover:text-primary transition-colors">
                    {{ course.title }}
                  </h4>
                  <div class="flex items-center justify-between text-xs text-gray-500 mb-1">
                    <div class="flex items-center space-x-3">
                      <span class="flex items-center">
                        <i class="fa fa-play mr-1 text-xs"></i>
                        {{ course.views }}
                      </span>
                      <span class="flex items-center">
                        <i class="fa fa-thumbs-up mr-1 text-xs"></i>
                        {{ course.rating }}
                      </span>
                    </div>
                    <span>{{ course.timeAgo || '最近更新' }}</span>
                  </div>
                  <div class="text-xs text-gray-400">{{ course.teacher }}</div>
                </div>
              </div>
            </div>

            <!-- 分页 -->
            <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-8">
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
          <div class="lg:w-1/4 space-y-6">
            <!-- 高级筛选 -->
            <div class="bg-white rounded-lg shadow p-5">
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

            <!-- 相关分类 -->
            <div v-if="relatedCategories.length > 0" class="bg-white rounded-lg shadow p-5">
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
      searchQuery: '',
      hotKeywords: ['Python编程', '人工智能', '机器学习', '数据分析', '金融投资', '医学基础', 'Web开发', '设计思维'],
      allCourses: [
        // 计算机与编程类
        { 
          id: 101, 
          title: '深度学习实战：从零搭建AI模型', 
          description: '本课程将带你从零开始学习深度学习，掌握TensorFlow和PyTorch框架，构建各种AI模型，包括图像识别、自然语言处理等实际应用案例。',
          teacher: '李明教授', 
          views: '25.6万播放', 
          rating: '98%好评',
          category: 'computer',
          duration: '12:54:00',
          timeAgo: '3天前',
          image: 'https://picsum.photos/400/225?random=101',
          badgeClass: 'badge-blue',
          badgeText: '新品',
          difficulty: 'intermediate',
          price: 'free',
          tags: ['人工智能', '深度学习', 'Python']
        },
        { 
          id: 102, 
          title: '机器学习基础：理论与Python实践', 
          description: '系统学习机器学习核心算法，包括线性回归、逻辑回归、决策树、支持向量机等，结合Python代码实践，掌握模型训练与评估方法。',
          teacher: '王静教授', 
          views: '18.3万播放', 
          rating: '96%好评',
          category: 'computer',
          duration: '15:20:00',
          timeAgo: '5天前',
          image: 'https://picsum.photos/400/225?random=102',
          badgeClass: 'badge-green',
          badgeText: '精讲',
          difficulty: 'beginner',
          price: 'free',
          tags: ['机器学习', 'Python', '数据分析']
        },
        { 
          id: 103, 
          title: 'Python数据分析实战：从数据处理到可视化', 
          description: '掌握Pandas、NumPy、Matplotlib等数据分析核心库，学习数据清洗、统计分析、可视化展示等技能，应用于实际业务场景。',
          teacher: '张伟教授', 
          views: '22.4万播放', 
          rating: '97%好评',
          category: 'computer',
          duration: '10:30:00',
          timeAgo: '1天前',
          image: 'https://picsum.photos/400/225?random=103',
          badgeClass: 'badge-blue',
          badgeText: '新品',
          difficulty: 'intermediate',
          price: 'free',
          tags: ['Python', '数据分析', '可视化']
        },
        { 
          id: 104, 
          title: 'Web全栈开发：React + Node.js实战', 
          description: '从零开始学习全栈开发，构建现代化Web应用，掌握前后端分离架构，实现用户认证、数据库操作等核心功能。',
          teacher: '王工程师', 
          views: '30.1万播放', 
          rating: '95%好评',
          category: 'computer',
          duration: '20:10:00',
          timeAgo: '7天前',
          image: 'https://picsum.photos/400/225?random=104',
          badgeClass: 'badge-orange',
          badgeText: '新课',
          difficulty: 'advanced',
          price: 'paid',
          tags: ['Web开发', 'React', 'Node.js']
        },
        
        // 商业管理类
        { 
          id: 201, 
          title: '商业分析实战：数据驱动决策', 
          description: '学习如何利用数据分析做出更好的商业决策，掌握商业智能工具使用，提升企业运营效率。',
          teacher: '李经理', 
          views: '15.6万播放', 
          rating: '94%好评',
          category: 'business',
          duration: '10:30:00',
          timeAgo: '4天前',
          image: 'https://picsum.photos/400/225?random=201',
          badgeClass: 'badge-blue',
          badgeText: '新品',
          difficulty: 'intermediate',
          price: 'paid',
          tags: ['商业分析', '数据驱动', '决策']
        },
        { 
          id: 202, 
          title: '项目管理PMP认证全攻略', 
          description: '全面掌握PMP认证知识体系，学习项目管理五大过程组和十大知识领域，提升项目管理实战能力。',
          teacher: '王总监', 
          views: '12.8万播放', 
          rating: '96%好评',
          category: 'business',
          duration: '18:45:00',
          timeAgo: '6天前',
          image: 'https://picsum.photos/400/225?random=202',
          badgeClass: 'badge-green',
          badgeText: '精讲',
          difficulty: 'advanced',
          price: 'paid',
          tags: ['项目管理', 'PMP认证', '职场提升']
        },
        
        // 设计创意类
        { 
          id: 301, 
          title: 'UI/UX设计从入门到精通', 
          description: '全面学习UI/UX设计理论，掌握用户研究、交互设计、视觉设计等核心技能，提升产品设计能力。',
          teacher: '张设计师', 
          views: '22.4万播放', 
          rating: '98%好评',
          category: 'design',
          duration: '25:30:00',
          timeAgo: '2天前',
          image: 'https://picsum.photos/400/225?random=301',
          badgeClass: 'badge-blue',
          badgeText: '新品',
          difficulty: 'beginner',
          price: 'free',
          tags: ['UI设计', 'UX设计', '产品设计']
        },
        { 
          id: 302, 
          title: '平面设计创意与实战', 
          description: '培养创意思维，学习平面设计原理，掌握Photoshop、Illustrator等工具，完成商业设计项目。',
          teacher: '李创意总监', 
          views: '16.8万播放', 
          rating: '95%好评',
          category: 'design',
          duration: '19:45:00',
          timeAgo: '3天前',
          image: 'https://picsum.photos/400/225?random=302',
          badgeClass: 'badge-green',
          badgeText: '精讲',
          difficulty: 'intermediate',
          price: 'paid',
          tags: ['平面设计', '创意', 'Photoshop']
        },
        
        // 语言学习类
        { 
          id: 401, 
          title: '英语口语速成：从零到流利', 
          description: '通过情景对话、发音训练、实战演练等方式，快速提升英语口语表达能力，克服哑巴英语。',
          teacher: '王老师', 
          views: '28.9万播放', 
          rating: '97%好评',
          category: 'language',
          duration: '16:20:00',
          timeAgo: '1天前',
          image: 'https://picsum.photos/400/225?random=401',
          badgeClass: 'badge-blue',
          badgeText: '新品',
          difficulty: 'beginner',
          price: 'free',
          tags: ['英语', '口语', '语言学习']
        },
        
        // 医学健康类
        { 
          id: 501, 
          title: '人工智能在医疗健康领域的应用', 
          description: '探索人工智能在医学影像分析、疾病诊断、药物研发等医疗健康领域的创新应用，学习相关算法模型和技术实现。',
          teacher: '刘芳教授', 
          views: '14.8万播放', 
          rating: '94%好评',
          category: 'medical',
          duration: '12:20:00',
          timeAgo: '5天前',
          image: 'https://picsum.photos/400/225?random=501',
          badgeClass: 'badge-green',
          badgeText: '精讲',
          difficulty: 'intermediate',
          price: 'paid',
          tags: ['人工智能', '医疗', '健康']
        },
        
        // 金融投资类
        { 
          id: 601, 
          title: '股票投资入门与实战', 
          description: '学习股票基础知识，掌握基本面分析和技术分析方法，建立自己的投资策略，规避投资风险。',
          teacher: '陈分析师', 
          views: '19.3万播放', 
          rating: '93%好评',
          category: 'finance',
          duration: '14:45:00',
          timeAgo: '4天前',
          image: 'https://picsum.photos/400/225?random=601',
          badgeClass: 'badge-orange',
          badgeText: '新课',
          difficulty: 'beginner',
          price: 'free',
          tags: ['股票', '投资', '金融']
        },
        
        // 职业技能类
        { 
          id: 701, 
          title: '高效办公：Excel高级技巧', 
          description: '掌握Excel高级函数、数据透视表、图表制作等技能，提升工作效率，实现数据自动化处理。',
          teacher: '赵老师', 
          views: '32.5万播放', 
          rating: '99%好评',
          category: 'skill',
          duration: '8:30:00',
          timeAgo: '2天前',
          image: 'https://picsum.photos/400/225?random=701',
          badgeClass: 'badge-green',
          badgeText: '精讲',
          difficulty: 'intermediate',
          price: 'free',
          tags: ['Excel', '办公技能', '效率提升']
        },
        
        // 考研考证类
        { 
          id: 801, 
          title: '考研数学高分攻略', 
          description: '系统梳理考研数学知识体系，掌握解题技巧，通过真题演练提升应试能力，助力考研成功。',
          teacher: '李教授', 
          views: '21.7万播放', 
          rating: '96%好评',
          category: 'exam',
          duration: '35:20:00',
          timeAgo: '8天前',
          image: 'https://picsum.photos/400/225?random=801',
          badgeClass: 'badge-blue',
          badgeText: '新品',
          difficulty: 'advanced',
          price: 'paid',
          tags: ['考研', '数学', '学习技巧']
        }
      ],
      categories: [
        { value: 'all', label: '全部分类' },
        { value: 'computer', label: '计算机与编程' },
        { value: 'business', label: '商业管理' },
        { value: 'design', label: '设计创意' },
        { value: 'language', label: '语言学习' },
        { value: 'medical', label: '医学健康' },
        { value: 'finance', label: '金融投资' },
        { value: 'skill', label: '职业技能' },
        { value: 'exam', label: '考研考证' }
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
      isFree: false,
      isPaid: false,
      relatedCategories: ['人工智能', '机器学习', '深度学习', 'Python编程', '数据分析', 'Web开发'],
      currentPage: 1,
      pageSize: 12
    }
  },
  computed: {
    searchResults() {
      let results = [...this.allCourses]
      
      // 搜索关键词过滤
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase().trim()
        results = results.filter(course => {
          // 搜索标题、描述、教师、标签
          return course.title.toLowerCase().includes(query) ||
                 course.description.toLowerCase().includes(query) ||
                 course.teacher.toLowerCase().includes(query) ||
                 (course.tags && course.tags.some(tag => tag.toLowerCase().includes(query)))
        })
      }
      
      // 分类过滤
      if (this.selectedCategory !== 'all') {
        results = results.filter(course => course.category === this.selectedCategory)
      }
      
      // 难度过滤
      if (this.selectedDifficulty.length > 0) {
        results = results.filter(course => this.selectedDifficulty.includes(course.difficulty))
      }
      
      // 时长过滤
      if (this.selectedDuration.length > 0) {
        results = results.filter(course => {
          const durationStr = course.duration
          const hoursMatch = durationStr.match(/(\d+):/)
          if (!hoursMatch) return false
          
          const hours = parseInt(hoursMatch[1])
          return this.selectedDuration.some(duration => {
            if (duration === 'short') return hours <= 5
            if (duration === 'medium') return hours > 5 && hours <= 15
            if (duration === 'long') return hours > 15
            return true
          })
        })
      }
      
      // 价格过滤
      const priceFilters = []
      if (this.isFree) priceFilters.push('free')
      if (this.isPaid) priceFilters.push('paid')
      if (priceFilters.length > 0) {
        results = results.filter(course => priceFilters.includes(course.price))
      }
      
      // 排序
      results.sort((a, b) => {
        switch (this.sortBy) {
          case 'hot':
            return parseFloat(b.views) - parseFloat(a.views)
          case 'time':
            // 根据timeAgo排序，越新的越靠前
            return this.getTimeValue(b.timeAgo) - this.getTimeValue(a.timeAgo)
          case 'rating':
            return parseFloat(b.rating) - parseFloat(a.rating)
          default:
            // 默认按相关度排序（如果有搜索词）
            if (this.searchQuery.trim()) {
              // 标题完全匹配的优先级最高
              const query = this.searchQuery.toLowerCase()
              const aTitleMatch = a.title.toLowerCase().includes(query)
              const bTitleMatch = b.title.toLowerCase().includes(query)
              
              if (aTitleMatch && !bTitleMatch) return -1
              if (!aTitleMatch && bTitleMatch) return 1
              
              // 标题匹配程度
              const aTitleIndex = a.title.toLowerCase().indexOf(query)
              const bTitleIndex = b.title.toLowerCase().indexOf(query)
              if (aTitleIndex !== bTitleIndex) return aTitleIndex - bTitleIndex
              
              // 按热度降序
              return parseFloat(b.views) - parseFloat(a.views)
            }
            return 0
        }
      })
      
      return results
    },
    
    paginatedCourses() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.searchResults.slice(start, end)
    },
    
    totalPages() {
      return Math.ceil(this.searchResults.length / this.pageSize)
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
    },
    
    hasActiveFilters() {
      return this.selectedCategory !== 'all' || 
             this.selectedDifficulty.length > 0 || 
             this.selectedDuration.length > 0 || 
             this.isFree || this.isPaid
    }
  },
  mounted() {
    // 页面加载时聚焦到搜索框
    const searchInput = document.getElementById('mainSearchInput')
    if (searchInput) {
      searchInput.focus()
    }
    
    // 检查URL中是否有搜索参数
    const queryParam = this.$route.query.q
    if (queryParam) {
      this.searchQuery = queryParam
      this.performSearch()
    }
  },
  methods: {
    setSearchQuery(query) {
      this.searchQuery = query
      this.performSearch()
    },
    
    performSearch() {
      if (this.searchQuery.trim()) {
        console.log(`正在搜索: ${this.searchQuery}`)
        this.currentPage = 1 // 重置到第一页
        this.updateRelatedContent()
        
        // 更新URL中的搜索参数
        this.$router.replace({
          query: { ...this.$route.query, q: this.searchQuery }
        })
      }
    },
    
    updateRelatedContent() {
      if (!this.searchQuery.trim()) {
        this.relatedCategories = ['人工智能', '机器学习', '深度学习', 'Python编程', '数据分析', 'Web开发']
        return
      }
      
      // 根据搜索词更新相关分类
      const query = this.searchQuery.toLowerCase()
      
      // 更新相关分类
      const matchedCategories = new Set()
      this.allCourses.forEach(course => {
        if (course.title.toLowerCase().includes(query) || 
            course.description.toLowerCase().includes(query) ||
            course.tags?.some(tag => tag.toLowerCase().includes(query))) {
          // 将课程分类转换为中文标签
          const categoryLabel = this.getCategoryLabel(course.category)
          if (categoryLabel) {
            matchedCategories.add(categoryLabel)
          }
        }
      })
      
      this.relatedCategories = Array.from(matchedCategories).slice(0, 6)
    },
    
    applyFilters() {
      this.currentPage = 1
      this.updateRelatedContent()
    },
    
    clearAllFilters() {
      this.selectedCategory = 'all'
      this.selectedDifficulty = []
      this.selectedDuration = []
      this.isFree = false
      this.isPaid = false
      this.currentPage = 1
    },
    
    removeDifficulty(level) {
      const index = this.selectedDifficulty.indexOf(level)
      if (index > -1) {
        this.selectedDifficulty.splice(index, 1)
      }
    },
    
    removeDuration(duration) {
      const index = this.selectedDuration.indexOf(duration)
      if (index > -1) {
        this.selectedDuration.splice(index, 1)
      }
    },
    
    clearPriceFilter() {
      this.isFree = false
      this.isPaid = false
    },
    
    getCategoryLabel(value) {
      const category = this.categories.find(c => c.value === value)
      return category ? category.label : value
    },
    
    getDifficultyLabel(value) {
      const level = this.difficultyLevels.find(l => l.value === value)
      return level ? level.label : value
    },
    
    getDurationLabel(value) {
      const duration = this.durationFilters.find(d => d.value === value)
      return duration ? duration.label : value
    },
    
    getPriceLabel() {
      if (this.isFree && this.isPaid) return '全部价格'
      if (this.isFree) return '免费'
      if (this.isPaid) return '付费'
      return ''
    },
    
    getTimeValue(timeAgo) {
      if (!timeAgo) return 0
      
      const match = timeAgo.match(/(\d+)/)
      if (!match) return 0
      
      const num = parseInt(match[1])
      if (timeAgo.includes('天')) {
        return num
      }
      return 999 // 如果包含其他单位，给个较大的值
    },
    
    // 跳转到课程详情页（使用与主页相同的逻辑）
    goToCourseDetail(course) {
      if (!course || !course.id) {
        console.warn('课程信息不完整')
        return
      }

      // 保存课程信息
      const courseData = {
        id: course.id,
        title: course.title,
        teacher: course.teacher,
        views: course.views,
        rating: course.rating,
        duration: course.duration,
        timeAgo: course.timeAgo || '最近更新',
        image: course.image,
        category: course.category || 'computer',
        description: course.description || `${course.title} - 精品课程，由${course.teacher}主讲`
      }

      console.log('保存课程数据:', courseData)
      localStorage.setItem('selectedCourse', JSON.stringify(courseData))

      // 保存浏览历史
      const currentUser = JSON.parse(localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser') || '{}')
      const userId = currentUser.userId || 'default'
      const history = JSON.parse(localStorage.getItem(`user_${userId}_history`) || '[]')
      
      const initialHistory = {
        id: `history_${course.id}_${Date.now()}`,
        courseId: course.id,
        courseName: course.title,
        teacher: course.teacher,
        watchedAt: new Date().toISOString().split('T')[0] + ' ' + 
                   new Date().toTimeString().split(' ')[0].substring(0, 5),
        progress: 0,
        courseData: courseData
      }
      
      // 去重
      const existingIndex = history.findIndex(h => h.courseId === course.id)
      if (existingIndex !== -1) {
        history[existingIndex] = initialHistory
      } else {
        history.unshift(initialHistory)
        if (history.length > 20) {
          history.pop()
        }
      }
      
      localStorage.setItem(`user_${userId}_history`, JSON.stringify(history))
      
      // 跳转到视频播放页
      this.$router.push({
        name: 'VideoPlayer',
        params: { 
          courseId: course.id,
          category: course.category || 'computer'
        }
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
/* 与主页相同的样式 */
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.card {
  transition: all 0.3s ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
}

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

/* 视频卡片样式（与主页一致） */
.video-card {
  transition: all 0.3s ease;
}

.video-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px -6px rgba(0, 0, 0, 0.15);
}

.group:hover .group-hover\:scale-105 {
  transform: scale(1.05);
}

.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}

.group:hover .group-hover\:text-primary {
  color: var(--primary-color, #3b82f6);
}

/* 课程标签 */
.badge-blue {
  @apply absolute top-2 left-2 bg-primary text-white text-xs px-2 py-0.5 rounded z-10;
}
.badge-green {
  @apply absolute top-2 left-2 bg-green-500 text-white text-xs px-2 py-0.5 rounded z-10;
}
.badge-orange {
  @apply absolute top-2 left-2 bg-orange-500 text-white text-xs px-2 py-0.5 rounded z-10;
}

/* 分页样式 */
button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

/* 筛选标签样式 */
.filter-tag {
  @apply inline-flex items-center px-3 py-1 rounded-full text-sm font-medium transition-colors;
}

.filter-tag:hover {
  @apply opacity-90;
}
</style>