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
              <img :src="teacher.avatar" :alt="teacher.name" class="w-full h-full object-cover">
            </div>
          </div>
          <div class="ml-6">
            <h2 class="text-2xl font-bold text-dark mb-2">{{ teacher.name }}</h2>
            <div class="flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-secondary">
              <div class="flex items-center gap-1">
                <i class="fa fa-graduation-cap text-primary"></i>
                <span>{{ teacher.department }}</span>
              </div>
              <div class="flex items-center gap-1">
                <i class="fa fa-map-marker text-primary"></i>
                <span>{{ teacher.location || '未设置位置' }}</span>
              </div>
              <div class="flex items-center gap-1">
                <i class="fa fa-star text-yellow-500"></i>
                <span>粉丝数: <span>{{ teacher.followers || 0 }}</span></span>
              </div>
              <div class="flex items-center gap-1">
                <i class="fa fa-book text-primary"></i>
                <span>发布课程: <span>{{ teacherCourses.length }}</span></span>
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
            <h3 class="text-lg font-semibold text-dark">教师的课程</h3>
            <button 
              class="text-link text-sm hover:underline flex items-center gap-1"
              @click="toggleExpandCourses"
            >
              {{ showAllCourses ? '收起' : '查看更多' }}
              <i class="fa" :class="showAllCourses ? 'fa-angle-up' : 'fa-angle-down'"></i>
            </button>
          </div>
          
          <!-- 课程网格 -->
          <div 
            class="grid gap-4 transition-all duration-300"
            :class="showAllCourses ? 'grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4' : 'grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 max-h-[500px] overflow-hidden'"
          >
            <!-- 课程卡片 - 使用主页视频样式 -->
            <div 
              v-for="course in displayedCourses" 
              :key="course.id"
              class="bg-white rounded-lg overflow-hidden cursor-pointer hover:shadow-lg transition-all duration-300 group video-card"
              @click="goToCourse(course)"
            >
              <!-- 视频封面 - 16:9比例 -->
              <div class="relative" style="aspect-ratio: 16/9;">
                <img 
                  :src="course.image" 
                  :alt="course.title" 
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                >
                <!-- 播放按钮 -->
                <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/20">
                  <div class="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                    <i class="fa fa-play text-white text-lg"></i>
                  </div>
                </div>
              </div>
              <!-- 课程信息 -->
              <div class="p-3">
                <h4 class="text-sm font-medium line-clamp-2 group-hover:text-primary transition-colors mb-1">
                  {{ course.title }}
                </h4>
                <div class="text-xs text-gray-500">{{ course.subject }}</div>
              </div>
            </div>
          </div>
          
          <!-- 空状态 -->
          <div v-if="teacherCourses.length === 0" class="text-center py-12">
            <i class="fa fa-book-open text-4xl text-gray-300 mb-4"></i>
            <p class="text-gray-500">该老师还没有发布任何课程</p>
          </div>
        </div>
        
        <!-- 返回按钮 -->
        <div class="mt-8 pt-6 border-t border-gray-200">
          <button @click="goBack" class="px-6 py-2.5 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors duration-200">
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

export default {
  name: 'TeacherSpace',
  components: {
    Header,
    Footer
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const teacher = JSON.parse(localStorage.getItem('currentTeacherInfo') || '{}')
    
    const goBack = () => {
      router.go(-1)
    }
    
    return {
      teacher,
      goBack
    }
  },
  data() {
    return {
      showAllCourses: false,
      teacherCourses: [
        { 
          id: 1, 
          title: '操作系统', 
          image: 'https://picsum.photos/400/225?random=100',
          subject: '计算机基础'
        },
        { 
          id: 2, 
          title: '互联网原理与应用', 
          image: 'https://picsum.photos/400/225?random=101',
          subject: '网络技术'
        },
        { 
          id: 3, 
          title: '数据结构与算法', 
          image: 'https://picsum.photos/400/225?random=102',
          subject: '编程基础'
        },
        { 
          id: 4, 
          title: '数据库系统原理', 
          image: 'https://picsum.photos/400/225?random=103',
          subject: '数据管理'
        },
        { 
          id: 5, 
          title: '计算机网络', 
          image: 'https://picsum.photos/400/225?random=104',
          subject: '网络工程'
        },
        { 
          id: 6, 
          title: '软件工程', 
          image: 'https://picsum.photos/400/225?random=105',
          subject: '软件开发'
        },
        { 
          id: 7, 
          title: '人工智能基础', 
          image: 'https://picsum.photos/400/225?random=106',
          subject: '人工智能'
        },
        { 
          id: 8, 
          title: '机器学习入门', 
          image: 'https://picsum.photos/400/225?random=107',
          subject: '机器学习'
        }
      ]
    }
  },
  computed: {
    displayedCourses() {
      return this.showAllCourses ? this.teacherCourses : this.teacherCourses.slice(0, 8)
    }
  },
  mounted() {
    // 如果从路由参数中获取了老师ID，可以加载对应老师的课程
    const teacherId = this.$route.query.teacherId
    if (teacherId) {
      this.loadTeacherCourses(teacherId)
    }
  },
  methods: {
    toggleExpandCourses() {
      this.showAllCourses = !this.showAllCourses
    },
    
    goToCourse(course) {
      this.$router.push({
        name: 'VideoPlayer',
        params: { courseId: course.id }
      })
    },
    
    loadTeacherCourses(teacherId) {
      // 这里可以根据teacherId从API加载对应老师的课程
      // 暂时使用模拟数据
      console.log('加载老师课程:', teacherId)
    }
  }
}
</script>

<style scoped>
/* 视频卡片样式（与主页一致） */
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

/* 链接样式 */
.text-link {
  @apply text-primary hover:text-primary/80 transition-colors duration-200 cursor-pointer;
}
</style>