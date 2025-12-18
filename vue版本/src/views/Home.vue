<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <Header />
    
    <!-- B站样式分类导航栏 -->
    <nav class="bg-white py-4 px-6 sticky top-[5rem] z-20 border-b border-gray-200 shadow-sm">
      <div class="max-w-7xl mx-auto">
        <!-- 第一行分类 -->
        <div class="grid grid-cols-8 gap-3 mb-3">
          <a v-for="category in firstRowCategories" :key="category.id" 
             :href="category.link || '#'" 
             class="category-tag"
             @click.prevent="goToCategory(category.id)">
            {{ category.name }}
          </a>
        </div>
        <!-- 第二行分类 -->
        <div class="grid grid-cols-8 gap-3">
          <a v-for="category in secondRowCategories" :key="category.id" 
             :href="category.link || '#'" 
             class="category-tag"
             @click.prevent="goToCategory(category.id)">
            {{ category.name }}
          </a>
        </div>
      </div>
    </nav>

    <main class="flex-1" ref="mainContent">
      <!-- 主内容区域 -->
      <div class="max-w-7xl mx-auto px-4 py-6">
        <!-- 主推荐区域 -->
        <div class="flex flex-col lg:flex-row gap-6 mb-8">
          <!-- 左侧主推荐课程区块 - 宽度等于6个小视频宽度 -->
          <div class="lg:w-[calc(75%-1rem)]">
            <div class="relative rounded-lg overflow-hidden bg-white shadow-md">
              <!-- 视频轮播 -->
              <div class="relative" style="aspect-ratio: 16/9;">
                <div class="absolute inset-0 overflow-hidden">
                  <div ref="carouselTrack" class="flex transition-transform duration-500 ease-in-out h-full">
                    <div v-for="(course, index) in mainCourses" :key="course.id" 
                         class="w-full h-full flex-shrink-0 relative cursor-pointer"
                         @click="goToCourseDetail(course)"
                         :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
                      <img :src="course.image" :alt="course.title" class="w-full h-full object-cover">
                      <!-- 视频信息遮罩 -->
                      <div class="absolute bottom ;
                     0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
                        <h3 class="text-white text-xl font-semibold mb-2">{{ course.title }}</h3>
                        <div class="flex items-center text-gray-300 text-sm">
                          <span class="flex items-center mr-4">
                            <i class="fa fa-play mr-1 text-xs"></i>
                            {{ course.views }}
                          </span>
                          <span class="flex items-center mr-4">
                            <i class="fa fa-comment mr-1 text-xs"></i>
                            {{ course.comments }}
                          </span>
                          <span>{{ course.duration }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- 轮播指示器 -->
                <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
                  <button v-for="(_, index) in mainCourses" :key="index"
                          @click.stop="goToSlide(index)"
                          :class="[
                            'w-2 h-2 rounded-full transition-all',
                            currentSlide === index ? 'bg-white w-4' : 'bg-white/50'
                          ]">
                  </button>
                </div>
                
                <!-- 左右切换按钮 -->
                <button @click.stop="prevSlide" 
                        class="absolute left-4 top-1/2 transform -translate-y-1/2 w-10 h-10 rounded-full bg-black/30 hover:bg-black/50 text-white flex items-center justify-center transition-all">
                  <i class="fa fa-angle-left"></i>
                </button>
                <button @click.stop="nextSlide" 
                        class="absolute right-4 top-1/2 transform -translate-y-1/2 w-10 h-10 rounded-full bg-black/30 hover:bg-black/50 text-white flex items-center justify-center transition-all">
                  <i class="fa fa-angle-right"></i>
                </button>
              </div>
            </div>
          </div>

          <!-- 右侧副推荐课程区块 - 宽度等于4个小视频宽度 -->
          <div class="lg:w-[calc(25%-1rem)] relative">
            <!-- 换一换按钮（在区块右侧边缘） -->
            <div class="absolute -right-4 top-0 z-10">
              <button @click="refreshRecommendations" 
                      class="flex flex-col items-center justify-center w-10 h-20 bg-white rounded-l-lg shadow-md hover:shadow-lg transition-all group border border-gray-200 border-r-0 hover:border-primary/30">
                <i class="fa fa-refresh text-gray-600 text-sm mb-1 group-hover:text-primary transition-colors"></i>
                <span class="text-xs text-gray-600 group-hover:text-primary transition-colors">换一换</span>
              </button>
            </div>
            
            <!-- 2排2列布局 - 与无限推荐区块完全一致的样式 -->
            <div class="grid grid-cols-2 gap-4 h-full">
              <div v-for="course in sideCourses" :key="course.id" 
                   class="bg-white rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow group video-card" 
                   @click="goToCourseDetail(course)">
                <!-- 视频封面 - 与无限推荐区块相同大小 -->
                <div class="relative" style="aspect-ratio: 16/9;">
                  <img :src="course.image" :alt="course.title" 
                       class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                  <span class="absolute bottom-2 right-2 bg-black/70 text-white text-xs px-1.5 py-0.5 rounded">
                    {{ course.duration }}
                  </span>
                  <!-- 播放按钮 -->
                  <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/20">
                    <div class="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                      <i class="fa fa-play text-white text-lg"></i>
                    </div>
                  </div>
                </div>
                <!-- 视频信息 - 与无限推荐区块完全一致 -->
                <div class="p-3">
                  <h4 class="text-sm font-medium line-clamp-2 mb-2 group-hover:text-primary transition-colors">{{ course.title }}</h4>
                  <div class="flex items-center justify-between text-xs text-gray-500 mb-1">
                    <div class="flex items-center space-x-3">
                      <span class="flex items-center">
                        <i class="fa fa-play mr-1 text-xs"></i>
                        {{ course.views }}
                      </span>
                      <span class="flex items-center">
                        <i class="fa fa-comment mr-1 text-xs"></i>
                        {{ course.comments }}
                      </span>
                    </div>
                    <span>{{ course.timeAgo }}</span>
                  </div>
                  <div class="text-xs text-gray-400">{{ course.teacher }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 无限视频推荐 -->
        <div class="mb-8">
          <!-- 视频网格 - 一行5个 -->
          <div ref="videoGrid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
            <div v-for="course in videoCourses" :key="course.id" 
                 class="bg-white rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow group video-card"
                 @click="goToCourseDetail(course)">
              <!-- 视频封面 - 16:9比例 -->
              <div class="relative" style="aspect-ratio: 16/9;">
                <img :src="course.image" :alt="course.title" 
                     class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                <span class="absolute bottom-2 right-2 bg-black/70 text-white text-xs px-1.5 py-0.5 rounded">
                  {{ course.duration }}
                </span>
                <!-- 播放按钮 -->
                <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/20">
                  <div class="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                    <i class="fa fa-play text-white text-lg"></i>
                  </div>
                </div>
              </div>
              <!-- 视频信息 -->
              <div class="p-3">
                <h4 class="text-sm font-medium line-clamp-2 mb-2 group-hover:text-primary transition-colors">{{ course.title }}</h4>
                <div class="flex items-center justify-between text-xs text-gray-500 mb-1">
                  <div class="flex items-center space-x-3">
                    <span class="flex items-center">
                      <i class="fa fa-play mr-1 text-xs"></i>
                      {{ course.views }}
                    </span>
                    <span class="flex items-center">
                      <i class="fa fa-comment mr-1 text-xs"></i>
                      {{ course.comments }}
                    </span>
                  </div>
                  <span>{{ course.timeAgo }}</span>
                </div>
                <div class="text-xs text-gray-400">{{ course.teacher }}</div>
              </div>
            </div>
          </div>
          
          <!-- 加载提示 -->
          <div v-if="loading" class="text-center py-8">
            <div class="inline-flex items-center justify-center space-x-2">
              <div class="w-3 h-3 bg-primary rounded-full animate-pulse"></div>
              <div class="w-3 h-3 bg-primary rounded-full animate-pulse" style="animation-delay: 0.2s"></div>
              <div class="w-3 h-3 bg-primary rounded-full animate-pulse" style="animation-delay: 0.4s"></div>
            </div>
            <div class="text-gray-500 text-sm mt-2">正在加载更多课程...</div>
          </div>
          
          <!-- 底部提示 -->
          <div v-if="!hasMore && videoCourses.length > 0" class="text-center py-12 text-gray-500 text-sm">
            <div class="flex flex-col items-center">
              <i class="fa fa-check-circle text-green-500 text-xl mb-3"></i>
              <div>已经到底了，看看其他内容吧~</div>
            </div>
          </div>
        </div>
      </div>
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
      // 当前用户信息
      currentUser: null,
      userId: null,
      
      // B站样式分类（2x8格式）
      firstRowCategories: [
        { id: 1, name: '精彩课程', link: '#' },
        { id: 2, name: '编程开发', link: '#' },
        { id: 3, name: '人工智能', link: '#' },
        { id: 4, name: '数据科学', link: '#' },
        { id: 5, name: '商业管理', link: '#' },
        { id: 6, name: '设计创意', link: '#' },
        { id: 7, name: '市场营销', link: '#' },
        { id: 8, name: '语言学习', link: '#' }
      ],
      secondRowCategories: [
        { id: 9, name: '职业技能', link: '#' },
        { id: 10, name: '考研考证', link: '#' },
        { id: 11, name: '生活兴趣', link: '#' },
        { id: 12, name: '职场提升', link: '#' },
        { id: 13, name: '创业指导', link: '#' },
        { id: 14, name: '教师成长', link: '#' },
        { id: 15, name: '学生专区', link: '#' },
        { id: 16, name: '更多分类', link: '#' }
      ],
      
      // 轮播图相关
      currentSlide: 0,
      autoSlideInterval: null,
      
      // 主推荐课程（轮播）- 根据用户ID推荐不同类型
      mainCourses: [],
      
      // 右侧副推荐课程（2排2列共4个）
      sideCourses: [],
      
      // 视频推荐列表
      videoCourses: [],
      page: 1,
      pageSize: 20,
      hasMore: true,
      loading: false,
      isLoadingMore: false,
      scrollObserver: null,
      lastScrollPosition: 0,
      loadingTriggered: false,
      
      // 与Category页面一致的课程数据
      allCourses: []
    }
  },
  created() {
    this.loadCurrentUser()
  },
  mounted() {
    this.startAutoSlide();
    this.loadVideos();
    this.$nextTick(() => {
      this.setupScrollObserver();
    });
  },
  beforeUnmount() {
    this.stopAutoSlide();
    if (this.scrollObserver) {
      this.scrollObserver.disconnect();
    }
  },
  methods: {
    // 加载当前用户信息
    loadCurrentUser() {
      const userData = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
      if (userData) {
        try {
          this.currentUser = JSON.parse(userData)
          this.userId = this.currentUser.id
          console.log('当前用户ID:', this.userId)
          // 根据用户ID初始化推荐课程
          this.initRecommendations()
        } catch (error) {
          console.error('解析用户数据失败:', error)
          this.loadDefaultRecommendations()
        }
      } else {
        console.log('用户未登录，使用默认推荐')
        this.loadDefaultRecommendations()
      }
    },
    
    // 初始化推荐课程
    initRecommendations() {
      if (!this.userId) {
        this.loadDefaultRecommendations()
        return
      }
      
      // 根据用户ID的最后一位数字确定推荐类型
      const lastDigit = parseInt(this.userId.toString().slice(-1)) || 1
      const categoryType = lastDigit % 3  // 0: 计算机, 1: 商业管理, 2: 设计创意
      
      console.log(`用户ID: ${this.userId}, 最后一位: ${lastDigit}, 推荐类型: ${categoryType}`)
      
      // 生成课程数据（与Category页面一致）
      this.generateCourses()
      
      // 设置主推荐课程
      this.setMainCourses(categoryType)
      
      // 设置侧边推荐课程
      this.setSideCourses(categoryType)
    },
    
    // 生成模拟课程数据 - 与Category页面完全一致
    generateCourses() {
      const categories = [
        '编程开发', '人工智能', '数据科学', '商业管理', '设计创意',
        '市场营销', '语言学习', '职业技能', '考研考证', '生活兴趣',
        '职场提升', '创业指导', '教师成长', '学生专区'
      ]

      const difficulties = ['beginner', 'intermediate', 'advanced']
      const prices = ['free', 'paid']

      // 教师映射，确保与Category页面的教师名称一致
      const teachers = ['张老师', '李教授', '王工程师', '刘老师', '陈教授', '赵导师', '李经理', '王总监', '张营销总监', '陈财务顾问', '刘HR总监', '张设计师', '李创意总监', '王视频制作人', '陈3D艺术家', '刘品牌设计师']

      // 生成200个课程 - 确保数据有规律
      this.allCourses = Array.from({ length: 200 }, (_, index) => {
        const categoryName = categories[index % categories.length]
        const difficulty = difficulties[index % difficulties.length]
        const price = prices[index % prices.length]

        // 根据分类名称映射到与Category页面一致的category字段
        let categoryKey = 'computer' // 默认
        if (categoryName.includes('商业') || categoryName.includes('市场') || categoryName.includes('创业') || categoryName.includes('职业') || categoryName.includes('职场')) {
          categoryKey = 'business'
        } else if (categoryName.includes('设计')) {
          categoryKey = 'design'
        }

        // 根据分类选择教师
        let teacher;
        if (categoryKey === 'computer') {
          teacher = ['张老师', '李教授', '王工程师', '刘老师', '陈教授'][index % 5]
        } else if (categoryKey === 'business') {
          teacher = ['李经理', '王总监', '张营销总监', '陈财务顾问', '刘HR总监'][index % 5]
        } else if (categoryKey === 'design') {
          teacher = ['张设计师', '李创意总监', '王视频制作人', '陈3D艺术家', '刘品牌设计师'][index % 5]
        } else {
          teacher = teachers[index % teachers.length]
        }

        // 生成有规律的课程数据
        const title = this.getCourseTitle(categoryKey, difficulty)
        
        // 1. 时间戳：越新的课程ID越大（模拟真实时间顺序）
        // 200个课程分布在过去30天内
        const daysAgo = 30 - Math.floor(index * 30 / 200) // 从30天前到1天前
        const createdAt = new Date(Date.now() - daysAgo * 24 * 60 * 60 * 1000)
        
        // 2. 播放量：有规律地分布（热度=播放量）
        // 热门课程播放量高，新课程播放量相对较低
        const baseViews = 5000 + (200 - index) * 100 // ID越小（越老）播放量越高
        const randomFactor = Math.random() * 0.5 + 0.75 // 0.75-1.25的随机因子
        const viewsNum = Math.floor(baseViews * randomFactor)
        
        // 3. 评论数和评分
        const commentsNum = Math.floor(viewsNum * 0.05) + Math.floor(Math.random() * 100)
        const rating = (3.5 + Math.random() * 1.5).toFixed(1) // 3.5-5.0

        return {
          id: index + 1,
          title: title,
          teacher: teacher,
          views: `${(viewsNum / 10000).toFixed(1)}万播放`, // 转换为"万播放"格式
          comments: `${commentsNum}`,
          duration: `${Math.floor(Math.random() * 40 + 10)}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`,
          timeAgo: this.getTimeAgo(daysAgo), // 使用计算出的天数
          category: categoryKey,
          categoryName: categoryName,
          difficulty: difficulty,
          price: price,
          rating: rating,
          // 热度分数 = 播放量（简化）
          hotScore: viewsNum,
          createdAt: createdAt.toISOString(),
          // 用于排序的原始数值
          rawViews: viewsNum, // 播放量就是热度
          rawComments: commentsNum,
          rawCreatedAt: createdAt.getTime(),
          image: `https://picsum.photos/400/225?random=${index + 1000}`,
          description: `${title} - 由${teacher}主讲，课程评分${rating}分，${daysAgo}天前发布，已有${viewsNum}次播放`
        }
      })
    },
    
    // 时间显示格式化方法 - 与Category页面一致
    getTimeAgo(days) {
      if (days === 0) return '今天'
      if (days === 1) return '昨天'
      if (days < 7) return `${days}天前`
      if (days < 30) return `${Math.floor(days / 7)}周前`
      if (days < 365) return `${Math.floor(days / 30)}个月前`
      return `${Math.floor(days / 365)}年前`
    },
    
    // 根据分类和难度生成课程标题 - 与Category页面一致
    getCourseTitle(categoryKey, difficulty) {
      const titles = {
        computer: {
          beginner: [
            'Python入门教程', 
            'Java基础编程', 
            'HTML/CSS网页设计',
            'Spring Boot企业级开发',
            'React Hooks深度解析'
          ],
          intermediate: [
            'TypeScript高级技巧',
            'Docker容器化实践',
            '微服务架构设计',
            'Redis缓存优化',
            'MySQL性能调优'
          ],
          advanced: [
            'Web安全攻防实战',
            '深度学习实战：从零搭建AI模型',
            '机器学习算法精讲与实战',
            '数据结构与算法面试',
            'Python自动化办公'
          ]
        },
        business: {
          beginner: [
            '管理学基础', 
            '市场营销入门', 
            '财务管理基础',
            '领导力与团队管理',
            '商业模式创新'
          ],
          intermediate: [
            '战略管理', 
            '组织行为学', 
            '人力资源管理',
            '财务报表分析',
            '客户关系管理'
          ],
          advanced: [
            '企业战略规划', 
            '领导力发展', 
            '商业创新管理',
            '商业分析实战：数据驱动决策',
            '项目管理PMP认证全攻略'
          ]
        },
        design: {
          beginner: [
            'UI/UX设计从入门到精通',
            '平面设计创意与实战',
            '视频剪辑与特效制作',
            '色彩理论与应用',
            '字体设计原理'
          ],
          intermediate: [
            '包装设计实战',
            'UI交互动效',
            '品牌视觉系统',
            '海报设计创意',
            '网页设计规范'
          ],
          advanced: [
            '移动端设计适配',
            '3D建模与动画设计',
            '品牌设计全流程',
            '插画设计与创作',
            '摄影构图与后期'
          ]
        }
      }

      const categoryTitles = titles[categoryKey] || titles.computer
      const difficultyTitles = categoryTitles[difficulty] || categoryTitles.beginner
      return difficultyTitles[Math.floor(Math.random() * difficultyTitles.length)]
    },
    
    // 设置主推荐课程
    setMainCourses(categoryType) {
      const categories = {
        0: 'computer', // 计算机相关
        1: 'business', // 商业管理相关
        2: 'design'    // 设计创意相关
      }
      
      const currentCategory = categories[categoryType] || 'computer'
      
      // 从allCourses中筛选出当前类别的课程，取前4个作为主推荐
      const categoryCourses = this.allCourses.filter(course => course.category === currentCategory)
      
      // 选择热度最高的4个课程（播放量最高）
      const topCourses = categoryCourses
        .sort((a, b) => b.rawViews - a.rawViews) // 按播放量降序
        .slice(0, 4)
        .map(course => ({
          ...course,
          image: course.image.replace('400/225', '1200/675') // 使用大图
        }))
      
      this.mainCourses = topCourses
    },
    
    // 设置侧边推荐课程
    setSideCourses(categoryType) {
      const categories = {
        0: 'computer', // 计算机相关
        1: 'business', // 商业管理相关
        2: 'design'    // 设计创意相关
      }
      
      const currentCategory = categories[categoryType] || 'computer'
      
      // 从allCourses中筛选出当前类别的课程
      const categoryCourses = this.allCourses.filter(course => course.category === currentCategory)
      
      // 选择播放量排名5-8的课程作为侧边推荐
      const sideCourses = categoryCourses
        .sort((a, b) => b.rawViews - a.rawViews) // 按播放量降序
        .slice(4, 8) // 取5-8名
        
      this.sideCourses = sideCourses
    },
    
    // 加载默认推荐（用户未登录时）
    loadDefaultRecommendations() {
      // 生成课程数据
      this.generateCourses()
      this.setMainCourses(0) // 默认显示计算机相关
      this.setSideCourses(0)
    },
    
    // 轮播图方法
    startAutoSlide() {
      this.autoSlideInterval = setInterval(() => {
        this.nextSlide();
      }, 5000);
    },
    
    stopAutoSlide() {
      if (this.autoSlideInterval) {
        clearInterval(this.autoSlideInterval);
        this.autoSlideInterval = null;
      }
    },
    
    nextSlide() {
      this.currentSlide = (this.currentSlide + 1) % this.mainCourses.length;
    },
    
    prevSlide() {
      this.currentSlide = this.currentSlide === 0 ? this.mainCourses.length - 1 : this.currentSlide - 1;
    },
    
    goToSlide(index) {
      this.currentSlide = index;
    },
    
    // 跳转到分类页面
    goToCategory(categoryId) {
      this.$router.push({
        name: 'Category',
        params: { categoryId: categoryId }
      })
    },
    
    // 跳转到课程详情
    goToCourseDetail(course) {
      if (!course || !course.id) {
        console.warn('课程信息不完整')
        return
      }

      // 保存完整的课程信息到 localStorage
      const courseData = {
        id: course.id,
        title: course.title,
        teacher: course.teacher,
        views: course.views,
        comments: course.comments,
        duration: course.duration,
        timeAgo: course.timeAgo,
        image: course.image,
        category: course.category || 'computer',
        description: course.description || `${course.title} - 精品课程，由${course.teacher}主讲`
      }

      console.log('保存到 localStorage 的课程数据:', courseData) // 调试用
      localStorage.setItem('selectedCourse', JSON.stringify(courseData))

      this.$router.push({
        name: 'VideoPlayer',
        params: { 
          courseId: course.id,
          category: course.category || 'computer'
        }
      })
    },
    
    // 刷新推荐课程
    refreshRecommendations() {
      // 保存当前滚动位置
      this.lastScrollPosition = window.scrollY;
      
      // 重新获取当前用户信息
      this.loadCurrentUser();
      
      // 刷新视频推荐
      this.page = 1;
      this.hasMore = true;
      this.loadVideos(true);
      
      // 使用更安全的消息提示方式
      this.showMessage('推荐已刷新', 'success');
    },
    
    // 加载视频列表
    async loadVideos(isRefresh = false) {
      if ((this.loading && !isRefresh) || (!isRefresh && !this.hasMore)) return;
      
      this.loading = true;
      
      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // 根据用户ID确定类别
      const lastDigit = this.userId ? parseInt(this.userId.toString().slice(-1)) % 3 : 0;
      const categoryTypes = ['computer', 'business', 'design']
      const currentCategory = categoryTypes[lastDigit] || 'computer'
      
      // 从allCourses中筛选出当前类别的课程
      const categoryCourses = this.allCourses.filter(course => course.category === currentCategory)
      
      // 计算起始和结束位置
      const start = (this.page - 1) * this.pageSize
      const end = start + this.pageSize
      
      // 获取当前页的课程
      let newVideos
      if (this.page === 1 || isRefresh) {
        // 如果是第一页或刷新，从热度最高的开始
        newVideos = categoryCourses
          .sort((a, b) => b.rawViews - a.rawViews) // 按播放量降序
          .slice(start, end)
      } else {
        // 如果是加载更多，按时间降序（最新的在前）
        newVideos = categoryCourses
          .sort((a, b) => b.rawCreatedAt - a.rawCreatedAt) // 按时间降序
          .slice(start, end)
      }
      
      if (this.page === 1 || isRefresh) {
        this.videoCourses = newVideos;
      } else {
        this.videoCourses = [...this.videoCourses, ...newVideos];
      }
      
      // 判断是否还有更多数据
      const totalCourses = categoryCourses.length
      const loadedCourses = this.page * this.pageSize
      this.hasMore = loadedCourses < totalCourses
      
      this.loading = false;
      this.loadingTriggered = false;
      
      // 如果是刷新操作，保持滚动位置
      if (isRefresh) {
        this.$nextTick(() => {
          window.scrollTo(0, this.lastScrollPosition);
        });
      }
    },
    
    // 设置滚动监听
    setupScrollObserver() {
      const options = {
        root: null,
        rootMargin: '200px', // 提前200px触发
        threshold: 0.1
      };
      
      this.scrollObserver = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && this.hasMore && !this.loading && !this.loadingTriggered) {
          this.loadingTriggered = true;
          this.page++;
          this.loadVideos();
        }
      }, options);
      
      // 创建并观察底部哨兵元素
      const sentinel = document.createElement('div');
      sentinel.id = 'scroll-sentinel';
      sentinel.className = 'h-1 w-full';
      sentinel.style.cssText = 'opacity: 0; pointer-events: none;';
      
      this.$nextTick(() => {
        const mainContent = this.$refs.mainContent;
        if (mainContent) {
          mainContent.appendChild(sentinel);
          this.scrollObserver.observe(sentinel);
        }
      });
    },
    
    // 显示消息提示
    showMessage(text, type = 'success') {
      // 可以使用UI库的消息提示，这里用简单的alert替代
      alert(text);
    }
  }
}
</script>

<style scoped>
/* B站样式分类标签 */
.category-tag {
  @apply inline-flex items-center justify-center px-3 py-2 text-sm font-medium text-gray-800 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer text-center;
  min-height: 36px;
}

/* 隐藏滚动条 */
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
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

/* 视频卡片统一样式 */
.video-card {
  /* 确保所有视频卡片样式完全一致 */
  transition: all 0.3s ease;
}

/* 阴影效果 */
.shadow-md {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.shadow-sm {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

/* 换一换按钮样式 */
.refresh-button {
  transition: all 0.3s ease;
}

.refresh-button:hover {
  transform: translateX(-2px);
  box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.1);
}

/* 响应式调整 */
@media (max-width: 1024px) {
  /* 在小屏幕上调整宽度 */
  .lg\:w-\[calc\(75\%-1rem\)\], .lg\:w-\[calc\(25\%-1rem\)\] {
    width: 100%;
  }
  
  /* 在小屏幕上调整换一换按钮位置 */
  .absolute.-right-4.top-0 {
    position: relative;
    right: 0;
    top: 0;
    margin-top: 1rem;
    margin-bottom: 1rem;
    display: flex;
    justify-content: center;
  }
  
  .absolute.-right-4.top-0 button {
    border-radius: 0.5rem;
    border: 1px solid #e5e7eb;
    width: 80px;
    height: 40px;
    flex-direction: row;
    gap: 0.5rem;
  }
  
  /* 在小屏幕上调整右侧副推荐区块的布局 */
  .lg\:w-\[calc\(25\%-1rem\)\] .grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

/* 视频卡片hover效果 */
.group:hover .group-hover\:scale-105 {
  transform: scale(1.05);
}

/* 播放按钮动画 */
.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}

/* 文字颜色过渡 */
.group:hover .group-hover\:text-primary {
  color: var(--primary-color, #3b82f6);
}

/* 加载动画 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 1.5s ease-in-out infinite;
}

/* 确保右侧副推荐区块与无限推荐区块的视频大小完全一致 */
.lg\:w-\[calc\(25\%-1rem\)\] .video-card {
  width: 100%;
}

.lg\:w-\[calc\(25\%-1rem\)\] .video-card > div:first-child {
  aspect-ratio: 16/9;
}

.lg\:w-\[calc\(25\%-1rem\)\] .video-card .p-3 {
  padding: 0.75rem;
}

/* 左侧主推荐区块宽度计算：6个小视频宽度 */
.lg\:w-\[calc\(75\%-1rem\)\] {
  width: calc(6 * (100% / 10) - 1rem); /* 6/10 = 60%，但为了匹配6个小视频，调整为75% */
}

/* 右侧副推荐区块宽度计算：4个小视频宽度 */
.lg\:w-\[calc\(25\%-1rem\)\] {
  width: calc(4 * (100% / 10) - 1rem); /* 4/10 = 40%，但为了匹配4个小视频，调整为25% */
}

/* 大屏幕上的精确布局 */
@media (min-width: 1280px) {
  .lg\:w-\[calc\(75\%-1rem\)\] {
    width: calc(6 * (100% / 10) - 1rem);
  }
  
  .lg\:w-\[calc\(25\%-1rem\)\] {
    width: calc(4 * (100% / 10) - 1rem);
  }
}
</style>