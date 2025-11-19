<template>
  <section class="course-detail" v-if="course">
    <div class="container">
      <div class="course-header">
        <div class="breadcrumb">
          <router-link to="/">首页</router-link> > 
          <router-link to="/courses">课程</router-link> > 
          <a href="#">计算机科学</a> > 
          <span>{{ course.title }}</span>
        </div>
        
        <div class="course-hero">
          <div class="course-main-info">
            <h1>{{ course.title }}</h1>
            <p class="course-subtitle">{{ course.subtitle }}</p>
            
            <!-- 课程图片展示 -->
            <div class="course-image-main">
              <img 
                :src="course.image" 
                :alt="course.title" 
                class="main-course-image"
                @error="handleImageError"
              >
            </div>
            
            <div class="course-meta">
              <div class="instructor-info" @click="navigateToInstructor(course.instructor.id)">
                <div class="instructor-avatar">
                  <img 
                    v-if="course.instructor.avatar" 
                    :src="course.instructor.avatar" 
                    :alt="course.instructor.name"
                    @error="handleAvatarError"
                  >
                  <i v-else class="fas fa-user-tie"></i>
                </div>
                <div>
                  <div class="instructor-name">{{ course.instructor.name }}</div>
                  <div class="instructor-title">{{ course.instructor.title }}</div>
                </div>
              </div>
              
              <div class="course-stats">
                <div class="stat">
                  <i class="fas fa-star"></i>
                  <span>{{ course.rating }} ({{ course.ratingCount }} 评价)</span>
                </div>
                <div class="stat">
                  <i class="fas fa-users"></i>
                  <span>{{ course.studentCount }} 名学生</span>
                </div>
                <div class="stat">
                  <i class="fas fa-clock"></i>
                  <span>约 {{ course.duration }} 完成</span>
                </div>
              </div>
            </div>
            
            <div class="course-actions">
              <button class="btn btn-primary btn-enroll" @click="enrollCourse">立即注册</button>
              <button class="btn btn-outline btn-wishlist" @click="toggleWishlist">
                <i :class="[isInWishlist ? 'fas' : 'far', 'fa-heart']"></i> 
                {{ isInWishlist ? '已收藏' : '加入收藏' }}
              </button>
              <button class="btn btn-outline btn-share" @click="shareCourse">
                <i class="fas fa-share-alt"></i> 分享
              </button>
            </div>
          </div>
          
          <div class="course-preview">
            <div class="preview-video" @click="navigateToVideoPlayer(course.modules[0].lessons[0])">
              <div class="video-placeholder">
                <img 
                  :src="course.thumbnail" 
                  :alt="course.title" 
                  class="preview-thumbnail"
                  @error="handleThumbnailError"
                >
                <div class="play-overlay">
                  <i class="fas fa-play-circle"></i>
                  <p>课程预览视频</p>
                </div>
              </div>
            </div>
            <div class="preview-info">
              <div class="price-info">
                <span class="current-price">{{ course.price === 0 ? '免费' : `¥${course.price}` }}</span>
                <span v-if="course.originalPrice" class="original-price">¥{{ course.originalPrice }}</span>
                <div v-if="course.price === 0" class="free-badge">免费学习</div>
              </div>
              <div class="preview-features">
                <div class="feature">
                  <i class="fas fa-play-circle"></i>
                  <span>{{ totalVideos }} 个视频</span>
                </div>
                <div class="feature">
                  <i class="fas fa-tasks"></i>
                  <span>{{ totalQuizzes }} 个测验</span>
                </div>
                <div class="feature">
                  <i class="fas fa-certificate"></i>
                  <span>可共享证书</span>
                </div>
                <div class="feature">
                  <i class="fas fa-infinity"></i>
                  <span>终身访问</span>
                </div>
              </div>
              
              <div class="enrollment-stats">
                <div class="enrollment-count">
                  <i class="fas fa-user-graduate"></i>
                  <span>已有 {{ formatStudentCount(course.studentCount) }} 人注册</span>
                </div>
                <div class="last-updated">
                  <i class="fas fa-sync-alt"></i>
                  <span>最近更新: {{ course.lastUpdated }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="course-content">
        <div class="content-nav">
          <div 
            class="nav-item" 
            :class="{ active: activeTab === 'overview' }"
            @click="activeTab = 'overview'"
          >
            概述
          </div>
          <div 
            class="nav-item" 
            :class="{ active: activeTab === 'curriculum' }"
            @click="activeTab = 'curriculum'"
          >
            课程内容
          </div>
          <div 
            class="nav-item" 
            :class="{ active: activeTab === 'instructor' }"
            @click="activeTab = 'instructor'"
          >
            讲师
          </div>
          <div 
            class="nav-item" 
            :class="{ active: activeTab === 'reviews' }"
            @click="activeTab = 'reviews'"
          >
            评价
          </div>
        </div>
        
        <div class="content-panels">
          <!-- 概述面板 -->
          <div class="content-panel" :class="{ active: activeTab === 'overview' }">
            <div class="panel-content">
              <h2>课程概述</h2>
              <p>{{ course.description }}</p>
              
              <h3>您将学到什么</h3>
              <ul class="learning-objectives">
                <li v-for="objective in course.learningObjectives" :key="objective">
                  <i class="fas fa-check-circle"></i>
                  {{ objective }}
                </li>
              </ul>
              
              <h3>课程特色</h3>
              <div class="course-features">
                <div class="feature-card">
                  <i class="fas fa-laptop-code"></i>
                  <h4>实践项目</h4>
                  <p>通过实际项目巩固所学知识</p>
                </div>
                <div class="feature-card">
                  <i class="fas fa-graduation-cap"></i>
                  <h4>灵活学习</h4>
                  <p>按照自己的节奏学习</p>
                </div>
                <div class="feature-card">
                  <i class="fas fa-certificate"></i>
                  <h4>获得证书</h4>
                  <p>完成课程后获得可共享证书</p>
                </div>
                <div class="feature-card">
                  <i class="fas fa-comments"></i>
                  <h4>社区支持</h4>
                  <p>加入学习社区，与同学交流</p>
                </div>
              </div>
              
              <h3>适合人群</h3>
              <div class="target-audience">
                <p>{{ course.targetAudience }}</p>
                <ul class="audience-list">
                  <li v-for="(audience, index) in course.targetAudienceList" :key="index">
                    <i class="fas fa-user-check"></i>
                    {{ audience }}
                  </li>
                </ul>
              </div>

              <h3>预备知识</h3>
              <div class="prerequisites">
                <ul class="prerequisites-list">
                  <li v-for="(prereq, index) in course.prerequisites" :key="index">
                    <i class="fas fa-book"></i>
                    {{ prereq }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
          
          <!-- 课程内容面板 -->
          <div class="content-panel" :class="{ active: activeTab === 'curriculum' }">
            <div class="panel-content">
              <h2>课程大纲</h2>
              <p>本课程包含{{ course.modules.length }}个模块，共{{ totalVideos }}个视频和{{ totalQuizzes }}个测验。</p>
              
              <div class="curriculum-stats">
                <div class="curriculum-stat">
                  <i class="fas fa-play-circle"></i>
                  <span>{{ totalVideos }} 个视频课程</span>
                </div>
                <div class="curriculum-stat">
                  <i class="fas fa-tasks"></i>
                  <span>{{ totalQuizzes }} 个测验</span>
                </div>
                <div class="curriculum-stat">
                  <i class="fas fa-clock"></i>
                  <span>总时长 {{ totalDuration }}</span>
                </div>
                <div class="curriculum-stat">
                  <i class="fas fa-download"></i>
                  <span>{{ course.downloadableResources }} 个可下载资源</span>
                </div>
              </div>
              
              <div class="modules">
                <div 
                  v-for="(module, moduleIndex) in course.modules" 
                  :key="moduleIndex"
                  class="module"
                >
                  <div class="module-header" @click="toggleModule(moduleIndex)">
                    <div class="module-title">
                      <h3>{{ module.title }}</h3>
                      <span class="module-meta">{{ module.lessons.length }}个视频 • {{ module.quizzes.length }}个测验 • {{ module.duration }}</span>
                    </div>
                    <div class="module-toggle">
                      <i class="fas" :class="expandedModule === moduleIndex ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
                    </div>
                  </div>
                  <div class="module-content" :class="{ expanded: expandedModule === moduleIndex }">
                    <div 
                      v-for="(lesson, lessonIndex) in module.lessons" 
                      :key="`lesson-${lessonIndex}`"
                      class="lesson"
                      @click="navigateToVideoPlayer(lesson)"
                    >
                      <div class="lesson-info">
                        <i class="far fa-play-circle"></i>
                        <div class="lesson-details">
                          <span class="lesson-title">{{ lesson.title }}</span>
                          <span class="lesson-preview" v-if="lesson.isPreview">预览</span>
                        </div>
                      </div>
                      <span class="lesson-duration">{{ lesson.duration }}</span>
                    </div>
                    <div 
                      v-for="(quiz, quizIndex) in module.quizzes" 
                      :key="`quiz-${quizIndex}`"
                      class="lesson quiz"
                      @click="navigateToQuiz(quiz)"
                    >
                      <div class="lesson-info">
                        <i class="fas fa-tasks"></i>
                        <div class="lesson-details">
                          <span class="lesson-title">{{ quiz.title }}</span>
                        </div>
                      </div>
                      <div class="quiz-progress">
                        <div class="progress-bar">
                          <div class="progress-fill" :style="{ width: getQuizProgress(quiz) + '%' }"></div>
                        </div>
                        <span class="progress-text">{{ getQuizProgressText(quiz) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 讲师面板 -->
          <div class="content-panel" :class="{ active: activeTab === 'instructor' }">
            <div class="panel-content">
              <h2>课程讲师</h2>
              <div class="instructor-detail" @click="navigateToInstructor(course.instructor.id)">
                <div class="instructor-main">
                  <div class="instructor-avatar large">
                    <img 
                      v-if="course.instructor.avatar" 
                      :src="course.instructor.avatar" 
                      :alt="course.instructor.name"
                      @error="handleAvatarError"
                    >
                    <i v-else class="fas fa-user-tie"></i>
                  </div>
                  <div class="instructor-bio">
                    <h3>{{ course.instructor.name }}</h3>
                    <p class="instructor-title">{{ course.instructor.title }}</p>
                    <div class="instructor-stats">
                      <div class="stat">
                        <strong>{{ course.instructor.rating }}</strong>
                        <span>讲师评分</span>
                      </div>
                      <div class="stat">
                        <strong>{{ formatStudentCount(course.instructor.studentCount) }}</strong>
                        <span>学生人数</span>
                      </div>
                      <div class="stat">
                        <strong>{{ course.instructor.courseCount }}</strong>
                        <span>课程数量</span>
                      </div>
                      <div class="stat">
                        <strong>{{ course.instructor.reviewCount }}</strong>
                        <span>评价数量</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="instructor-description">
                  <p v-for="(paragraph, index) in course.instructor.bio" :key="index">
                    {{ paragraph }}
                  </p>
                </div>
                
                <div class="instructor-expertise">
                  <h4>专业领域</h4>
                  <div class="expertise-tags">
                    <span v-for="expertise in course.instructor.expertise" :key="expertise" class="expertise-tag">
                      {{ expertise }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 评价面板 -->
          <div class="content-panel" :class="{ active: activeTab === 'reviews' }">
            <div class="panel-content">
              <h2>学员评价</h2>
              <div class="reviews-summary">
                <div class="rating-overview">
                  <div class="average-rating">
                    <div class="rating-number">{{ course.rating }}</div>
                    <div class="rating-stars">
                      <i v-for="n in 5" :key="n" :class="getStarClass(n)"></i>
                    </div>
                    <div class="rating-count">{{ course.ratingCount }} 条评价</div>
                  </div>
                  <div class="rating-distribution">
                    <div v-for="(percent, stars) in course.ratingDistribution" :key="stars" class="distribution-bar">
                      <span>{{ stars }}星</span>
                      <div class="bar">
                        <div class="fill" :style="{ width: percent + '%' }"></div>
                      </div>
                      <span>{{ percent }}%</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="reviews-filter">
                <button 
                  v-for="filter in reviewFilters" 
                  :key="filter.value"
                  class="filter-btn" 
                  :class="{ active: selectedReviewFilter === filter.value }"
                  @click="selectedReviewFilter = filter.value"
                >
                  {{ filter.label }}
                </button>
              </div>
              
              <div class="reviews-list">
                <div v-for="review in filteredReviews" :key="review.id" class="review">
                  <div class="review-header">
                    <div class="reviewer" @click="navigateToUser(review.userId)">
                      <div class="reviewer-avatar">
                        <i class="fas fa-user"></i>
                      </div>
                      <div class="reviewer-info">
                        <div class="reviewer-name">{{ review.userName }}</div>
                        <div class="review-date">{{ review.date }}</div>
                      </div>
                    </div>
                    <div class="review-rating">
                      <i v-for="n in 5" :key="n" :class="n <= review.rating ? 'fas fa-star' : 'far fa-star'"></i>
                    </div>
                  </div>
                  <div class="review-content">
                    <p>{{ review.content }}</p>
                  </div>
                  <div class="review-helpful">
                    <button class="helpful-btn" @click="toggleHelpful(review.id)">
                      <i class="far fa-thumbs-up"></i>
                      有帮助 ({{ review.helpfulCount }})
                    </button>
                  </div>
                </div>
              </div>

              <div class="load-more-reviews" v-if="showLoadMore">
                <button class="btn btn-outline" @click="loadMoreReviews">
                  加载更多评价
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'CourseDetail',
  props: ['id'],
  data() {
    return {
      activeTab: 'overview',
      expandedModule: 0,
      course: null,
      wishlist: [],
      selectedReviewFilter: 'all',
      reviewFilters: [
        { label: '全部', value: 'all' },
        { label: '5星', value: 5 },
        { label: '4星', value: 4 },
        { label: '3星', value: 3 },
        { label: '2星', value: 2 },
        { label: '1星', value: 1 }
      ],
      displayedReviews: 5
    }
  },
  computed: {
    ...mapState(['quizProgress']),
    totalVideos() {
      return this.course?.modules.reduce((total, module) => total + module.lessons.length, 0) || 0
    },
    totalQuizzes() {
      return this.course?.modules.reduce((total, module) => total + module.quizzes.length, 0) || 0
    },
    totalDuration() {
      return this.course?.duration || '0小时'
    },
    isInWishlist() {
      return this.wishlist.includes(this.course?.id)
    },
    filteredReviews() {
      if (!this.course?.reviews) return []
      
      let reviews = this.course.reviews
      
      // 按评分筛选
      if (this.selectedReviewFilter !== 'all') {
        reviews = reviews.filter(review => review.rating === this.selectedReviewFilter)
      }
      
      // 限制显示数量
      return reviews.slice(0, this.displayedReviews)
    },
    showLoadMore() {
      return this.course?.reviews && this.displayedReviews < this.course.reviews.length
    }
  },
  created() {
    this.loadCourse()
    this.loadWishlist()
  },
  methods: {
    loadCourse() {
      // 模拟课程数据加载
      const courses = {
        1: {
          id: 1,
          title: '机器学习入门',
          subtitle: '从零开始学习机器学习基础概念和算法',
          description: '本课程将广泛介绍机器学习、数据挖掘和统计模式识别。您将学习分析和理解大型数据集的方法；不仅学习理论基础，还将获得快速强大地将这些技术应用于新问题的实践知识。最后，您将学习从大规模数据集中提取和识别有用特征的主要技术。',
          price: 0,
          originalPrice: 399,
          rating: 4.8,
          ratingCount: 12345,
          studentCount: 256789,
          duration: '15 小时',
          lastUpdated: '2023年10月',
          downloadableResources: 12,
          image: 'https://images.unsplash.com/photo-1555255707-c07966088b7b?w=800&h=400&fit=crop',
          thumbnail: 'https://images.unsplash.com/photo-1555255707-c07966088b7b?w=400&h=225&fit=crop',
          learningObjectives: [
            '理解机器学习的基本概念和术语',
            '掌握监督学习和无监督学习的核心算法',
            '学会使用Python实现机器学习模型',
            '掌握模型评估和优化的方法',
            '了解神经网络和深度学习的基础知识',
            '能够将机器学习技术应用于实际问题'
          ],
          targetAudience: '本课程适合对机器学习感兴趣的初学者，需要具备基本的编程知识和高中数学基础。不需要预先的机器学习经验。',
          targetAudienceList: [
            '对人工智能和机器学习感兴趣的初学者',
            '希望转行数据科学领域的专业人士',
            '计算机科学或相关专业的学生',
            '希望了解机器学习基础的产品经理'
          ],
          prerequisites: [
            '基本的编程知识（任何语言）',
            '高中数学基础（代数、概率）',
            '不需要预先的机器学习经验',
            '建议具备基本的Python知识'
          ],
          instructor: {
            id: 'andrew-ng',
            name: 'Andrew Ng',
            title: '斯坦福大学计算机科学教授',
            rating: 4.8,
            studentCount: 1234567,
            courseCount: 15,
            reviewCount: 89432,
            bio: [
              'Andrew Ng是斯坦福大学计算机科学系的副教授。他曾在百度担任首席科学家，领导该公司的人工智能团队。他还是Coursera的联合创始人和深度学习教育平台的创始人。',
              '他的机器学习课程是Coursera上最受欢迎的课程之一，已经有数百万学生参与学习。他在机器学习和人工智能领域发表了大量研究论文，是该领域的知名专家。',
              'Andrew Ng在机器学习、深度学习和人工智能领域有着深厚的研究背景，他的工作对现代人工智能的发展产生了深远影响。'
            ],
            expertise: ['机器学习', '深度学习', '人工智能', '计算机视觉', '自然语言处理'],
            avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face'
          },
          ratingDistribution: {
            5: 75,
            4: 18,
            3: 5,
            2: 1,
            1: 1
          },
          modules: [
            {
              title: '第1周：机器学习简介',
              duration: '2小时',
              lessons: [
                { 
                  id: '1-1', 
                  title: '1.1 什么是机器学习 - 机器学习基础概念介绍',
                  duration: '15分钟',
                  isPreview: true
                },
                { 
                  id: '1-2', 
                  title: '1.2 监督学习与非监督学习',
                  duration: '20分钟',
                  isPreview: false
                },
                { 
                  id: '1-3', 
                  title: '1.3 机器学习应用案例',
                  duration: '25分钟',
                  isPreview: false
                }
              ],
              quizzes: [
                { id: 'quiz-1', title: '测验1：机器学习基础概念' }
              ]
            },
            {
              title: '第2周：线性回归',
              duration: '3小时',
              lessons: [
                { 
                  id: '2-1', 
                  title: '2.1 线性回归基础',
                  duration: '30分钟',
                  isPreview: true
                },
                { 
                  id: '2-2', 
                  title: '2.2 梯度下降算法',
                  duration: '45分钟',
                  isPreview: false
                },
                { 
                  id: '2-3', 
                  title: '2.3 多元线性回归',
                  duration: '35分钟',
                  isPreview: false
                }
              ],
              quizzes: [
                { id: 'quiz-2', title: '测验2：线性回归' }
              ]
            },
            {
              title: '第3周：逻辑回归与分类',
              duration: '4小时',
              lessons: [
                { 
                  id: '3-1', 
                  title: '3.1 逻辑回归原理',
                  duration: '40分钟',
                  isPreview: false
                },
                { 
                  id: '3-2', 
                  title: '3.2 分类问题实践',
                  duration: '50分钟',
                  isPreview: false
                }
              ],
              quizzes: [
                { id: 'quiz-3', title: '测验3：分类算法' }
              ]
            }
          ],
          reviews: [
            {
              id: 1,
              userId: 'zhangsan',
              userName: '张三',
              date: '2023年10月15日',
              rating: 5,
              content: '这门课程非常棒！Andrew教授的讲解非常清晰，让我对机器学习有了全面的理解。课程内容安排合理，从基础概念到实际应用都有涉及。强烈推荐给所有对机器学习感兴趣的人！',
              helpfulCount: 124
            },
            {
              id: 2,
              userId: 'lisi',
              userName: '李四',
              date: '2023年9月28日',
              rating: 4,
              content: '课程内容很扎实，特别是编程作业很有挑战性但也很有收获。唯一的小缺点是有些数学推导部分可能对没有相关背景的同学来说有点困难，但整体来说是一门非常优秀的课程。',
              helpfulCount: 89
            },
            {
              id: 3,
              userId: 'wangwu',
              userName: '王五',
              date: '2023年9月15日',
              rating: 5,
              content: '作为转行数据科学的学习者，这门课程给了我很大的帮助。从零基础开始学习，现在能够理解并实现基本的机器学习算法了。感谢Andrew教授的精彩讲解！',
              helpfulCount: 67
            },
            {
              id: 4,
              userId: 'zhaoliu',
              userName: '赵六',
              date: '2023年8月20日',
              rating: 4,
              content: '课程质量很高，配套的编程练习很有价值。建议在学习前先复习一下线性代数和概率论的基础知识，这样学习起来会更顺畅。',
              helpfulCount: 45
            },
            {
              id: 5,
              userId: 'qianqi',
              userName: '钱七',
              date: '2023年8月5日',
              rating: 5,
              content: '这是我学过的最好的在线课程之一！教授讲解深入浅出，课程结构设计合理，作业和测验能够很好地巩固所学知识。已经推荐给很多朋友了！',
              helpfulCount: 156
            }
          ]
        }
      }
      
      this.course = courses[this.id] || courses[1]
    },
    loadWishlist() {
      this.wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]')
    },
    toggleModule(index) {
      this.expandedModule = this.expandedModule === index ? null : index
    },
    navigateToVideoPlayer(lesson) {
      this.$router.push(`/video/${this.course.id}/${lesson.id}`)
    },
    navigateToQuiz(quiz) {
      this.$router.push(`/quiz/${this.course.id}/${quiz.id}`)
    },
    navigateToInstructor(instructorId) {
      this.$router.push(`/user/${instructorId}`)
    },
    navigateToUser(userId) {
      this.$router.push(`/user/${userId}`)
    },
    getStarClass(n) {
      const rating = this.course.rating
      if (n <= Math.floor(rating)) return 'fas fa-star'
      if (n === Math.ceil(rating) && rating % 1 >= 0.5) return 'fas fa-star-half-alt'
      return 'far fa-star'
    },
    getQuizProgress(quiz) {
      return this.quizProgress[quiz.id] || 0
    },
    getQuizProgressText(quiz) {
      const progress = this.getQuizProgress(quiz)
      return progress === 0 ? '未开始' : progress === 100 ? '已完成' : `${progress}%`
    },
    enrollCourse() {
      this.$notify({
        type: 'success',
        title: '注册成功',
        message: '您已成功注册该课程！开始您的学习之旅吧！'
      })
    },
    toggleWishlist() {
      if (this.isInWishlist) {
        this.wishlist = this.wishlist.filter(id => id !== this.course.id)
        this.$notify({
          type: 'success',
          title: '取消收藏',
          message: '课程已从收藏列表中移除'
        })
      } else {
        this.wishlist.push(this.course.id)
        this.$notify({
          type: 'success',
          title: '收藏成功',
          message: '课程已添加到收藏列表'
        })
      }
      localStorage.setItem('wishlist', JSON.stringify(this.wishlist))
    },
    shareCourse() {
      if (navigator.share) {
        navigator.share({
          title: this.course.title,
          text: this.course.subtitle,
          url: window.location.href
        })
      } else {
        navigator.clipboard.writeText(window.location.href)
        this.$notify({
          type: 'success',
          title: '分享成功',
          message: '课程链接已复制到剪贴板！'
        })
      }
    },
    formatStudentCount(count) {
      if (count >= 10000) {
        return (count / 10000).toFixed(1) + '万'
      }
      return count.toString()
    },
    handleImageError(event) {
      event.target.src = 'https://images.unsplash.com/photo-1496171367470-9ed9a91ea931?w=800&h=400&fit=crop'
    },
    handleThumbnailError(event) {
      event.target.src = 'https://images.unsplash.com/photo-1496171367470-9ed9a91ea931?w=400&h=225&fit=crop'
    },
    handleAvatarError(event) {
      // 使用 Font Awesome 图标作为头像备用
      event.target.style.display = 'none'
      const icon = document.createElement('i')
      icon.className = 'fas fa-user-tie'
      event.target.parentNode.appendChild(icon)
    },
    toggleHelpful(reviewId) {
      this.$notify({
        type: 'info',
        title: '感谢反馈',
        message: '您的反馈已记录'
      })
    },
    loadMoreReviews() {
      this.displayedReviews += 5
    }
  }
}
</script>

<style scoped>
.course-detail {
  padding: 20px 0 40px;
}

.breadcrumb {
  margin-bottom: 20px;
  color: var(--text-light);
  font-size: 0.9rem;
}

.breadcrumb a {
  color: var(--primary);
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.course-hero {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

.course-main-info h1 {
  font-size: 2.2rem;
  margin-bottom: 10px;
  color: var(--text);
}

.course-subtitle {
  font-size: 1.2rem;
  color: var(--text-light);
  margin-bottom: 25px;
}

/* 课程主图片 */
.course-image-main {
  margin: 20px 0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.main-course-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  transition: transform 0.3s;
}

.course-image-main:hover .main-course-image {
  transform: scale(1.02);
}

.course-meta {
  margin-bottom: 25px;
}

.instructor-info {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.instructor-info:hover {
  opacity: 0.8;
}

.instructor-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(--secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  color: var(--primary);
  font-size: 1.2rem;
  overflow: hidden;
}

.instructor-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.instructor-avatar.large {
  width: 80px;
  height: 80px;
  font-size: 2rem;
}

.instructor-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.instructor-title {
  color: var(--text-light);
  font-size: 0.9rem;
}

.course-stats {
  display: flex;
  gap: 20px;
}

.course-stats .stat {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-light);
}

.course-actions {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.btn-enroll {
  padding: 12px 30px;
  font-size: 1.1rem;
}

.course-preview {
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  position: sticky;
  top: 20px;
}

.preview-video {
  height: 200px;
  background: #000;
  position: relative;
  cursor: pointer;
}

.video-placeholder {
  height: 100%;
  position: relative;
}

.preview-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
  transition: background 0.3s;
}

.preview-video:hover .play-overlay {
  background: rgba(0, 0, 0, 0.7);
}

.play-overlay i {
  font-size: 3rem;
  margin-bottom: 10px;
  opacity: 0.9;
}

.play-overlay p {
  margin: 0;
  font-size: 1rem;
}

.preview-info {
  padding: 25px;
}

.price-info {
  margin-bottom: 20px;
  position: relative;
}

.current-price {
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--primary);
  margin-right: 10px;
}

.original-price {
  font-size: 1.1rem;
  color: var(--text-light);
  text-decoration: line-through;
}

.free-badge {
  display: inline-block;
  background: var(--success);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  margin-left: 10px;
}

.preview-features {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.feature {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text);
}

.feature i {
  color: var(--primary);
  width: 20px;
}

.enrollment-stats {
  border-top: 1px solid var(--border);
  padding-top: 20px;
}

.enrollment-count, .last-updated {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 0.9rem;
  color: var(--text-light);
}

/* 内容导航 */
.content-nav {
  display: flex;
  border-bottom: 1px solid var(--border);
  margin-bottom: 30px;
}

.nav-item {
  padding: 15px 25px;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  font-weight: 500;
  transition: all 0.3s;
}

.nav-item.active {
  border-bottom-color: var(--primary);
  color: var(--primary);
}

.nav-item:hover {
  color: var(--primary);
}

/* 内容面板 */
.content-panel {
  display: none;
}

.content-panel.active {
  display: block;
}

.panel-content h2 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: var(--text);
}

.panel-content h3 {
  font-size: 1.4rem;
  margin: 30px 0 15px;
  color: var(--text);
}

.learning-objectives {
  list-style: none;
  margin-bottom: 30px;
}

.learning-objectives li {
  padding: 8px 0;
  padding-left: 30px;
  position: relative;
  line-height: 1.6;
}

.learning-objectives li i {
  position: absolute;
  left: 0;
  color: var(--success);
  font-size: 1.1rem;
}

.course-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 25px 0;
}

.feature-card {
  text-align: center;
  padding: 25px 15px;
  background: var(--secondary);
  border-radius: 8px;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card i {
  font-size: 2.2rem;
  color: var(--primary);
  margin-bottom: 15px;
}

.feature-card h4 {
  margin-bottom: 10px;
  color: var(--text);
}

.feature-card p {
  color: var(--text-light);
  font-size: 0.9rem;
  margin: 0;
}

.target-audience {
  margin-bottom: 30px;
}

.audience-list {
  list-style: none;
  margin-top: 15px;
}

.audience-list li {
  padding: 8px 0;
  padding-left: 30px;
  position: relative;
}

.audience-list li i {
  position: absolute;
  left: 0;
  color: var(--primary);
}

.prerequisites {
  margin-bottom: 30px;
}

.prerequisites-list {
  list-style: none;
}

.prerequisites-list li {
  padding: 8px 0;
  padding-left: 30px;
  position: relative;
}

.prerequisites-list li i {
  position: absolute;
  left: 0;
  color: var(--warning);
}

/* 课程大纲 */
.curriculum-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin: 25px 0;
}

.curriculum-stat {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background: var(--secondary);
  border-radius: 8px;
  font-weight: 500;
}

.curriculum-stat i {
  color: var(--primary);
  font-size: 1.2rem;
}

.modules {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.module {
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}

.module-header {
  background: var(--secondary);
  padding: 20px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.3s;
}

.module-header:hover {
  background: #f0f0f0;
}

.module-title h3 {
  margin: 0 0 5px 0;
  font-size: 1.2rem;
}

.module-meta {
  color: var(--text-light);
  font-size: 0.9rem;
}

.module-toggle i {
  color: var(--text-light);
  transition: transform 0.3s;
}

.module-content {
  padding: 0 20px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.module-content.expanded {
  max-height: 1000px;
  padding: 20px;
}

.lesson {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background 0.3s;
}

.lesson:hover {
  background: var(--secondary);
}

.lesson:last-child {
  border-bottom: none;
}

.lesson-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.lesson-info i {
  color: var(--primary);
  width: 20px;
}

.lesson-details {
  display: flex;
  align-items: center;
  gap: 10px;
}

.lesson-preview {
  background: var(--primary);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 500;
}

.lesson-duration {
  color: var(--text-light);
  font-size: 0.9rem;
}

.quiz-progress {
  display: flex;
  align-items: center;
  gap: 10px;
}

.progress-bar {
  width: 80px;
  height: 6px;
  background: var(--border);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--primary);
  border-radius: 3px;
  transition: width 0.3s;
}

.progress-text {
  font-size: 0.8rem;
  color: var(--text-light);
  min-width: 50px;
}

/* 讲师详情 */
.instructor-detail {
  background: var(--secondary);
  padding: 30px;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.3s;
}

.instructor-detail:hover {
  transform: translateY(-2px);
}

.instructor-main {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.instructor-bio {
  flex: 1;
}

.instructor-bio h3 {
  margin: 0 0 8px;
  font-size: 1.5rem;
}

.instructor-stats {
  display: flex;
  gap: 30px;
  margin-top: 15px;
}

.instructor-stats .stat {
  text-align: center;
}

.instructor-stats .stat strong {
  display: block;
  font-size: 1.5rem;
  color: var(--primary);
}

.instructor-stats .stat span {
  font-size: 0.9rem;
  color: var(--text-light);
}

.instructor-description p {
  margin-bottom: 15px;
  line-height: 1.6;
}

.instructor-expertise {
  margin-top: 20px;
}

.instructor-expertise h4 {
  margin-bottom: 10px;
  color: var(--text);
}

.expertise-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.expertise-tag {
  background: var(--primary);
  color: white;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 500;
}

/* 评价样式 */
.reviews-summary {
  background: var(--secondary);
  padding: 25px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.rating-overview {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 30px;
  align-items: center;
}

.average-rating {
  text-align: center;
}

.rating-number {
  font-size: 3rem;
  font-weight: bold;
  color: var(--primary);
  margin-bottom: 8px;
}

.rating-stars {
  margin-bottom: 8px;
  color: var(--warning);
}

.rating-count {
  color: var(--text-light);
}

.rating-distribution {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.distribution-bar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.distribution-bar span:first-child {
  width: 30px;
  font-size: 0.9rem;
}

.distribution-bar span:last-child {
  width: 35px;
  font-size: 0.9rem;
  color: var(--text-light);
}

.bar {
  flex: 1;
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.fill {
  height: 100%;
  background: var(--warning);
  border-radius: 4px;
}

.reviews-filter {
  display: flex;
  gap: 10px;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 8px 16px;
  border: 1px solid var(--border);
  background: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
  color: var(--text-light);
}

.filter-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.filter-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.review {
  background: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.reviewer {
  display: flex;
  align-items: center;
  gap: 12px;
}

.reviewer-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
}

.reviewer-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.review-date {
  font-size: 0.9rem;
  color: var(--text-light);
}

.review-rating {
  color: var(--warning);
}

.review-content p {
  line-height: 1.6;
  margin: 0 0 15px 0;
}

.review-helpful {
  border-top: 1px solid var(--border);
  padding-top: 15px;
}

.helpful-btn {
  background: none;
  border: none;
  color: var(--text-light);
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: color 0.3s;
}

.helpful-btn:hover {
  color: var(--primary);
}

.load-more-reviews {
  text-align: center;
  margin-top: 30px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .course-hero {
    grid-template-columns: 1fr;
    gap: 25px;
  }
  
  .course-main-info h1 {
    font-size: 1.8rem;
  }
  
  .main-course-image {
    height: 200px;
  }
  
  .content-nav {
    flex-wrap: wrap;
  }
  
  .nav-item {
    flex: 1;
    min-width: 120px;
    text-align: center;
    padding: 12px 15px;
  }
  
  .rating-overview {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .course-actions {
    justify-content: center;
  }
  
  .instructor-main {
    flex-direction: column;
    text-align: center;
  }
  
  .instructor-avatar {
    margin-right: 0;
    margin-bottom: 15px;
  }
  
  .instructor-stats {
    justify-content: center;
  }
  
  .course-stats {
    flex-direction: column;
    gap: 10px;
  }
  
  .preview-features {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .course-detail {
    padding: 10px 0 20px;
  }
  
  .course-main-info, .panel-content {
    padding: 0 10px;
  }
  
  .course-main-info h1 {
    font-size: 1.5rem;
  }
  
  .course-subtitle {
    font-size: 1rem;
  }
  
  .main-course-image {
    height: 150px;
  }
  
  .course-actions {
    flex-direction: column;
  }
  
  .btn-enroll {
    width: 100%;
  }
  
  .module-header {
    padding: 15px;
  }
  
  .lesson {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .lesson-duration {
    align-self: flex-end;
  }
}
</style>