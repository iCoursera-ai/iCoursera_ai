<template>
  <section class="user-profile-page" v-if="user">
    <div class="container">
      <!-- 用户头部信息 -->
      <div class="user-header">
        <div class="user-basic-info">
          <div class="user-avatar large">
            <i class="fas fa-user-tie"></i>
          </div>
          <div class="user-details">
            <h1>{{ user.name }}</h1>
            <p class="user-title">{{ user.title }}</p>
            <p class="user-location"><i class="fas fa-map-marker-alt"></i> {{ user.location }}</p>
            <div class="user-stats">
              <div class="stat">
                <strong>{{ user.stats.students }}</strong>
                <span>学生人数</span>
              </div>
              <div class="stat">
                <strong>{{ user.stats.courses }}</strong>
                <span>课程数量</span>
              </div>
              <div class="stat">
                <strong>{{ user.stats.rating }}</strong>
                <span>讲师评分</span>
              </div>
            </div>
          </div>
        </div>
        <div class="user-actions">
          <button class="btn btn-primary" @click="toggleFollow" :class="{ active: isFollowing }">
            <i class="fas fa-plus"></i> {{ isFollowing ? '已关注' : '关注' }}
          </button>
          <button class="btn btn-outline">
            <i class="fas fa-envelope"></i> 发送消息
          </button>
        </div>
      </div>

      <!-- 用户内容标签 -->
      <div class="user-content-tabs">
        <div 
          class="tab" 
          :class="{ active: activeTab === 'about' }"
          @click="activeTab = 'about'"
        >
          关于我
        </div>
        <div 
          class="tab" 
          :class="{ active: activeTab === 'courses' }"
          @click="activeTab = 'courses'"
        >
          课程
        </div>
        <div 
          class="tab" 
          :class="{ active: activeTab === 'reviews' }"
          @click="activeTab = 'reviews'"
        >
          评价
        </div>
      </div>

      <div class="user-content">
        <!-- 关于我标签页 -->
        <div class="tab-content" :class="{ active: activeTab === 'about' }">
          <div class="about-section">
            <div class="bio-section">
              <h3>个人简介</h3>
              <p v-for="(paragraph, index) in user.bio" :key="index">{{ paragraph }}</p>
            </div>

            <div class="education-section">
              <h3>教育背景</h3>
              <div v-for="(edu, index) in user.education" :key="index" class="education-item">
                <div class="edu-icon">
                  <i class="fas fa-graduation-cap"></i>
                </div>
                <div class="edu-details">
                  <h4>{{ edu.degree }}</h4>
                  <p class="edu-school">{{ edu.school }}</p>
                  <p class="edu-period">{{ edu.period }}</p>
                </div>
              </div>
            </div>

            <div class="experience-section">
              <h3>工作经历</h3>
              <div v-for="(exp, index) in user.experience" :key="index" class="experience-item">
                <div class="exp-icon">
                  <i class="fas fa-briefcase"></i>
                </div>
                <div class="exp-details">
                  <h4>{{ exp.position }}</h4>
                  <p class="exp-company">{{ exp.company }}</p>
                  <p class="exp-period">{{ exp.period }}</p>
                  <p class="exp-description">{{ exp.description }}</p>
                </div>
              </div>
            </div>

            <div class="skills-section">
              <h3>专业领域</h3>
              <div class="skills-list">
                <span v-for="skill in user.skills" :key="skill" class="skill-tag">{{ skill }}</span>
              </div>
            </div>

            <div class="contact-section">
              <h3>联系方式</h3>
              <div class="contact-info">
                <div class="contact-item">
                  <i class="fas fa-envelope"></i>
                  <span>{{ user.contact.email }}</span>
                </div>
                <div class="contact-item">
                  <i class="fas fa-globe"></i>
                  <span>{{ user.contact.website }}</span>
                </div>
                <div class="contact-item">
                  <i class="fab fa-linkedin"></i>
                  <span>{{ user.contact.linkedin }}</span>
                </div>
                <div class="contact-item">
                  <i class="fab fa-twitter"></i>
                  <span>{{ user.contact.twitter }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 课程标签页 -->
        <div class="tab-content" :class="{ active: activeTab === 'courses' }">
          <div class="courses-section">
            <h3>教授的课程</h3>
            <div class="instructor-courses">
              <div 
                v-for="course in user.courses" 
                :key="course.id"
                class="course-card"
                @click="navigateToCourse(course.id)"
              >
                <div class="course-image">
                  <img :src="course.image" :alt="course.title">
                </div>
                <div class="course-info">
                  <h4>{{ course.title }}</h4>
                  <p class="course-description">{{ course.description }}</p>
                  <div class="course-stats">
                    <span class="rating">
                      <i class="fas fa-star"></i> {{ course.rating }}
                    </span>
                    <span class="students">{{ course.students }} 名学生</span>
                  </div>
                  <div class="course-meta">
                    <span class="level">{{ getLevelText(course.level) }}</span>
                    <span class="duration">{{ course.duration }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 评价标签页 -->
        <div class="tab-content" :class="{ active: activeTab === 'reviews' }">
          <div class="reviews-section">
            <h3>学生评价</h3>
            <div class="instructor-reviews">
              <div class="review-summary">
                <div class="overall-rating">
                  <div class="rating-number">{{ user.stats.rating }}</div>
                  <div class="rating-stars">
                    <i v-for="n in 5" :key="n" :class="getStarClass(n)"></i>
                  </div>
                  <div class="rating-count">基于 {{ user.reviews.length }} 条评价</div>
                </div>
              </div>

              <div class="reviews-list">
                <div v-for="review in user.reviews" :key="review.id" class="review-item">
                  <div class="reviewer-info">
                    <div class="reviewer-avatar">
                      <i class="fas fa-user"></i>
                    </div>
                    <div>
                      <div class="reviewer-name">{{ review.userName }}</div>
                      <div class="review-date">{{ review.date }}</div>
                    </div>
                  </div>
                  <div class="review-rating">
                    <i v-for="n in 5" :key="n" :class="n <= review.rating ? 'fas fa-star' : 'far fa-star'"></i>
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
export default {
  name: 'UserProfile',
  props: ['id'],
  data() {
    return {
      activeTab: 'about',
      isFollowing: false,
      user: null
    }
  },
  created() {
    this.loadUserData()
  },
  methods: {
    loadUserData() {
      // 模拟用户数据
      const users = {
        'andrew-ng': {
          id: 'andrew-ng',
          name: 'Andrew Ng',
          title: '斯坦福大学计算机科学教授',
          location: '美国加利福尼亚州',
          avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face',
          stats: {
            students: 1234567,
            courses: 15,
            rating: 4.8
          },
          bio: [
            'Andrew Ng是斯坦福大学计算机科学系的副教授，也是人工智能领域的知名专家。他曾在百度担任首席科学家，领导该公司的人工智能团队。作为Coursera的联合创始人和深度学习教育平台的创始人，他在在线教育领域有着深远的影响。',
            '他的机器学习课程是Coursera上最受欢迎的课程之一，已经有数百万学生参与学习。他在机器学习和人工智能领域发表了大量研究论文，是该领域的权威专家。'
          ],
          education: [
            {
              degree: '博士学位 - 计算机科学',
              school: '加州大学伯克利分校',
              period: '1998年'
            },
            {
              degree: '硕士学位 - 计算机科学',
              school: '麻省理工学院',
              period: '1996年'
            }
          ],
          experience: [
            {
              position: '首席科学家',
              company: '百度',
              period: '2014年 - 2017年',
              description: '领导百度人工智能团队，负责深度学习和大数据技术研发。'
            },
            {
              position: '副教授',
              company: '斯坦福大学',
              period: '2002年 - 至今',
              description: '教授机器学习和人工智能课程，指导研究生研究项目。'
            }
          ],
          skills: ['机器学习', '深度学习', '人工智能', '数据挖掘', '神经网络', '计算机视觉', '自然语言处理'],
          contact: {
            email: 'andrew.ng@stanford.edu',
            website: 'www.andrewng.org',
            linkedin: 'linkedin.com/in/andrewng',
            twitter: '@AndrewYNg'
          },
          courses: [
            {
              id: 1,
              title: '机器学习入门',
              description: '从零开始学习机器学习基础概念和算法，涵盖监督学习、无监督学习和深度学习。',
              rating: 4.8,
              students: 256789,
              level: 'beginner',
              duration: '15小时',
              image: 'https://images.unsplash.com/photo-1555255707-c07966088b7b?w=300&h=160&fit=crop'
            },
            {
              id: 7,
              title: '深度学习专项课程',
              description: '深入学习神经网络、卷积网络、循环网络和深度学习应用。',
              rating: 4.9,
              students: 189234,
              level: 'advanced',
              duration: '45小时',
              image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=300&h=160&fit=crop'
            },
            {
              id: 12,
              title: '人工智能导论',
              description: '面向非技术背景的学习者，介绍人工智能的基本概念和应用场景。',
              rating: 4.7,
              students: 345678,
              level: 'beginner',
              duration: '12小时',
              image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=300&h=160&fit=crop'
            }
          ],
          reviews: [
            {
              id: 1,
              userName: '张三',
              date: '2023年10月15日',
              rating: 5,
              content: 'Andrew教授是我遇到过的最好的老师之一。他的讲解非常清晰，能够把复杂的概念用简单的方式表达出来。强烈推荐他的所有课程！'
            },
            {
              id: 2,
              userName: '李四',
              date: '2023年9月28日',
              rating: 4,
              content: '课程内容非常扎实，Andrew教授的知识渊博。唯一的小建议是希望有更多实际项目的指导。'
            }
          ]
        }
      }
      
      this.user = users[this.id] || users['andrew-ng']
    },
    toggleFollow() {
      this.isFollowing = !this.isFollowing
      this.$notify({
        type: 'success',
        title: this.isFollowing ? '关注成功' : '取消关注',
        message: this.isFollowing ? `您已关注 ${this.user.name}` : `您已取消关注 ${this.user.name}`
      })
    },
    navigateToCourse(courseId) {
      this.$router.push(`/course/${courseId}`)
    },
    getStarClass(n) {
      const rating = this.user.stats.rating
      if (n <= Math.floor(rating)) return 'fas fa-star'
      if (n === Math.ceil(rating) && rating % 1 >= 0.5) return 'fas fa-star-half-alt'
      return 'far fa-star'
    },
    getLevelText(level) {
      const levels = {
        'beginner': '初级',
        'intermediate': '中级',
        'advanced': '高级'
      }
      return levels[level] || level
    }
  }
}
</script>