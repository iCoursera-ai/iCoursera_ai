<template>
  <div class="min-h-screen bg-gray-100">
    <Header />
    
    <!-- 面包屑导航 -->
    <div class="container">
      <nav class="breadcrumb">
        <router-link to="/">首页</router-link> > 
        <router-link to="/category/2">编程开发</router-link> > 
        <span>{{ course.title }}</span>
      </nav>
    </div>

    <!-- 主要内容区域 -->
    <div class="container">
      <div class="main-layout">
        <!-- 左侧视频播放区 -->
        <div class="left-column">
          <!-- 视频容器 -->
          <div class="video-container" ref="videoContainer">
            <!-- 加载状态 -->
            <div v-if="isLoading" class="video-loading">
              <div class="loading-spinner">
                <i class="fa fa-spinner fa-spin"></i>
              </div>
              <div class="loading-text">正在加载视频...</div>
            </div>
            
            <!-- 错误提示 -->
            <div v-if="videoError && !isLoading" class="video-error">
              <div class="error-icon">
                <i class="fa fa-exclamation-triangle"></i>
              </div>
              <div class="error-text">{{ videoError }}</div>
              <button @click="retryLoadVideo" class="retry-button">
                <i class="fa fa-redo"></i> 重试
              </button>
            </div>
            
            <!-- 视频播放器主区域 -->
            <div class="video-player" id="videoPlayer" @click="togglePlay">
              <!-- 播放前显示播放按钮 -->
              <div v-if="!isPlaying && videoUrl" class="video-placeholder">
                <i class="fa fa-play-circle text-white text-6xl mb-4 opacity-70 cursor-pointer hover:opacity-100 transition-opacity"></i>
                <p class="text-white text-lg">点击播放视频</p>
                <p class="text-white text-sm mt-2">当前视频: {{ course.title }}</p>
              </div>
              
              <!-- 视频加载中状态 -->
              <div v-if="!videoUrl && !videoError && !isLoading" class="w-full h-full flex items-center justify-center bg-gray-800">
                <div class="text-center text-white">
                  <i class="fa fa-video-slash text-4xl mb-3"></i>
                  <p class="text-lg">视频加载中...</p>
                  <p class="text-sm mt-2">正在获取视频资源</p>
                </div>
              </div>
              
              <!-- 视频元素 -->
              <video 
                ref="videoElement"
                class="video-element w-full h-full object-contain"
                :src="videoUrl"
                @timeupdate="updateProgress"
                @loadedmetadata="onVideoLoaded"
                @ended="onVideoEnded"
                @error="handleVideoError"
                playsinline
                preload="metadata"
                v-show="isPlaying && videoUrl"
              >
                您的浏览器不支持视频播放。
              </video>
            </div>
            
            <!-- 视频控制栏 -->
            <div class="video-controls">
              <div class="control-group">
                <!-- 播放/暂停按钮 -->
                <button class="control-btn play-pause" @click="togglePlay">
                  <i :class="playPauseIcon"></i>
                </button>
                
                <!-- 上一集/下一集 -->
                <button class="control-btn" @click="prevVideo">
                  <i class="fa fa-step-backward"></i>
                </button>
                <button class="control-btn" @click="nextVideo">
                  <i class="fa fa-step-forward"></i>
                </button>
                
                <!-- 进度条 -->
                <div class="progress-container" @click="seekToTime">
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
                    <div class="progress-handle" :style="{ left: progressPercentage + '%' }"></div>
                  </div>
                </div>
                
                <!-- 时间显示 -->
                <div class="time-display">
                  {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
                </div>
                
                <!-- 新的全屏按钮 -->
                <button class="control-btn fullscreen-btn" @click="toggleFullscreenV2" :title="isFullscreenV2 ? '退出全屏 (ESC)' : '进入全屏 (F)'">
                  <div class="fullscreen-icon-wrapper">
                    <i class="fa fa-expand" :class="{ 'hidden': isFullscreenV2 }"></i>
                    <i class="fa fa-compress" :class="{ 'hidden': !isFullscreenV2 }"></i>
                  </div>
                </button>
              </div>
            </div>
          </div>
          
          <!-- 视频信息 -->
          <div class="video-details">
            <h1 class="video-title">{{ course.title }}</h1>
            <div v-if="videoUrl" class="text-sm text-gray-500 mb-3">
              <i class="fa fa-file-video mr-1"></i>
              视频文件: {{ getVideoFileName(videoUrl) }}
            </div>
            <div class="author-section">
              <div class="author-info">
                <div class="author-avatar" @click="goToTeacherSpace(instructor)">👤</div>
                <div>
                  <div class="author-name">{{ instructor.name }}</div>
                  <div class="author-date">{{ course.updateTime }}</div>
                </div>
                <button class="follow-btn" @click="toggleFollow">
                  {{ isFollowing ? '已关注' : '关注' }}
                </button>
              </div>
              <div class="video-stats">
                <!-- 点赞 -->
                <span class="stat-item" @click="toggleLike">
                  <i :class="isLiked ? 'fa fa-heart text-red-500' : 'fa fa-heart'"></i>
                  <span class="stat-number">{{ likeCount }}</span>
                </span>
                
                <!-- 收藏（关联到收藏管理页面） -->
                <span class="stat-item" @click="toggleFavoriteWithRedirect">
                  <i :class="isFavorited ? 'fa fa-star text-yellow-500' : 'fa fa-star'"></i>
                  <span class="stat-number">{{ favoriteCount }}</span>
                </span>
                
                <!-- 我的收藏链接 -->
                <span class="stat-item" @click="goToFavorites">
                  <i class="fa fa-bookmark"></i>
                  <span class="stat-number">我的收藏</span>
                </span>
              </div>
            </div>
          </div>

          <!-- 标签页 -->
          <div class="tabs">
            <button 
              class="tab" 
              :class="{ active: activeTab === 'intro' }" 
              @click="activeTab = 'intro'"
            >
              简介
            </button>
            <button 
              class="tab" 
              :class="{ active: activeTab === 'comments' }" 
              @click="activeTab = 'comments'"
            >
              评论 ({{ comments.length }})
            </button>
          </div>

          <!-- 课程简介 -->
          <div class="course-intro" v-if="activeTab === 'intro'">
            <h3>【课程简介】</h3>
            <p>{{ course.description }}</p>
            <div class="tags">
              <span class="tag" v-for="tag in course.tags" :key="tag">{{ tag }}</span>
            </div>
            <div v-if="videoUrl" class="mt-4 p-3 bg-blue-50 rounded">
              <h4 class="font-medium text-blue-800 mb-2">视频信息</h4>
              <p class="text-sm text-blue-600">视频地址: {{ videoUrl }}</p>
              <p class="text-sm text-blue-600">课程ID: {{ course.id }}</p>
            </div>
          </div>

          <!-- 评论区 -->
          <div class="comments-section" v-if="activeTab === 'comments'">
            <div class="comments-header">
              <h3>💬 评论 ({{ comments.length }})</h3>
              <div class="comment-sort">
                <span @click="sortBy = 'all'" :class="{ active: sortBy === 'all' }">全部</span>
                <span @click="sortBy = 'hot'" :class="{ active: sortBy === 'hot' }">最热</span>
              </div>
            </div>

            <div class="comment-input-box">
              <textarea 
                placeholder="说点什么吧..." 
                class="comment-input"
                v-model="newComment"
                @keypress.ctrl.enter="submitComment"
              ></textarea>
              <div class="comment-actions">
                <button class="submit-comment-btn" @click="submitComment">发送评论</button>
              </div>
            </div>

            <!-- 评论列表 -->
            <div class="comments-list">
              <div class="comment" v-for="comment in sortedComments" :key="comment.id">
                <div class="comment-avatar">{{ comment.avatar }}</div>
                <div class="comment-content">
                  <div class="comment-header">
                    <span class="comment-author">{{ comment.author }}</span>
                    <span class="comment-time">{{ comment.time }}</span>
                  </div>
                  <p>{{ comment.content }}</p>
                  <div class="comment-stats">
                    <span @click="likeComment(comment.id)">👍 {{ comment.likes }}</span>
                    <span @click="showReplyBox(comment.id)">💬 回复</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="load-more">
              <button class="load-more-btn" @click="loadMoreComments">
                加载更多评论
              </button>
            </div>
          </div>
        </div>

        <!-- 右侧课程导航栏 -->
        <div class="right-column-nav">
          <!-- 课程信息卡片 -->
          <div class="course-card">
            <!-- 右侧课程卡片中的作者信息部分 -->
            <div class="course-card-header">
              <div class="course-author" @click="goToTeacherSpace(instructor)">
                <div class="course-author-avatar">👤</div>
                <div>
                  <div class="course-author-name">{{ instructor.name }}</div>
                  <div class="course-author-title">{{ instructor.title || '讲师' }}</div>
                </div>
              </div>
              
              <!-- 作者统计数据 -->
              <div class="author-stats">
                <span class="stat-item"><i class="fa fa-users"></i> {{ formatNumber(instructor.follower_count) }}粉丝</span>
                <span class="stat-item"><i class="fa fa-book"></i> {{ instructor.course_count }}课程</span>
              </div>
              
              <button 
                class="follow-btn-small" 
                @click="toggleFollow"
                :class="{ 'following': isFollowing }"
              >
                {{ isFollowing ? '已关注' : '关注' }}
              </button>
            </div>
            <p class="course-description">{{ instructor.description }}</p>
            <button class="enter-space-btn" @click="goToTeacherSpace(instructor)">进入空间</button>
          </div>

          <!-- 课程章节导航 - 基于API数据 -->
          <div class="course-navigation">
            <div class="course-section-title">
              {{ course.title }} - 课程目录
            </div>
            
            <!-- 加载状态 -->
            <div v-if="isStructureLoading" class="p-4 text-center text-gray-500">
              <i class="fa fa-spinner fa-spin mr-2"></i>
              加载课程目录中...
            </div>
            
            <!-- 错误状态 -->
            <div v-else-if="structureError" class="p-4 text-center text-red-500">
              <i class="fa fa-exclamation-triangle mr-2"></i>
              {{ structureError }}
              <button @click="loadCourseFullData" class="ml-2 text-blue-500 hover:text-blue-700">
                重试
              </button>
            </div>
            
            <!-- 空状态 -->
            <div v-else-if="!courseFullData.modules || courseFullData.modules.length === 0" class="p-4 text-center text-gray-500">
              暂无课程内容
            </div>
            
            <!-- 模块列表 -->
            <div v-else>
              <div 
                v-for="module in courseFullData.modules" 
                :key="module.module_id"
                class="border-b border-gray-200"
              >
                <!-- 模块标题 -->
                <div 
                  class="course-section-title flex justify-between items-center cursor-pointer" 
                  @click="toggleModule(module.module_id)"
                >
                  <span>{{ module.module_name }}</span>
                  <i class="fa" :class="openModules[module.module_id] ? 'fa-angle-down' : 'fa-angle-right'"></i>
                </div>
                
                <!-- 模块内容 -->
                <div class="pl-2" v-show="openModules[module.module_id]">
                  <!-- 视频列表 -->
                  <div v-if="module.videos && module.videos.length > 0">
                    <div 
                      v-for="video in module.videos" 
                      :key="video.video_id"
                      class="course-item" 
                      :class="{ 
                        'active': currentVideo.video_id === video.video_id,
                        'unpublished': !video.is_published 
                      }"
                      @click="setCurrentVideo(video)"
                    >
                      <div class="course-item-icon course-item-video">
                        <i class="fa" :class="currentVideo.video_id === video.video_id ? 'fa-play-circle text-blue-500' : 'fa-play'"></i>
                      </div>
                      <div class="flex-1 min-w-0">
                        <div class="truncate">{{ video.video_name }}</div>
                        <div v-if="!video.is_published" class="text-xs text-gray-400">(未发布)</div>
                      </div>
                      <div class="ml-2 text-xs text-gray-500 whitespace-nowrap">
                        {{ formatTime(video.duration || 0) }}
                      </div>
                    </div>
                  </div>
                  
                  <!-- 习题列表 -->
                  <div v-if="module.quizzes && module.quizzes.length > 0">
                    <div 
                      v-for="quiz in module.quizzes" 
                      :key="quiz.quiz_id"
                      class="course-item" 
                      @click="navigateToQuiz(quiz)"
                    >
                      <div class="course-item-icon course-item-exercise">
                        <i class="fa fa-pencil text-xs"></i>
                      </div>
                      <div class="flex-1 min-w-0">
                        <div class="truncate">{{ quiz.quiz_title }}</div>
                      </div>
                      <div class="ml-2 text-xs text-gray-500 whitespace-nowrap">
                        {{ quiz.score || 0 }}分
                      </div>
                    </div>
                  </div>
                  
                  <!-- 空状态 -->
                  <div v-if="(!module.videos || module.videos.length === 0) && (!module.quizzes || module.quizzes.length === 0)" 
                      class="p-3 text-center text-gray-400 text-sm">
                    暂无内容
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 课程统计数据 -->
            <div v-if="courseStats.totalVideos > 0" class="mt-4 p-3 bg-blue-50 rounded">
              <div class="text-sm text-blue-800 mb-1">课程统计</div>
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div class="flex items-center">
                  <i class="fa fa-video mr-1 text-blue-600"></i>
                  <span>{{ courseStats.totalVideos }}个视频</span>
                </div>
                <div class="flex items-center">
                  <i class="fa fa-pencil-alt mr-1 text-blue-600"></i>
                  <span>{{ courseStats.totalQuizzes }}个习题</span>
                </div>
                <div class="flex items-center">
                  <i class="fa fa-clock mr-1 text-blue-600"></i>
                  <span>{{ courseStats.totalDuration }}</span>
                </div>
                <div class="flex items-center">
                  <i class="fa fa-layer-group mr-1 text-blue-600"></i>
                  <span>{{ courseStats.totalModules }}个模块</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script>
  import Header from '@/components/Header.vue'
  import Footer from '@/components/Footer.vue'
  import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import courseService from '@/service/course.js'
  import teacherService from '@/service/teacher.js'

  export default {
    name: 'VideoPlayer',
    components: {
      Header,
      Footer
    },
    setup() {
      const route = useRoute()
      const router = useRouter()

      // ========== 核心状态 ==========
      const videoUrl = ref('')
      const isLoading = ref(false)
      const videoError = ref('')
      const isComponentMounted = ref(true)

      // 课程完整结构数据
      const courseFullData = ref({
        course_info: {},
        modules: []
      })
      
      // 当前播放的视频信息
      const currentVideo = ref({
        video_id: null,
        video_name: '',
        file_path: '',
        module_id: '',
        module_name: '',
        description: '',
        duration: 0,
        view_count: 0
      })

      // 课程基本信息（从完整数据中提取）
      const course = computed(() => {
        const info = courseFullData.value.course_info
        return {
          id: info.course_id || '',
          title: info.course_name || '',
          description: info.description || '',
          difficulty: info.difficulty || 1,
          domain: info.domain || '',
          rating: info.rating || 0,
          chapterCount: info.chapter_count || 0,
          durationHours: info.duration_hours || 0,
          thumbnailUrl: info.thumbnail_url || ''
        }
      })

      // ========== 视频播放状态 ==========
      const isPlaying = ref(false)
      const currentTime = ref(0)
      const duration = ref(0)
      const isFullscreenV2 = ref(false)
      const autoPlay = ref(true)
      const videoElement = ref(null)
      const videoContainer = ref(null)

      // ========== 互动状态 ==========
      const isLiked = ref(false)
      const likeCount = ref(371)
      const isFavorited = ref(false)
      const favoriteCount = ref(124)
      const isFollowing = ref(false)
      const activeTab = ref('intro')
      const newComment = ref('')
      const sortBy = ref('all') // 添加排序状态

      // ========== 课程导航状态 ==========
      const openModules = ref({}) // 控制模块展开/折叠
      const isStructureLoading = ref(false)
      const structureError = ref('')

      // ========== 讲师数据 ==========
      const instructor = ref({
        name: '加载中...',
        userId: '',
        title: '讲师',
        bio: '',
        description: '',
        follower_count: 0,
        course_count: 0,
        total_students: 0,
        avatar: '',
        expertise: [],
        tags: []
      })

      // ========== 评论数据 ==========
      const comments = ref([
        {
          id: 1,
          avatar: '👤',
          author: '研究生挣M001',
          time: '2天前',
          content: '已经在备考二遍了，讲解寿命清晰，特别是关于电视和视频的讲评，移学谢阳月阳！感谢王道田的协作者们认认，以人为刚能高于上班课程学生们！',
          likes: 1472
        }
      ])

      // ========== 计算属性 ==========
      const playPauseIcon = computed(() => 
        isPlaying.value ? 'fa fa-pause' : 'fa fa-play')

      const progressPercentage = computed(() => {
        if (duration.value > 0) {
          return (currentTime.value / duration.value) * 100
        }
        return 0
      })

      // 计算课程统计数据
      const courseStats = computed(() => {
        const modules = courseFullData.value.modules || []
        let totalVideos = 0
        let totalQuizzes = 0
        let totalDuration = 0

        modules.forEach(module => {
          if (module.videos) {
            totalVideos += module.videos.length
            module.videos.forEach(video => {
              totalDuration += video.duration || 0
            })
          }
          if (module.quizzes) {
            totalQuizzes += module.quizzes.length
          }
        })

        return {
          totalVideos,
          totalQuizzes,
          totalDuration: formatDuration(totalDuration),
          totalModules: modules.length
        }
      })

      // 扁平化的所有视频列表（用于播放导航）
      const allVideos = computed(() => {
        const videos = []
        courseFullData.value.modules?.forEach(module => {
          if (module.videos) {
            module.videos.forEach(video => {
              videos.push({
                ...video,
                module_id: module.module_id,
                module_name: module.module_name,
                module_order: module.module_order
              })
            })
          }
        })
        return videos
      })

      // 当前视频在扁平化列表中的索引
      const currentVideoGlobalIndex = computed(() => {
        if (!currentVideo.value.video_id || !allVideos.value.length) return -1
        return allVideos.value.findIndex(v => v.video_id === currentVideo.value.video_id)
      })

      // ========== 核心方法 ==========
      
      // 获取课程ID
      const getCourseId = () => {
        const routeCourseId = route.params.courseId
        const queryCourseId = route.query.courseId
        
        if (routeCourseId) {
          console.log('从路由参数获取课程ID:', routeCourseId)
          return routeCourseId
        }
        
        if (queryCourseId) {
          console.log('从查询参数获取课程ID:', queryCourseId)
          return queryCourseId
        }
        
        console.log('路由参数:', route.params)
        console.log('查询参数:', route.query)
        
        return 'C001'
      }
      // 获取视频文件名（解码后的）
      const getVideoFileName = (url) => {
        if (!url) return '未加载视频'
        try {
          const parts = url.split('/')
          const encodedName = parts[parts.length - 1]
          return decodeURIComponent(encodedName)
        } catch (error) {
          console.error('解码文件名失败:', error)
          return '未知文件'
        }
      }
      // 加载课程完整数据
      const loadCourseFullData = async () => {
        const courseId = getCourseId()
        if (!courseId) {
          videoError.value = '缺少课程ID'
          return
        }

        isStructureLoading.value = true
        structureError.value = ''
        isLoading.value = true
        videoError.value = ''

        try {
          console.log(`正在获取课程 ${courseId} 的完整数据...`)
          
          const result = await courseService.getCourseFullStructure(courseId)
          
          console.log('课程结构API返回:', result)
          
          if (result.code === 200 && result.data) {
            courseFullData.value = result.data
            console.log('课程完整数据加载成功:', courseFullData.value)
            if (courseFullData.value.course_info?.user_id) {
              await loadTeacherInfo(courseFullData.value.course_info.user_id)
            }
            // 自动展开第一个模块
            if (courseFullData.value.modules?.length > 0) {
              const firstModuleId = courseFullData.value.modules[0].module_id
              openModules.value[firstModuleId] = true
              
              // 自动设置第一个视频
              const firstModule = courseFullData.value.modules[0]
              if (firstModule.videos && firstModule.videos.length > 0) {
                setCurrentVideo(firstModule.videos[0])
              }
            }
            
          } else {
            structureError.value = result.msg || '获取课程数据失败'
            showNotification(structureError.value)
          }
        } catch (error) {
          console.error('加载课程数据失败:', error)
          structureError.value = '网络错误，请检查连接'
          showNotification('加载课程数据失败，请刷新重试')
        } finally {
          isStructureLoading.value = false
          isLoading.value = false
        }
      }

      const loadTeacherInfo = async (teacherId) => {
        if (!teacherId) {
          console.log('没有老师ID，使用默认信息')
          setDefaultInstructor()
          return
        }

        try {
          console.log('正在通过API加载老师信息，ID:', teacherId)
          const response = await teacherService.getTeacherInfo(teacherId)
          
          if (response.code === 200 && response.data) {
            const teacherData = response.data
            instructor.value = {
              name: teacherData.name || `老师${teacherId}`,
              userId: teacherData.user_id || teacherId,
              title: teacherData.title || '讲师',
              bio: teacherData.bio || teacherData.description || '暂无个人简介',
              description: teacherData.description || teacherData.bio || '暂无个人简介',
              follower_count: teacherData.follower_count || 0,
              course_count: teacherData.course_count || 0,
              total_students: teacherData.total_students || 0,
              avatar: teacherData.avatar || getDefaultAvatar(teacherData.name || teacherData.user_id),
              expertise: teacherData.expertise || [],
              tags: teacherData.tags || []
            }
            console.log('老师信息加载成功:', instructor.value)
          } else {
            console.error('获取老师信息失败:', response.msg)
            setDefaultInstructor(teacherId)
          }
        } catch (error) {
          console.error('加载老师信息失败:', error)
          setDefaultInstructor(teacherId)
        }
      }
      // 设置默认讲师信息
      const setDefaultInstructor = (teacherId = '') => {
        instructor.value = {
          name: teacherId ? `老师${teacherId}` : '未知讲师',
          userId: teacherId,
          title: '讲师',
          bio: '暂无个人简介',
          description: '暂无个人简介',
          follower_count: 0,
          course_count: 0,
          total_students: 0,
          avatar: getDefaultAvatar(teacherId || '老师'),
          expertise: [],
          tags: []
        }
      }
      // 添加默认头像生成方法
      const getDefaultAvatar = (name) => {
        const colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
        const index = name ? name.charCodeAt(0) % colors.length : 0
        return `https://ui-avatars.com/api/?name=${encodeURIComponent(name || '老师')}&background=${colors[index].slice(1)}&color=fff&size=150`
      }
      // 设置当前播放的视频
      const setCurrentVideo = (video) => {
        if (!video?.file_path) {
          console.error('无效的视频数据:', video)
          return
        }

        currentVideo.value = { ...currentVideo.value, ...video }
        
        const encodedFileName = encodeURIComponent(video.file_path)
        videoUrl.value = `/videos/${encodedFileName}`
        
        if (video.module_id) {
          openModules.value[video.module_id] = true
        }
        
        nextTick(() => {
          if (!isComponentMounted.value) {
            console.log('组件已卸载，跳过加载视频')
            return
          }
          
          if (videoElement.value) {
            console.log('开始加载视频...')
            
            // 在加载前检查组件状态
            if (!isComponentMounted.value) return
            
            videoElement.value.load()
            
            // 延迟播放，添加组件状态检查
            const playTimeout = setTimeout(() => {
              if (isComponentMounted.value && videoElement.value) {
                playVideo()
              }
            }, 500)
            
            // 存储定时器以便清理
            window.currentVideoTimeout = playTimeout
          }
        })
        
        showNotification(`正在播放: ${video.video_name}`)
      }

      // 播放视频 - 静音自动播放版本
      // 播放视频 - 静音自动播放版本
      const playVideo = () => {
        // 关键修复：检查组件是否已卸载
        if (!isComponentMounted.value) {
          console.log('组件已卸载，跳过播放操作')
          return
        }
        
        if (!videoElement.value || !videoUrl.value || !document.body.contains(videoElement.value)) {
          console.warn('视频元素不可用，跳过播放')
          return
        }
        
        try {
          videoElement.value.muted = true
          const playPromise = videoElement.value.play()
          
          if (playPromise !== undefined) {
            playPromise
              .then(() => {
                // 再次检查组件状态
                if (!isComponentMounted.value || !videoElement.value || !document.body.contains(videoElement.value)) {
                  console.log('组件已卸载或视频元素不存在，停止播放')
                  return
                }
                
                isPlaying.value = true
                videoError.value = ''
                console.log('视频开始播放（静音模式）')
                
                // 取消静音定时器
                const unmuteTimeout = setTimeout(() => {
                  if (isComponentMounted.value && isPlaying.value && videoElement.value && document.body.contains(videoElement.value)) {
                    videoElement.value.muted = false
                  }
                }, 2000)
                
                // 使用局部变量存储定时器
                const cleanupTimer = () => {
                  clearTimeout(unmuteTimeout)
                }
                
                // 监听组件卸载
                window.addEventListener('beforeunload', cleanupTimer)
                window.addEventListener('unload', cleanupTimer)
                
                // 在组件卸载时清理
                onBeforeUnmount(() => {
                  cleanupTimer()
                  window.removeEventListener('beforeunload', cleanupTimer)
                  window.removeEventListener('unload', cleanupTimer)
                })
              })
              .catch(error => {
                console.warn('静音播放被阻止:', error)
                if (isComponentMounted.value && videoElement.value && document.body.contains(videoElement.value)) {
                  videoElement.value.muted = false
                }
                isPlaying.value = false
                showNotification('点击播放按钮开始观看')
              })
          }
        } catch (error) {
          console.error('播放视频时出错:', error)
        }
      }
      const retryLoadVideo = () => {
        if (currentVideo.value.file_path) {
          setCurrentVideo(currentVideo.value)
        } else if (courseFullData.value.modules?.length > 0) {
          const firstVideo = courseFullData.value.modules[0]?.videos?.[0]
          if (firstVideo) {
            setCurrentVideo(firstVideo)
          }
        }
      }
      const goToFavorites = () => {
        router.push('/my/favorites')
      }
      // 收藏并重定向
      const toggleFavoriteWithRedirect = () => {
        isFavorited.value = !isFavorited.value
        favoriteCount.value += isFavorited.value ? 1 : -1
        
        if (isFavorited.value) {
          // 保存收藏信息到 localStorage
          const favoriteItem = {
            id: course.value.id,
            title: course.value.title,
            thumbnail: course.value.thumbnailUrl,
            instructor: instructor.value.name,
            collectedAt: new Date().toISOString(),
            type: 'video'
          }
          
          const favorites = JSON.parse(localStorage.getItem('userFavorites') || '[]')
          favorites.push(favoriteItem)
          localStorage.setItem('userFavorites', JSON.stringify(favorites))
          
          showNotification('已收藏，正在跳转到我的收藏...')
          setTimeout(() => {
            goToFavorites()
          }, 1500)
        } else {
          showNotification('已取消收藏')
        }
      }
      // 视频错误处理
      const handleVideoError = (event) => {
        console.error('视频播放错误:', event)
        
        // 如果 videoUrl 为空，忽略错误
        if (!videoUrl.value) {
          console.warn('videoUrl为空，忽略错误')
          return
        }
        
        const video = videoElement.value
        if (video && video.error) {
          switch (video.error.code) {
            case video.error.MEDIA_ERR_ABORTED:
              videoError.value = '视频加载被中止'
              break
            case video.error.MEDIA_ERR_NETWORK:
              videoError.value = '网络错误，请检查连接'
              break
            case video.error.MEDIA_ERR_DECODE:
              videoError.value = '视频解码错误'
              break
            case video.error.MEDIA_ERR_SRC_NOT_SUPPORTED:
              videoError.value = '视频格式不支持'
              break
            default:
              videoError.value = '视频加载失败'
          }
          
          showNotification(videoError.value)
        }
      }
      // 显示回复框
      const showReplyBox = (commentId) => {
        showNotification('回复功能正在开发中')
      }

      // 加载更多评论
      const loadMoreComments = () => {
        // 模拟加载更多评论
        for (let i = 1; i <= 5; i++) {
          comments.value.push({
            id: comments.value.length + 1,
            avatar: '👤',
            author: `用户${comments.value.length + 1}`,
            time: `${i}小时前`,
            content: `这是第${comments.value.length + 1}条模拟评论，用于测试加载更多功能`,
            likes: Math.floor(Math.random() * 100)
          })
        }
        showNotification(`加载了5条新评论，共${comments.value.length}条`)
      }
      // ========== 视频导航方法 ==========
      
      const prevVideo = () => {
        if (allVideos.value.length === 0) {
          showNotification('没有更多视频')
          return
        }
        
        const currentIndex = currentVideoGlobalIndex.value
        if (currentIndex > 0) {
          setCurrentVideo(allVideos.value[currentIndex - 1])
        } else {
          showNotification('已经是第一个视频')
        }
      }

      const nextVideo = () => {
        if (allVideos.value.length === 0) {
          showNotification('没有更多视频')
          return
        }
        
        const currentIndex = currentVideoGlobalIndex.value
        if (currentIndex < allVideos.value.length - 1) {
          setCurrentVideo(allVideos.value[currentIndex + 1])
        } else {
          showNotification('已经是最后一个视频')
        }
      }

      const togglePlay = () => {
        if (!isComponentMounted.value || !videoElement.value || !document.body.contains(videoElement.value)) return
        
        if (videoElement.value.paused) {
          videoElement.value.play()
            .then(() => isPlaying.value = true)
            .catch(error => {
              console.error('播放失败:', error)
              isPlaying.value = false
            })
        } else {
          videoElement.value.pause()
          isPlaying.value = false
        }
      }

      // ========== 工具方法 ==========
      
      const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60)
        const secs = Math.floor(seconds % 60)
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
      }

      const formatDuration = (seconds) => {
        const hours = Math.floor(seconds / 3600)
        const mins = Math.floor((seconds % 3600) / 60)
        
        if (hours > 0) {
          return `${hours}小时${mins}分钟`
        }
        return `${mins}分钟`
      }
      // 添加评论排序计算属性
      const sortedComments = computed(() => {
        const allComments = [...comments.value]
        
        if (sortBy.value === 'hot') {
          return allComments.sort((a, b) => b.likes - a.likes)
        }
        
        return allComments
      })
      // 数字格式化方法
      const formatNumber = (num) => {
        if (!num && num !== 0) return '0'
        if (num >= 10000) {
          return (num / 10000).toFixed(1) + '万'
        }
        return num.toString()
      }
      const toggleModule = (moduleId) => {
        openModules.value[moduleId] = !openModules.value[moduleId]
      }

      const getQuizIcon = (quizType) => {
        switch (quizType) {
          case 1: // 选择题
            return 'fa-check-square'
          case 2: // 判断题
            return 'fa-toggle-on'
          case 3: // 简答题
            return 'fa-keyboard'
          case 4: // 编程题
            return 'fa-code'
          default:
            return 'fa-question-circle'
        }
      }

      const getQuizTypeText = (quizType) => {
        switch (quizType) {
          case 1:
            return '选择题'
          case 2:
            return '判断题'
          case 3:
            return '简答题'
          case 4:
            return '编程题'
          default:
            return '习题'
        }
      }

      // 导航到习题
      const navigateToQuiz = (quiz) => {
        console.log('导航到习题:', quiz)
        
        // 立即标记组件为即将卸载状态
        isComponentMounted.value = false
        
        // 停止当前视频播放
        if (videoElement.value) {
          videoElement.value.pause()
          videoElement.value.src = '' // 清空视频源
          videoElement.value.load() // 重置视频
          isPlaying.value = false
          console.log('停止并重置视频播放')
        }
        
        // 清除所有定时器
        if (window.currentVideoTimeout) {
          clearTimeout(window.currentVideoTimeout)
          delete window.currentVideoTimeout
        }
        if (window.unmuteTimeout) {
          clearTimeout(window.unmuteTimeout)
          delete window.unmuteTimeout
        }
        
        const quizSessionData = {
          courseId: course.value.id,
          courseName: course.value.title,
          moduleId: quiz.module_id,
          quizId: quiz.quiz_id,
          quizTitle: quiz.quiz_title,
          quizType: quiz.quiz_type,
          score: quiz.score,
          createdAt: quiz.created_time
        }
        
        localStorage.setItem('currentQuizSession', JSON.stringify(quizSessionData))
        
        // 使用 router.replace 而不是 push，避免保留状态
        router.replace({
          path: `/course/${course.value.id}/exercise/${quiz.quiz_id}`,
          query: {
            courseId: course.value.id,
            courseName: course.value.title,
            moduleId: quiz.module_id,
            quizId: quiz.quiz_id,
            quizTitle: quiz.quiz_title
          }
        })
      }
      const showNotification = (message) => {
        const existingNotifications = document.querySelectorAll('.custom-notification')
        existingNotifications.forEach(notification => {
          if (notification.parentNode) {
            document.body.removeChild(notification)
          }
        })
        
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
          display: flex;
          align-items: center;
          gap: 10px;
        `
        
        notification.innerHTML = `
          <i class="fa fa-info-circle"></i>
          <span>${message}</span>
        `
        
        document.body.appendChild(notification)
        
        setTimeout(() => {
          notification.style.animation = 'slideOut 0.3s ease'
          setTimeout(() => {
            if (notification.parentNode) {
              document.body.removeChild(notification)
            }
          }, 300)
        }, 3000)
      }

      const updateProgress = () => {
        if (isComponentMounted.value && videoElement.value) {
          currentTime.value = videoElement.value.currentTime
        }
      }

      const onVideoLoaded = () => {
        if (videoElement.value) {
          duration.value = videoElement.value.duration
          console.log('视频加载完成，时长:', duration.value)
          
          // 清除错误状态
          if (videoError.value) {
            videoError.value = ''
          }
        }
      }

      const onVideoEnded = () => {
        if (!isComponentMounted.value) return
        
        isPlaying.value = false
        if (autoPlay.value) nextVideo()
      }
      const seekToTime = (event) => {
        if (!isComponentMounted.value || !videoElement.value || !duration.value) return
        
        const rect = event.currentTarget.getBoundingClientRect()
        const percentage = (event.clientX - rect.left) / rect.width
        videoElement.value.currentTime = percentage * duration.value
      }
      // ========== 全屏功能 ==========
      
      const toggleFullscreenV2 = () => {
        if (!videoContainer.value) return
        
        if (!isFullscreenV2.value) {
          const elem = videoContainer.value
          
          if (elem.requestFullscreen) {
            elem.requestFullscreen()
          } else if (elem.webkitRequestFullscreen) {
            elem.webkitRequestFullscreen()
          } else if (elem.msRequestFullscreen) {
            elem.msRequestFullscreen()
          } else if (elem.mozRequestFullScreen) {
            elem.mozRequestFullScreen()
          }
          
          isFullscreenV2.value = true
          showNotification('已进入沉浸式全屏模式')
          
          // 全屏时添加特殊样式
          document.body.classList.add('video-fullscreen-active')
        } else {
          if (document.exitFullscreen) {
            document.exitFullscreen()
          } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen()
          } else if (document.msExitFullscreen) {
            document.msExitFullscreen()
          } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen()
          }
          
          isFullscreenV2.value = false
          showNotification('已退出全屏模式')
          
          // 移除全屏样式
          document.body.classList.remove('video-fullscreen-active')
        }
      }

      const handleFullscreenChange = () => {
        isFullscreenV2.value = !!document.fullscreenElement
        if (!isFullscreenV2.value) {
          document.body.classList.remove('video-fullscreen-active')
        }
      }

      // 关注/取消关注讲师
      const toggleFollow = () => {
        isFollowing.value = !isFollowing.value
        saveFollowData()
        showNotification(isFollowing.value ? '已关注讲师' : '已取消关注')
      }
      
      const saveFollowData = () => {
        // 获取当前关注的老师列表
        const followedTeachers = JSON.parse(localStorage.getItem('userFollowedTeachers') || '[]')
        
        const teacherData = {
          id: Date.now(),
          userId: instructor.value.userId || `teacher_${instructor.value.name}_${Date.now()}`,
          name: instructor.value.name,
          department: instructor.value.department || '计算机学院',
          avatar: instructor.value.avatar || 'https://picsum.photos/48/48?random=' + Math.floor(Math.random() * 100),
          followedAt: new Date().toISOString().split('T')[0]
        }

        if (isFollowing.value) {
          // 添加到关注列表
          const existingIndex = followedTeachers.findIndex(t => t.name === teacherData.name)
          if (existingIndex === -1) {
            followedTeachers.push(teacherData)
            localStorage.setItem('userFollowedTeachers', JSON.stringify(followedTeachers))
          }
        } else {
          // 从关注列表中移除
          const updatedTeachers = followedTeachers.filter(t => t.name !== teacherData.name)
          localStorage.setItem('userFollowedTeachers', JSON.stringify(updatedTeachers))
        }
      }
      // 跳转到老师空间
      const goToTeacherSpace = (teacher) => {
        const teacherInfo = {
          name: teacher.name,
          userId: teacher.userId || `teacher_${teacher.name}`,
          department: teacher.department || '计算机学院',
          avatar: teacher.avatar || 'https://picsum.photos/48/48?random=50',
          description: teacher.description || '资深讲师'
        }
        
        localStorage.setItem('currentTeacherInfo', JSON.stringify(teacherInfo))
        
        router.push({
          path: '/teacher-space',
          query: {
            teacherId: teacher.userId || `teacher_${teacher.name}`,
            teacherName: teacher.name
          }
        })
      }
      // 加载关注状态
      const loadFollowStatus = () => {
        const followedTeachers = JSON.parse(localStorage.getItem('userFollowedTeachers') || '[]')
        const isTeacherFollowed = followedTeachers.some(teacher => teacher.name === instructor.value.name)
        isFollowing.value = isTeacherFollowed
      }
      
      const toggleLike = () => {
        isLiked.value = !isLiked.value
        likeCount.value += isLiked.value ? 1 : -1
        showNotification(isLiked.value ? '已点赞' : '已取消点赞')
      }
      
      const toggleFavorite = () => {
        isFavorited.value = !isFavorited.value
        favoriteCount.value += isFavorited.value ? 1 : -1
        showNotification(isFavorited.value ? '已收藏' : '已取消收藏')
      }

      const likeComment = (commentId) => {
        const comment = comments.value.find(c => c.id === commentId)
        if (comment) {
          comment.likes += 1
        }
      }
      
      const submitComment = () => {
        if (!newComment.value.trim()) {
          showNotification('请输入评论内容')
          return
        }
        const newCommentObj = {
          id: comments.value.length + 1,
          avatar: '👤',
          author: '当前用户',
          time: '刚刚',
          content: newComment.value,
          likes: 0
        } 
        comments.value.unshift(newCommentObj)
        newComment.value = ''
        showNotification('评论发送成功')
      }
      
      const handleKeyDown = (event) => {
        // F键进入/退出全屏
        if (event.key === 'f' || event.key === 'F') {
          event.preventDefault()
          toggleFullscreenV2()
        }
        // ESC键退出全屏
        if (event.key === 'Escape' && isFullscreenV2.value) {
          toggleFullscreenV2()
        }
        // 空格键播放/暂停
        if (event.key === ' ' && event.target.tagName !== 'TEXTAREA' && event.target.tagName !== 'INPUT') {
          event.preventDefault()
          togglePlay()
        }
      }

      onMounted(() => {
        console.log('VideoPlayer mounted')
        
        // 检查用户是否已登录
        const user = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
        if (!user) {
          router.push('/login')
          return
        }
        
        // 加载课程完整数据
        loadCourseFullData()
        
        // 加载关注状态
        loadFollowStatus()

        // 添加事件监听器
        document.addEventListener('fullscreenchange', handleFullscreenChange)
        document.addEventListener('keydown', handleKeyDown)
      })

      onBeforeUnmount(() => {
        console.log('VideoPlayer 组件卸载，清理资源...')
        isComponentMounted.value = false // 标记组件已卸载
        document.removeEventListener('fullscreenchange', handleFullscreenChange)
        document.removeEventListener('keydown', handleKeyDown)
      })

      
      return {
        // 状态
        videoUrl,
        isLoading,
        videoError,
        courseFullData,
        currentVideo,
        course,
        isPlaying,
        currentTime,
        duration,
        isFullscreenV2,
        autoPlay,
        isLiked,
        likeCount,
        isFavorited,
        favoriteCount,
        isFollowing,
        activeTab,
        newComment,
        openModules,
        isStructureLoading,
        structureError,
        instructor,
        comments,
        
        // DOM 引用
        videoElement,
        videoContainer,
        
        // 计算属性
        playPauseIcon,
        progressPercentage,
        courseStats,
        allVideos,
        currentVideoGlobalIndex,
        
        // 核心方法
        setCurrentVideo,
        playVideo,
        togglePlay,
        prevVideo,
        nextVideo,
        loadCourseFullData,
        goToTeacherSpace,
        retryLoadVideo,
        goToFavorites,
        toggleFavoriteWithRedirect,
        showReplyBox,
        loadMoreComments,
        sortBy,
        sortedComments,
        
        // 工具方法
        formatTime,
        formatDuration,
        toggleModule,
        getQuizIcon,
        getVideoFileName,
        getQuizTypeText,
        navigateToQuiz,
        showNotification,
        formatNumber,
        // 视频事件
        updateProgress,
        onVideoLoaded,
        onVideoEnded,
        handleVideoError,
        seekToTime,
        
        // 全屏功能
        toggleFullscreenV2,
        
        // 互动功能
        toggleFollow,
        toggleLike,
        toggleFavorite,
        likeComment,
        submitComment
      }
    }
  }
</script>

<style scoped>
/* ========== 基础样式 ========== */
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.min-h-screen {
  min-height: 100vh;
}

.bg-gray-100 {
  background-color: #f5f5f5;
}

/* ========== 面包屑导航 ========== */
.breadcrumb {
  padding: 15px 0;
  font-size: 14px;
  color: #666;
}

.breadcrumb a {
  color: #666;
  text-decoration: none;
  transition: color 0.2s;
}

.breadcrumb a:hover {
  color: #1890ff;
}

/* ========== 主布局 ========== */
.main-layout {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 20px;
  margin-bottom: 40px;
}

/* ========== 视频容器 ========== */
.video-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

/* 视频播放区域 */
.video-player {
  position: relative;
  width: 100%;
  height: 500px;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-placeholder {
  text-align: center;
  color: white;
}

.video-placeholder i {
  cursor: pointer;
  transition: opacity 0.3s ease;
}

.video-placeholder i:hover {
  opacity: 1;
}

/* 视频控制栏 */
.video-controls {
  background-color: rgba(0, 0, 0, 0.8);
  padding: 1rem;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.control-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.control-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #FF9F43;
}

/* 进度条 */
.progress-container {
  flex-grow: 1;
  cursor: pointer;
  padding: 10px 0;
}

.progress-bar {
  height: 4px;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  position: relative;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #FF9F43;
  border-radius: 2px;
  transition: width 0.1s;
}

.time-display {
  color: white;
  font-size: 0.9rem;
  min-width: 100px;
  text-align: center;
  font-family: monospace;
}

/* 错误提示 */
.video-error {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  z-index: 10;
}

/* ========== 视频详情区域 ========== */
.video-details {
  background: white;
  padding: 20px;
  border-radius: 12px;
  margin-top: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.video-title {
  font-size: 24px;
  margin-bottom: 15px;
  color: #333;
  font-weight: 600;
}

.author-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.author-avatar:hover {
  opacity: 0.8;
}

.follow-btn {
  padding: 8px 20px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.follow-btn:hover {
  background: #40a9ff;
  transform: translateY(-1px);
}

.video-stats {
  display: flex;
  gap: 20px;
  align-items: center;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  transition: all 0.2s;
  padding: 8px 12px;
  border-radius: 6px;
}

.stat-item:hover {
  background: #f5f5f5;
  color: #1890ff;
}

/* ========== 标签页 ========== */
.tabs {
  display: flex;
  gap: 30px;
  background: white;
  padding: 0 20px;
  margin-top: 15px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.tab {
  padding: 15px 0;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 15px;
  color: #666;
  position: relative;
  transition: color 0.2s;
}

.tab:hover {
  color: #1890ff;
}

.tab.active {
  color: #1890ff;
  font-weight: 500;
}

.tab.active::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: #1890ff;
}

/* ========== 内容区域 ========== */
.content-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  margin-top: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.content-section h3 {
  font-size: 18px;
  margin-bottom: 12px;
  color: #333;
  font-weight: 600;
}

/* 课程简介 */
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 15px;
}

.tag {
  padding: 6px 12px;
  background: #f0f0f0;
  border-radius: 20px;
  font-size: 13px;
  color: #666;
  transition: all 0.2s;
}

.tag:hover {
  background: #1890ff;
  color: white;
}

/* 评论区 */
.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.comment-sort {
  display: flex;
  gap: 15px;
}

.comment-sort span {
  cursor: pointer;
  color: #666;
  position: relative;
  padding: 4px 0;
  transition: color 0.2s;
}

.comment-sort span:hover,
.comment-sort span.active {
  color: #1890ff;
}

.comment-sort span.active::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: #1890ff;
}

.comment-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
  transition: border-color 0.2s;
}

.comment-input:focus {
  outline: none;
  border-color: #1890ff;
}

.comment-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.submit-btn {
  padding: 8px 24px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.submit-btn:hover {
  background: #40a9ff;
  transform: translateY(-1px);
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.comment {
  display: flex;
  gap: 12px;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 500;
  color: #333;
}

.comment-time {
  font-size: 13px;
  color: #999;
}

.comment-content p {
  line-height: 1.6;
  color: #333;
  margin-bottom: 10px;
}

.comment-stats {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: #666;
}

.comment-stats span {
  cursor: pointer;
  transition: color 0.2s;
}

.comment-stats span:hover {
  color: #1890ff;
}

.load-more-btn {
  padding: 10px 30px;
  border: 1px solid #e0e0e0;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.load-more-btn:hover {
  background: #f9f9f9;
  border-color: #1890ff;
  color: #1890ff;
}

/* ========== 右侧侧边栏 ========== */
.right-column-nav {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 课程卡片 */
.course-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.course-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.course-author {
  display: flex;
  gap: 10px;
  align-items: center;
  cursor: pointer;
  transition: opacity 0.2s;
}

.course-author:hover {
  opacity: 0.8;
}

.course-author-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.course-author-name {
  font-weight: 600;
  font-size: 15px;
}

.course-author-fans {
  font-size: 12px;
  color: #999;
}

.follow-btn-small {
  padding: 6px 16px;
  background: #f0f0f0;
  color: #666;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.follow-btn-small.following {
  background: #1890ff;
  color: white;
}

.follow-btn-small:hover {
  transform: translateY(-1px);
}

.course-description {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
}

.enter-space-btn {
  width: 100%;
  padding: 10px;
  border: 1px solid #1890ff;
  background: white;
  color: #1890ff;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.enter-space-btn:hover {
  background: #1890ff;
  color: white;
}

/* 课程导航 */
.course-navigation {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.course-section-title {
  font-weight: 500;
  color: #666;
  padding: 12px 16px;
  border-bottom: 1px solid #e8e8e8;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 14px;
}

.course-item:hover {
  background-color: rgba(24, 144, 255, 0.05);
}

.course-item.active {
  background-color: rgba(24, 144, 255, 0.1);
  color: #1890ff;
  font-weight: 500;
}

.course-item-icon {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}

.course-item-video {
  background-color: rgba(24, 144, 255, 0.1);
  color: #1890ff;
}

.course-item-exercise {
  background-color: rgba(82, 196, 26, 0.1);
  color: #52c41a;
}

/* ========== 全屏样式 ========== */
:fullscreen .video-container {
  border-radius: 0;
  box-shadow: none;
  background: #000;
}

:fullscreen body {
  background: #000;
}

:fullscreen .video-controls {
  background-color: rgba(0, 0, 0, 0.95);
}

:fullscreen .video-player {
  height: calc(100vh - 60px);
}

:fullscreen .control-btn:hover {
  background-color: rgba(255, 255, 255, 0.15);
}

/* ========== 响应式设计 ========== */
@media (max-width: 1024px) {
  .main-layout {
    grid-template-columns: 1fr;
  }
  
  .right-column-nav {
    display: none;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 15px;
  }
  
  .video-player {
    height: 300px;
  }
  
  .author-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .video-stats {
    width: 100%;
    justify-content: space-between;
  }
  
  .tabs {
    gap: 15px;
    padding: 0 15px;
  }
  
  .tab {
    font-size: 14px;
    padding: 12px 0;
  }
  
  .control-group {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .control-btn {
    width: 32px;
    height: 32px;
    font-size: 1rem;
  }
  
  .time-display {
    min-width: 80px;
    font-size: 12px;
  }
  
  .video-title {
    font-size: 20px;
  }
}

/* 加载状态 */
.video-loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  z-index: 10;
}

.loading-spinner i {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>