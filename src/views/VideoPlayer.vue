<template>
  <section class="video-player-page" v-if="video">
    <div class="container">
      <div class="video-layout">
        <!-- 左侧主内容区 -->
        <div class="video-main">
          <!-- 视频播放器 -->
          <div class="video-container">
            <div class="video-wrapper" @mousemove="showControlsWithTimeout" @mouseleave="hideControls">
              <video 
                ref="videoPlayer" 
                :poster="video.thumbnail"
                @timeupdate="updateProgress"
                @loadedmetadata="setDuration"
                @click="togglePlay"
                @play="handlePlay"
                @pause="handlePause"
                @ended="handleEnded"
              >
                <source :src="video.src" type="video/mp4">
                您的浏览器不支持 HTML5 视频。
              </video>
              <div class="video-controls-overlay" v-show="showControls">
                <div class="video-title-overlay">
                  <h2>{{ video.title }}</h2>
                </div>
                <div class="playback-controls">
                  <button class="control-btn" @click="togglePlay">
                    <i :class="isPlaying ? 'fas fa-pause' : 'fas fa-play'"></i>
                  </button>
                  <div class="progress-container">
                    <div class="progress-bar" @click="seekVideo">
                      <div class="progress-fill" :style="{ width: progress + '%' }"></div>
                      <div class="progress-handle" :style="{ left: progress + '%' }"></div>
                    </div>
                    <div class="time-display">
                      <span class="current-time">{{ formatTime(currentTime) }}</span> / 
                      <span class="duration">{{ formatTime(duration) }}</span>
                    </div>
                  </div>
                  <button class="control-btn" @click="toggleFullscreen">
                    <i :class="isFullscreen ? 'fas fa-compress' : 'fas fa-expand'"></i>
                  </button>
                </div>
              </div>
              
              <!-- 播放覆盖层 -->
              <div class="play-overlay" v-show="!isPlaying && showPlayOverlay" @click="togglePlay">
                <i class="fas fa-play"></i>
              </div>
            </div>
          </div>

          <!-- 视频信息 -->
          <div class="video-info">
            <div class="video-meta-header">
              <h1>{{ video.title }}</h1>
              <div class="video-stats">
                <span><i class="fas fa-play"></i> {{ video.views }} 次播放</span>
                <span><i class="far fa-calendar"></i> {{ video.date }}</span>
              </div>
            </div>

            <!-- 互动操作 -->
            <div class="video-actions">
              <div class="action-group">
                <button 
                  class="action-btn like-btn" 
                  :class="{ active: isLiked }"
                  @click="toggleLike"
                >
                  <i :class="isLiked ? 'fas fa-thumbs-up' : 'far fa-thumbs-up'"></i>
                  <span class="action-count">{{ video.likes }}</span>
                </button>
                <button class="action-btn dislike-btn" @click="toggleDislike">
                  <i :class="isDisliked ? 'fas fa-thumbs-down' : 'far fa-thumbs-down'"></i>
                </button>
              </div>
              <div class="action-group">
                <button 
                  class="action-btn" 
                  :class="{ active: isCollected }"
                  @click="toggleCollect"
                >
                  <i :class="isCollected ? 'fas fa-star' : 'far fa-star'"></i>
                  <span class="action-text">{{ isCollected ? '已收藏' : '收藏' }}</span>
                  <span class="action-count">{{ video.collections }}</span>
                </button>
              </div>
              <div class="action-group">
                <button class="action-btn" @click="shareVideo">
                  <i class="fas fa-share"></i>
                  <span class="action-text">分享</span>
                </button>
              </div>
              <div class="action-group">
                <button class="action-btn download-btn" @click="downloadVideo">
                  <i class="fas fa-download"></i>
                  <span class="action-text">下载</span>
                </button>
              </div>
            </div>

            <!-- 课程信息 -->
            <div class="course-info-card">
              <div class="instructor-info">
                <div class="instructor-avatar">
                  <i class="fas fa-user-tie"></i>
                </div>
                <div class="instructor-details">
                  <h4>{{ course.instructor.name }}</h4>
                  <p>{{ course.instructor.title }}</p>
                </div>
                <button class="btn btn-outline btn-follow" @click="toggleFollow">
                  {{ isFollowing ? '已关注' : '关注' }}
                </button>
              </div>
              <div class="course-description">
                <p>{{ course.description }}</p>
              </div>
            </div>
          </div>

          <!-- 评论区 -->
          <div class="comments-section">
            <div class="comments-header">
              <h3>评论 <span class="comments-count">{{ comments.length }}</span></h3>
              <div class="comments-sort">
                <select class="sort-select" v-model="sortBy">
                  <option value="hot">最热</option>
                  <option value="newest">最新</option>
                </select>
              </div>
            </div>

            <!-- 评论输入 -->
            <div class="comment-input">
              <div class="user-avatar">
                <i class="fas fa-user"></i>
              </div>
              <div class="input-container">
                <textarea 
                  v-model="newComment" 
                  placeholder="发一条友善的评论" 
                  class="comment-textarea"
                  @input="checkComment"
                  @focus="showCommentActions = true"
                ></textarea>
                <div class="comment-actions" v-show="showCommentActions">
                  <button type="button" class="btn btn-outline" @click="cancelComment">取消</button>
                  <button 
                    type="button" 
                    class="btn btn-primary" 
                    :disabled="!newComment.trim()"
                    @click="submitComment"
                  >
                    评论
                  </button>
                </div>
              </div>
            </div>

            <!-- 评论列表 -->
            <div class="comments-list">
              <div v-for="comment in sortedComments" :key="comment.id" class="comment-item">
                <div class="comment-avatar">
                  <i class="fas fa-user"></i>
                </div>
                <div class="comment-content">
                  <div class="comment-header">
                    <span class="comment-author">{{ comment.author }}</span>
                    <span class="comment-time">{{ comment.time }}</span>
                  </div>
                  <div class="comment-text">
                    <p>{{ comment.content }}</p>
                  </div>
                  <div class="comment-actions">
                    <button class="comment-action-btn" @click="likeComment(comment.id)">
                      <i class="far fa-thumbs-up"></i>
                      <span>{{ comment.likes }}</span>
                    </button>
                    <button class="comment-action-btn" @click="dislikeComment(comment.id)">
                      <i class="far fa-thumbs-down"></i>
                    </button>
                    <button class="comment-action-btn reply-btn" @click="replyToComment(comment.id)">回复</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧边栏 -->
        <div class="video-sidebar">
          <!-- 播放列表 -->
          <div class="playlist-section">
            <div class="section-header">
              <h3>课程目录</h3>
              <span class="playlist-count">{{ totalLessons }}个视频</span>
            </div>
            <div class="playlist">
              <div 
                v-for="(module, moduleIndex) in course.modules" 
                :key="moduleIndex"
                class="playlist-module"
              >
                <div class="module-title">{{ module.title }}</div>
                <div 
                  v-for="(lesson, lessonIndex) in module.lessons" 
                  :key="lessonIndex"
                  class="playlist-item"
                  :class="{ 
                    active: currentVideoId === lesson.id,
                    locked: !isLessonUnlocked(lesson.id)
                  }"
                  @click="switchVideo(lesson)"
                >
                  <div class="item-icon">
                    <i 
                      :class="currentVideoId === lesson.id ? 'fas fa-play-circle' : 
                             (isLessonUnlocked(lesson.id) ? 'far fa-play-circle' : 'fas fa-lock')"
                    ></i>
                  </div>
                  <div class="item-content">
                    <div class="item-title">{{ lesson.title }}</div>
                    <div class="item-meta">
                      <span class="item-duration">{{ lesson.duration }}</span>
                      <span v-if="currentVideoId === lesson.id" class="item-status">正在播放</span>
                      <span v-else-if="isLessonCompleted(lesson.id)" class="item-status completed">已完成</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 推荐视频 -->
          <div class="recommendations-section">
            <div class="section-header">
              <h3>相关推荐</h3>
            </div>
            <div class="recommendations-list">
              <div 
                v-for="(recommendation, index) in recommendedVideos" 
                :key="index"
                class="recommendation-item"
                @click="navigateToRecommendedVideo(recommendation)"
              >
                <div class="recommendation-thumbnail">
                  <img :src="recommendation.thumbnail" :alt="recommendation.title">
                  <div class="video-duration">{{ recommendation.duration }}</div>
                </div>
                <div class="recommendation-info">
                  <h4 class="video-title">{{ recommendation.title }}</h4>
                  <p class="video-instructor">{{ recommendation.instructor }}</p>
                  <div class="video-stats">
                    <span>{{ recommendation.views }}次播放</span>
                    <span>{{ recommendation.comments }}条评论</span>
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
  name: 'VideoPlayer',
  props: ['courseId', 'videoId'],
  data() {
    return {
      video: null,
      course: null,
      isPlaying: false,
      isFullscreen: false,
      showControls: true,
      showPlayOverlay: true,
      currentTime: 0,
      duration: 0,
      progress: 0,
      isLiked: false,
      isDisliked: false,
      isCollected: false,
      isFollowing: false,
      sortBy: 'hot',
      newComment: '',
      showCommentActions: false,
      comments: [],
      controlsTimeout: null,
      completedLessons: new Set(),
      recommendedVideos: []
    }
  },
  computed: {
    currentVideoId() {
      return this.video?.id
    },
    totalLessons() {
      return this.course?.modules.reduce((total, module) => total + module.lessons.length, 0) || 0
    },
    sortedComments() {
      const comments = [...this.comments]
      if (this.sortBy === 'hot') {
        return comments.sort((a, b) => b.likes - a.likes)
      } else {
        return comments.sort((a, b) => new Date(b.time) - new Date(a.time))
      }
    }
  },
  created() {
    this.loadVideoData()
  },
  mounted() {
    this.setupEventListeners()
  },
  beforeUnmount() {
    this.removeEventListeners()
    this.clearControlsTimeout()
  },
  watch: {
    videoId(newVideoId) {
      this.switchVideoById(newVideoId)
    }
  },
  methods: {
    loadVideoData() {
      // 模拟视频数据
      const courses = {
        1: {
          id: 1,
          title: '机器学习入门',
          description: '本课程将广泛介绍机器学习、数据挖掘和统计模式识别。您将学习分析和理解大型数据集的方法；不仅学习理论基础，还将获得快速强大地将这些技术应用于新问题的实践知识。',
          instructor: {
            name: 'Andrew Ng',
            title: '斯坦福大学计算机科学教授'
          },
          modules: [
            {
              title: '第1周：机器学习简介',
              lessons: [
                { 
                  id: '1-1', 
                  title: '1.1 什么是机器学习 - 机器学习基础概念介绍',
                  duration: '15:30',
                  src: 'https://example.com/videos/1-1.mp4',
                  thumbnail: 'https://via.placeholder.com/800x450/0056d2/ffffff?text=视频封面',
                  views: 12456,
                  date: '2023-10-15',
                  likes: 1234,
                  collections: 896
                },
                { 
                  id: '1-2', 
                  title: '1.2 监督学习与非监督学习',
                  duration: '20:15',
                  src: 'https://example.com/videos/1-2.mp4',
                  thumbnail: 'https://via.placeholder.com/800x450/0056d2/ffffff?text=视频封面',
                  views: 11234,
                  date: '2023-10-15',
                  likes: 987,
                  collections: 654
                },
                { 
                  id: '1-3', 
                  title: '1.3 机器学习应用案例',
                  duration: '25:45',
                  src: 'https://example.com/videos/1-3.mp4',
                  thumbnail: 'https://via.placeholder.com/800x450/0056d2/ffffff?text=视频封面',
                  views: 9876,
                  date: '2023-10-15',
                  likes: 765,
                  collections: 432
                }
              ]
            },
            {
              title: '第2周：线性回归',
              lessons: [
                { 
                  id: '2-1', 
                  title: '2.1 线性回归基础',
                  duration: '30:20',
                  src: 'https://example.com/videos/2-1.mp4',
                  thumbnail: 'https://via.placeholder.com/800x450/0056d2/ffffff?text=视频封面',
                  views: 8765,
                  date: '2023-10-15',
                  likes: 654,
                  collections: 321
                }
              ]
            }
          ]
        }
      }
      
      this.course = courses[this.courseId] || courses[1]
      this.switchVideoById(this.videoId)
      
      // 模拟评论数据
      this.comments = [
        {
          id: 1,
          author: '张三',
          time: '2天前',
          content: 'Andrew教授的讲解非常清晰，让我对机器学习有了全新的认识。特别是梯度下降算法的部分，讲得太好了！',
          likes: 256
        },
        {
          id: 2,
          author: '李四',
          time: '3天前',
          content: '课程内容很扎实，但是有些数学推导对于没有相关背景的同学来说可能有点困难。建议先学习一些线性代数的基础知识。',
          likes: 189
        }
      ]

      // 模拟推荐视频
      this.recommendedVideos = [
        {
          id: 'rec-1',
          title: 'Python编程入门',
          instructor: 'Charles Severance',
          duration: '12:30',
          thumbnail: 'https://via.placeholder.com/120x68/28a745/ffffff?text=Python',
          views: '8.7万',
          comments: 256
        },
        {
          id: 'rec-2',
          title: '数据科学基础',
          instructor: '李明',
          duration: '18:45',
          thumbnail: 'https://via.placeholder.com/120x68/dc3545/ffffff?text=Data+Science',
          views: '6.3万',
          comments: 189
        },
        {
          id: 'rec-3',
          title: '深度学习入门',
          instructor: '吴恩达',
          duration: '22:15',
          thumbnail: 'https://via.placeholder.com/120x68/ffc107/333333?text=Deep+Learning',
          views: '12.4万',
          comments: 432
        }
      ]
    },

    switchVideoById(videoId) {
      const lesson = this.course.modules
        .flatMap(module => module.lessons)
        .find(lesson => lesson.id === videoId)
      
      if (lesson) {
        this.switchVideo(lesson)
      } else {
        this.video = this.course.modules[0].lessons[0]
      }
    },

    switchVideo(lesson) {
      if (!this.isLessonUnlocked(lesson.id)) {
        this.showAlert('课程锁定', '请先完成前面的课程内容', 'warning')
        return
      }

      // 保存当前视频进度
      if (this.video) {
        this.saveVideoProgress()
      }

      this.video = lesson
      this.$nextTick(() => {
        this.resetVideoState()
        // 不自动播放，等待用户点击
        this.showPlayOverlay = true
        this.isPlaying = false
      })
    },

    resetVideoState() {
      this.currentTime = 0
      this.progress = 0
      this.isPlaying = false
      this.showPlayOverlay = true
      this.showControls = true
    },

    setupEventListeners() {
      document.addEventListener('fullscreenchange', this.handleFullscreenChange)
      document.addEventListener('keydown', this.handleKeydown)
      
      // 添加点击事件监听器来控制显示/隐藏控件
      document.addEventListener('click', this.handleDocumentClick)
    },

    removeEventListeners() {
      document.removeEventListener('fullscreenchange', this.handleFullscreenChange)
      document.removeEventListener('keydown', this.handleKeydown)
      document.removeEventListener('click', this.handleDocumentClick)
    },

    handleDocumentClick(event) {
      // 如果点击的是视频区域但不是控件按钮，切换播放状态
      const videoWrapper = this.$el.querySelector('.video-wrapper')
      if (videoWrapper && videoWrapper.contains(event.target)) {
        const isControlButton = event.target.closest('.control-btn') || 
                               event.target.closest('.playback-controls')
        if (!isControlButton) {
          this.togglePlay()
        }
      }
    },

    async togglePlay() {
      const video = this.$refs.videoPlayer
      if (!video) return

      try {
        if (this.isPlaying) {
          video.pause()
        } else {
          await video.play()
          this.showPlayOverlay = false
        }
      } catch (error) {
        console.error('播放控制错误:', error)
        this.showAlert('播放错误', '视频播放出现问题，请刷新页面重试', 'error')
      }
    },

    handlePlay() {
      this.isPlaying = true
      this.showPlayOverlay = false
      this.hideControlsWithTimeout()
    },

    handlePause() {
      this.isPlaying = false
      this.showPlayOverlay = true
      this.showControlsWithTimeout()
    },

    handleEnded() {
      this.isPlaying = false
      this.showPlayOverlay = true
      this.showControls = true
      this.markLessonAsCompleted(this.video.id)
      
      this.showAlert('学习完成', `恭喜完成 "${this.video.title}" 的学习！`, 'success')
    },

    toggleFullscreen() {
      const videoWrapper = this.$el.querySelector('.video-wrapper')
      if (!this.isFullscreen) {
        if (videoWrapper.requestFullscreen) {
          videoWrapper.requestFullscreen()
        } else if (videoWrapper.webkitRequestFullscreen) {
          videoWrapper.webkitRequestFullscreen()
        } else if (videoWrapper.msRequestFullscreen) {
          videoWrapper.msRequestFullscreen()
        }
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen()
        } else if (document.webkitExitFullscreen) {
          document.webkitExitFullscreen()
        } else if (document.msExitFullscreen) {
          document.msExitFullscreen()
        }
      }
    },

    handleFullscreenChange() {
      this.isFullscreen = !!document.fullscreenElement
    },

    handleKeydown(event) {
      if (event.code === 'Space') {
        event.preventDefault()
        this.togglePlay()
      }
    },

    updateProgress() {
      const video = this.$refs.videoPlayer
      if (video && video.duration) {
        this.currentTime = video.currentTime
        this.progress = (video.currentTime / video.duration) * 100
      }
    },

    setDuration() {
      const video = this.$refs.videoPlayer
      if (video) {
        this.duration = video.duration
      }
    },

    seekVideo(event) {
      const progressBar = event.currentTarget
      const clickPosition = event.offsetX
      const width = progressBar.offsetWidth
      const percentage = clickPosition / width
      
      const video = this.$refs.videoPlayer
      if (video && video.duration) {
        video.currentTime = percentage * video.duration
      }
    },

    formatTime(seconds) {
      if (isNaN(seconds)) return '00:00'
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    },

    showControlsWithTimeout() {
      this.showControls = true
      this.clearControlsTimeout()
      this.controlsTimeout = setTimeout(() => {
        if (this.isPlaying) {
          this.showControls = false
        }
      }, 3000)
    },

    hideControls() {
      if (this.isPlaying) {
        this.showControls = false
      }
    },

    hideControlsWithTimeout() {
      this.clearControlsTimeout()
      this.controlsTimeout = setTimeout(() => {
        this.showControls = false
      }, 3000)
    },

    clearControlsTimeout() {
      if (this.controlsTimeout) {
        clearTimeout(this.controlsTimeout)
        this.controlsTimeout = null
      }
    },

    toggleLike() {
      this.isLiked = !this.isLiked
      if (this.isLiked) {
        this.video.likes++
        this.isDisliked = false
      } else {
        this.video.likes--
      }
    },

    toggleDislike() {
      this.isDisliked = !this.isDisliked
      if (this.isDisliked) {
        this.isLiked = false
      }
    },

    toggleCollect() {
      this.isCollected = !this.isCollected
      this.video.collections += this.isCollected ? 1 : -1
    },

    toggleFollow() {
      this.isFollowing = !this.isFollowing
      this.showAlert(
        this.isFollowing ? '关注成功' : '取消关注',
        this.isFollowing ? 
          `您已关注 ${this.course.instructor.name}` : 
          `您已取消关注 ${this.course.instructor.name}`,
        'success'
      )
    },

    shareVideo() {
      if (navigator.share) {
        navigator.share({
          title: this.video.title,
          text: `观看课程: ${this.video.title}`,
          url: window.location.href
        })
      } else {
        navigator.clipboard.writeText(window.location.href)
        this.showAlert('分享成功', '视频链接已复制到剪贴板！', 'success')
      }
    },

    downloadVideo() {
      this.showAlert('下载功能', '视频下载功能将在完整版本中实现', 'info')
    },

    isLessonUnlocked(lessonId) {
      // 简单的解锁逻辑：前面的课程都解锁
      const allLessons = this.course.modules.flatMap(module => module.lessons)
      const currentIndex = allLessons.findIndex(lesson => lesson.id === lessonId)
      return currentIndex <= 1 // 模拟：前两个课程解锁
    },

    isLessonCompleted(lessonId) {
      return this.completedLessons.has(lessonId)
    },

    markLessonAsCompleted(lessonId) {
      this.completedLessons.add(lessonId)
    },

    saveVideoProgress() {
      // 保存视频观看进度到本地存储或后端
      const progress = {
        courseId: this.courseId,
        videoId: this.video.id,
        currentTime: this.currentTime,
        progress: this.progress,
        timestamp: new Date().toISOString()
      }
      localStorage.setItem(`videoProgress_${this.courseId}_${this.video.id}`, JSON.stringify(progress))
    },

    loadVideoProgress() {
      // 从本地存储加载视频观看进度
      const savedProgress = localStorage.getItem(`videoProgress_${this.courseId}_${this.video.id}`)
      if (savedProgress) {
        const progress = JSON.parse(savedProgress)
        const video = this.$refs.videoPlayer
        if (video) {
          video.currentTime = progress.currentTime
        }
      }
    },

    checkComment() {
      // 评论验证逻辑
    },

    submitComment() {
      if (!this.newComment.trim()) return
      
      const newComment = {
        id: Date.now(),
        author: '当前用户',
        time: '刚刚',
        content: this.newComment,
        likes: 0
      }
      
      this.comments.unshift(newComment)
      this.newComment = ''
      this.showCommentActions = false
      
      this.showAlert('评论成功', '您的评论已发布', 'success')
    },

    cancelComment() {
      this.newComment = ''
      this.showCommentActions = false
    },

    likeComment(commentId) {
      const comment = this.comments.find(c => c.id === commentId)
      if (comment) {
        comment.likes++
      }
    },

    dislikeComment(commentId) {
      // 点踩功能
      const comment = this.comments.find(c => c.id === commentId)
      if (comment) {
        // 可以添加点踩逻辑
      }
    },

    replyToComment(commentId) {
      this.showAlert('回复功能', '回复评论功能将在完整版本中实现', 'info')
    },

    navigateToRecommendedVideo(recommendation) {
      this.showAlert('跳转视频', `跳转到推荐视频: ${recommendation.title}`, 'info')
      // 在实际应用中，这里会跳转到对应的视频页面
    },

    // 替换 $notify 的通用提示方法
    showAlert(title, message, type = 'info') {
      // 使用浏览器原生 alert 作为临时解决方案
      alert(`${title}: ${message}`)
      
      // 或者使用全局的 $notify 如果存在的话
      if (this.$notify) {
        this.$notify({
          type: type,
          title: title,
          message: message
        })
      }
    }
  }
}
</script>

<style scoped>
.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: opacity 0.3s;
  z-index: 10;
}

.play-overlay i {
  font-size: 4rem;
  color: white;
  opacity: 0.8;
  transition: opacity 0.3s;
}

.play-overlay:hover i {
  opacity: 1;
}

.playlist-item .completed {
  color: var(--success);
  font-weight: 500;
}

.item-status.completed::before {
  content: '✓ ';
  font-weight: bold;
}

.recommendation-item {
  cursor: pointer;
  transition: background-color 0.3s;
}

.recommendation-item:hover {
  background-color: var(--secondary);
}

.comment-actions {
  margin-top: 10px;
}
</style>