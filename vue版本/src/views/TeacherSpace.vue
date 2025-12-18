<template>
  <div class="min-h-screen bg-gray-100">
    <Header />
    
    <div class="container mx-auto px-4 py-8">
      <div class="bg-white rounded-lg shadow-md p-6">
        <h1 class="text-2xl font-bold mb-6">老师空间</h1>
        
        <!-- 教师信息头部 -->
        <div class="flex items-center mb-8">
          <div class="relative">
            <div class="w-24 h-24 rounded-full overflow-hidden border-4 border-white shadow-sm">
              <!-- 使用默认头像或实际头像 -->
              <div v-if="!teacher.avatar || teacher.avatar === '👤'" 
                   class="w-full h-full bg-gradient-to-br from-blue-400 to-purple-600 flex items-center justify-center text-white text-3xl">
                {{ getInitials(teacher.name) }}
              </div>
              <img v-else :src="teacher.avatar" :alt="teacher.name" class="w-full h-full object-cover">
            </div>
          </div>
          <div class="ml-6">
            <h2 class="text-2xl font-bold text-dark mb-2">{{ teacher.name }}</h2>
            <div class="flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-secondary">
              <div class="flex items-center gap-1">
                <i class="fa fa-graduation-cap text-primary"></i>
                <span>{{ teacher.department || '未设置学院' }}</span>
              </div>
              <div class="flex items-center gap-1">
                <i class="fa fa-user-plus text-green-500"></i>
                <button 
                  @click.stop="toggleFollowTeacher"
                  class="px-3 py-1 text-xs rounded-full transition-colors"
                  :class="isFollowingTeacher ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600 hover:bg-blue-50 hover:text-blue-600'"
                >
                  {{ isFollowingTeacher ? '已关注' : '关注' }}
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="text-gray-700 mb-8 p-4 bg-gray-50 rounded-lg">
          <h3 class="font-semibold text-dark mb-2">教师简介</h3>
          <p>{{ teacher.description || '这位老师还没有填写个人简介' }}</p>
        </div>
        
        <!-- 课程区域 -->
        <div class="mt-8">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-lg font-semibold text-dark">
              老师的课程 ({{ displayedCourses.length }})
            </h3>
            
            <!-- 查看更多/收起按钮 -->
            <button 
              v-if="teacherCourses.length > initialCourseCount"
              class="text-link text-sm hover:underline flex items-center gap-1 px-3 py-1.5 rounded-md hover:bg-blue-50 transition-colors"
              @click="toggleExpandCourses"
            >
              {{ showAllCourses ? '收起课程' : `查看更多 (${teacherCourses.length - initialCourseCount}个课程)` }}
              <i class="fa" :class="showAllCourses ? 'fa-angle-up' : 'fa-angle-down'"></i>
            </button>
          </div>
          
          <!-- 空状态 -->
          <div v-if="displayedCourses.length === 0" class="text-center py-12 bg-gray-50 rounded-lg">
            <i class="fa fa-video-slash text-4xl text-gray-300 mb-4"></i>
            <p class="text-gray-500 mb-4">该老师暂无课程</p>
          </div>
          
          <!-- 课程网格 -->
          <div 
            v-else
            class="grid gap-6 transition-all duration-300"
            :class="gridColsClass"
          >
            <!-- 课程卡片 -->
            <div 
              v-for="course in displayedCourses" 
              :key="course.id"
              class="bg-white rounded-xl overflow-hidden cursor-pointer hover:shadow-xl transition-all duration-300 group video-card border border-gray-100"
              @click="goToVideoPlayer(course)"
            >
              <!-- 视频封面 -->
              <div class="relative" style="aspect-ratio: 16/9;">
                <!-- 使用真实课程图片 -->
                <div class="w-full h-full relative">
                  <img :src="course.image" :alt="course.title" 
                       class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                  
                  <!-- 播放按钮 -->
                  <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/30">
                    <div class="w-16 h-16 rounded-full bg-white/30 backdrop-blur-sm flex items-center justify-center">
                      <i class="fa fa-play text-white text-2xl"></i>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 课程信息 -->
              <div class="p-4">
                <h4 class="text-base font-semibold line-clamp-2 group-hover:text-primary transition-colors">
                  {{ course.title }}
                </h4>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 返回按钮 -->
        <div class="mt-8 pt-6 border-t border-gray-200">
          <button @click="goBack" class="px-6 py-2.5 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-200 shadow-sm">
            <i class="fa fa-arrow-left mr-2"></i>返回上一页
          </button>
        </div>
      </div>
    </div>
    
    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { useRoute, useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'TeacherSpace',
  components: {
    Header,
    Footer
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // 从本地存储获取老师信息
    const teacher = ref(JSON.parse(localStorage.getItem('currentTeacherInfo') || '{}'))
    
    // 关注状态
    const isFollowingTeacher = ref(false)
    
    // 检查是否已关注该老师
    const checkFollowStatus = () => {
      const currentUser = JSON.parse(localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser') || '{}')
      const userId = currentUser.userId || currentUser.email || 'default'
      const userSpecificKey = `userFollowedTeachers_${userId}`
      const followedTeachers = JSON.parse(localStorage.getItem(userSpecificKey) || '[]')
      
      isFollowingTeacher.value = followedTeachers.some(t => t.userId === teacher.value.userId)
    }
    
    // 关注/取消关注老师
    const toggleFollowTeacher = () => {
      const currentUser = JSON.parse(localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser') || '{}')
      const userId = currentUser.userId || currentUser.email || 'default'
      const userSpecificKey = `userFollowedTeachers_${userId}`
      const followedTeachers = JSON.parse(localStorage.getItem(userSpecificKey) || '[]')
      
      if (isFollowingTeacher.value) {
        // 取消关注
        const updatedTeachers = followedTeachers.filter(t => t.userId !== teacher.value.userId)
        localStorage.setItem(userSpecificKey, JSON.stringify(updatedTeachers))
        isFollowingTeacher.value = false
      } else {
        // 关注
        const teacherData = {
          id: Date.now(),
          userId: teacher.value.userId,
          name: teacher.value.name,
          department: teacher.value.department,
          avatar: teacher.value.avatar,
          description: teacher.value.description,
          followedAt: new Date().toISOString().split('T')[0]
        }
        
        followedTeachers.push(teacherData)
        localStorage.setItem(userSpecificKey, JSON.stringify(followedTeachers))
        isFollowingTeacher.value = true
      }
      
      window.dispatchEvent(new CustomEvent('followUpdated'))
    }
    
    // 获取姓名首字母
    const getInitials = (name) => {
      if (!name) return '教'
      const chineseName = name.trim()
      if (chineseName.length >= 2) {
        return chineseName.substring(0, 2)
      }
      return chineseName || '教'
    }
    
    // 跳转到视频播放页面
    const goToVideoPlayer = (course) => {
      // 准备课程数据
      const courseData = {
        id: course.id,
        name: course.title,
        title: course.title,
        description: `${course.title} - 由${teacher.value.name}主讲`,
        category: course.category,
        teacher: teacher.value.name,
        image: course.image
      }
      
      // 保存课程数据到localStorage
      localStorage.setItem('selectedCourse', JSON.stringify(courseData))
      
      // 跳转到视频播放页面
      router.push({
        name: 'VideoPlayer',
        params: { 
          courseId: course.id 
        },
        query: {
          teacher: teacher.value.name,
          category: course.category,
          fromTeacherSpace: 'true'
        }
      })
    }
    
    const goBack = () => {
      router.go(-1)
    }
    
    return {
      teacher,
      goBack,
      goToVideoPlayer,
      getInitials,
      isFollowingTeacher,
      toggleFollowTeacher,
      checkFollowStatus
    }
  },
  data() {
    return {
      showAllCourses: false,
      initialCourseCount: 8,
      teacherCourses: [],
      allCoursesData: []
    }
  },
  computed: {
    // 直接显示所有课程
    displayedCourses() {
      if (this.showAllCourses) {
        return this.teacherCourses
      }
      return this.teacherCourses.slice(0, this.initialCourseCount)
    },
    
    // 移除所有统计计算属性
    gridColsClass() {
      const baseClass = 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
      if (this.showAllCourses) {
        return baseClass
      }
      return `${baseClass} max-h-[600px] overflow-hidden`
    }
  },
  mounted() {
    this.loadAllCourses()
    this.loadTeacherCourses()
    this.checkFollowStatus()
  },
  methods: {
    toggleExpandCourses() {
      this.showAllCourses = !this.showAllCourses
    },
    
    // 加载所有课程数据
    async loadAllCourses() {
      try {
        // 尝试从localStorage获取课程数据
        const savedCourses = localStorage.getItem('allCourses')
        if (savedCourses) {
          this.allCoursesData = JSON.parse(savedCourses)
        } else {
          // 如果没有保存的数据，生成新的课程数据
          this.allCoursesData = this.generateAllCourses()
          // 保存到localStorage供下次使用
          localStorage.setItem('allCourses', JSON.stringify(this.allCoursesData))
        }
      } catch (error) {
        console.error('加载课程数据失败:', error)
        this.allCoursesData = this.generateAllCourses()
      }
    },
    
    // 加载老师课程
    loadTeacherCourses() {
      const teacherName = this.teacher.name
      
      if (!teacherName) {
        console.warn('没有老师信息，无法加载课程')
        this.teacherCourses = []
        return
      }
      
      try {
        // 从所有课程数据中筛选出该老师的课程（去重）
        this.teacherCourses = this.getTeacherCoursesFromData(teacherName)
      } catch (error) {
        console.error('加载老师课程失败:', error)
        this.teacherCourses = []
      }
    },
    
    // 从数据中获取老师课程（去重）
    getTeacherCoursesFromData(teacherName) {
      if (!teacherName || this.allCoursesData.length === 0) {
        return []
      }
      
      // 1. 筛选出该老师的课程
      const teacherCourses = this.allCoursesData.filter(course => 
        course.teacher && course.teacher.includes(teacherName)
      )
      
      // 2. 去重：同名课程只保留第一个
      const uniqueCourses = []
      const seenTitles = new Set()
      
      teacherCourses.forEach(course => {
        if (!seenTitles.has(course.title)) {
          seenTitles.add(course.title)
          uniqueCourses.push(course)
        }
      })
      
      return uniqueCourses
    },
    
    // 生成所有课程数据（简化版）
    generateAllCourses() {
      // 教师映射
      const teachers = {
        computer: ['张老师', '李教授', '王工程师', '刘老师', '陈教授', '赵导师'],
        business: ['李经理', '王总监', '张营销总监', '陈财务顾问', '刘HR总监'],
        design: ['张设计师', '李创意总监', '王视频制作人', '陈3D艺术家', '刘品牌设计师']
      }

      // 课程标题库
      const courseTitles = {
        computer: [
          'Python入门教程', 'Java基础编程', 'HTML/CSS网页设计', 'Spring Boot企业级开发', 
          'React Hooks深度解析', 'TypeScript高级技巧', 'Docker容器化实践', '微服务架构设计',
          'Redis缓存优化', 'MySQL性能调优', 'Web安全攻防实战', '深度学习实战'
        ],
        business: [
          '管理学基础', '市场营销入门', '财务管理基础', '领导力与团队管理', 
          '商业模式创新', '战略管理', '组织行为学', '人力资源管理',
          '财务报表分析', '客户关系管理', '企业战略规划', '商业分析实战'
        ],
        design: [
          'UI/UX设计从入门到精通', '平面设计创意与实战', '视频剪辑与特效制作', 
          '色彩理论与应用', '字体设计原理', '包装设计实战', 'UI交互动效',
          '品牌视觉系统', '海报设计创意', '网页设计规范', '移动端设计适配', '3D建模与动画设计'
        ]
      }

      // 生成课程数据
      const allCourses = []
      let courseId = 1
      
      // 为每个老师生成课程
      for (const category in teachers) {
        const categoryTeachers = teachers[category]
        const categoryTitles = courseTitles[category] || courseTitles.computer
        
        categoryTeachers.forEach(teacher => {
          // 每个老师有3-6个课程
          const courseCount = 3 + Math.floor(Math.random() * 3)
          
          for (let i = 0; i < courseCount; i++) {
            // 选择课程标题
            const titleIndex = (courseId - 1) % categoryTitles.length
            const title = categoryTitles[titleIndex]
            
            allCourses.push({
              id: courseId,
              title: title,
              teacher: teacher,
              category: category,
              image: `https://picsum.photos/400/225?random=${courseId + 1000}`
            })
            
            courseId++
          }
        })
      }
      
      return allCourses
    }
  }
}
</script>

<style scoped>
/* 视频卡片样式 */
.video-card {
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.video-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
}

.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

/* 查看更多按钮样式 */
.text-link {
  @apply text-blue-600 hover:text-blue-800 transition-colors duration-200;
}

/* 图片缩放效果 */
.group-hover\:scale-105 {
  transition: transform 0.3s ease;
}
</style>