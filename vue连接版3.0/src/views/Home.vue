<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <Header />
      <!-- B站样式分类导航栏 -->
      <nav class="bg-white py-3 px-6 sticky top-[5rem] z-20 border-b border-gray-200 shadow-sm">
        <div class="max-w-7xl mx-auto">
          <!-- 第一行分类 - 删除了推荐按钮 -->
          <div class="grid grid-cols-7 gap-3">
            <a v-for="category in categories" :key="category.id" 
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
                    <!-- 轮播图容器 -->
                    <div class="flex transition-transform duration-500 ease-in-out h-full" 
                        :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
                      <div v-for="(course, index) in mainCourses" :key="course.id" 
                          class="w-full h-full flex-shrink-0 relative cursor-pointer"
                          @click="goToCourseDetail(course)">
                        <img :src="course.image" :alt="course.title" class="w-full h-full object-cover">
                        <!-- 视频信息遮罩 -->
                        <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
                          <h3 class="text-white text-xl font-semibold mb-2">{{ course.title }}</h3>
                          <div class="flex items-center text-gray-300 text-sm flex-wrap">
                            <span class="flex items-center mr-4">
                              <i class="fa fa-play mr-1 text-xs"></i>
                              {{ course.views }}
                            </span>
                            <span v-if="course.predictedRating" class="flex items-center mr-4">
                              <i class="fa fa-star mr-1 text-xs text-yellow-400"></i>
                              {{ course.predictedRating.toFixed(1) }}
                            </span>
                            <span class="flex items-center mr-4">
                              <i class="fa fa-comment mr-1 text-xs"></i>
                              {{ course.comments }}
                            </span>
                            <span>{{ course.duration }}</span>
                          </div>
                          <!-- 显示推荐标签 -->
                          <div v-if="course.viewedBadge" class="mt-2">
                            <span :class="['text-xs px-2 py-0.5 rounded-full', 
                                          course.viewedClass === 'viewed' ? 'bg-blue-500' : 'bg-orange-500']">
                              {{ course.viewedBadge }}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 轮播指示器 -->
                  <div v-if="mainCourses.length > 1" class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
                    <button v-for="(_, index) in mainCourses" :key="index"
                            @click.stop="goToSlide(index)"
                            :class="[
                              'w-2 h-2 rounded-full transition-all',
                              currentSlide === index ? 'bg-white w-4' : 'bg-white/50'
                            ]">
                    </button>
                  </div>
                  
                  <!-- 左右切换按钮 -->
                  <button v-if="mainCourses.length > 1" @click.stop="prevSlide" 
                          class="absolute left-4 top-1/2 transform -translate-y-1/2 w-10 h-10 rounded-full bg-black/30 hover:bg-black/50 text-white flex items-center justify-center transition-all">
                    <i class="fa fa-angle-left"></i>
                  </button>
                  <button v-if="mainCourses.length > 1" @click.stop="nextSlide" 
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

          <!-- 推荐视频列表 -->
          <div class="mb-8">
            <!-- 标题区域 -->
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold">
                推荐课程
                <span class="text-sm font-normal text-gray-500 ml-2">
                  (共 {{ recommendedCourses.length }} 个)
                </span>
              </h2>
              
              <!-- 状态显示 -->
              <div class="flex items-center space-x-4">
                <div v-if="isLoadingRecommend" class="flex items-center text-blue-500 text-sm">
                  <i class="fa fa-spinner fa-spin mr-2"></i>
                  正在加载推荐...
                </div>
                
                <div v-else-if="recommendedCourses.length === 0" class="text-gray-500 text-sm">
                  暂无推荐课程
                </div>
                
                <div v-else class="text-gray-500 text-sm">
                  已为您推荐 {{ recommendedCourses.length }} 个课程
                </div>
                
                <button @click="refreshRecommendations" 
                        class="px-3 py-1.5 text-sm bg-blue-50 text-blue-600 rounded hover:bg-blue-100 transition-colors">
                  <i class="fa fa-refresh mr-1"></i>刷新推荐
                </button>
              </div>
            </div>
            
            <!-- 视频网格 - 一行5个 -->
            <div v-if="videoCourses.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
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
                  <!-- 难度标签 -->
                  <div v-if="course.difficulty" class="absolute top-2 left-2 bg-blue-500 text-white text-xs px-2 py-0.5 rounded">
                    难度: {{ '★'.repeat(course.difficulty) }}
                  </div>
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
                  <div class="flex justify-between items-center">
                    <div class="text-xs text-gray-400">{{ course.teacher }}</div>
                    <div v-if="course.predictedRating" class="flex items-center text-yellow-500 text-xs">
                      <i class="fa fa-star mr-0.5"></i>
                      {{ course.predictedRating.toFixed(1) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 空状态 -->
            <div v-else-if="!isLoadingRecommend" class="text-center py-12 bg-gray-50 rounded-lg">
              <div class="flex flex-col items-center">
                <i class="fa fa-film text-gray-400 text-4xl mb-4"></i>
                <h3 class="text-gray-600 font-medium mb-2">暂无更多推荐课程</h3>
                <p class="text-gray-500 text-sm mb-6 max-w-md">
                  推荐系统暂时没有为您找到更多课程，<br>
                  您可以刷新试试或浏览其他分类。
                </p>
                <button @click="refreshRecommendations" 
                        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">
                  <i class="fa fa-refresh mr-2"></i>刷新推荐
                </button>
              </div>
            </div>
            
            <!-- 加载提示 -->
            <div v-if="isLoadingRecommend" class="text-center py-8">
              <div class="inline-flex items-center justify-center space-x-2">
                <div class="w-3 h-3 bg-primary rounded-full animate-pulse"></div>
                <div class="w-3 h-3 bg-primary rounded-full animate-pulse" style="animation-delay: 0.2s"></div>
                <div class="w-3 h-3 bg-primary rounded-full animate-pulse" style="animation-delay: 0.4s"></div>
              </div>
              <div class="text-gray-500 text-sm mt-2">正在为您推荐课程...</div>
            </div>
            
            <!-- 推荐统计 -->
            <div v-if="recommendedCourses.length > 0 && !isLoadingRecommend" class="mt-6 pt-6 border-t text-center text-gray-500 text-sm">
              <div class="flex flex-wrap justify-center gap-4">
                <div class="flex items-center">
                  <span class="w-3 h-3 bg-blue-500 rounded-full mr-2"></span>
                  主轮播图: {{ mainCourses.length }} 个
                </div>
                <div class="flex items-center">
                  <span class="w-3 h-3 bg-green-500 rounded-full mr-2"></span>
                  右侧推荐: {{ sideCourses.length }} 个
                </div>
                <div class="flex items-center">
                  <span class="w-3 h-3 bg-purple-500 rounded-full mr-2"></span>
                  推荐列表: {{ videoCourses.length }} 个
                </div>
                <div class="flex items-center font-medium">
                  <i class="fa fa-chart-bar mr-2"></i>
                  总计: {{ recommendedCourses.length }} 个推荐
                </div>
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
  import recommendService from '@/service/recommend.js'

  export default {
    name: 'Home',
    components: {
      Header,
      Footer
    },
    
    data() {
      return {
        // B站样式分类（2x8格式）
        categories: [
          { id: 1, name: '编程开发', link: '#' },
          { id: 2, name: '人工智能', link: '#' },
          { id: 3, name: '数据科学', link: '#' },
          { id: 4, name: '商业管理', link: '#' },
          { id: 5, name: '设计创意', link: '#' },
          { id: 6, name: '市场营销', link: '#' },
          { id: 7, name: '语言学习', link: '#' }
        ],
        
        // 轮播图相关
        currentSlide: 0,
        autoSlideInterval: null,
        
        // 主推荐课程（轮播）- 大小为6个小视频的宽度
        mainCourses: [
          { 
            id: 1, 
            title: '深度学习实战：从零搭建AI模型', 
            teacher: '李明教授', 
            views: '25.6万播放', 
            comments: '1.2万',
            duration: '12:54:00', 
            image: 'https://picsum.photos/1200/675?random=1'
          },
          { 
            id: 2, 
            title: 'Python数据分析实战：从入门到精通', 
            teacher: '张老师', 
            views: '18.3万播放', 
            comments: '8.5千',
            duration: '15:20:00', 
            image: 'https://picsum.photos/1200/675?random=22'
          },
          { 
            id: 3, 
            title: 'Web全栈开发：React + Node.js实战', 
            teacher: '王工程师', 
            views: '22.1万播放', 
            comments: '1.5万',
            duration: '20:10:00', 
            image: 'https://picsum.photos/1200/675?random=23'
          },
          { 
            id: 4, 
            title: '机器学习算法精讲与实战', 
            teacher: '陈教授', 
            views: '30.5万播放', 
            comments: '2.3万',
            duration: '18:45:00', 
            image: 'https://picsum.photos/1200/675?random=24'
          }
        ],
        
        // 右侧副推荐课程（2排2列共4个）
        sideCourses: [
          { 
            id: 5, 
            title: 'Java核心技术精讲', 
            teacher: '刘老师', 
            views: '8.3万播放', 
            comments: '3.2千',
            duration: '45:20', 
            timeAgo: '3天前',
            image: 'https://picsum.photos/400/225?random=25' 
          },
          { 
            id: 6, 
            title: '前端框架Vue3实战', 
            teacher: '赵工程师', 
            views: '12.1万播放', 
            comments: '5.6千',
            duration: '38:45', 
            timeAgo: '5天前',
            image: 'https://picsum.photos/400/225?random=26' 
          },
          { 
            id: 7, 
            title: '数据结构与算法面试', 
            teacher: '李教授', 
            views: '15.8万播放', 
            comments: '4.8千',
            duration: '52:10', 
            timeAgo: '1天前',
            image: 'https://picsum.photos/400/225?random=27' 
          },
          { 
            id: 8, 
            title: 'Python自动化办公', 
            teacher: '王老师', 
            views: '9.6万播放', 
            comments: '2.9千',
            duration: '41:25', 
            timeAgo: '2天前',
            image: 'https://picsum.photos/400/225?random=28' 
          }
        ],
        
        // 视频推荐列表
        videoCourses: [],
        
        recommendedCourses: [],      // 从API获取的推荐课程
        userId: '',                  // 当前用户ID（从本地存储获取）
        isLoadingRecommend: false,   // 推荐加载状态
        recommendError: null,           // 错误信息
        isRecommendEmpty: false,       // 是否无推荐
        recommendRetryCount: 0,        // 重试次数
        isRefreshing: false,
      }
    },
    mounted() {
      this.startAutoSlide();
      this.loadUserRecommendations();
    },
    beforeUnmount() {
      this.stopAutoSlide();
    },
    methods: {
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
      
      // 刷新推荐课程
      refreshRecommendations() {
        console.log('刷新推荐');
        
        // 防止重复点击
        if (this.isRefreshing) return;
        
        this.isRefreshing = true;
        
        // 显示刷新提示
        this.showMessage('正在刷新推荐...', 'info');
        
        // 重新加载推荐
        this.loadUserRecommendations();
        
        // 重置刷新状态
        setTimeout(() => {
          this.isRefreshing = false;
        }, 2000);
      },
      
      // 获取随机标题
      getRandomTitle() {
        const titles = [
          'Spring Boot企业级开发',
          'React Hooks深度解析',
          'TypeScript高级技巧',
          'Docker容器化实践',
          '微服务架构设计',
          'Redis缓存优化',
          'MySQL性能调优',
          'Web安全攻防实战',
          '小程序云开发',
          'Flutter跨平台开发'
        ];
        return titles[Math.floor(Math.random() * titles.length)];
      },
      
      getRandomMainTitle() {
        const titles = [
          '全栈工程师成长之路',
          '人工智能算法实战',
          '大数据处理与分析',
          '云计算架构设计',
          'DevOps实践指南'
        ];
        return titles[Math.floor(Math.random() * titles.length)];
      },
      
      // 数组洗牌
      shuffleArray(array) {
        const newArray = [...array];
        for (let i = newArray.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
        }
        return newArray;
      },
      
      // 加载视频列表
      async loadVideos(isRefresh = false) {
        if ((this.loading && !isRefresh) || (!isRefresh && !this.hasMore)) return;
        
        this.loading = true;
        
        // 模拟API调用延迟
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 生成模拟数据
        const newVideos = Array.from({ length: this.pageSize }, (_, index) => {
          const baseId = (this.page - 1) * this.pageSize + index + (isRefresh ? 10000 : 1);
          
          return {
            id: baseId,
            title: this.getRandomTitle(),
            teacher: ['张老师', '李教授', '王工程师', '刘老师', '陈教授'][Math.floor(Math.random() * 5)],
            views: `${(Math.random() * 50 + 5).toFixed(1)}万播放`,
            comments: `${Math.floor(Math.random() * 5000 + 1000)}`,
            duration: `${Math.floor(Math.random() * 60 + 10)}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`,
            timeAgo: `${Math.floor(Math.random() * 30 + 1)}天前`,
            image: `https://picsum.photos/400/225?random=${baseId}`
          };
        });
        
        if (this.page === 1 || isRefresh) {
          this.videoCourses = newVideos;
        } else {
          this.videoCourses = [...this.videoCourses, ...newVideos];
        }
        
        // 模拟是否有更多数据
        this.hasMore = this.page < 10;
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
      },

      getCurrentUserId() {
        // 从本地存储获取用户信息
        const userStr = localStorage.getItem('bgareaCurrentUser') || 
                        sessionStorage.getItem('bgareaCurrentUser');
        
        if (userStr) {
          try {
            const user = JSON.parse(userStr);
            console.log('解析用户信息:', user); // 添加日志
            
            // 优先级：user_id > userId > id > username
            const userId = user.user_id || user.userId || user.id || user.username;
            
            console.log('提取的用户ID:', userId); // 添加日志
            
            if (!userId) {
              console.warn('用户信息中没有找到ID字段');
              return 'U001'; // 返回默认ID
            }
            
            return userId;
            
          } catch (error) {
            console.error('解析用户信息失败:', error);
            console.error('原始数据:', userStr);
            return 'U001'; // 出错时返回U001
          }
        }
        
        console.log('没有找到用户信息，使用默认ID: U001');
        return 'U001'; // 使用正确的默认ID
      },
      async loadUserRecommendations() {
        try {
          this.isLoadingRecommend = true;
          this.recommendError = null;

          // 获取用户ID
          const userId = this.getCurrentUserId();
          this.userId = userId;

          console.log('=== 推荐请求详情 ===');
          console.log('用户ID:', userId);
          
          // 使用推荐服务
          const result = await recommendService.getRecommendations(userId,23);
          
          console.log('推荐API返回完整数据:', result);
          
          // 修复判断逻辑
          if (result && result.code === 200) {
            // 即使data为空数组，也算成功，只是没有推荐
            this.recommendedCourses = result.data || [];
            
            if (this.recommendedCourses.length > 0) {
              console.log(`成功获取 ${this.recommendedCourses.length} 个推荐课程`);
              this.isRecommendEmpty = false;
              
              // 使用推荐数据更新页面
              this.updateHomeWithRecommendations();
              
              // 显示成功消息（可选）
              this.showMessage(`为您找到 ${this.recommendedCourses.length} 个推荐课程`, 'success');
            } else {
              console.log('推荐API返回空数组，没有推荐课程');
              this.isRecommendEmpty = true;
              this.showMessage('暂时没有找到适合您的推荐课程', 'info');
              this.useMockRecommendations(); // 使用模拟数据填充
            }
          } else {
            // API返回错误码
            this.isRecommendEmpty = true;
            console.warn('推荐API返回错误:', {
              code: result?.code,
              msg: result?.msg
            });
            
            this.showMessage(result?.msg || '获取推荐失败', 'warning');
            this.useMockRecommendations();
          }
          
        } catch (error) {
          console.error('获取推荐失败:', error);
          
          // 更详细的错误信息
          if (error.response) {
            console.error('错误响应:', {
              status: error.response.status,
              data: error.response.data
            });
          }
          
          this.recommendError = error.message;
          this.isRecommendEmpty = true;
          
          // 可以考虑重试机制
          if (this.recommendRetryCount < 3) {
            this.recommendRetryCount++;
            console.log(`第 ${this.recommendRetryCount} 次重试...`);
            setTimeout(() => this.loadUserRecommendations(), 2000);
            return;
          } else {
            console.log('重试次数用完，使用模拟数据');
            this.showMessage('推荐系统暂时不可用，使用模拟数据', 'warning');
            this.useMockRecommendations();
          }
        } finally {
          this.isLoadingRecommend = false;
        }
      },
      updateHomeWithRecommendations() {
        if (!this.recommendedCourses || this.recommendedCourses.length === 0) {
          console.log('没有推荐数据可更新');
          return;
        }
        
        console.log('使用推荐数据更新页面，数量:', this.recommendedCourses.length);
        
        const totalCourses = this.recommendedCourses.length;
        
        // 1. 主轮播图 - 最多显示4个
        const mainCount = Math.min(4, totalCourses);
        this.mainCourses = this.recommendedCourses.slice(0, mainCount).map((course, index) => {
          if (!course) return null;
          
          return {
            id: index + 1,
            course_id: course.course_id || `C00${index + 1}`,
            title: course.course_name || '未命名课程',
            teacher: this.getTeacherByDomain(course.domain),
            views: this.formatViews(course.predicted_rating || course.rating || 4.5),
            comments: this.generateComments(course.enrolled_count || course.difficulty || 3),
            duration: this.formatDuration(course.duration || course.difficulty || 3),
            image: this.getCourseImage(course.course_id),
            videoFile: this.getVideoFile(course.course_id),
            predictedRating: course.predicted_rating || course.rating,
            difficulty: course.difficulty,
            domain: course.domain,
            is_viewed: course.is_viewed || false,
            viewedBadge: course.is_viewed ? '👁️ 已观看' : '🔥 新推荐',
            viewedClass: course.is_viewed ? 'viewed' : 'new'
          };
        }).filter(item => item !== null);
        
        // 2. 右侧推荐 - 最多显示4个（从第5个开始）
        const sideStart = 4;
        const sideEnd = Math.min(8, totalCourses);
        if (sideEnd > sideStart) {
          this.sideCourses = this.recommendedCourses.slice(sideStart, sideEnd).map((course, index) => {
            if (!course) return null;
            
            return {
              id: sideStart + index + 1,
              course_id: course.course_id || `C00${sideStart + index + 1}`,
              title: course.course_name || '未命名课程',
              teacher: this.getTeacherByDomain(course.domain),
              views: this.formatViews(course.predicted_rating || course.rating || 4.5),
              comments: this.generateComments(course.enrolled_count || course.difficulty || 3),
              duration: this.formatDurationByDifficulty(course.duration || course.difficulty || 3),
              timeAgo: this.generateTimeAgo(index),
              image: this.getCourseImage(course.course_id),
              videoFile: this.getVideoFile(course.course_id),
              predictedRating: course.predicted_rating || course.rating,
              difficulty: course.difficulty,
              is_viewed: course.is_viewed || false
            };
          }).filter(item => item !== null);
        } else {
          this.sideCourses = [];
        }
        
        // 3. 视频列表 - 显示剩余的所有推荐（如果有的话）
        const videoStart = 8;
        if (totalCourses > videoStart) {
          this.videoCourses = this.recommendedCourses.slice(videoStart).map((course, index) => {
            if (!course) return null;
            
            return {
              id: videoStart + index + 1,
              course_id: course.course_id || `C00${videoStart + index + 1}`,
              title: course.course_name || '未命名课程',
              teacher: this.getTeacherByDomain(course.domain),
              views: this.formatViews(course.predicted_rating || course.rating || 4.5),
              comments: this.generateComments(course.enrolled_count || course.difficulty || 3),
              duration: this.formatDurationByDifficulty(course.duration || course.difficulty || 3),
              timeAgo: this.generateTimeAgo(videoStart + index),
              image: this.getCourseImage(course.course_id),
              videoFile: this.getVideoFile(course.course_id),
              predictedRating: course.predicted_rating || course.rating,
              difficulty: course.difficulty,
              is_viewed: course.is_viewed || false
            };
          }).filter(item => item !== null);
        } else {
          this.videoCourses = [];
        }
        
        // 4. 更新页面标题显示实际推荐数量
        this.updatePageTitle(totalCourses);
        
        // 重新开始轮播
        this.stopAutoSlide();
        this.currentSlide = 0;
        this.startAutoSlide();
        
        console.log('页面更新完成');
        console.log('主轮播图:', this.mainCourses.length, '个');
        console.log('右侧推荐:', this.sideCourses.length, '个');
        console.log('视频列表:', this.videoCourses.length, '个');
        console.log('总推荐数:', totalCourses, '个');
      },

      // 添加方法：更新页面标题
      updatePageTitle(totalCourses) {
        const titleElement = document.querySelector('.recommendations-title');
        if (titleElement) {
          titleElement.textContent = `为您推荐 (${totalCourses}个课程)`;
        }
      },
      useMockRecommendations() {
        console.log('使用模拟推荐数据');
        
        // 模拟API返回的数据结构
        this.recommendedCourses = [
          {
            course_id: 'C001',
            course_name: 'Python编程基础',
            difficulty: 3,
            domain: 'Python',
            predicted_rating: 4.5
          },
          {
            course_id: 'C002',
            course_name: 'Java核心技术',
            difficulty: 4,
            domain: 'Java',
            predicted_rating: 4.2
          },
          {
            course_id: 'C003',
            course_name: 'Web前端开发',
            difficulty: 3,
            domain: '前端',
            predicted_rating: 4.7
          },
          {
            course_id: 'C004',
            course_name: '数据结构与算法',
            difficulty: 5,
            domain: '算法',
            predicted_rating: 4.8
          },
          {
            course_id: 'C005',
            course_name: '数据库系统原理',
            difficulty: 4,
            domain: '数据库',
            predicted_rating: 4.3
          },
          {
            course_id: 'C006',
            course_name: '操作系统',
            difficulty: 5,
            domain: '系统',
            predicted_rating: 4.6
          },
          {
            course_id: 'C007',
            course_name: '计算机网络',
            difficulty: 4,
            domain: '网络',
            predicted_rating: 4.4
          },
          {
            course_id: 'C008',
            course_name: '机器学习入门',
            difficulty: 5,
            domain: 'AI',
            predicted_rating: 4.9
          },
          {
            course_id: 'C009',
            course_name: '深度学习实战',
            difficulty: 5,
            domain: 'AI',
            predicted_rating: 4.7
          },
          {
            course_id: 'C010',
            course_name: '软件工程',
            difficulty: 4,
            domain: '工程',
            predicted_rating: 4.1
          }
        ];
        
        // 使用模拟数据更新页面
        this.updateHomeWithRecommendations();
      },
      formatDuration(difficulty) {
        const baseTime = 30; // 30分钟基础
        const addTime = difficulty * 15; // 难度每级加15分钟
        const totalMinutes = baseTime + addTime;
        
        const hours = Math.floor(totalMinutes / 60);
        const minutes = totalMinutes % 60;
        
        if (hours > 0) {
          return `${hours}:${minutes.toString().padStart(2, '0')}:00`;
        }
        return `${minutes}:00`;
      },
      getCourseImage(courseId) {
        if (!courseId) return 'https://picsum.photos/1200/675';
        
        // 根据course_id生成不同的图片
        const index = courseId.replace('C', '');
        return `https://picsum.photos/1200/675?random=${index}`;
      },
      getVideoFile(courseId) {
        if (!courseId) return 'C001_v1.mp4';
        
        // 假设每个课程的第一个视频命名规则：C001_v1.mp4
        return `${courseId}_v1.mp4`;
      },
      getRandomTeacher() {
        const teachers = ['张老师', '李教授', '王工程师', '刘老师', '陈教授'];
        return teachers[Math.floor(Math.random() * teachers.length)];
      },
      goToCourseDetail(course) {
        if (!course || !course.id) {
          console.warn('课程信息不完整');
          return;
        }
        console.log('点击课程详情:', course);
        // 优先使用推荐数据中的course_id
        const courseId = course.course_id || course.id;
        const courseName = course.course_name || course.title;

        if (!courseId) {
          console.error('课程ID缺失:', course);
          return;
        }

        // 构建路由参数
        const routeParams = {
          name: 'VideoPlayer',
          params: {
            courseId: courseId
          },
          query: {
            title: courseName,
            // 传递推荐相关数据（如果存在）
            ...(course.predicted_rating && { predictedRating: course.predicted_rating }),
            ...(course.difficulty && { difficulty: course.difficulty }),
            ...(course.domain && { domain: course.domain }),
            ...(course.is_viewed !== undefined && { is_viewed: course.is_viewed })
          }
        };
        
        console.log('跳转参数:', routeParams);
        this.$router.push(routeParams);
      },
      refreshRecommendations() {
        this.showMessage('正在刷新推荐...', 'info');
        this.loadUserRecommendations();
      },
      refreshSideRecommendations() {
        // 保存当前滚动位置
        this.lastScrollPosition = window.scrollY;
        
        // 刷新右侧推荐课程
        const newSideCourses = [...this.sideCourses];
        for (let i = 0; i < newSideCourses.length; i++) {
          const randomId = Date.now() + i;
          newSideCourses[i].id = 1000 + i;
          newSideCourses[i].image = `https://picsum.photos/400/225?random=${randomId}`;
          newSideCourses[i].title = this.getRandomTitle();
          newSideCourses[i].views = `${(Math.random() * 30 + 5).toFixed(1)}万播放`;
          newSideCourses[i].comments = `${Math.floor(Math.random() * 4000 + 1000)}`;
          newSideCourses[i].timeAgo = `${Math.floor(Math.random() * 7 + 1)}天前`;
        }
        this.sideCourses = this.shuffleArray(newSideCourses);
        
        // 刷新主推荐的一个课程
        const randomIndex = Math.floor(Math.random() * this.mainCourses.length);
        this.mainCourses[randomIndex].image = `https://picsum.photos/1200/675?random=${Date.now()}`;
        this.mainCourses[randomIndex].title = this.getRandomMainTitle();
        
        // 刷新视频推荐
        this.page = 1;
        this.hasMore = true;
        this.loadVideos(true);
        
        // 使用更安全的消息提示方式
        this.showMessage('侧边推荐已刷新', 'success');
      },
      getTeacherByDomain(domain) {
        const teacherMap = {
          'Java': '张老师',
          'Python': '李教授', 
          '前端': '王工程师',
          '算法': '刘老师',
          '数据库': '陈教授',
          '系统': '赵老师',
          '网络': '孙工程师',
          'AI': '周教授',
          '工程': '吴老师',
          'MySQL': '数据库专家'
        };
        return teacherMap[domain] || '资深讲师';
      },
      formatViews(predictedRating) {
        // 评分越高，观看数越多
        const baseViews = 10000;
        const multiplier = predictedRating * 10000;
        const totalViews = baseViews + multiplier;
        
        if (totalViews >= 10000) {
          return (totalViews / 10000).toFixed(1) + '万播放';
        }
        return Math.round(totalViews) + '播放';
      },
      // 根据难度生成评论数
      generateComments(difficulty) {
        // 难度越高，评论越多（因为更挑战）
        const baseComments = 500;
        const multiplier = difficulty * 300;
        return Math.round(baseComments + multiplier) + '';
      },
      formatDuration(difficulty) {
        // 难度越高，课程越长
        const baseMinutes = 30;
        const addMinutes = difficulty * 15;
        const totalMinutes = baseMinutes + addMinutes;
        
        const hours = Math.floor(totalMinutes / 60);
        const minutes = totalMinutes % 60;
        
        if (hours > 0) {
          return `${hours}:${minutes.toString().padStart(2, '0')}:00`;
        }
        return `${minutes}:00`;
      },
      // 另一种时长格式（用于侧边推荐）
      formatDurationByDifficulty(difficulty) {
        const baseMinutes = 15 + difficulty * 5;
        const minutes = Math.min(baseMinutes, 60);
        return `${minutes}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`;
      },
      // 生成发布时间
      generateTimeAgo(index) {
        const daysAgo = Math.floor(index / 2) + 1; // 索引越大，发布时间越早
        return `${daysAgo}天前`;
      },
      // 获取课程图片
      getCourseImage(courseId) {
        if (!courseId) return 'https://picsum.photos/1200/675';
        
        // 根据course_id生成不同的图片
        const index = courseId.replace('C', '');
        return `https://picsum.photos/1200/675?random=${index}`;
      },
      // 获取视频文件
      getVideoFile(courseId) {
        if (!courseId) return 'C001_v1.mp4';
        
        // 假设每个课程的第一个视频命名规则：C001_v1.mp4
        return `${courseId}_v1.mp4`;
      },
      // 添加这个方法到 Home.vue
      getVideoFile(courseId) {
        if (!courseId) return 'C001_v1.mp4';
        // 假设每个课程的第一个视频命名规则：C001_v1.mp4
        return `${courseId}_v1.mp4`;
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