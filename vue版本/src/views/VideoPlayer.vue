<template>
  <div class="font-inter min-h-screen bg-gray-100">
    <Header />
    
    <!-- 页面导航 -->
    <div class="page-header">
      <div class="breadcrumb">
        <router-link to="/">首页</router-link> > 
        <router-link to="/courses?category=programming">我的课程</router-link> > 
        <router-link :to="`/course/${course.id}`">{{ course.title }}</router-link> > 
        <span>{{ currentLesson.title }}</span>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧视频播放区域 -->
      <div class="video-section">
        <!-- 视频播放器 -->
        <div class="video-container" ref="videoContainer">
          <div class="video-player" id="videoPlayer" @click="togglePlay">
            <div class="video-placeholder" v-if="!isPlaying">
              <i class="fas fa-play-circle text-white text-6xl mb-4 opacity-70 cursor-pointer hover:opacity-100 transition-opacity"></i>
              <p class="text-white text-lg">点击播放视频</p>
            </div>
            <video 
              class="video-element w-full h-full object-contain"
              ref="videoElement"
              preload="metadata"
              @timeupdate="updateProgress"
              @loadedmetadata="onVideoLoaded"
              @ended="onVideoEnded"
              v-show="isPlaying"
              @error="handleVideoError"
            >
              <!-- 使用可靠的测试视频源 -->
              <source src="https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4" type="video/mp4">
              <source src="https://videos.pexels.com/video-files/3195399/3195399-hd_1920_1080_30fps.mp4" type="video/mp4">
              您的浏览器不支持视频播放。
            </video>
            
            <!-- 字幕区域 -->
            <div class="subtitle-container" v-show="showSubtitles && isPlaying">
              <div class="subtitle-text">{{ currentSubtitle }}</div>
            </div>
          </div>
          
          <div class="video-controls">
            <div class="control-group">
              <button class="control-btn play-pause" @click="togglePlay">
                <i :class="playPauseIcon"></i>
              </button>
              <button class="control-btn" @click="prevLesson">
                <i class="fas fa-step-backward"></i>
              </button>
              <button class="control-btn" @click="nextLesson">
                <i class="fas fa-step-forward"></i>
              </button>
              
              <div class="progress-container" @click="seekToTime">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
                  <div class="progress-handle" :style="{ left: progressPercentage + '%' }"></div>
                </div>
              </div>
              
              <div class="time-display">
                {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
              </div>
            </div>
            
            <div class="control-group">
              <button class="control-btn" @click="toggleMute">
                <i :class="volumeIcon"></i>
              </button>
              
              <div class="video-settings relative">
                <button class="control-btn" @click="showSettings = !showSettings">
                  <i class="fas fa-cog"></i>
                </button>
                <div class="settings-menu" v-show="showSettings" @click.stop>
                  <div 
                    v-for="speed in playbackSpeeds" 
                    :key="speed.value"
                    class="settings-item" 
                    :class="{ 'active': playbackRate === speed.value }"
                    @click="setPlaybackSpeed(speed.value)"
                  >
                    {{ speed.label }}
                  </div>
                  <div class="settings-item" @click="toggleSubtitles">
                    {{ showSubtitles ? '关闭AI字幕' : '开启AI字幕' }}
                  </div>
                  <div class="settings-item" @click="togglePictureInPicture">
                    画中画模式
                  </div>
                </div>
              </div>
              
              <button class="control-btn" @click="toggleFullscreen">
                <i :class="fullscreenIcon"></i>
              </button>
            </div>
          </div>
        </div>
        
        <!-- 视频信息 -->
        <div class="video-info">
          <h2 class="current-video-title">{{ currentLesson.title }}</h2>
          <p class="video-description">
            {{ currentLesson.description }}
          </p>
          
          <div class="video-meta">
            <div class="meta-item">
              <i class="fas fa-clock text-primary"></i>
              <span>时长: {{ formatDuration(currentLesson.duration) }}</span>
            </div>
            <div class="meta-item">
              <i class="fas fa-eye text-primary"></i>
              <span>已学习: {{ formatDuration(learnedTime) }}</span>
            </div>
            <div class="meta-item">
              <i class="fas fa-closed-captioning text-primary"></i>
              <span>AI字幕: {{ showSubtitles ? '已开启' : '已关闭' }}</span>
            </div>
            <div class="meta-item">
              <i class="fas fa-download text-primary"></i>
              <span>资料: {{ currentLesson.hasMaterials ? '可下载' : '无资料' }}</span>
            </div>
          </div>
        </div>
        
        <!-- 学习工具 -->
        <div class="learning-tools">
          <h2 class="tools-title">学习工具</h2>
          
          <div class="tool-buttons">
            <button class="tool-btn" :class="{ 'active': activeTool === 'qa' }" @click="activateTool('qa')">
              <i class="fas fa-question-circle text-primary text-xl"></i>
              <span>课程问答</span>
            </button>
            <button class="tool-btn" :class="{ 'active': activeTool === 'notes' }" @click="activateTool('notes')">
              <i class="fas fa-file-alt text-primary text-xl"></i>
              <span>课堂笔记</span>
            </button>
            <button class="tool-btn active" @click="activateTool('exercise')">
              <i class="fas fa-tasks text-primary text-xl"></i>
              <span>章节习题</span>
            </button>
            <button class="tool-btn" :class="{ 'active': activeTool === 'download' }" @click="activateTool('download')">
              <i class="fas fa-download text-primary text-xl"></i>
              <span>资料下载</span>
            </button>
          </div>
          
          <div class="ai-assistant" @click="showAIModal = true">
            <div class="ai-icon">
              <i class="fas fa-robot text-white"></i>
            </div>
            <div class="ai-text">
              <h4>AI学习助手小翔</h4>
              <p>点击我可以解答学习疑问、生成个性化习题</p>
            </div>
          </div>
        </div>
        
        <!-- 讨论区 -->
        <div class="discussion-section">
          <div class="discussion-header">
            <h3 class="discussion-title">课程讨论区</h3>
            <button class="new-question-btn" @click="showQuestionModal = true">
              <i class="fas fa-plus"></i>
              <span>提问</span>
            </button>
          </div>
          
          <ul class="question-list">
            <li class="question-item" v-for="question in questions" :key="question.id">
              <div class="question-header">
                <div class="questioner">
                  <div class="questioner-avatar">
                    <img :src="question.avatar" :alt="question.name">
                  </div>
                  <div class="questioner-info">
                    <h4>{{ question.name }}</h4>
                    <div class="question-date">{{ question.date }}</div>
                  </div>
                </div>
                <div class="question-ai-tag" v-if="question.aiAnswered">
                  <span class="ai-tag">
                    <i class="fas fa-robot"></i> AI已解答
                  </span>
                </div>
              </div>
              <div class="question-content">
                {{ question.content }}
              </div>
              <div class="question-actions">
                <div class="action-btn" @click="likeQuestion(question.id)">
                  <i class="fas fa-thumbs-up"></i>
                  <span>{{ question.likes }}</span>
                </div>
                <div class="action-btn" @click="showNotification('评论功能开发中')">
                  <i class="fas fa-comment"></i>
                  <span>{{ question.comments }}</span>
                </div>
                <div class="action-btn" @click="showNotification('分享功能开发中')">
                  <i class="fas fa-share"></i>
                  <span>分享</span>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
      
      <!-- 右侧课程目录区域 -->
      <div class="course-sidebar">
        <!-- 课程目录 -->
        <div class="course-directory">
          <div class="directory-header">
            <h3 class="directory-title">课程目录</h3>
            <div class="course-progress">
              <i class="fas fa-chart-line"></i>
              <span>已学 {{ progressPercentage }}%</span>
            </div>
          </div>
          
          <ul class="directory-list">
            <li class="directory-section" v-for="chapter in syllabus" :key="chapter.id">
              <div class="section-header" @click="toggleChapter(chapter.id)">
                <span>{{ chapter.title }}</span>
                <i class="fas fa-chevron-down" :class="{ 'rotated': !chapter.expanded }"></i>
              </div>
              <ul class="lesson-list" v-show="chapter.expanded">
                <li 
                  class="lesson-item" 
                  v-for="lesson in chapter.lessons" 
                  :key="lesson.id"
                  :class="{ 
                    'active': currentLesson.id === lesson.id,
                    'completed': lesson.completed 
                  }"
                  @click="selectLesson(lesson)"
                >
                  <div class="lesson-info">
                    <div class="lesson-icon">
                      <i class="fas fa-play-circle"></i>
                    </div>
                    <div>
                      <div class="lesson-title">{{ lesson.title }}</div>
                      <div class="lesson-duration">{{ formatDuration(lesson.duration) }}</div>
                    </div>
                  </div>
                  <div class="lesson-status">
                    <i 
                      v-if="currentLesson.id === lesson.id" 
                      class="fas fa-volume-up text-green-500"
                    ></i>
                    <i 
                      v-else-if="lesson.completed" 
                      class="fas fa-check-circle text-green-500"
                    ></i>
                  </div>
                </li>
              </ul>
            </li>
          </ul>
        </div>
        
        <!-- AI学习分析 -->
        <div class="learning-tools mt-6">
          <h2 class="tools-title">AI学习分析</h2>
          
          <div class="mb-6">
            <div class="flex justify-between mb-2">
              <span class="text-sm text-gray-600">当前章节掌握度</span>
              <span class="font-semibold text-primary">{{ masteryPercentage }}%</span>
            </div>
            <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
              <div 
                class="h-full rounded-full transition-all duration-300" 
                :class="masteryPercentage >= 80 ? 'bg-green-500' : masteryPercentage >= 60 ? 'bg-yellow-500' : 'bg-red-500'"
                :style="{ width: masteryPercentage + '%' }"
              ></div>
            </div>
          </div>
          
          <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded mb-4">
            <div class="font-semibold text-gray-800 mb-1 flex items-center">
              <i class="fas fa-lightbulb text-yellow-500 mr-2"></i>
              AI学习建议
            </div>
            <div class="text-sm text-gray-600">
              {{ aiSuggestion }}
            </div>
          </div>
          
          <button 
            class="w-full bg-blue-50 hover:bg-blue-100 text-primary border border-blue-200 py-3 px-4 rounded-lg cursor-pointer flex items-center justify-center gap-2 transition-colors"
            @click="showNotification('学习报告功能开发中')"
          >
            <i class="fas fa-chart-bar"></i>
            <span>查看详细学习报告</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 模态框 -->
    <ExerciseModal v-if="showExerciseModal" @close="showExerciseModal = false" />
    <AIAssistantModal v-if="showAIModal" @close="showAIModal = false" />
    <QuestionModal v-if="showQuestionModal" @close="showQuestionModal = false" />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import ExerciseModal from '@/components/ExerciseModal.vue'
import AIAssistantModal from '@/components/AIAssistantModal.vue'
import QuestionModal from '@/components/QuestionModal.vue'
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'VideoPlayer',
  components: {
    Header,
    ExerciseModal,
    AIAssistantModal,
    QuestionModal
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // 视频播放状态
    const isPlaying = ref(false)
    const currentTime = ref(0)
    const duration = ref(0)
    const isMuted = ref(false)
    const volume = ref(1.0)
    const playbackRate = ref(1.0)
    const showSubtitles = ref(true)
    const isFullscreen = ref(false)
    const showSettings = ref(false)
    
    // 学习状态
    const activeTool = ref('exercise')
    const progressPercentage = ref(35)
    const masteryPercentage = ref(72)
    const learnedTime = ref(743) // 秒
    
    // 模态框状态
    const showExerciseModal = ref(false)
    const showAIModal = ref(false)
    const showQuestionModal = ref(false)
    
    // 课程数据
    const course = ref({
      id: route.params.courseId || 1,
      title: 'Python数据分析与可视化实战',
      progress: 35
    })
    
    const currentLesson = ref({
      id: 2,
      title: '1.2 Pandas数据结构详解',
      description: '本节详细介绍Pandas的核心数据结构：Series和DataFrame。学习如何创建、访问和操作这些数据结构，为后续的数据分析打下坚实基础。我们将通过实际代码演示，展示如何从列表、字典和NumPy数组创建Series和DataFrame，并介绍常用的数据访问方法。',
      duration: 1475, // 秒
      hasMaterials: true
    })
    
    // 字幕数据
    const currentSubtitle = ref('Pandas是Python中最重要的数据分析库之一')
    const subtitles = ref([
      "Pandas是Python中最重要的数据分析库之一",
      "它提供了两种核心数据结构：Series和DataFrame",
      "Series是一维数组，可以存储任意数据类型",
      "DataFrame是二维表格，可以看作多个Series的集合",
      "我们现在来看如何创建Series对象"
    ])
    
    // 课程大纲
    const syllabus = ref([
      {
        id: 1,
        title: '第一章：Python数据分析基础',
        expanded: true,
        lessons: [
          { id: 1, title: '1.1 课程介绍与环境搭建', duration: 1080, completed: true },
          { id: 2, title: '1.2 Pandas数据结构详解', duration: 1475, completed: false },
          { id: 3, title: '1.3 数据导入与导出', duration: 1320, completed: false }
        ]
      },
      {
        id: 2,
        title: '第二章：数据清洗与预处理',
        expanded: false,
        lessons: [
          { id: 4, title: '2.1 缺失值处理', duration: 1680, completed: false },
          { id: 5, title: '2.2 异常值检测与处理', duration: 1920, completed: false }
        ]
      }
    ])
    
    // 讨论区问题
    const questions = ref([
      {
        id: 1,
        name: '王同学',
        date: '2023-10-15 14:23',
        avatar: 'https://randomuser.me/api/portraits/women/32.jpg',
        content: 'Series和DataFrame在内存使用上有什么区别？在处理大数据集时应该如何选择？',
        likes: 12,
        comments: 5,
        aiAnswered: true
      },
      {
        id: 2,
        name: '李同学',
        date: '2023-10-14 09:15',
        avatar: 'https://randomuser.me/api/portraits/men/45.jpg',
        content: 'DataFrame的索引有什么作用？如何合理设置索引以提高查询效率？',
        likes: 8,
        comments: 3,
        aiAnswered: false
      }
    ])
    
    // 播放速度选项
    const playbackSpeeds = ref([
      { value: 0.5, label: '0.5x 速度' },
      { value: 0.75, label: '0.75x 速度' },
      { value: 1.0, label: '正常速度' },
      { value: 1.25, label: '1.25x 速度' },
      { value: 1.5, label: '1.5x 速度' },
      { value: 2.0, label: '2.0x 速度' }
    ])
    
    // AI建议
    const aiSuggestion = ref('您已掌握Series的基本操作，建议重点关注DataFrame的多维数据操作。')
    
    // 计算属性
    const playPauseIcon = computed(() => 
      isPlaying.value ? 'fas fa-pause' : 'fas fa-play'
    )
    
    const volumeIcon = computed(() => {
      if (isMuted.value || volume.value === 0) {
        return 'fas fa-volume-mute'
      } else if (volume.value < 0.5) {
        return 'fas fa-volume-down'
      } else {
        return 'fas fa-volume-up'
      }
    })
    
    const fullscreenIcon = computed(() => 
      isFullscreen.value ? 'fas fa-compress' : 'fas fa-expand'
    )
    
    // DOM 引用
    const videoElement = ref(null)
    const videoContainer = ref(null)
    
    // 方法
    const togglePlay = () => {
      if (!videoElement.value) return
      
      if (videoElement.value.paused) {
        videoElement.value.play()
        isPlaying.value = true
      } else {
        videoElement.value.pause()
        isPlaying.value = false
      }
    }
    
    const updateProgress = () => {
      if (!videoElement.value) return
      
      currentTime.value = videoElement.value.currentTime
      if (duration.value > 0) {
        progressPercentage.value = (currentTime.value / duration.value) * 100
      }
      
      // 更新学习时间
      learnedTime.value = Math.max(learnedTime.value, currentTime.value)
      
      // 更新字幕
      if (showSubtitles.value && duration.value > 0) {
        updateSubtitle()
      }
    }
    
    const onVideoLoaded = () => {
      if (videoElement.value) {
        duration.value = videoElement.value.duration
        showNotification('视频加载完成')
      }
    }
    
    const onVideoEnded = () => {
      isPlaying.value = false
      markLessonAsCompleted(currentLesson.value.id)
      showNotification('本节内容已学习完成，系统已记录您的学习进度')
    }
    
    // 视频错误处理
    const handleVideoError = (error) => {
      console.error('视频加载错误:', error)
      showNotification('视频加载失败，请检查网络连接或刷新页面')
      
      // 尝试使用备用视频源
      if (videoElement.value) {
        // 如果有多个source标签，浏览器会自动尝试下一个
        console.log('尝试备用视频源...')
      }
    }
    
    const seekToTime = (event) => {
      if (!videoElement.value || !duration.value) return
      
      const rect = event.currentTarget.getBoundingClientRect()
      const clickPosition = event.clientX - rect.left
      const percentage = clickPosition / rect.width
      
      videoElement.value.currentTime = percentage * duration.value
    }
    
    const toggleMute = () => {
      if (!videoElement.value) return
      
      if (isMuted.value) {
        videoElement.value.volume = volume.value
        isMuted.value = false
      } else {
        volume.value = videoElement.value.volume
        videoElement.value.volume = 0
        isMuted.value = true
      }
    }
    
    const setPlaybackSpeed = (speed) => {
      playbackRate.value = speed
      if (videoElement.value) {
        videoElement.value.playbackRate = speed
      }
      showSettings.value = false
    }
    
    const toggleSubtitles = () => {
      showSubtitles.value = !showSubtitles.value
      showSettings.value = false
    }
    
    const togglePictureInPicture = async () => {
      try {
        if (document.pictureInPictureElement) {
          await document.exitPictureInPicture()
        } else if (document.pictureInPictureEnabled && videoElement.value) {
          await videoElement.value.requestPictureInPicture()
        }
      } catch (error) {
        showNotification('您的浏览器不支持画中画模式')
      }
      showSettings.value = false
    }
    
    const toggleFullscreen = () => {
      if (!videoContainer.value) return
      
      if (!document.fullscreenElement) {
        videoContainer.value.requestFullscreen()
          .then(() => {
            isFullscreen.value = true
          })
          .catch(err => {
            console.log('全屏请求失败:', err)
          })
      } else {
        document.exitFullscreen()
        isFullscreen.value = false
      }
    }
    
    const updateSubtitle = () => {
      if (!duration.value || subtitles.value.length === 0) return
      
      const timeSegments = duration.value / subtitles.value.length
      const currentSegment = Math.floor(currentTime.value / timeSegments)
      
      if (currentSegment < subtitles.value.length) {
        currentSubtitle.value = subtitles.value[currentSegment]
      }
    }
    
    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
    
    const formatDuration = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return secs > 0 ? `${mins}分${secs}秒` : `${mins}分钟`
    }
    
    const selectLesson = (lesson) => {
      if (currentLesson.value.id === lesson.id) return
      
      currentLesson.value = { ...lesson }
      isPlaying.value = false
      currentTime.value = 0
      progressPercentage.value = 0
      
      // 重置视频
      if (videoElement.value) {
        videoElement.value.load()
      }
      
      showNotification(`正在加载: ${lesson.title}`)
    }
    
    const prevLesson = () => {
      showNotification('切换到上一节内容')
    }
    
    const nextLesson = () => {
      const currentChapter = syllabus.value.find(ch => 
        ch.lessons.some(lesson => lesson.id === currentLesson.value.id)
      )
      
      if (currentChapter) {
        const currentIndex = currentChapter.lessons.findIndex(
          lesson => lesson.id === currentLesson.value.id
        )
        
        if (currentIndex < currentChapter.lessons.length - 1) {
          const nextLesson = currentChapter.lessons[currentIndex + 1]
          selectLesson(nextLesson)
        }
      }
    }
    
    const toggleChapter = (chapterId) => {
      const chapter = syllabus.value.find(ch => ch.id === chapterId)
      if (chapter) {
        chapter.expanded = !chapter.expanded
      }
    }
    
    const markLessonAsCompleted = (lessonId) => {
      syllabus.value.forEach(chapter => {
        chapter.lessons.forEach(lesson => {
          if (lesson.id === lessonId) {
            lesson.completed = true
          }
        })
      })
    }
    
    const activateTool = (tool) => {
      activeTool.value = tool
      
      if (tool === 'exercise') {
        showExerciseModal.value = true
      }
      
      showNotification(`打开${getToolName(tool)}功能`)
    }
    
    const getToolName = (tool) => {
      const toolNames = {
        qa: '课程问答',
        notes: '课堂笔记',
        exercise: '章节习题',
        download: '资料下载'
      }
      return toolNames[tool] || tool
    }
    
    const likeQuestion = (questionId) => {
      const question = questions.value.find(q => q.id === questionId)
      if (question) {
        question.likes += 1
      }
    }
    
    const showNotification = (message) => {
      // 移除之前可能存在的通知
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
        background-color: #165DFF;
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
        <i class="fas fa-info-circle"></i>
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
    
    // 键盘事件处理
    const handleKeydown = (event) => {
      if (!videoElement.value) return
      
      switch (event.key) {
        case ' ':
        case 'k':
          event.preventDefault()
          togglePlay()
          break
        case 'm':
          event.preventDefault()
          toggleMute()
          break
        case 'f':
          event.preventDefault()
          toggleFullscreen()
          break
        case 'ArrowLeft':
          event.preventDefault()
          videoElement.value.currentTime -= 10
          break
        case 'ArrowRight':
          event.preventDefault()
          videoElement.value.currentTime += 10
          break
      }
    }
    
    const handleFullscreenChange = () => {
      isFullscreen.value = !!document.fullscreenElement
    }
    
    // 加载学习进度
    const loadLearningProgress = () => {
      const progress = localStorage.getItem(`course_${course.value.id}_progress`)
      if (progress) {
        const data = JSON.parse(progress)
        progressPercentage.value = data.progressPercentage || 35
        learnedTime.value = data.learnedTime || 743
        
        // 更新课程完成状态
        if (data.completedLessons) {
          syllabus.value.forEach(chapter => {
            chapter.lessons.forEach(lesson => {
              lesson.completed = data.completedLessons.includes(lesson.id)
            })
          })
        }
      }
    }
    
    // 保存学习进度
    const saveLearningProgress = () => {
      const completedLessons = []
      syllabus.value.forEach(chapter => {
        chapter.lessons.forEach(lesson => {
          if (lesson.completed) {
            completedLessons.push(lesson.id)
          }
        })
      })
      
      const progress = {
        progressPercentage: progressPercentage.value,
        learnedTime: learnedTime.value,
        completedLessons,
        lastPlayed: new Date().toISOString()
      }
      
      localStorage.setItem(`course_${course.value.id}_progress`, JSON.stringify(progress))
    }
    
    // 初始化Font Awesome
    const initFontAwesome = () => {
      // 检查是否已经加载了Font Awesome
      if (!document.querySelector('link[href*="font-awesome"]')) {
        const link = document.createElement('link')
        link.rel = 'stylesheet'
        link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
        link.integrity = 'sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw=='
        link.crossOrigin = 'anonymous'
        link.referrerPolicy = 'no-referrer'
        document.head.appendChild(link)
      }
    }
    
    // 生命周期钩子
    onMounted(() => {
      // 初始化Font Awesome
      initFontAwesome()
      
      loadLearningProgress()
      
      // 添加事件监听器
      document.addEventListener('fullscreenchange', handleFullscreenChange)
      document.addEventListener('keydown', handleKeydown)
      
      // 检查用户是否已登录
      const user = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
      if (!user) {
        router.push('/login')
      }
      
      // 初始化视频
      if (videoElement.value) {
        videoElement.value.playbackRate = playbackRate.value
      }
      
      // 添加动画样式
      if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style')
        style.id = 'notification-styles'
        style.textContent = `
          @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
          }
          @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
          }
        `
        document.head.appendChild(style)
      }
    })
    
    onBeforeUnmount(() => {
      saveLearningProgress()
      
      // 移除事件监听器
      document.removeEventListener('fullscreenchange', handleFullscreenChange)
      document.removeEventListener('keydown', handleKeydown)
    })
    
    return {
      // 状态
      isPlaying,
      currentTime,
      duration,
      isMuted,
      volume,
      playbackRate,
      showSubtitles,
      isFullscreen,
      showSettings,
      activeTool,
      progressPercentage,
      masteryPercentage,
      learnedTime,
      showExerciseModal,
      showAIModal,
      showQuestionModal,
      course,
      currentLesson,
      currentSubtitle,
      subtitles,
      syllabus,
      questions,
      playbackSpeeds,
      aiSuggestion,
      
      // 计算属性
      playPauseIcon,
      volumeIcon,
      fullscreenIcon,
      
      // DOM 引用
      videoElement,
      videoContainer,
      
      // 方法
      togglePlay,
      updateProgress,
      onVideoLoaded,
      onVideoEnded,
      handleVideoError,
      seekToTime,
      toggleMute,
      setPlaybackSpeed,
      toggleSubtitles,
      togglePictureInPicture,
      toggleFullscreen,
      updateSubtitle,
      formatTime,
      formatDuration,
      selectLesson,
      prevLesson,
      nextLesson,
      toggleChapter,
      markLessonAsCompleted,
      activateTool,
      getToolName,
      likeQuestion,
      showNotification
    }
  }
}
</script>


<style scoped>
/* 从原H5页面复制关键样式，确保Tailwind不覆盖自定义样式 */

.page-header {
  max-width: 1400px;
  margin: 1rem auto 0;
  padding: 0 1.5rem;
}

.breadcrumb {
  display: flex;
  gap: 0.5rem;
  color: #4E5969;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.breadcrumb a {
  color: #165DFF;
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem 3rem;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}

.video-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.video-container {
  background-color: #000;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.video-player {
  width: 100%;
  height: 500px;
  background-color: #111;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

@media (max-width: 1200px) {
  .video-player {
    height: 400px;
  }
}

@media (max-width: 768px) {
  .video-player {
    height: 300px;
  }
}

.video-placeholder {
  text-align: center;
  color: white;
  z-index: 1;
}

.video-controls {
  background-color: rgba(0, 0, 0, 0.8);
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 1rem;
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

.progress-container {
  flex-grow: 1;
  margin: 0 1rem;
  position: relative;
  cursor: pointer;
}

.progress-bar {
  height: 4px;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  position: relative;
  overflow: hidden;
}

.progress-fill {
  position: absolute;
  height: 100%;
  background-color: #FF9F43;
  border-radius: 2px;
  transition: width 0.1s;
}

.progress-handle {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 12px;
  height: 12px;
  background-color: #FF9F43;
  border-radius: 50%;
  display: none;
}

.progress-container:hover .progress-handle {
  display: block;
}

.time-display {
  color: white;
  font-size: 0.9rem;
  min-width: 100px;
  text-align: center;
}

.video-settings {
  position: relative;
}

.settings-menu {
  position: absolute;
  bottom: 100%;
  right: 0;
  background-color: rgba(0, 0, 0, 0.9);
  border-radius: 8px;
  padding: 0.8rem;
  min-width: 150px;
  z-index: 10;
}

.settings-item {
  color: white;
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
  font-size: 0.9rem;
}

.settings-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.settings-item.active {
  background-color: rgba(255, 255, 255, 0.15);
  color: #FF9F43;
}

.subtitle-container {
  position: absolute;
  bottom: 80px;
  left: 0;
  right: 0;
  text-align: center;
  z-index: 5;
  padding: 0 2rem;
}

.subtitle-text {
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  display: inline-block;
  font-size: 1.1rem;
  max-width: 80%;
}

.video-info {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
}

.current-video-title {
  font-size: 1.5rem;
  margin-bottom: 0.8rem;
  color: #1F2937;
}

.video-description {
  color: #4E5969;
  margin-bottom: 1.2rem;
  line-height: 1.6;
}

.video-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #F7F8FA;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #4E5969;
  font-size: 0.9rem;
}

.learning-tools {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
}

.tools-title {
  font-size: 1.2rem;
  margin-bottom: 1.2rem;
  color: #1F2937;
}

.tool-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 768px) {
  .tool-buttons {
    grid-template-columns: 1fr;
  }
}

.tool-btn {
  padding: 0.8rem;
  border-radius: 8px;
  border: 1px solid #F7F8FA;
  background-color: white;
  color: #1F2937;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.tool-btn:hover,
.tool-btn.active {
  background-color: #f8fdff;
  border-color: #165DFF;
}

.ai-assistant {
  background-color: #f0f9ff;
  border: 1px solid #c2e7ff;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.ai-assistant:hover {
  background-color: #e1f5ff;
}

.ai-icon {
  width: 50px;
  height: 50px;
  background-color: #165DFF;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}

.ai-text h4 {
  font-size: 1rem;
  margin-bottom: 0.3rem;
  color: #1F2937;
}

.ai-text p {
  color: #4E5969;
  font-size: 0.9rem;
}

.discussion-section {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
}

.discussion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.discussion-title {
  font-size: 1.2rem;
  color: #1F2937;
}

.new-question-btn {
  background-color: #165DFF;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s;
}

.new-question-btn:hover {
  background-color: #6B7280;
}

.question-list {
  list-style: none;
}

.question-item {
  padding: 1.2rem;
  border: 1px solid #F7F8FA;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.question-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.8rem;
}

.questioner {
  display: flex;
  align-items: center;
  gap: 10px;
}

.questioner-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #F7F8FA;
}

.questioner-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.questioner-info h4 {
  font-size: 1rem;
  margin-bottom: 0.2rem;
  color: #1F2937;
}

.question-date {
  color: #E5E6EB;
  font-size: 0.9rem;
}

.ai-tag {
  background-color: #f0f9ff;
  color: #165DFF;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.question-content {
  color: #1F2937;
  line-height: 1.7;
  margin-bottom: 1rem;
}

.question-actions {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #4E5969;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  transition: color 0.3s;
}

.action-btn:hover {
  color: #165DFF;
}

.course-directory {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
}

.directory-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.directory-title {
  font-size: 1.2rem;
  color: #1F2937;
}

.course-progress {
  background-color: #f0f9ff;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #165DFF;
  font-weight: 500;
}

.directory-list {
  list-style: none;
  max-height: 600px;
  overflow-y: auto;
}

.directory-section {
  margin-bottom: 1rem;
}

.section-header {
  padding: 0.8rem 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  font-weight: 600;
  color: #1F2937;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.3s;
}

.section-header:hover {
  background-color: #f0f9ff;
}

.section-header i {
  transition: transform 0.3s;
}

.section-header i.rotated {
  transform: rotate(-90deg);
}

.lesson-list {
  padding-left: 1rem;
  margin-top: 0.5rem;
  overflow: hidden;
}

.lesson-item {
  padding: 0.8rem 1rem;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.lesson-item:hover {
  background-color: #f8fdff;
}

.lesson-item.active {
  background-color: #f0f9ff;
  border-left: 3px solid #165DFF;
}

.lesson-item.completed .lesson-title {
  color: #10B981;
}

.lesson-info {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.lesson-icon {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #f0f9ff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #165DFF;
  font-size: 0.9rem;
}

.lesson-title {
  font-weight: 500;
}

.lesson-duration {
  color: #4E5969;
  font-size: 0.85rem;
}

.lesson-status {
  display: flex;
  align-items: center;
}

/* 动画 */
@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

@keyframes slideOut {
  from { transform: translateX(0); opacity: 1; }
  to { transform: translateX(100%); opacity: 0; }
}

@media (max-width: 576px) {
  .main-content {
    padding: 0 1rem 2rem;
  }
  
  .video-info,
  .learning-tools,
  .course-directory,
  .discussion-section {
    padding: 1.2rem;
  }
  
  .current-video-title {
    font-size: 1.3rem;
  }
  
  .video-meta {
    gap: 1rem;
  }
  
  .control-group {
    gap: 0.5rem;
  }
  
  .progress-container {
    margin: 0 0.5rem;
  }
}

/* 确保Font Awesome图标正常显示 */
.fas {
  font-family: 'Font Awesome 6 Free' !important;
  font-weight: 900 !important;
}

/* 模态框定位 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}
</style>