<template>
  <div class="font-inter min-h-screen flex-col">
    <Header />
    
    <!-- 页面标题和导航 -->
    <div class="page-header">
      <h1 class="page-title">课程详情</h1>
      <div class="breadcrumb">
        <router-link to="/">首页</router-link> > 
        <router-link to="/courses?category=programming">编程开发</router-link> > 
        <router-link to="/courses?category=python">Python</router-link> > 
        <span>{{ course.title }}</span>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧课程详情区域 -->
      <div class="course-detail">
        <!-- 课程头部信息 -->
        <div class="course-header">
          <h1 class="course-title">{{ course.title }}</h1>
          <p class="course-subtitle">{{ course.subtitle }}</p>
          
          <div class="course-meta">
            <div class="meta-item">
              <i class="fas fa-clock"></i>
              <span>{{ course.duration }}</span>
            </div>
            <div class="meta-item">
              <i class="fas fa-user-graduate"></i>
              <span>{{ course.students }}人学习</span>
            </div>
            <div class="meta-item">
              <i class="fas fa-star"></i>
              <span>{{ course.rating }}分 ({{ course.reviews }}评价)</span>
            </div>
            <div class="difficulty-badge">{{ course.difficulty }}</div>
          </div>
          
          <!-- 讲师信息 -->
          <div class="course-instructor">
            <div class="instructor-avatar">
              <img :src="instructor.avatar" :alt="instructor.name">
            </div>
            <div class="instructor-info">
              <h3>{{ instructor.name }}</h3>
              <p class="instructor-bio">{{ instructor.bio }}</p>
              <div class="instructor-verified" v-if="instructor.verified">
                <i class="fas fa-check-circle"></i>
                <span>平台认证讲师</span>
              </div>
            </div>
          </div>
          
          <!-- 课程操作按钮 -->
          <div class="course-actions">
            <button class="btn btn-primary" @click="startLearning">
              <i class="fas fa-play"></i> {{ hasStarted ? '继续学习' : '开始学习' }}
            </button>
            <button 
              class="btn" 
              :class="isAdded ? 'btn-primary' : 'btn-secondary'"
              @click="toggleLearningList"
            >
              <i :class="isAdded ? 'fas fa-check' : 'fas fa-plus'"></i> 
              {{ isAdded ? '已加入学习' : '加入学习' }}
            </button>
            <button class="btn btn-outline">
              <i class="fas fa-share-alt"></i> 分享课程
            </button>
            <button class="btn btn-outline">
              <i class="fas fa-flag"></i> 举报
            </button>
          </div>
        </div>
        
        <!-- 课程大纲 -->
        <div class="course-syllabus">
          <h2 class="section-title">课程大纲</h2>
          <ul class="syllabus-list">
            <li 
              v-for="(chapter, index) in syllabus" 
              :key="index"
              class="syllabus-item" 
              :class="{ active: activeChapter === index }"
              @click="selectChapter(index)"
            >
              <div class="syllabus-header">
                <div class="syllabus-title">{{ chapter.title }}</div>
                <div class="syllabus-duration">{{ chapter.duration }}</div>
              </div>
              <p class="syllabus-description">{{ chapter.description }}</p>
              <div class="syllabus-meta">
                <span><i class="fas fa-video"></i> {{ chapter.videos }}个视频</span>
                <span><i class="fas fa-file-alt"></i> {{ chapter.readings }}篇阅读</span>
                <span><i class="fas fa-question-circle"></i> {{ chapter.quizzes }}个测验</span>
              </div>
            </li>
          </ul>
        </div>
        
        <!-- 课程描述 -->
        <div class="course-description">
          <h2 class="section-title">课程描述</h2>
          <div class="description-content">
            <p>{{ course.description }}</p>
            
            <h3>课程亮点：</h3>
            <ul>
              <li v-for="(highlight, index) in course.highlights" :key="index">
                <strong>{{ highlight.title }}</strong>：{{ highlight.description }}
              </li>
            </ul>
            
            <h3>学习目标：</h3>
            <ul>
              <li v-for="(goal, index) in course.goals" :key="'goal-' + index">
                {{ goal }}
              </li>
            </ul>
          </div>
        </div>
        
        <!-- 课程评价 -->
        <div class="course-reviews">
          <h2 class="section-title">学员评价</h2>
          <div class="review-summary">
            <div class="rating-score">{{ course.rating }}</div>
            <div>
              <div class="rating-stars">
                <i v-for="star in starRating" :key="star" :class="star"></i>
              </div>
              <div class="review-count">基于{{ course.reviews }}条评价</div>
            </div>
          </div>
          
          <div class="review-item" v-for="review in reviews" :key="review.id">
            <div class="review-header">
              <div class="reviewer">
                <div class="reviewer-avatar">
                  <img :src="review.avatar" :alt="review.name">
                </div>
                <div class="reviewer-info">
                  <h4>{{ review.name }}</h4>
                  <div class="review-date">{{ review.date }}</div>
                </div>
              </div>
              <div class="rating-stars">
                <i v-for="n in 5" :key="n" class="fas" :class="n <= review.stars ? 'fa-star' : 'fa-star-o'"></i>
              </div>
            </div>
            <div class="review-content">
              {{ review.content }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- 右侧侧边栏区域 -->
      <div class="course-sidebar">
        <!-- 课程信息卡片 -->
        <div class="course-info-card">
          <h3 class="section-title" style="border-bottom: none; margin-bottom: 1rem;">课程信息</h3>
          <div class="info-item">
            <span class="info-label">课程时长</span>
            <span class="info-value">{{ courseInfo.duration }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">课程节数</span>
            <span class="info-value">{{ courseInfo.lessons }}小节</span>
          </div>
          <div class="info-item">
            <span class="info-label">课程难度</span>
            <span class="info-value">{{ courseInfo.difficulty }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">学习人数</span>
            <span class="info-value">{{ courseInfo.students }}人</span>
          </div>
          <div class="info-item">
            <span class="info-label">课程评分</span>
            <span class="info-value">{{ courseInfo.rating }}分</span>
          </div>
          <div class="info-item">
            <span class="info-label">课程语言</span>
            <span class="info-value">{{ courseInfo.language }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">课程分类</span>
            <span class="info-value">{{ courseInfo.category }}</span>
          </div>
        </div>
        
        <!-- 课程特色 -->
        <div class="course-features">
          <h3 class="section-title" style="border-bottom: none; margin-bottom: 1rem;">课程特色</h3>
          <ul class="features-list">
            <li class="feature-item" v-for="feature in features" :key="feature.id">
              <div class="feature-icon">
                <i :class="feature.icon"></i>
              </div>
              <div class="feature-content">
                <h4>{{ feature.title }}</h4>
                <p>{{ feature.description }}</p>
              </div>
            </li>
          </ul>
        </div>
        
        <!-- 相关课程 -->
        <div class="related-courses">
          <h3 class="section-title" style="border-bottom: none; margin-bottom: 1rem;">相关课程</h3>
          <div class="course-grid">
            <router-link 
              v-for="relatedCourse in relatedCourses" 
              :key="relatedCourse.id"
              :to="'/course/' + relatedCourse.id" 
              class="course-card"
            >
              <div class="course-thumbnail">
                <img :src="relatedCourse.image" :alt="relatedCourse.title">
              </div>
              <div class="course-card-content">
                <h3 class="course-card-title">{{ relatedCourse.title }}</h3>
                <div class="course-card-instructor">{{ relatedCourse.instructor }}</div>
                <div class="course-card-meta">
                  <span>{{ relatedCourse.duration }} · {{ relatedCourse.difficulty }}</span>
                  <span>{{ relatedCourse.rating }}分</span>
                </div>
              </div>
            </router-link>
          </div>
        </div>
        
        <!-- 学习须知 -->
        <div class="learning-notice">
          <h3 class="section-title" style="border-bottom: none; margin-bottom: 1rem;">学习须知</h3>
          <ul class="notice-list">
            <li class="notice-item" v-for="notice in notices" :key="notice.id">
              <i class="fas fa-exclamation-circle"></i>
              <span>{{ notice.text }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'

export default {
  name: 'CourseDetail',
  components: {
    Header
  },
  data() {
    return {
      course: {
        id: 1,
        title: 'Python数据分析与可视化实战',
        subtitle: '从零开始掌握数据分析核心技能，使用Pandas、Matplotlib、Seaborn完成真实商业数据分析项目',
        duration: '24小时 · 48小节',
        students: '12,850',
        rating: 4.8,
        reviews: '2,345',
        difficulty: '中级',
        description: '本课程专为希望掌握Python数据分析与可视化技能的学习者设计。通过理论与实践相结合的方式，您将学习到从基础数据处理到高级可视化技术的完整知识体系。',
        highlights: [
          { title: '实战驱动', description: '基于真实商业场景的数据分析项目' },
          { title: 'AI辅助学习', description: '智能推荐学习路径，个性化习题生成' },
          { title: '全方位支持', description: '视频讲解、图文资料、在线答疑、项目实战' },
          { title: '持续更新', description: '课程内容定期更新，紧跟行业发展趋势' }
        ],
        goals: [
          '掌握Python数据分析核心库（NumPy, Pandas）的使用',
          '能够熟练进行数据清洗、转换和预处理',
          '使用Matplotlib和Seaborn创建专业的可视化图表',
          '完成完整的商业数据分析项目并生成分析报告',
          '具备解决实际业务问题的数据分析能力'
        ]
      },
      instructor: {
        name: '李明教授',
        bio: '数据科学家，前阿里巴巴高级分析师，10年数据分析经验',
        avatar: 'https://randomuser.me/api/portraits/men/44.jpg',
        verified: true
      },
      syllabus: [
        {
          title: '第一章：Python数据分析基础',
          duration: '4小时20分钟',
          description: '学习Python数据处理基础，掌握NumPy和Pandas核心操作',
          videos: 8,
          readings: 3,
          quizzes: 2
        },
        {
          title: '第二章：数据清洗与预处理',
          duration: '5小时10分钟',
          description: '处理缺失值、异常值，数据规范化与转换技巧',
          videos: 10,
          readings: 4,
          quizzes: 3
        },
        {
          title: '第三章：数据可视化实战',
          duration: '6小时30分钟',
          description: '使用Matplotlib和Seaborn创建专业级图表',
          videos: 12,
          readings: 5,
          quizzes: 4
        },
        {
          title: '第四章：项目实战 - 电商数据分析',
          duration: '8小时15分钟',
          description: '完整电商数据分析项目，从数据获取到可视化报告',
          videos: 15,
          readings: 6,
          quizzes: 5
        }
      ],
      reviews: [
        {
          id: 1,
          name: '王同学',
          date: '2023-10-15',
          stars: 5,
          content: '课程内容非常实用，老师讲解清晰，特别是项目实战部分，让我真正掌握了数据分析的工作流程。AI生成的习题也很有针对性，能够及时巩固知识点。',
          avatar: 'https://randomuser.me/api/portraits/women/44.jpg'
        },
        {
          id: 2,
          name: '李同学',
          date: '2023-09-28',
          stars: 5,
          content: '作为一名转行者，这门课程对我帮助极大。自适应学习机制根据我的进度调整难度，AI助手随时解答疑问。现在我已经成功找到数据分析师的工作！',
          avatar: 'https://randomuser.me/api/portraits/men/22.jpg'
        }
      ],
      courseInfo: {
        duration: '24小时',
        lessons: '48',
        difficulty: '中级',
        students: '12,850',
        rating: '4.8',
        language: '中文',
        category: '编程开发 / 数据分析'
      },
      features: [
        {
          id: 1,
          icon: 'fas fa-robot',
          title: 'AI自适应学习',
          description: '根据你的学习进度和掌握程度，智能调整学习路径和难度'
        },
        {
          id: 2,
          icon: 'fas fa-chart-line',
          title: '实时学习分析',
          description: '跟踪学习行为，提供个性化学习报告和优化建议'
        },
        {
          id: 3,
          icon: 'fas fa-question-circle',
          title: 'AI习题生成',
          description: '基于学习内容自动生成针对性习题，巩固知识点'
        },
        {
          id: 4,
          icon: 'fas fa-certificate',
          title: '结业证书',
          description: '完成课程并通过考核后，可获得平台认证的结业证书'
        }
      ],
      relatedCourses: [
        {
          id: 2,
          title: '机器学习入门与实践',
          instructor: '张教授 · 人工智能专家',
          duration: '18小时',
          difficulty: '中级',
          rating: '4.9',
          image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'
        },
        {
          id: 3,
          title: 'SQL数据库高级查询',
          instructor: '李老师 · 数据库架构师',
          duration: '12小时',
          difficulty: '初级',
          rating: '4.7',
          image: 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'
        }
      ],
      notices: [
        { id: 1, text: '学习本课程需要具备Python基础编程知识' },
        { id: 2, text: '建议每周学习3-5小时，持续2个月完成课程' },
        { id: 3, text: '课程中包含实践项目，需要完成并提交' },
        { id: 4, text: '通过所有测验和项目可获得结业证书' }
      ],
      activeChapter: 0,
      isAdded: false,
      hasStarted: false
    }
  },
  computed: {
    starRating() {
      const stars = []
      const fullStars = Math.floor(this.course.rating)
      const hasHalfStar = this.course.rating % 1 >= 0.5
      
      for (let i = 0; i < fullStars; i++) {
        stars.push('fas fa-star')
      }
      
      if (hasHalfStar) {
        stars.push('fas fa-star-half-alt')
      }
      
      const remainingStars = 5 - stars.length
      for (let i = 0; i < remainingStars; i++) {
        stars.push('fas fa-star')
      }
      
      return stars
    }
  },
  created() {
    // 从路由参数获取课程ID
    const courseId = this.$route.params.id
    // 这里可以添加根据courseId获取课程数据的逻辑
    
    // 检查用户是否已加入学习
    this.checkLearningStatus()
  },
  methods: {
    selectChapter(index) {
      this.activeChapter = index
    },
    
    startLearning() {
      if (!this.hasStarted) {
        // 如果还没开始学习，先加入学习列表
        this.toggleLearningList()
        this.hasStarted = true
      }
      // 跳转到视频播放页面
      this.$router.push({
        name: 'VideoPlayer',
        params: { courseId: this.course.id }
      })
    },
    
    toggleLearningList() {
      this.isAdded = !this.isAdded
      
      // 显示通知
      this.showNotification(
        this.isAdded ? '课程已成功添加到我的学习列表' : '已从学习列表中移除'
      )
      
      // 保存到本地存储
      this.saveLearningStatus()
    },
    
    checkLearningStatus() {
      // 从本地存储检查学习状态
      const learningList = JSON.parse(localStorage.getItem('myLearningList') || '[]')
      this.isAdded = learningList.includes(this.course.id)
      
      // 检查是否已经开始学习
      const learningProgress = JSON.parse(localStorage.getItem('learningProgress') || '{}')
      this.hasStarted = !!learningProgress[this.course.id]
    },
    
    saveLearningStatus() {
      // 获取当前学习列表
      let learningList = JSON.parse(localStorage.getItem('myLearningList') || '[]')
      
      if (this.isAdded) {
        // 添加课程ID（如果不存在）
        if (!learningList.includes(this.course.id)) {
          learningList.push(this.course.id)
        }
      } else {
        // 移除课程ID
        learningList = learningList.filter(id => id !== this.course.id)
      }
      
      // 保存到本地存储
      localStorage.setItem('myLearningList', JSON.stringify(learningList))
    },
    
    showNotification(message) {
      // 创建通知元素
      const notification = document.createElement('div')
      notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background-color: var(--accent-green, #10B981);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        z-index: 1000;
        animation: slideIn 0.3s ease;
      `
      
      notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
          <i class="fas fa-check-circle"></i>
          <span>${message}</span>
        </div>
      `
      
      document.body.appendChild(notification)
      
      // 3秒后移除通知
      setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease'
        setTimeout(() => {
          document.body.removeChild(notification)
        }, 300)
      }, 3000)
    }
  }
}
</script>

<style scoped>
/* 保持原有的CSS样式，但将部分选择器改为Vue作用域样式 */
.page-header {
  max-width: 1200px;
  margin: 2rem auto 1rem;
  padding: 0 1.5rem;
}

.page-title {
  font-size: 2rem;
  color: var(--dark-gray, #1F2937);
  margin-bottom: 0.5rem;
}

.breadcrumb {
  display: flex;
  gap: 0.5rem;
  color: var(--text-gray, #4E5969);
  font-size: 0.9rem;
  margin-bottom: 2rem;
}

.breadcrumb a {
  color: var(--primary-blue, #165DFF);
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto 3rem;
  padding: 0 1.5rem;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.course-detail {
  background-color: var(--white, #ffffff);
  border-radius: var(--radius, 8px);
  box-shadow: var(--shadow, 0 4px 12px rgba(0, 0, 0, 0.08));
  padding: 2rem;
}

.course-header {
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--medium-gray, #E5E6EB);
  padding-bottom: 1.5rem;
}

.course-title {
  font-size: 2rem;
  color: var(--dark-gray, #1F2937);
  margin-bottom: 0.5rem;
}

.course-subtitle {
  font-size: 1.1rem;
  color: var(--text-gray, #4E5969);
  margin-bottom: 1.5rem;
}

.course-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-gray, #4E5969);
}

.meta-item i {
  color: var(--primary-blue, #165DFF);
}

.difficulty-badge {
  background-color: var(--accent-yellow, #FF9F43);
  color: var(--dark-gray, #1F2937);
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.course-instructor {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.instructor-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  background-color: var(--light-gray, #F7F8FA);
}

.instructor-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.instructor-info h3 {
  font-size: 1.2rem;
  margin-bottom: 0.3rem;
}

.instructor-bio {
  color: var(--text-gray, #4E5969);
  font-size: 0.95rem;
}

.instructor-verified {
  color: var(--accent-green, #10B981);
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 0.3rem;
}

.course-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.btn {
  padding: 0.7rem 1.5rem;
  border-radius: var(--radius, 8px);
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary {
  background-color: var(--primary-blue, #165DFF);
  color: var(--white, #ffffff);
}

.btn-primary:hover {
  background-color: rgba(22, 93, 255, 0.9);
}

.btn-secondary {
  background-color: var(--white, #ffffff);
  color: var(--primary-blue, #165DFF);
  border: 2px solid var(--primary-blue, #165DFF);
}

.btn-secondary:hover {
  background-color: rgba(22, 93, 255, 0.05);
}

.btn-outline {
  background-color: transparent;
  color: var(--text-gray, #4E5969);
  border: 1px solid var(--medium-gray, #E5E6EB);
}

.btn-outline:hover {
  background-color: var(--light-gray, #F9FAFB);
}

.course-syllabus {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.4rem;
  margin-bottom: 1.2rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--medium-gray, #E5E6EB);
  color: var(--dark-gray, #1F2937);
}

.syllabus-list {
  list-style: none;
}

.syllabus-item {
  padding: 1rem;
  border: 1px solid var(--medium-gray, #E5E6EB);
  border-radius: var(--radius, 8px);
  margin-bottom: 0.8rem;
  cursor: pointer;
  transition: all 0.3s;
}

.syllabus-item:hover {
  border-color: var(--primary-blue, #165DFF);
  background-color: rgba(22, 93, 255, 0.03);
}

.syllabus-item.active {
  border-color: var(--primary-blue, #165DFF);
  background-color: rgba(22, 93, 255, 0.08);
}

.syllabus-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.syllabus-title {
  font-weight: 600;
  font-size: 1.1rem;
}

.syllabus-duration {
  color: var(--text-gray, #4E5969);
  font-size: 0.9rem;
}

.syllabus-description {
  color: var(--text-gray, #4E5969);
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
}

.syllabus-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: var(--secondary-blue, #6B7280);
}

.course-reviews {
  margin-bottom: 2rem;
}

.review-summary {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.rating-score {
  font-size: 3rem;
  font-weight: 700;
  color: var(--primary-blue, #165DFF);
}

.rating-stars {
  color: var(--accent-yellow, #FF9F43);
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.review-count {
  color: var(--text-gray, #4E5969);
}

.review-item {
  padding: 1.2rem;
  border: 1px solid var(--medium-gray, #E5E6EB);
  border-radius: var(--radius, 8px);
  margin-bottom: 1rem;
}

.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.8rem;
}

.reviewer {
  display: flex;
  align-items: center;
  gap: 10px;
}

.reviewer-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  background-color: var(--light-gray, #F7F8FA);
}

.reviewer-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.reviewer-info h4 {
  font-size: 1rem;
  margin-bottom: 0.2rem;
}

.review-date {
  color: var(--secondary-blue, #6B7280);
  font-size: 0.9rem;
}

.review-content {
  color: var(--dark-gray, #1F2937);
  line-height: 1.7;
}

.course-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.related-courses {
  background-color: var(--white, #ffffff);
  border-radius: var(--radius, 8px);
  box-shadow: var(--shadow, 0 4px 12px rgba(0, 0, 0, 0.08));
  padding: 1.5rem;
}

.course-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.course-card {
  border: 1px solid var(--medium-gray, #E5E6EB);
  border-radius: var(--radius, 8px);
  overflow: hidden;
  transition: all 0.3s;
  text-decoration: none;
  color: inherit;
  display: block;
}

.course-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow, 0 4px 12px rgba(0, 0, 0, 0.08));
  border-color: var(--primary-blue, #165DFF);
}

.course-thumbnail {
  height: 140px;
  background-color: var(--secondary-blue, #6B7280);
  overflow: hidden;
}

.course-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.course-card:hover .course-thumbnail img {
  transform: scale(1.05);
}

.course-card-content {
  padding: 1rem;
}

.course-card-title {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.course-card-instructor {
  color: var(--text-gray, #4E5969);
  font-size: 0.9rem;
  margin-bottom: 0.8rem;
}

.course-card-meta {
  display: flex;
  justify-content: space-between;
  color: var(--secondary-blue, #6B7280);
  font-size: 0.85rem;
}

.course-features {
  background-color: var(--white, #ffffff);
  border-radius: var(--radius, 8px);
  box-shadow: var(--shadow, 0 4px 12px rgba(0, 0, 0, 0.08));
  padding: 1.5rem;
}

.features-list {
  list-style: none;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.2rem;
  padding-bottom: 1.2rem;
  border-bottom: 1px solid var(--medium-gray, #E5E6EB);
}

.feature-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.feature-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(22, 93, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-blue, #165DFF);
  font-size: 1.2rem;
}

.feature-content h4 {
  font-size: 1rem;
  margin-bottom: 0.3rem;
  color: var(--dark-gray, #1F2937);
}

.feature-content p {
  color: var(--text-gray, #4E5969);
  font-size: 0.9rem;
}

.course-info-card {
  background-color: var(--white, #ffffff);
  border-radius: var(--radius, 8px);
  box-shadow: var(--shadow, 0 4px 12px rgba(0, 0, 0, 0.08));
  padding: 1.5rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.8rem 0;
  border-bottom: 1px solid var(--medium-gray, #E5E6EB);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  color: var(--text-gray, #4E5969);
}

.info-value {
  font-weight: 500;
  color: var(--dark-gray, #1F2937);
}

.learning-notice {
  background-color: var(--white, #ffffff);
  border-radius: var(--radius, 8px);
  box-shadow: var(--shadow, 0 4px 12px rgba(0, 0, 0, 0.08));
  padding: 1.5rem;
}

.notice-list {
  list-style: none;
}

.notice-item {
  display: flex;
  align-items: flex-start;
  gap: 0.8rem;
  margin-bottom: 0.8rem;
  color: var(--text-gray, #4E5969);
  font-size: 0.9rem;
}

.notice-item i {
  color: var(--accent-red, #F53F3F);
  margin-top: 0.2rem;
}

@media (max-width: 992px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .course-sidebar {
    order: -1;
  }
}

@media (max-width: 768px) {
  .course-actions {
    flex-wrap: wrap;
  }
  
  .btn {
    flex-grow: 1;
  }
}

@media (max-width: 576px) {
  .main-content {
    padding: 0 1rem;
  }
  
  .course-detail, .related-courses, .course-features, .course-info-card, .learning-notice {
    padding: 1.5rem;
  }
  
  .course-title {
    font-size: 1.6rem;
  }
  
  .course-meta {
    gap: 1rem;
  }
  
  .review-summary {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}

/* 添加动画样式 */
@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

@keyframes slideOut {
  from { transform: translateX(0); opacity: 1; }
  to { transform: translateX(100%); opacity: 0; }
}
</style>