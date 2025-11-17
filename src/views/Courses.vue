<template>
  <section class="courses-page">
    <div class="container">
      <!-- 页面标题和搜索 -->
      <div class="page-header">
        <div class="breadcrumb">
          <router-link to="/">首页</router-link> > 
          <span>所有课程</span>
        </div>
        <h1>探索所有课程</h1>
        <p>从数千门课程中选择，开启您的学习之旅</p>
      </div>

      <!-- 筛选器 -->
      <div class="courses-filters">
        <div class="filter-section">
          <div class="filter-group">
            <label>分类</label>
            <div class="filter-options">
              <button 
                class="filter-btn" 
                :class="{ active: selectedCategory === 'all' }"
                @click="selectCategory('all')"
              >
                全部
              </button>
              <button 
                v-for="category in categories" 
                :key="category.value"
                class="filter-btn" 
                :class="{ active: selectedCategory === category.value }"
                @click="selectCategory(category.value)"
              >
                {{ category.label }}
              </button>
            </div>
          </div>

          <div class="filter-group">
            <label>难度</label>
            <div class="filter-options">
              <button 
                class="filter-btn" 
                :class="{ active: selectedLevel === 'all' }"
                @click="selectLevel('all')"
              >
                全部
              </button>
              <button 
                v-for="level in levels" 
                :key="level.value"
                class="filter-btn" 
                :class="{ active: selectedLevel === level.value }"
                @click="selectLevel(level.value)"
              >
                {{ level.label }}
              </button>
            </div>
          </div>

          <div class="filter-group">
            <label>排序</label>
            <select class="sort-select" v-model="sortBy">
              <option value="popular">最受欢迎</option>
              <option value="newest">最新发布</option>
              <option value="rating">最高评分</option>
              <option value="duration">课程时长</option>
            </select>
          </div>
        </div>

        <div class="search-box">
          <input 
            type="text" 
            v-model="searchQuery"
            @input="handleSearch"
            placeholder="搜索课程..." 
            class="form-control"
          >
          <i class="fas fa-search"></i>
        </div>
      </div>

      <!-- 课程统计 -->
      <div class="courses-stats">
        <div class="stat">
          <strong>{{ filteredCourses.length }}</strong>
          <span>门课程</span>
        </div>
        <div class="stat">
          <strong>{{ uniqueInstructors }}</strong>
          <span>位讲师</span>
        </div>
        <div class="stat">
          <strong>{{ totalStudents }}</strong>
          <span>名学员</span>
        </div>
      </div>

      <!-- 课程网格 -->
      <div class="courses-grid">
        <CourseCard 
          v-for="course in paginatedCourses" 
          :key="course.id"
          :course="course"
          @click="navigateToCourse(course.id)"
        />
        
        <div v-if="filteredCourses.length === 0" class="empty-courses">
          <i class="fas fa-search"></i>
          <h3>未找到相关课程</h3>
          <p>请尝试调整搜索条件或筛选条件</p>
          <button class="btn btn-primary" @click="resetFilters">重置筛选</button>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination" v-if="totalPages > 1">
        <button 
          class="page-btn" 
          :class="{ disabled: currentPage === 1 }"
          @click="changePage(currentPage - 1)"
        >
          <i class="fas fa-chevron-left"></i>
        </button>
        
        <button 
          v-for="page in visiblePages" 
          :key="page"
          class="page-btn" 
          :class="{ active: page === currentPage }"
          @click="changePage(page)"
        >
          {{ page }}
        </button>
        
        <button 
          class="page-btn" 
          :class="{ disabled: currentPage === totalPages }"
          @click="changePage(currentPage + 1)"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>
  </section>
</template>

<script>
import CourseCard from '../components/CourseCard.vue'

export default {
  name: 'Courses',
  components: {
    CourseCard
  },
  data() {
    return {
      searchQuery: '',
      selectedCategory: 'all',
      selectedLevel: 'all',
      sortBy: 'popular',
      currentPage: 1,
      pageSize: 12,
      courses: [],
      categories: [
        { value: 'technology', label: '技术' },
        { value: 'data-science', label: '数据科学' },
        { value: 'business', label: '商业' },
        { value: 'design', label: '设计' },
        { value: 'marketing', label: '市场营销' }
      ],
      levels: [
        { value: 'beginner', label: '初级' },
        { value: 'intermediate', label: '中级' },
        { value: 'advanced', label: '高级' }
      ]
    }
  },
  computed: {
    filteredCourses() {
      let filtered = this.courses

      // 搜索过滤
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(course => 
          course.title.toLowerCase().includes(query) ||
          course.instructor.toLowerCase().includes(query) ||
          course.description.toLowerCase().includes(query)
        )
      }

      // 分类过滤
      if (this.selectedCategory !== 'all') {
        filtered = filtered.filter(course => course.category === this.selectedCategory)
      }

      // 难度过滤
      if (this.selectedLevel !== 'all') {
        filtered = filtered.filter(course => course.level === this.selectedLevel)
      }

      // 排序
      switch (this.sortBy) {
        case 'newest':
          filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
          break
        case 'rating':
          filtered.sort((a, b) => b.rating - a.rating)
          break
        case 'duration':
          filtered.sort((a, b) => this.parseDuration(b.duration) - this.parseDuration(a.duration))
          break
        case 'popular':
        default:
          filtered.sort((a, b) => b.ratingCount - a.ratingCount)
      }

      return filtered
    },
    paginatedCourses() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredCourses.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.filteredCourses.length / this.pageSize)
    },
    visiblePages() {
      const pages = []
      const start = Math.max(1, this.currentPage - 2)
      const end = Math.min(this.totalPages, start + 4)
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    },
    uniqueInstructors() {
      const instructors = new Set(this.filteredCourses.map(course => course.instructor))
      return instructors.size
    },
    totalStudents() {
      return this.filteredCourses.reduce((total, course) => total + course.studentCount, 0)
    }
  },
  created() {
    this.loadCourses()
    this.initializeFromQuery()
  },
  watch: {
    '$route.query': {
      handler(query) {
        this.initializeFromQuery()
      },
      deep: true
    },
    currentPage() {
      this.scrollToTop()
    }
  },
  methods: {
    loadCourses() {
      // 模拟课程数据
      this.courses = [
        {
          id: 1,
          title: '机器学习入门',
          instructor: '斯坦福大学 · Andrew Ng',
          rating: 4.8,
          ratingCount: 12345,
          studentCount: 256789,
          price: 0,
          originalPrice: 399,
          level: 'beginner',
          duration: '15小时',
          category: 'technology',
          description: '从零开始学习机器学习基础概念和算法',
          image: 'https://via.placeholder.com/300x160/0056d2/ffffff?text=Machine+Learning',
          featured: true,
          isNew: false,
          tags: ['Python', 'AI', '数据科学'],
          createdAt: '2023-01-15'
        },
        {
          id: 2,
          title: 'Python 编程',
          instructor: '密歇根大学 · Charles Severance',
          rating: 4.9,
          ratingCount: 8765,
          studentCount: 189234,
          price: 0,
          level: 'beginner',
          duration: '20小时',
          category: 'technology',
          description: '学习Python编程基础，掌握数据处理和自动化',
          image: 'https://via.placeholder.com/300x160/28a745/ffffff?text=Python',
          featured: false,
          isNew: true,
          tags: ['编程', '基础'],
          createdAt: '2023-09-01'
        },
        {
          id: 3,
          title: 'Web 开发全栈',
          instructor: '香港大学 · John Doe',
          rating: 4.7,
          ratingCount: 5432,
          studentCount: 98765,
          price: 399,
          level: 'intermediate',
          duration: '35小时',
          category: 'technology',
          description: '学习现代Web开发技术，包括前端和后端',
          image: 'https://via.placeholder.com/300x160/dc3545/ffffff?text=Web+Dev',
          featured: true,
          isNew: false,
          tags: ['JavaScript', 'React', 'Node.js'],
          createdAt: '2023-06-20'
        },
        {
          id: 4,
          title: '数据科学基础',
          instructor: '清华大学 · 李明',
          rating: 4.6,
          ratingCount: 4321,
          studentCount: 76543,
          price: 299,
          level: 'intermediate',
          duration: '25小时',
          category: 'data-science',
          description: '掌握数据分析和可视化的核心技术',
          image: 'https://via.placeholder.com/300x160/ffc107/333333?text=Data+Science',
          featured: false,
          isNew: false,
          tags: ['数据分析', '可视化'],
          createdAt: '2023-03-10'
        },
        {
          id: 5,
          title: '数字营销策略',
          instructor: '伊利诺伊大学 · Aric Rindfleisch',
          rating: 4.6,
          ratingCount: 5432,
          studentCount: 87654,
          price: 399,
          level: 'intermediate',
          duration: '18小时',
          category: 'marketing',
          description: '学习现代数字营销策略和工具',
          image: 'https://via.placeholder.com/300x160/17a2b8/ffffff?text=Marketing',
          featured: false,
          isNew: true,
          tags: ['营销', '策略'],
          createdAt: '2023-10-01'
        }
      ]
    },
    initializeFromQuery() {
      const query = this.$route.query
      this.searchQuery = query.search || ''
      this.selectedCategory = query.category || 'all'
      this.selectedLevel = query.level || 'all'
      this.sortBy = query.sort || 'popular'
      this.currentPage = parseInt(query.page) || 1
    },
    selectCategory(category) {
      this.selectedCategory = category
      this.currentPage = 1
      this.updateRoute()
    },
    selectLevel(level) {
      this.selectedLevel = level
      this.currentPage = 1
      this.updateRoute()
    },
    handleSearch() {
      this.currentPage = 1
      this.updateRoute()
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        this.updateRoute()
      }
    },
    updateRoute() {
      const query = {
        search: this.searchQuery || undefined,
        category: this.selectedCategory !== 'all' ? this.selectedCategory : undefined,
        level: this.selectedLevel !== 'all' ? this.selectedLevel : undefined,
        sort: this.sortBy !== 'popular' ? this.sortBy : undefined,
        page: this.currentPage !== 1 ? this.currentPage : undefined
      }
      
      this.$router.push({ 
        query: Object.fromEntries(
          Object.entries(query).filter(([_, value]) => value !== undefined)
        )
      })
    },
    navigateToCourse(courseId) {
      this.$router.push(`/course/${courseId}`)
    },
    resetFilters() {
      this.searchQuery = ''
      this.selectedCategory = 'all'
      this.selectedLevel = 'all'
      this.sortBy = 'popular'
      this.currentPage = 1
      this.updateRoute()
    },
    parseDuration(duration) {
      const match = duration.match(/(\d+)\s*小时/)
      return match ? parseInt(match[1]) : 0
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }
}
</script>