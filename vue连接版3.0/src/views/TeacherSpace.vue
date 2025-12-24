<template>
  <div class="min-h-screen bg-gray-100">
    <Header />
    
    <div class="container mx-auto px-4 py-8">
      <!-- 加载状态 -->
      <div v-if="isLoading" class="text-center py-12">
        <i class="fa fa-spinner fa-spin text-4xl text-blue-500 mb-4"></i>
        <p class="text-gray-600">正在加载教师信息...</p>
      </div>
      
      <!-- 错误状态 -->
      <div v-else-if="loadError" class="bg-red-50 border border-red-200 rounded-lg p-6 my-6">
        <div class="flex items-center">
          <i class="fa fa-exclamation-triangle text-red-500 text-2xl mr-3"></i>
          <div>
            <h3 class="text-red-800 font-semibold">加载失败</h3>
            <p class="text-red-600 mt-1">{{ loadError }}</p>
            <button @click="loadTeacherData" class="mt-3 px-4 py-2 bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors">
              <i class="fa fa-redo mr-2"></i>重新加载
            </button>
          </div>
        </div>
      </div>
      
      <!-- 正常状态 -->
      <div v-else class="bg-white rounded-lg shadow-md p-6">
        <!-- 教师信息头部 -->
        <div class="flex items-center mb-8">
          <div class="relative">
            <div class="w-24 h-24 rounded-full overflow-hidden border-4 border-white shadow-lg bg-blue-100 flex items-center justify-center">
              <img 
                v-if="teacher.avatar" 
                :src="teacher.avatar" 
                :alt="teacher.name" 
                class="w-full h-full object-cover"
              >
              <div v-else class="text-blue-500 text-4xl">
                <i class="fa fa-user-graduate"></i>
              </div>
            </div>
            <div v-if="teacher.is_verified" class="absolute bottom-0 right-0 bg-blue-500 text-white p-1 rounded-full">
              <i class="fa fa-check text-xs"></i>
            </div>
          </div>
          <div class="ml-6 flex-1">
            <div class="flex items-center mb-2">
              <h2 class="text-2xl font-bold text-gray-800">{{ teacher.name }}</h2>
              <span v-if="teacher.title" class="ml-3 px-3 py-1 bg-blue-100 text-blue-700 text-sm rounded-full">
                {{ teacher.title }}
              </span>
            </div>
            
            <div class="flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-gray-600">
              <div class="flex items-center gap-1">
                <i class="fa fa-university text-blue-500"></i>
                <span>{{ teacher.department || '未设置院系' }}</span>
              </div>
              <div class="flex items-center gap-1">
                <i class="fa fa-users text-blue-500"></i>
                <span>粉丝: {{ teacher.followers || 0 }}</span>
              </div>
              <div class="flex items-center gap-1">
                <i class="fa fa-book text-blue-500"></i>
                <span>课程: {{ teacher.course_count || totalCourses }}</span>
              </div>
              <div class="flex items-center gap-1">
                <i class="fa fa-star text-yellow-500"></i>
                <span>评分: {{ teacher.rating || '暂无' }}</span>
              </div>
            </div>
            
            <!-- 专长标签 -->
            <div v-if="expertiseDisplay.length > 0" class="mt-3 flex flex-wrap gap-2">
              <span 
                v-for="(expertise, index) in expertiseDisplay" 
                :key="index"
                class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
              >
                {{ expertise }}
              </span>
            </div>
          </div>
        </div>
        
        <!-- 教师简介 -->
        <div class="mb-8 p-4 bg-gray-50 rounded-lg">
          <h3 class="font-semibold text-gray-700 mb-2 flex items-center">
            <i class="fa fa-info-circle mr-2 text-blue-500"></i>
            教师简介
          </h3>
          <p class="text-gray-600">{{ teacher.description || teacher.bio || '这位老师还没有填写个人简介' }}</p>
        </div>
        
        <!-- 课程区域 -->
        <div class="mt-8">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-xl font-semibold text-gray-800">
              教师的课程 ({{ totalCourses }})
            </h3>
            
            <!-- 分页信息 -->
            <div v-if="pagination && pagination.total_pages > 1" class="flex items-center space-x-2">
              <span class="text-sm text-gray-600">
                第 {{ pagination?.page || 1 }} 页 / 共 {{ pagination?.total_pages || 1 }} 页
              </span>
              <button 
                v-if="pagination?.page > 1"
                @click="loadPage(pagination.page - 1)"
                class="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded"
              >
                <i class="fa fa-chevron-left"></i>
              </button>
              <button 
                v-if="pagination && pagination.page < pagination.total_pages"
                @click="loadPage(pagination.page + 1)"
                class="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded"
              >
                <i class="fa fa-chevron-right"></i>
              </button>
            </div>

            <!-- 分页控制 -->
            <div v-if="pagination && pagination.total_pages > 1" class="mt-8 flex justify-center">
              <nav class="flex items-center space-x-2">
                <button
                  v-for="pageNum in (pagination.total_pages || 1)"
                  :key="pageNum"
                  @click="loadPage(pageNum)"
                  class="px-3 py-1.5 text-sm rounded transition-colors"
                  :class="{
                    'bg-blue-500 text-white': (pagination?.page || 1) === pageNum,
                    'bg-gray-100 text-gray-700 hover:bg-gray-200': (pagination?.page || 1) !== pageNum
                  }"
                >
                  {{ pageNum }}
                </button>
              </nav>
            </div>
          </div>
          
          <!-- 课程网格 -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <div 
              v-for="course in teacherCourses" 
              :key="course.course_id"
              class="bg-white rounded-lg overflow-hidden border border-gray-200 hover:border-blue-300 hover:shadow-lg transition-all duration-300 cursor-pointer group"
              @click="goToCourse(course)"
            >
              <!-- 课程封面 -->
              <div class="relative h-48 bg-gradient-to-br from-blue-50 to-gray-100 overflow-hidden">
                <img 
                  v-if="course.thumbnail_url"
                  :src="course.thumbnail_url" 
                  :alt="course.course_name"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                >
                <div v-else class="w-full h-full flex items-center justify-center">
                  <i class="fa fa-book-open text-4xl text-blue-300"></i>
                </div>
                
                <!-- 难度标签 -->
                <div class="absolute top-3 left-3 px-2 py-1 bg-black/60 text-white text-xs rounded">
                  {{ getDifficultyText(course.difficulty) }}
                </div>
                
                <!-- 播放按钮 -->
                <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
                  <div class="w-12 h-12 rounded-full bg-white/90 backdrop-blur-sm flex items-center justify-center transform scale-90 group-hover:scale-100 transition-transform duration-300">
                    <i class="fa fa-play text-blue-600 text-lg"></i>
                  </div>
                </div>
              </div>
              
              <!-- 课程信息 -->
              <div class="p-4">
                <h4 class="text-sm font-semibold text-gray-800 line-clamp-2 mb-2 group-hover:text-blue-600 transition-colors">
                  {{ course.course_name }}
                </h4>
                
                <div class="flex items-center justify-between text-xs text-gray-500 mb-2">
                  <div class="flex items-center">
                    <i class="fa fa-layer-group mr-1"></i>
                    <span>{{ course.chapter_count || 0 }}章节</span>
                  </div>
                  <div class="flex items-center">
                    <i class="fa fa-clock mr-1"></i>
                    <span>{{ course.duration_hours || 0 }}小时</span>
                  </div>
                </div>
                
                <div class="flex items-center justify-between text-xs">
                  <div class="flex items-center">
                    <i class="fa fa-user-graduate mr-1 text-blue-500"></i>
                    <span>{{ course.enrolled_count || 0 }}人学习</span>
                  </div>
                  <div class="flex items-center">
                    <i class="fa fa-star text-yellow-500 mr-1"></i>
                    <span>{{ course.rating || '未评分' }}</span>
                  </div>
                </div>
                
                <!-- 创建时间 -->
                <div class="mt-3 pt-3 border-t border-gray-100 text-xs text-gray-400">
                  <i class="fa fa-calendar mr-1"></i>
                  {{ course.created_at ? formatDisplayDate(course.created_at) : '未知时间' }}
                </div>
              </div>
            </div>
          </div>
          
          <!-- 空状态 -->
          <div v-if="!isLoading && teacherCourses.length === 0" class="text-center py-16">
            <i class="fa fa-book-open text-5xl text-gray-300 mb-4"></i>
            <h4 class="text-gray-500 font-medium mb-2">暂无课程</h4>
            <p class="text-gray-400 text-sm">该老师还没有发布任何课程</p>
          </div>
          
          <!-- 分页控制 -->
          <div v-if="pagination.total_pages > 1" class="mt-8 flex justify-center">
            <nav class="flex items-center space-x-2">
              <button
                v-for="pageNum in pagination.total_pages"
                :key="pageNum"
                @click="loadPage(pageNum)"
                class="px-3 py-1.5 text-sm rounded transition-colors"
                :class="{
                  'bg-blue-500 text-white': pagination.page === pageNum,
                  'bg-gray-100 text-gray-700 hover:bg-gray-200': pagination.page !== pageNum
                }"
              >
                {{ pageNum }}
              </button>
            </nav>
          </div>
        </div>
        
        <!-- 返回按钮 -->
        <div class="mt-10 pt-6 border-t border-gray-200">
          <button @click="goBack" class="px-6 py-2.5 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-200 shadow-sm hover:shadow">
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
import teacherService from '@/service/teacher.js'
import courseService from '@/service/course.js'

export default {
  name: 'TeacherSpace',
  components: {
    Header,
    Footer
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    return { route, router }
  },
  data() {
    return {
      showAllCourses: false,
      initialCourseCount: 8,
      teacherCourses: [], // 初始为空，等待API加载
      pagination: {
        page: 1,
        page_size: 12,
        total: 0,
        total_pages: 0
      },
      // 教师信息 - 从多个来源整合
      teacher: {
        name: '',
        userId: '',
        department: '计算机学院',
        location: '',
        avatar: '',
        description: '',
        bio: '',
        title: '讲师',
        followers: 0,
        following: 0,
        course_count: 0,
        total_students: 0,
        expertise: [],
        tags: [],
        contact_email: '',
        contact_phone: '',
        social_links: {},
        join_date: '',
        rating: 0,
        achievements: [],
        is_verified: false
      },
      
      isLoading: true,
      teacherIdFromRoute: null
    }
  },
  computed: {
    displayedCourses() {
      if (this.showAllCourses) {
        return this.teacherCourses
      }
      return this.teacherCourses.slice(0, this.initialCourseCount)
    },
    
    totalCourses() {
      return this.pagination?.total || this.teacherCourses.length
    },
    
    gridColsClass() {
      if (this.teacherCourses.length === 0) return ''
      
      const baseClass = 'grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4'
      
      if (this.showAllCourses) {
        return baseClass
      }
      
      // 根据课程数量动态调整
      if (this.displayedCourses.length <= 2) return 'grid-cols-1 sm:grid-cols-2'
      if (this.displayedCourses.length <= 4) return 'grid-cols-2 md:grid-cols-4'
      
      return baseClass
    },
    
    // 教师是否已验证
    isVerified() {
      return this.teacher.is_verified || this.teacher.achievements?.length > 0
    },
    
    // 专长领域显示
    expertiseDisplay() {
      if (this.teacher.expertise?.length > 0) {
        return this.teacher.expertise
      }
      
      // 如果专长字段为空，从标签或课程中推断
      const tags = this.teacher.tags || []
      if (tags.length > 0) {
        return tags.slice(0, 5) // 最多显示5个
      }
      
      // 从课程主题推断
      const subjects = [...new Set(this.teacherCourses.map(course => course.subject))]
      return subjects.slice(0, 3)
    }
  },
  mounted() {
    this.loadTeacherData()
    
    // 添加CSS动画
    this.addCustomStyles()
  },
  methods: {
    async loadTeacherData() {
      this.isLoading = true
      
      try {
        // 1. 获取教师ID
        this.teacherIdFromRoute = this.route.query.teacherId || this.route.query.teacherName
        
        // 2. 从多个来源整合教师信息
        await this.integrateTeacherInfo()
        
        // 3. 加载教师课程
        await this.loadTeacherCourses()
        
        console.log('教师数据加载完成:', this.teacher)
        
      } catch (error) {
        console.error('加载教师数据失败:', error)
        this.showNotification('加载教师信息失败，请稍后重试')
        
        // 使用默认数据
        this.useDefaultTeacherData()
      } finally {
        this.isLoading = false
      }
    },
    
    async integrateTeacherInfo() {
      const teacherId = this.teacherIdFromRoute
      const storedTeacherInfo = JSON.parse(localStorage.getItem('currentTeacherInfo') || '{}')
      
      console.log('整合教师信息:', {
        routeTeacherId: teacherId,
        storedTeacherInfo,
        routeQuery: this.route.query
      })
      
      // 尝试1: 从API获取教师信息
      if (teacherId) {
        try {
          const apiResponse = await teacherService.getTeacherInfo(teacherId)
          if (apiResponse.code === 200 && apiResponse.data) {
            this.setTeacherFromApi(apiResponse.data)
            return
          }
        } catch (apiError) {
          console.warn('API获取教师信息失败:', apiError)
        }
      }
      
      // 尝试2: 使用localStorage中的信息
      if (storedTeacherInfo.name) {
        this.setTeacherFromStorage(storedTeacherInfo)
        return
      }
      
      // 尝试3: 使用路由参数中的信息
      if (this.route.query.teacherName) {
        this.setTeacherFromRoute()
        return
      }
      
      // 尝试4: 使用默认信息
      this.setDefaultTeacherInfo()
    },
    
    setTeacherFromApi(teacherData) {
      console.log('使用API数据设置教师信息:', teacherData)
      
      this.teacher = {
        name: teacherData.name || this.route.query.teacherName || '未知教师',
        userId: teacherData.user_id || this.teacherIdFromRoute || `teacher_${Date.now()}`,
        department: teacherData.department || '计算机学院',
        location: teacherData.location || '',
        avatar: teacherData.avatar || this.getDefaultAvatar(teacherData.name),
        description: teacherData.description || teacherData.bio || '暂无个人简介',
        bio: teacherData.bio || teacherData.description || '暂无个人简介',
        title: teacherData.title || '讲师',
        followers: teacherData.follower_count || 0,
        following: teacherData.following_count || 0,
        course_count: teacherData.course_count || 0,
        total_students: teacherData.total_students || 0,
        expertise: teacherData.expertise || [],
        tags: teacherData.tags || [],
        contact_email: teacherData.contact_email || '',
        contact_phone: teacherData.contact_phone || '',
        social_links: teacherData.social_links || {},
        join_date: teacherData.join_date || '',
        rating: teacherData.rating || 0,
        achievements: teacherData.achievements || [],
        is_verified: teacherData.is_verified || false
      }
      
      // 更新本地存储
      localStorage.setItem('currentTeacherInfo', JSON.stringify({
        name: this.teacher.name,
        userId: this.teacher.userId,
        department: this.teacher.department,
        avatar: this.teacher.avatar,
        description: this.teacher.description
      }))
    },
    
    setTeacherFromStorage(storedInfo) {
      console.log('使用本地存储设置教师信息:', storedInfo)
      
      this.teacher = {
        name: storedInfo.name || this.route.query.teacherName || '未知教师',
        userId: storedInfo.userId || this.teacherIdFromRoute || `teacher_${Date.now()}`,
        department: storedInfo.department || '计算机学院',
        location: storedInfo.location || '',
        avatar: storedInfo.avatar || this.getDefaultAvatar(storedInfo.name),
        description: storedInfo.description || storedInfo.bio || '暂无个人简介',
        bio: storedInfo.description || '暂无个人简介',
        title: storedInfo.title || '讲师',
        followers: storedInfo.followers || 0,
        following: storedInfo.following || 0,
        course_count: storedInfo.course_count || 0,
        total_students: storedInfo.total_students || 0,
        expertise: storedInfo.expertise || [],
        tags: storedInfo.tags || [],
        contact_email: storedInfo.contact_email || '',
        contact_phone: storedInfo.contact_phone || '',
        social_links: storedInfo.social_links || {},
        join_date: storedInfo.join_date || '',
        rating: storedInfo.rating || 0,
        achievements: storedInfo.achievements || [],
        is_verified: storedInfo.is_verified || false
      }
    },
    
    setTeacherFromRoute() {
      console.log('使用路由参数设置教师信息')
      
      this.teacher = {
        name: this.route.query.teacherName || '未命名教师',
        userId: this.route.query.teacherId || `teacher_${Date.now()}`,
        department: this.route.query.department || '计算机学院',
        location: '',
        avatar: this.getDefaultAvatar(this.route.query.teacherName),
        description: this.route.query.description || '暂无个人简介',
        bio: this.route.query.description || '暂无个人简介',
        title: this.route.query.title || '讲师',
        followers: 0,
        following: 0,
        course_count: 0,
        total_students: 0,
        expertise: [],
        tags: [],
        contact_email: '',
        contact_phone: '',
        social_links: {},
        join_date: '',
        rating: 0,
        achievements: [],
        is_verified: false
      }
    },
    
    setDefaultTeacherInfo() {
      console.log('使用默认教师信息')
      
      const teacherName = this.route.query.teacherName || '未命名教师'
      
      this.teacher = {
        name: teacherName,
        userId: this.route.query.teacherId || `teacher_${Date.now()}`,
        department: '计算机学院',
        location: '',
        avatar: this.getDefaultAvatar(teacherName),
        description: '这位老师还没有填写个人简介',
        bio: '这位老师还没有填写个人简介',
        title: '讲师',
        followers: 0,
        following: 0,
        course_count: 0,
        total_students: 0,
        expertise: [],
        tags: [],
        contact_email: '',
        contact_phone: '',
        social_links: {},
        join_date: '',
        rating: 0,
        achievements: [],
        is_verified: false
      }
      
      this.showNotification('正在使用默认教师信息')
    },
    
    useDefaultTeacherData() {
      // 使用本地模拟数据作为fallback
      this.teacher = {
        name: this.route.query.teacherName || '测试讲师',
        userId: this.route.query.teacherId || 'teacher_001',
        department: '计算机学院',
        location: '北京',
        avatar: this.getDefaultAvatar(this.route.query.teacherName || '老师'),
        description: '资深计算机科学讲师，拥有10年教学经验',
        bio: '专注于计算机科学教育，擅长操作系统、数据结构、网络技术等课程',
        title: '高级讲师',
        followers: 1256,
        following: 89,
        course_count: 8,
        total_students: 3245,
        expertise: ['操作系统', '数据结构', '计算机网络', '数据库'],
        tags: ['计算机基础', '编程', '算法', '网络'],
        contact_email: 'teacher@example.com',
        contact_phone: '13800138000',
        social_links: { weibo: '@teacher', github: 'teacher' },
        join_date: '2020-01-01',
        rating: 4.8,
        achievements: ['优秀教师奖', '教学创新奖'],
        is_verified: true
      }
    },
    // 获取课程封面图片
    getCourseCoverImage(course, index = 0) {
      // 1. 优先使用API返回的封面
      if (course.thumbnail_url) {
        return course.thumbnail_url
      }
      
      // 2. 根据课程领域生成相关图片
      const domain = course.domain || ''
      if (domain) {
        const encodedDomain = encodeURIComponent(domain)
        return `https://source.unsplash.com/random/400x225/?${encodedDomain},learning,education&sig=${course.course_id || index}`
      }
      
      // 3. 默认随机图片
      return `https://picsum.photos/400/225?random=${course.course_id || Date.now() + index}`
    },
    async loadTeacherCourses() {
      try {
        if (this.teacher.userId) {
          const response = await courseService.getCoursesByTeacher(this.teacher.userId)
          
          if (response.code === 200 && response.data && response.data.courses) {
            const data = response.data
            
            // 调试：查看原始数据
            console.log('原始课程数据:', data.courses[0])
            console.log('章节数:', data.courses[0]?.chapter_count)
            
            // 映射课程数据
            this.teacherCourses = data.courses.map(course => {
              // 统一处理字段值
              const chapterCount = course.chapter_count || 0
              const enrolledCount = course.enrolled_count || 0
              const durationHours = course.duration_hours || 0
              const ratingValue = course.rating || 0
              
              return {
                // 核心字段（确保模板能访问到）
                course_id: course.course_id,
                course_name: course.course_name,
                chapter_count: chapterCount,      // 模板使用这个
                enrolled_count: enrolledCount,    // 模板使用这个
                duration_hours: durationHours,    // 模板使用这个
                rating: ratingValue,              // 模板使用这个
                difficulty: course.difficulty || 1,
                domain: course.domain || '编程开发',
                created_at: course.created_at || '未知时间',
                thumbnail_url: course.thumbnail_url || this.getRandomCourseImage(course.course_id),
                description: course.description || '',
                user_id: course.user_id,
                
                // 兼容字段（如果有其他代码使用）
                id: course.course_id,
                title: course.course_name,
                image: course.thumbnail_url || this.getRandomCourseImage(),
                subject: course.domain || '编程开发',
                chapterCount: chapterCount,       // 兼容字段
                studentCount: enrolledCount,      // 兼容字段
                durationHours: durationHours,     // 兼容字段
                createdAt: course.created_at || '未知时间'
              }
            })
            
            // 设置分页
            this.pagination = {
              page: data.pagination?.page || 1,
              page_size: data.pagination?.page_size || 12,
              total: data.pagination?.total || 0,
              total_pages: data.pagination?.total_pages || 0
            }

            this.teacher.course_count = this.teacherCourses.length
            
            // 调试：查看映射后的数据
            console.log('映射后第一个课程:', this.teacherCourses[0])
            console.log('章节数字段值:', this.teacherCourses[0]?.chapter_count)
            
            return
          }
        }
      } catch (error) {
        console.warn('API加载课程失败，使用模拟数据:', error)
      }
      
      this.useMockCourses()
    },
    
    useMockCourses() {
      // 修改模拟数据格式，添加course_id字段
      this.teacherCourses = [
        { 
          course_id: 'C001', 
          id: 'C001',
          title: '操作系统', 
          course_name: '操作系统',
          image: 'https://picsum.photos/400/225?random=100', 
          subject: '计算机基础', 
          createdAt: '2024-01-15',
          thumbnail_url: 'https://picsum.photos/400/225?random=100',
          enrolled_count: 1234,
          duration_hours: 24.5,
          domain: '计算机基础',
          difficulty: 2,
          rating: 4.8,
          chapter_count: 12,
          created_at: '2024-01-15 10:00:00'
        },
        // ... 其他课程保持类似格式
      ]
      // 设置模拟分页信息
      this.pagination = {
        page: 1,
        page_size: 12,
        total: this.teacherCourses.length,
        total_pages: Math.ceil(this.teacherCourses.length / 12)
      }
      
      this.teacher.course_count = this.teacherCourses.length
    },
    
    // 工具方法
    getDifficultyText(difficulty) {
      const difficultyMap = {
        1: '入门',
        2: '初级',
        3: '中级',
        4: '高级',
        5: '专家'
      }
      return difficultyMap[difficulty] || '未知'
    },
    getDefaultAvatar(name) {
      const colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
      const index = name ? name.charCodeAt(0) % colors.length : 0
      return `https://ui-avatars.com/api/?name=${encodeURIComponent(name || '老师')}&background=${colors[index].slice(1)}&color=fff&size=150`
    },
    formatDisplayDate(dateString) {
      if (!dateString) return '未知时间'
      
      try {
        // 尝试解析日期
        const date = new Date(dateString)
        
        // 检查是否是有效日期
        if (isNaN(date.getTime())) {
          // 如果不是有效日期，尝试其他格式
          const match = dateString.match(/(\d{4})-(\d{2})-(\d{2})/)
          if (match) {
            return match[0] // 返回 YYYY-MM-DD 格式
          }
          return dateString.split(' ')[0] || dateString
        }
        
        const now = new Date()
        const diffTime = Math.abs(now - date)
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
        
        if (diffDays === 0) {
          return '今天'
        } else if (diffDays === 1) {
          return '昨天'
        } else if (diffDays < 7) {
          return `${diffDays}天前`
        } else if (diffDays < 30) {
          return `${Math.floor(diffDays / 7)}周前`
        } else {
          // 超过30天显示具体日期
          return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
          })
        }
      } catch (error) {
        console.warn('格式化日期失败:', dateString, error)
        // 简单处理：只显示日期部分
        return dateString.split(' ')[0] || dateString
      }
    },
    getRandomCourseImage() {
      const images = [
        'https://picsum.photos/400/225?random=1',
        'https://picsum.photos/400/225?random=2',
        'https://picsum.photos/400/225?random=3',
        'https://picsum.photos/400/225?random=4',
        'https://picsum.photos/400/225?random=5'
      ]
      return images[Math.floor(Math.random() * images.length)]
    },
    
    formatDate(dateString) {
      try {
        const date = new Date(dateString)
        return date.toISOString().split('T')[0]
      } catch (error) {
        return '未知时间'
      }
    },
    
    showNotification(message) {
      const notification = document.createElement('div')
      notification.className = 'custom-notification'
      notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background-color: #1890ff;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        z-index: 1000;
        animation: slideIn 0.3s ease;
      `
      notification.textContent = message
      document.body.appendChild(notification)
      
      setTimeout(() => {
        if (notification.parentNode) {
          document.body.removeChild(notification)
        }
      }, 3000)
    },
    
    addCustomStyles() {
      const style = document.createElement('style')
      style.textContent = `
        @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
          from { transform: translateX(0); opacity: 1; }
          to { transform: translateX(100%); opacity: 0; }
        }
        .line-clamp-2 {
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }
        .text-secondary {
          color: #6b7280;
        }
        .text-link {
          color: #3b82f6;
        }
        .bg-blue-50 {
          background-color: #eff6ff;
        }
        .hover\:bg-blue-50:hover {
          background-color: #dbeafe;
        }
      `
      document.head.appendChild(style)
    },
    
    toggleExpandCourses() {
      this.showAllCourses = !this.showAllCourses
    },
    
    goToCourse(course) {
      console.log('跳转到课程:', course)
      
      // 确定课程ID，优先使用course_id
      const courseId = course.course_id || course.id
      
      if (!courseId) {
        console.error('课程ID不存在:', course)
        this.showNotification('课程信息不完整，无法跳转')
        return
      }
      
      // 保存必要信息到 localStorage
      localStorage.setItem('currentCourseInfo', JSON.stringify({
        course_id: courseId,
        course_name: course.course_name || course.title
      }))
      
      // 保存教师信息（用于返回时保持状态）
      localStorage.setItem('currentTeacherInfo', JSON.stringify({
        name: this.teacher.name,
        userId: this.teacher.userId,
        department: this.teacher.department,
        avatar: this.teacher.avatar
      }))
      
      // 跳转到 VideoPlayer.vue
      // 只需要传递 courseId，VideoPlayer 会自己调用 /api/course/<course_id>/structure
      this.$router.push({
        name: 'VideoPlayer',
        params: {
          courseId: courseId
        },
        query: {
          courseId: courseId,
          from: 'teacher-space',
          teacherId: this.teacher.userId, // 可选：用于返回
          teacherName: this.teacher.name  // 可选：用于返回
        }
      })
    },
    
    goBack() {
      this.router.go(-1)
    }
  }
}
</script>

<style scoped>
/* 视频卡片样式 */
.video-card {
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.video-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
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
</style>