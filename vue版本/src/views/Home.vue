<template>
  <div class="min-h-screen flex flex-col">
    <Header />
    
    <!-- 分类导航栏 -->
    <nav class="bg-white py-3 px-6 md:px-8 sticky top-[5rem] z-20 border-b border-gray-200">
      <div class="container mx-auto overflow-x-auto hide-scrollbar">
        <div class="flex items-center justify-center gap-4 text-sm whitespace-nowrap">
          <a href="#" class="text-primary font-medium py-1 border-b-2 border-primary text-center w-20">推荐</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">编程开发</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">人工智能</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">数据科学</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">商业管理</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">设计创意</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">市场营销</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">语言学习</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">职业技能</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">考研考证</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">生活兴趣</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">职场提升</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">创业指导</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">教师成长</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">学生专区</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">更多 <i class="fa fa-angle-down text-xs"></i></a>
          <span class="border-l border-gray-200 h-4 mx-2"></span>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">精品课程</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">学习路径</a>
          <a href="#" class="text-gray-500 hover:text-primary py-1 border-b-2 border-transparent hover:border-primary/30 transition-colors text-center w-20">学习社区</a>
        </div>
      </div>
    </nav>

    <main class="flex-1">
      <!-- 第一区域：热门推荐 -->
      <section class="bg-white p-6 md:p-8">
        <div class="max-w-6xl mx-auto">
          <div class="flex items-center gap-2 mb-6">
            <div class="h-5 w-0.5 bg-primary"></div>
            <h2 class="text-lg font-semibold text-dark">热门推荐</h2>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- 左侧主推荐课程 -->
            <div class="lg:col-span-2 video-card-hover" @click="goToCourseDetail(mainCourse)">
              <div class="relative rounded-lg overflow-hidden mb-4">
                <img src="https://picsum.photos/800/450?random=1" alt="深度学习实战" class="w-full h-80 object-cover">
                <span class="badge-hot">热门</span>
                <span class="video-time">12:54:00</span>
                <!-- 播放按钮 -->
                <div class="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-300 bg-black/20">
                  <div class="w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                    <i class="fa fa-play text-white text-xl"></i>
                  </div>
                </div>
                <!-- 右上角小图标 -->
                <div class="absolute top-2 right-2 text-gray-400 hover:text-primary cursor-pointer">
                  <i class="fa fa-bookmark-o"></i>
                </div>
              </div>
              <!-- 文字信息区域 -->
              <div class="px-1">
                <!-- 左右切换箭头 -->
                <div class="flex justify-between items-center mb-3">
                  <button class="w-8 h-8 rounded-full border border-gray-200 flex items-center justify-center text-gray-400 hover:border-primary hover:text-primary transition-colors">
                    <i class="fa fa-angle-left"></i>
                  </button>
                  <button class="w-8 h-8 rounded-full border border-gray-200 flex items-center justify-center text-gray-400 hover:border-primary hover:text-primary transition-colors">
                    <i class="fa fa-angle-right"></i>
                  </button>
                </div>
                <!-- 课程标题 -->
                <h3 class="text-xl font-semibold text-dark mb-2 hover:text-primary transition-colors">深度学习实战：从零搭建AI模型</h3>
                <!-- 讲师信息 -->
                <div class="text-sm text-gray-500 mb-3 flex items-center gap-2">
                  <i class="fa fa-user text-gray-400"></i>
                  <span>李明教授</span>
                </div>
                <!-- 课程描述 -->
                <p class="text-sm text-gray-600 mb-4">
                  本课程将带你从零开始学习深度学习，掌握TensorFlow和PyTorch框架，构建各种AI模型，包括图像识别、自然语言处理等实际应用案例。
                </p>
                <!-- 播放量和好评 -->
                <div class="flex items-center gap-4 text-sm text-gray-500">
                  <span class="flex items-center gap-1"><i class="fa fa-eye text-gray-400"></i> 25.6万播放</span>
                  <span class="flex items-center gap-1"><i class="fa fa-thumbs-up text-gray-400"></i> 98%</span>
                </div>
              </div>
            </div>

            <!-- 右侧热门课程列表 -->
            <div class="space-y-3 flex flex-col h-full">
              <div v-for="course in hotCourses" :key="course.id" 
                   class="flex gap-3 video-card-hover flex-shrink-0 h-24" 
                   @click="goToCourseDetail(course)">
                <div class="relative w-1/3 rounded-lg overflow-hidden flex-shrink-0">
                  <img :src="course.image" :alt="course.title" class="w-full h-full object-cover">
                  <span :class="course.badgeClass">{{ course.badgeText }}</span>
                  <span class="video-time">{{ course.duration }}</span>
                </div>
                <div class="w-2/3 flex flex-col justify-center">
                  <h4 class="text-sm font-medium text-dark line-clamp-1 hover:text-primary transition-colors">{{ course.title }}</h4>
                  <div class="text-xs text-gray-500 mt-1 line-clamp-1">{{ course.teacher }} · {{ course.views }}</div>
                  <div class="text-xs text-gray-400 mt-1 line-clamp-1">{{ course.date }} · {{ course.category }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 第二区域：推荐视频课程 + 权威师资团队 -->
      <section class="bg-gray-50 p-6 md:p-8">
        <div class="max-w-6xl mx-auto">
          <!-- 推荐视频课程区域 -->
          <div class="mb-12">
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center gap-2">
                <div class="h-5 w-0.5 bg-primary"></div>
                <h2 class="text-lg font-semibold text-dark">推荐视频课程</h2>
              </div>
              <div class="flex items-center gap-4 text-sm">
                <div class="flex items-center gap-3">
                  <a href="#" class="text-primary font-medium">最新</a>
                  <a href="#" class="text-gray-500 hover:text-primary">热门</a>
                  <a href="#" class="text-gray-500 hover:text-primary">更多 <i class="fa fa-angle-right"></i></a>
                </div>
              </div>
            </div>

            <!-- 课程卡片 -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <div v-for="course in recommendedCourses" :key="course.id" 
                   class="video-card-hover" @click="goToCourseDetail(course)">
                <div class="relative rounded-lg overflow-hidden mb-2">
                  <img :src="course.image" :alt="course.title" class="w-full h-40 object-cover">
                  <span :class="course.badgeClass">{{ course.badgeText }}</span>
                  <span class="video-time">{{ course.duration }}</span>
                  <div class="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-300 bg-black/20">
                    <div class="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                      <i class="fa fa-play text-white text-lg"></i>
                    </div>
                  </div>
                </div>
                <h4 class="text-sm font-medium text-dark mb-1 line-clamp-1 hover:text-primary transition-colors">{{ course.title }}</h4>
                <div class="text-xs text-gray-500 mb-1">{{ course.teacher }}</div>
                <div class="flex justify-between items-center text-xs text-gray-400">
                  <span>{{ course.views }}</span>
                  <span>{{ course.date }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 权威师资团队区域 -->
          <div class="w-full">
            <!-- 标题区域 -->
            <div class="text-center mb-8">
              <h2 class="text-xl font-semibold text-dark mb-2">权威师资团队</h2>
              <p class="text-sm text-gray-500 max-w-2xl mx-auto">汇聚全国顶尖名校知名教授，带你探索学科奥秘，提升专业素养。</p>
            </div>

            <!-- 师资列表容器 -->
            <div class="relative">
              <!-- 左右切换箭头 -->
              <button class="absolute left-0 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-white border border-gray-200 flex items-center justify-center text-gray-500 hover:text-primary hover:border-primary z-10 shadow-sm">
                <i class="fa fa-angle-left"></i>
              </button>
              <button class="absolute right-0 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-white border border-gray-200 flex items-center justify-center text-gray-500 hover:text-primary hover:border-primary z-10 shadow-sm">
                <i class="fa fa-angle-right"></i>
              </button>

              <!-- 滚动容器 -->
              <div class="flex justify-center overflow-x-auto hide-scrollbar pb-6">
                <div class="flex items-center gap-10 min-w-max">
                  <div v-for="teacher in teachers" :key="teacher.id" class="teacher-card">
                    <div class="teacher-avatar-container">
                      <img :src="teacher.image" :alt="teacher.name" class="w-full h-full object-cover">
                    </div>
                    <h4 class="text-base font-medium text-dark">{{ teacher.name }}</h4>
                    <p class="text-sm text-gray-500 mt-1">{{ teacher.university }}</p>
                    <p class="text-base text-primary mt-0.5">{{ teacher.major }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- 查看全部按钮 -->
            <div class="text-center mt-8">
              <button @click="goToTeacherDashboard" class="inline-flex items-center gap-1 px-4 py-2 border border-primary text-primary rounded-md hover:bg-primary/5 transition-colors">
                <span>查看全部师资</span>
                <i class="fa fa-angle-right text-xs"></i>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 第三区域：热门热搜课程 + 注册横幅 + 页脚 -->
      <section class="bg-white">
        <!-- 热门热搜课程区域 -->
        <div class="p-6 md:p-8">
          <div class="max-w-6xl mx-auto">
            <div class="flex items-center gap-2 mb-6">
              <div class="h-5 w-0.5 bg-primary"></div>
              <h2 class="text-lg font-semibold text-dark">热门热搜课程</h2>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              <div v-for="course in hotSearchCourses" :key="course.id" 
                   class="video-card-hover" @click="goToCourseDetail(course)">
                <div class="relative rounded-lg overflow-hidden mb-2">
                  <img :src="course.image" :alt="course.title" class="w-full h-24 object-cover">
                  <span class="video-time">{{ course.duration }}</span>
                </div>
                <h4 class="text-sm font-medium text-dark mb-1 line-clamp-1 hover:text-primary transition-colors">{{ course.title }}</h4>
                <div class="text-xs text-gray-500 mb-1">{{ course.teacher }}</div>
                <div class="flex justify-between items-center text-xs text-gray-400">
                  <span>{{ course.views }}</span>
                  <span>{{ course.rating }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 注册横幅 -->
        <div class="w-full bg-gradient-to-r from-blue-900 to-purple-900 py-16 px-6 relative overflow-hidden">
          <div class="max-w-4xl mx-auto bg-black/30 rounded-none p-10 shadow-2xl border border-white/10">
            <div class="text-center">
              <h3 class="text-2xl font-bold text-white mb-4">立即注册，开启学习之旅</h3>
              <p class="text-base text-white/70 mb-8 max-w-2xl mx-auto">加入BGarea，立享优质教育资源，提升专业技能，实现职业发展目标。专属学习路径、权威师资指导、社区交流互动，助你快速成长。</p>
              <div class="flex flex-wrap justify-center gap-6">
                <button @click="goToRegister" class="px-8 py-3 bg-white text-primary font-semibold rounded-md hover:bg-white/90 transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] shadow-lg">
                  免费注册
                </button>
                <button @click="showMemberBenefits" class="px-8 py-3 bg-transparent border-2 border-white text-white font-semibold rounded-md hover:bg-white/10 transition-all duration-300">
                  了解会员特权
                </button>
              </div>
            </div>
          </div>
          <!-- 装饰性元素 -->
          <div class="absolute top-1/4 left-10 w-20 h-20 bg-primary/20 rounded-full blur-2xl"></div>
          <div class="absolute bottom-1/4 right-10 w-32 h-32 bg-purple-500/20 rounded-full blur-3xl"></div>
        </div>
      </section>
    </main>

    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'Home',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      // 主推课程数据
      mainCourse: {
        id: 1,
        title: '深度学习实战：从零搭建AI模型',
        teacher: '李明教授',
        views: '25.6万播放',
        rating: '98%'
      },
      // 热门课程数据
      hotCourses: [
        { 
          id: 1, 
          title: 'Python数据分析实战', 
          teacher: '陈老师', 
          views: '12.3万播放', 
          date: '2023-10-15', 
          category: '数据分析', 
          duration: '38:20', 
          image: 'https://picsum.photos/200/120?random=2', 
          badgeClass: 'badge-blue', 
          badgeText: '新品' 
        },
        { 
          id: 2, 
          title: '金融投资策略分析', 
          teacher: '王教授', 
          views: '9.3万播放', 
          date: '2023-09-28', 
          category: '金融理财', 
          duration: '45:15', 
          image: 'https://picsum.photos/200/120?random=3', 
          badgeClass: 'badge-green', 
          badgeText: '精讲' 
        },
        { 
          id: 3, 
          title: '现代医学前沿研究', 
          teacher: '张医生', 
          views: '7.5万播放', 
          date: '2023-10-22', 
          category: '医学健康', 
          duration: '32:40', 
          image: 'https://picsum.photos/200/120?random=4', 
          badgeClass: 'badge-orange', 
          badgeText: '新课' 
        },
        { 
          id: 4, 
          title: '建筑设计创新思维', 
          teacher: '刘芳教授', 
          views: '6.2万播放', 
          date: '2023-10-18', 
          category: '建筑设计', 
          duration: '38:10', 
          image: 'https://picsum.photos/200/120?random=5', 
          badgeClass: 'badge-blue', 
          badgeText: '新品' 
        },
        { 
          id: 5, 
          title: '区块链技术与应用', 
          teacher: '刘教授', 
          views: '5.8万播放', 
          date: '2023-10-10', 
          category: '区块链', 
          duration: '48:35', 
          image: 'https://picsum.photos/200/120?random=6', 
          badgeClass: 'badge-green', 
          badgeText: '精讲' 
        }
      ],
      // 推荐课程数据
      recommendedCourses: [
        { 
          id: 1, 
          title: '人工智能基础：从原理到实践', 
          teacher: '李明教授', 
          views: '12.3万播放', 
          date: '2023-10-10', 
          duration: '48:25', 
          image: 'https://picsum.photos/300/180?random=7', 
          badgeClass: 'badge-blue', 
          badgeText: '新品' 
        },
        { 
          id: 2, 
          title: '数据结构与算法：进阶与应用', 
          teacher: '陈明教授', 
          views: '8.9万播放', 
          date: '2023-09-28', 
          duration: '62:18', 
          image: 'https://picsum.photos/300/180?random=8', 
          badgeClass: 'badge-green', 
          badgeText: '精讲' 
        },
        { 
          id: 3, 
          title: '财务管理：理论与实践', 
          teacher: '王静教授', 
          views: '5.6万播放', 
          date: '2023-10-20', 
          duration: '54:36', 
          image: 'https://picsum.photos/300/180?random=9', 
          badgeClass: 'badge-orange', 
          badgeText: '新课' 
        },
        { 
          id: 4, 
          title: '医学基础知识精讲', 
          teacher: '张伟教授', 
          views: '7.8万播放', 
          date: '2023-09-15', 
          duration: '42:10', 
          image: 'https://picsum.photos/300/180?random=10', 
          badgeClass: 'badge-blue', 
          badgeText: '新品' 
        }
      ],
      // 师资数据
      teachers: [
        { id: 1, name: '李明教授', university: '北京大学', major: '计算机科学', image: 'https://picsum.photos/400/500?random=11' },
        { id: 2, name: '王静教授', university: '清华大学', major: '经济学', image: 'https://picsum.photos/400/500?random=12' },
        { id: 3, name: '张伟教授', university: '复旦大学', major: '医学', image: 'https://picsum.photos/400/500?random=13' },
        { id: 4, name: '陈明教授', university: '上海交通大学', major: '机械工程', image: 'https://picsum.photos/400/500?random=14' },
        { id: 5, name: '刘芳教授', university: '浙江大学', major: '建筑学', image: 'https://picsum.photos/400/500?random=15' }
      ],
      // 热搜课程数据
      hotSearchCourses: [
        { 
          id: 1, 
          title: 'Python编程从入门到精通', 
          teacher: '李明教授', 
          views: '12.3万播放', 
          rating: '4.5分', 
          duration: '40:20', 
          image: 'https://picsum.photos/200/120?random=16' 
        },
        { 
          id: 2, 
          title: '机器学习实战：核心方法与应用', 
          teacher: '李明教授', 
          views: '8.9万播放', 
          rating: '4.5分', 
          duration: '60:25', 
          image: 'https://picsum.photos/200/120?random=17' 
        },
        { 
          id: 3, 
          title: '金融投资学：投资与理财', 
          teacher: '王静教授', 
          views: '15.5万播放', 
          rating: '4.3分', 
          duration: '54:16', 
          image: 'https://picsum.photos/200/120?random=18' 
        },
        { 
          id: 4, 
          title: '医学基础知识精讲', 
          teacher: '张伟教授', 
          views: '21.3万播放', 
          rating: '4.5分', 
          duration: '72:40', 
          image: 'https://picsum.photos/200/120?random=19' 
        },
        { 
          id: 5, 
          title: '机械设计原理与应用', 
          teacher: '陈明教授', 
          views: '9.4万播放', 
          rating: '4.5分', 
          duration: '45:30', 
          image: 'https://picsum.photos/200/120?random=20' 
        },
        { 
          id: 6, 
          title: '现代建筑设计与理论', 
          teacher: '刘芳教授', 
          views: '12.1万播放', 
          rating: '4.7分', 
          duration: '50:40', 
          image: 'https://picsum.photos/200/120?random=21' 
        }
      ]
    }
  },
  mounted() {
    // 添加滚动效果
    this.setupScrollEffects();
  },
  methods: {
    // 修复的跳转方法：添加防御性编程
    goToCourseDetail(course) {
      // 检查 course 是否存在
      if (!course) {
        console.warn('Course is undefined');
        alert('课程信息加载失败，请稍后再试');
        return;
      }
      
      // 检查是否有 id
      if (!course.id) {
        console.warn('Course missing id property', course);
        alert('课程信息不完整');
        // 可以给一个默认的 id 或跳转到列表页
        this.$router.push('/');
        return;
      }
      
      // 跳转到课程详情页
      this.$router.push(`/course/${course.id}`);
    },
    
    // 跳转到教师管理后台
    goToTeacherDashboard() {
      this.$router.push('/teacher-dashboard');
    },
    
    // 跳转到注册页面
    goToRegister() {
      this.$router.push('/register');
    },
    
    // 显示会员特权（临时实现）
    showMemberBenefits() {
      alert('会员特权页面开发中，敬请期待！\n\n会员特权包括：\n1. 无限制观看所有课程\n2. 专属学习路径\n3. 一对一导师辅导\n4. 优先参与线下活动\n5. 高清视频下载权限');
    },
    
    // 其他页面跳转方法
    goToLogin() {
      this.$router.push('/login');
    },
    
    goToPersonalInfo() {
      this.$router.push('/personal-information');
    },
    
    goToArticleManagement() {
      this.$router.push('/article-management');
    },
    
    setupScrollEffects() {
      // 师资团队左右箭头滚动
      const teacherContainer = document.querySelector('.overflow-x-auto');
      if (teacherContainer) {
        const leftBtn = teacherContainer.previousElementSibling;
        const rightBtn = teacherContainer.nextElementSibling;
        
        if (leftBtn && rightBtn) {
          leftBtn.addEventListener('click', () => {
            teacherContainer.scrollBy({ left: -300, behavior: 'smooth' });
          });
          
          rightBtn.addEventListener('click', () => {
            teacherContainer.scrollBy({ left: 300, behavior: 'smooth' });
          });
        }
      }
    }
  }
}
</script>

<style scoped>
/* 引入Tailwind中的自定义工具类 */
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* 视频卡片hover效果优化 */
.video-card-hover img {
  transition: transform 0.3s ease;
}
.video-card-hover:hover img {
  transform: scale(1.03);
}

/* 确保分类导航栏文字居中且宽度一致 */
.text-center.w-20 {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* 注册横幅黑色区块阴影增强 */
.bg-black\/30 {
  background-color: rgba(0, 0, 0, 0.3);
}

/* 确保所有课程卡片都有手型光标 */
.video-card-hover {
  cursor: pointer;
}

/* 限制行数 */
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

/* 视频相关工具类 */
.badge-hot {
  @apply absolute top-2 left-2 bg-red-500 text-white text-xs px-2 py-0.5 rounded z-10;
}
.badge-blue {
  @apply absolute top-2 left-2 bg-primary text-white text-xs px-2 py-0.5 rounded z-10;
}
.badge-green {
  @apply absolute top-2 left-2 bg-success text-white text-xs px-2 py-0.5 rounded z-10;
}
.badge-orange {
  @apply absolute top-2 left-2 bg-orange-500 text-white text-xs px-2 py-0.5 rounded z-10;
}
.video-time {
  @apply absolute bottom-2 right-2 bg-black/70 text-white text-xs px-1.5 py-0.5 rounded z-10;
}
.video-card-hover {
  @apply hover:shadow-md transition-shadow duration-200 cursor-pointer;
}

/* 师资卡片样式 */
.teacher-card {
  @apply flex flex-col items-center text-center w-44 bg-white border border-transparent rounded-lg p-4 shadow-sm hover:shadow-md transition-all duration-300;
}
.teacher-avatar-container {
  @apply w-36 h-52 bg-gray-200 rounded-lg overflow-hidden mb-5;
}
</style>