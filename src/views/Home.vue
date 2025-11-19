<template>
  <section class="page active">
    <div class="hero">
      <div class="container">
        <h1>开启您的学习之旅</h1>
        <p>从世界顶尖大学和公司学习课程，获得可共享的证书，提升您的职业生涯。</p>
        <div class="search-bar">
          <input 
            type="text" 
            v-model="searchTerm"
            @keypress.enter="performSearch"
            placeholder="搜索您感兴趣的课程..."
          >
          <button @click="performSearch"><i class="fas fa-search"></i></button>
        </div>
      </div>
    </div>

    <div class="recommended-courses">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">推荐课程</h2>
          <p class="section-subtitle">根据您的兴趣精心挑选</p>
          <router-link to="/courses" class="view-all">
            查看全部 <i class="fas fa-chevron-right"></i>
          </router-link>
        </div>
        <div class="courses-carousel">
          <CourseCard 
            v-for="course in featuredCourses" 
            :key="course.id"
            :course="course"
            @click="navigateToCourse(course.id)"
          />
        </div>
      </div>
    </div>

    <div class="categories">
      <div class="container">
        <h2 class="section-title">探索热门类别</h2>
        <div class="category-list">
          <div class="category-card" @click="navigateToCategory('technology')">
            <div class="category-icon">
              <i class="fas fa-laptop-code"></i>
            </div>
            <h3>计算机科学</h3>
            <p>编程、算法、人工智能等</p>
          </div>
          <div class="category-card" @click="navigateToCategory('data-science')">
            <div class="category-icon">
              <i class="fas fa-chart-line"></i>
            </div>
            <h3>数据科学</h3>
            <p>数据分析、机器学习、可视化</p>
          </div>
          <div class="category-card" @click="navigateToCategory('business')">
            <div class="category-icon">
              <i class="fas fa-briefcase"></i>
            </div>
            <h3>商业</h3>
            <p>管理、金融、市场营销</p>
          </div>
          <div class="category-card" @click="navigateToCategory('health')">
            <div class="category-icon">
              <i class="fas fa-heartbeat"></i>
            </div>
            <h3>健康</h3>
            <p>医学、营养学、公共卫生</p>
          </div>
        </div>
      </div>
    </div>

    <div class="featured-courses">
      <div class="container">
        <h2 class="section-title">精选课程</h2>
        <div class="course-list">
          <CourseCard 
            v-for="course in popularCourses" 
            :key="course.id"
            :course="course"
            @click="navigateToCourse(course.id)"
          />
        </div>
      </div>
    </div>

    <div class="platform-features">
      <div class="container">
        <h2 class="section-title">为什么选择 BGarea</h2>
        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">
              <i class="fas fa-graduation-cap"></i>
            </div>
            <h3>世界级课程</h3>
            <p>来自顶尖大学和公司的专业课程</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <i class="fas fa-certificate"></i>
            </div>
            <h3>可共享证书</h3>
            <p>完成课程获得专业证书，提升简历</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <i class="fas fa-user-tie"></i>
            </div>
            <h3>专家讲师</h3>
            <p>向行业专家和知名教授学习</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <i class="fas fa-laptop"></i>
            </div>
            <h3>灵活学习</h3>
            <p>随时随地按照自己的节奏学习</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import CourseCard from '../components/CourseCard.vue'

export default {
  name: 'Home',
  components: {
    CourseCard
  },
  data() {
  return {
    searchTerm: '',
    featuredCourses: [
      {
        id: 1,
        title: '机器学习入门',
        instructor: '斯坦福大学 · Andrew Ng',
        rating: 4.8,
        ratingCount: 12345,
        price: 0,
        level: '初级',
        duration: '15小时',
        image: 'https://images.unsplash.com/photo-1555255707-c07966088b7b?w=300&h=160&fit=crop',
        featured: true
      },
      {
        id: 2,
        title: 'Python 编程',
        instructor: '密歇根大学 · Charles Severance',
        rating: 4.9,
        ratingCount: 8765,
        price: 0,
        level: '初级',
        duration: '20小时',
        image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=300&h=160&fit=crop',
        featured: false
      },
      {
        id: 3,
        title: 'Web 开发全栈',
        instructor: '香港大学 · John Doe',
        rating: 4.7,
        ratingCount: 5432,
        price: 399,
        level: '中级',
        duration: '35小时',
        image: 'https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=300&h=160&fit=crop',
        featured: true
      }
    ],
    popularCourses: [
      {
        id: 1,
        title: '机器学习入门',
        instructor: '斯坦福大学 · Andrew Ng',
        rating: 4.8,
        ratingCount: 12345,
        price: 0,
        level: '初级',
        duration: '15小时',
        image: 'https://images.unsplash.com/photo-1555255707-c07966088b7b?w=300&h=160&fit=crop'
      },
      {
        id: 2,
        title: 'Python 编程',
        instructor: '密歇根大学 · Charles Severance',
        rating: 4.9,
        ratingCount: 8765,
        price: 0,
        level: '初级',
        duration: '20小时',
        image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=300&h=160&fit=crop'
      },
      {
        id: 5,
        title: '数字营销策略',
        instructor: '伊利诺伊大学 · Aric Rindfleisch',
        rating: 4.6,
        ratingCount: 5432,
        price: 399,
        level: '中级',
        duration: '18小时',
        image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=300&h=160&fit=crop'
      },
      {
        id: 6,
        title: 'UI/UX 设计原理',
        instructor: '加州艺术学院 · Sarah Johnson',
        rating: 4.7,
        ratingCount: 3210,
        price: 349,
        level: '初级',
        duration: '22小时',
        image: 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=300&h=160&fit=crop'
      }
    ]
  }
},
  methods: {
    performSearch() {
      if (this.searchTerm.trim()) {
        this.$router.push({
          path: '/courses',
          query: { search: this.searchTerm }
        })
      }
    },
    navigateToCourse(courseId) {
      this.$router.push(`/course/${courseId}`)
    },
    navigateToCategory(category) {
      this.$router.push({
        path: '/courses',
        query: { category }
      })
    }
  }
}
</script>