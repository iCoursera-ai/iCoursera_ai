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
            
            <div class="course-meta">
              <div class="instructor-info" @click="navigateToInstructor(course.instructor.id)">
                <div class="instructor-avatar">
                  <i class="fas fa-user-tie"></i>
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
                <i class="fas fa-play-circle"></i>
                <p>课程预览视频</p>
              </div>
            </div>
            <div class="preview-info">
              <div class="price-info">
                <span class="current-price">{{ course.price === 0 ? '免费' : `¥${course.price}` }}</span>
                <span v-if="course.originalPrice" class="original-price">¥{{ course.originalPrice }}</span>
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
              </div>
              
              <h3>适合人群</h3>
              <p>{{ course.targetAudience }}</p>
            </div>
          </div>
          
          <!-- 课程内容面板 -->
          <div class="content-panel" :class="{ active: activeTab === 'curriculum' }">
            <div class="panel-content">
              <h2>课程大纲</h2>
              <p>本课程包含{{ course.modules.length }}个模块，共{{ totalVideos }}个视频和{{ totalQuizzes }}个测验。</p>
              
              <div class="modules">
                <div 
                  v-for="(module, moduleIndex) in course.modules" 
                  :key="moduleIndex"
                  class="module"
                >
                  <div class="module-header" @click="toggleModule(moduleIndex)">
                    <h3>{{ module.title }}</h3>
                    <span>{{ module.lessons.length }}个视频 • {{ module.quizzes.length }}个测验 • {{ module.duration }}</span>
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
                        <span>{{ lesson.title }}</span>
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
                        <span>{{ quiz.title }}</span>
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
                    <i class="fas fa-user-tie"></i>
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
                        <strong>{{ course.instructor.studentCount }}</strong>
                        <span>学生人数</span>
                      </div>
                      <div class="stat">
                        <strong>{{ course.instructor.courseCount }}</strong>
                        <span>课程数量</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="instructor-description">
                  <p v-for="(paragraph, index) in course.instructor.bio" :key="index">
                    {{ paragraph }}
                  </p>
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
              
              <div class="reviews-list">
                <div v-for="review in course.reviews" :key="review.id" class="review">
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
                </div>
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
      wishlist: []
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
    isInWishlist() {
      return this.wishlist.includes(this.course?.id)
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
          learningObjectives: [
            '理解机器学习的基本概念和术语',
            '掌握监督学习和无监督学习的核心算法',
            '学会使用Python实现机器学习模型',
            '掌握模型评估和优化的方法',
            '了解神经网络和深度学习的基础知识',
            '能够将机器学习技术应用于实际问题'
          ],
          targetAudience: '本课程适合对机器学习感兴趣的初学者，需要具备基本的编程知识和高中数学基础。不需要预先的机器学习经验。',
          instructor: {
            id: 'andrew-ng',
            name: 'Andrew Ng',
            title: '斯坦福大学计算机科学教授',
            rating: 4.8,
            studentCount: 1234567,
            courseCount: 15,
            bio: [
              'Andrew Ng是斯坦福大学计算机科学系的副教授。他曾在百度担任首席科学家，领导该公司的人工智能团队。他还是Coursera的联合创始人和深度学习教育平台的创始人。',
              '他的机器学习课程是Coursera上最受欢迎的课程之一，已经有数百万学生参与学习。他在机器学习和人工智能领域发表了大量研究论文，是该领域的知名专家。'
            ]
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
                { id: '1-1', title: '1.1 什么是机器学习', duration: '15分钟' },
                { id: '1-2', title: '1.2 监督学习与非监督学习', duration: '20分钟' },
                { id: '1-3', title: '1.3 机器学习应用案例', duration: '25分钟' }
              ],
              quizzes: [
                { id: 'quiz-1', title: '测验1：机器学习基础概念' }
              ]
            },
            {
              title: '第2周：线性回归',
              duration: '3小时',
              lessons: [
                { id: '2-1', title: '2.1 线性回归基础', duration: '30分钟' },
                { id: '2-2', title: '2.2 梯度下降算法', duration: '45分钟' },
                { id: '2-3', title: '2.3 多元线性回归', duration: '35分钟' }
              ],
              quizzes: [
                { id: 'quiz-2', title: '测验2：线性回归' }
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
              content: '这门课程非常棒！Andrew教授的讲解非常清晰，让我对机器学习有了全面的理解。课程内容安排合理，从基础概念到实际应用都有涉及。强烈推荐给所有对机器学习感兴趣的人！'
            },
            {
              id: 2,
              userId: 'lisi',
              userName: '李四',
              date: '2023年9月28日',
              rating: 4,
              content: '课程内容很扎实，特别是编程作业很有挑战性但也很有收获。唯一的小缺点是有些数学推导部分可能对没有相关背景的同学来说有点困难，但整体来说是一门非常优秀的课程。'
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
      alert('课程注册成功！开始您的学习之旅吧！')
    },
    toggleWishlist() {
      if (this.isInWishlist) {
        this.wishlist = this.wishlist.filter(id => id !== this.course.id)
      } else {
        this.wishlist.push(this.course.id)
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
        alert('课程链接已复制到剪贴板！')
      }
    }
  }
}
</script>