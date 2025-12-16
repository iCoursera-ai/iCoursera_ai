<template>
  <div class="min-h-screen bg-gray-100">
    <Header />
    
    <!-- 面包屑导航 -->
    <div class="container">
      <nav class="breadcrumb">
        <router-link to="/">首页</router-link> > 
        <router-link :to="'/category/' + categoryId">{{ categoryName }}</router-link> > 
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
            <!-- 视频播放器 -->
            <div class="video-player" id="videoPlayer" @click="handleVideoPlayerClick">
              <div class="video-placeholder" v-if="!isPlaying && !hasStartedPlaying">
                <i class="fa fa-play-circle text-white text-6xl mb-4 opacity-70 cursor-pointer hover:opacity-100 transition-opacity"></i>
                <p class="text-white text-lg">点击播放视频</p>
              </div>
              <div v-if="hasStartedPlaying" class="video-wrapper">
                <video 
                  class="video-element w-full h-full object-contain"
                  ref="videoElement"
                  preload="metadata"
                  @timeupdate="updateProgress"
                  @loadedmetadata="onVideoLoaded"
                  @ended="onVideoEnded"
                  @error="handleVideoError"
                  :src="currentVideoUrl"
                  playsinline
                  webkit-playsinline
                >
                  您的浏览器不支持视频播放。
                </video>
              </div>
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
            <h3>{{ course.introTitle }}</h3>
            <p>{{ course.description }}</p>
            <div class="tags">
              <span class="tag" v-for="tag in course.tags" :key="tag">{{ tag }}</span>
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
            <div class="course-card-header">
              <div class="course-author" @click="goToTeacherSpace(instructor)">
                <div class="course-author-avatar">👤</div>
                <div>
                  <div class="course-author-name">{{ instructor.name }}</div>
                  <div class="course-author-fans">粉丝: {{ instructor.fans }}</div>
                </div>
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

          <!-- 课程章节导航 -->
          <div class="course-navigation">
            <div class="course-section-title">
              {{ courseTitle }}
            </div>
            
            <!-- 第一章 -->
            <div class="border-b border-gray-200">
              <div class="course-section-title flex justify-between items-center cursor-pointer" @click="toggleSection('section1')">
                <span>第一章 {{ getChapterName('section1') }}</span>
                <i class="fa" :class="section1Open ? 'fa-angle-down' : 'fa-angle-right'"></i>
              </div>
              <div class="pl-2" v-show="section1Open">
                <div 
                  class="course-item" 
                  :class="{ 'active': currentVideoIndex === 1 }"
                  @click="playVideo(1, '第一章 - ' + getVideoTitle(1))"
                >
                  <div class="course-item-icon course-item-video">
                    <i class="fa fa-play text-xs"></i>
                  </div>
                  <span>1.1 {{ getVideoTitle(1) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': false }"
                  @click="goToExerciseSeries('section_1_1')"
                >
                  <div class="course-item-icon course-item-exercise">
                    <i class="fa fa-pencil text-xs"></i>
                  </div>
                  <span>习题1.1：{{ getExerciseTitle(1) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': currentVideoIndex === 2 }"
                  @click="playVideo(2, '第一章 - ' + getVideoTitle(2))"
                >
                  <div class="course-item-icon course-item-video">
                    <i class="fa fa-play text-xs"></i>
                  </div>
                  <span>1.2 {{ getVideoTitle(2) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': false }"
                  @click="goToExerciseSeries('section_1_2')"
                >
                  <div class="course-item-icon course-item-exercise">
                    <i class="fa fa-pencil text-xs"></i>
                  </div>
                  <span>习题1.2：{{ getExerciseTitle(2) }}</span>
                </div>
              </div>
            </div>
            
            <!-- 第二章 -->
            <div class="border-b border-gray-200">
              <div class="course-section-title flex justify-between items-center cursor-pointer" @click="toggleSection('section2')">
                <span>第二章 {{ getChapterName('section2') }}</span>
                <i class="fa" :class="section2Open ? 'fa-angle-down' : 'fa-angle-right'"></i>
              </div>
              <div class="pl-2" v-show="section2Open">
                <div 
                  class="course-item" 
                  :class="{ 'active': currentVideoIndex === 3 }"
                  @click="playVideo(3, '第二章 - ' + getVideoTitle(3))"
                >
                  <div class="course-item-icon course-item-video">
                    <i class="fa fa-play text-xs"></i>
                  </div>
                  <span>2.1 {{ getVideoTitle(3) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': false }"
                  @click="goToExerciseSeries('section_2_1')"
                >
                  <div class="course-item-icon course-item-exercise">
                    <i class="fa fa-pencil text-xs"></i>
                  </div>
                  <span>习题2.1：{{ getExerciseTitle(3) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': currentVideoIndex === 4 }"
                  @click="playVideo(4, '第二章 - ' + getVideoTitle(4))"
                >
                  <div class="course-item-icon course-item-video">
                    <i class="fa fa-play text-xs"></i>
                  </div>
                  <span>2.2 {{ getVideoTitle(4) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': false }"
                  @click="goToExerciseSeries('section_2_2')"
                >
                  <div class="course-item-icon course-item-exercise">
                    <i class="fa fa-pencil text-xs"></i>
                  </div>
                  <span>习题2.2：{{ getExerciseTitle(4) }}</span>
                </div>
              </div>
            </div>
            
            <!-- 第三章 -->
            <div class="border-b border-gray-200">
              <div class="course-section-title flex justify-between items-center cursor-pointer" @click="toggleOtherSection('section3')">
                <span>第三章 {{ getChapterName('section3') }}</span>
                <i class="fa" :class="openSections['section3'] ? 'fa-angle-down' : 'fa-angle-right'"></i>
              </div>
              <div class="pl-2" v-show="openSections['section3']">
                <div 
                  class="course-item" 
                  :class="{ 'active': currentVideoIndex === 5 }"
                  @click="playVideo(5, '第三章 - ' + getVideoTitle(5))"
                >
                  <div class="course-item-icon course-item-video">
                    <i class="fa fa-play text-xs"></i>
                  </div>
                  <span>3.1 {{ getVideoTitle(5) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': false }"
                  @click="goToExerciseSeries('section_3_1')"
                >
                  <div class="course-item-icon course-item-exercise">
                    <i class="fa fa-pencil text-xs"></i>
                  </div>
                  <span>习题3.1：{{ getExerciseTitle(5) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': currentVideoIndex === 6 }"
                  @click="playVideo(6, '第三章 - ' + getVideoTitle(6))"
                >
                  <div class="course-item-icon course-item-video">
                    <i class="fa fa-play text-xs"></i>
                  </div>
                  <span>3.2 {{ getVideoTitle(6) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': false }"
                  @click="goToExerciseSeries('section_3_2')"
                >
                  <div class="course-item-icon course-item-exercise">
                    <i class="fa fa-pencil text-xs"></i>
                  </div>
                  <span>习题3.2：{{ getExerciseTitle(6) }}</span>
                </div>
              </div>
            </div>
            
            <!-- 第四章 -->
            <div class="border-b border-gray-200">
              <div class="course-section-title flex justify-between items-center cursor-pointer" @click="toggleOtherSection('section4')">
                <span>第四章 {{ getChapterName('section4') }}</span>
                <i class="fa" :class="openSections['section4'] ? 'fa-angle-down' : 'fa-angle-right'"></i>
              </div>
              <div class="pl-2" v-show="openSections['section4']">
                <div 
                  class="course-item" 
                  :class="{ 'active': currentVideoIndex === 7 }"
                  @click="playVideo(7, '第四章 - ' + getVideoTitle(7))"
                >
                  <div class="course-item-icon course-item-video">
                    <i class="fa fa-play text-xs"></i>
                  </div>
                  <span>4.1 {{ getVideoTitle(7) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': false }"
                  @click="goToExerciseSeries('section_4_1')"
                >
                  <div class="course-item-icon course-item-exercise">
                    <i class="fa fa-pencil text-xs"></i>
                  </div>
                  <span>习题4.1：{{ getExerciseTitle(7) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': currentVideoIndex === 8 }"
                  @click="playVideo(8, '第四章 - ' + getVideoTitle(8))"
                >
                  <div class="course-item-icon course-item-video">
                    <i class="fa fa-play text-xs"></i>
                  </div>
                  <span>4.2 {{ getVideoTitle(8) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': false }"
                  @click="goToExerciseSeries('section_4_2')"
                >
                  <div class="course-item-icon course-item-exercise">
                    <i class="fa fa-pencil text-xs"></i>
                  </div>
                  <span>习题4.2：{{ getExerciseTitle(8) }}</span>
                </div>
              </div>
            </div>
            
            <!-- 第五章 -->
            <div class="border-b border-gray-200">
              <div class="course-section-title flex justify-between items-center cursor-pointer" @click="toggleOtherSection('section5')">
                <span>第五章 {{ getChapterName('section5') }}</span>
                <i class="fa" :class="openSections['section5'] ? 'fa-angle-down' : 'fa-angle-right'"></i>
              </div>
              <div class="pl-2" v-show="openSections['section5']">
                <div 
                  class="course-item" 
                  :class="{ 'active': currentVideoIndex === 9 }"
                  @click="playVideo(9, '第五章 - ' + getVideoTitle(9))"
                >
                  <div class="course-item-icon course-item-video">
                    <i class="fa fa-play text-xs"></i>
                  </div>
                  <span>5.1 {{ getVideoTitle(9) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': false }"
                  @click="goToExerciseSeries('section_5_1')"
                >
                  <div class="course-item-icon course-item-exercise">
                    <i class="fa fa-pencil text-xs"></i>
                  </div>
                  <span>习题5.1：{{ getExerciseTitle(9) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': currentVideoIndex === 10 }"
                  @click="playVideo(10, '第五章 - ' + getVideoTitle(10))"
                >
                  <div class="course-item-icon course-item-video">
                    <i class="fa fa-play text-xs"></i>
                  </div>
                  <span>5.2 {{ getVideoTitle(10) }}</span>
                </div>
                <div 
                  class="course-item" 
                  :class="{ 'active': false }"
                  @click="goToExerciseSeries('section_5_2')"
                >
                  <div class="course-item-icon course-item-exercise">
                    <i class="fa fa-pencil text-xs"></i>
                  </div>
                  <span>习题5.2：{{ getExerciseTitle(10) }}</span>
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
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import pinyin from 'pinyin'

export default {
  name: 'VideoPlayer',
  components: {
    Header,
    Footer
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // 课程类别信息
    const categoryId = ref('2')
    const categoryName = ref('编程开发')
    
    // 视频播放状态 - 添加 hasStartedPlaying 状态
    const isPlaying = ref(false)
    const currentTime = ref(0)
    const duration = ref(0)
    const isFullscreenV2 = ref(false)
    const autoPlay = ref(true)
    const currentVideoIndex = ref(1) // 当前播放的视频索引
    const currentVideoUrl = ref('') // 当前视频URL
    const hasStartedPlaying = ref(false) // 添加：是否已经开始播放
    
    // 互动状态
    const isLiked = ref(false)
    const likeCount = ref(371)
    const isFavorited = ref(false)
    const favoriteCount = ref(124)
    const isFollowing = ref(false)
    const activeTab = ref('intro')
    const sortBy = ref('all')
    const newComment = ref('')
    
    // 课程章节导航状态
    const section1Open = ref(true)
    const section2Open = ref(false)
    const openSections = ref({})
    
    // 课程数据
    const course = ref({
      id: parseInt(route.params.courseId) || 1,
      title: '王道计算机考研操作系统',
      introTitle: '【王道论坛】欢迎你我，青春无悔！来和大咖朋友交朋友吧啦！',
      updateTime: '2019-10-19 14:02:39',
      description: '自从在发表面试的2024考研《恭喜你你》、《祝你心自由》、《冲刺版》、《冲刺版》、《高数版》、《高数版》，学好就地理学对压正的，可能我在某些要多套版的教材你的动力。',
      tags: ['操作系统', '考研', '教育', '计算机', '王道', '考研专题']
    })
    
    // 计算课程标题
    const courseTitle = computed(() => {
      const category = getCategoryFromCourse()
      if (category === 'computer') {
        return '操作系统课程'
      } else if (category === 'business') {
        return '商业分析课程'
      } else {
        return 'UI/UX设计课程'
      }
    })
    
    // 讲师数据
    const instructor = ref({
      name: '',
      fans: '0',
      description: '',
      userId: '',
      department: '',
      avatar: '👤'  // 默认头像
    })

    // 格式化粉丝数
    const formatFansCount = (views) => {
      const fans = Math.floor(views * 0.05) // 假设5%的观看者成为粉丝
      if (fans >= 10000) {
        return `${(fans / 10000).toFixed(1)}万`
      } else if (fans >= 1000) {
        return `${(fans / 1000).toFixed(1)}千`
      }
      return fans.toString()
    }

    // 根据类别获取部门
    const getDepartmentByCategory = (category) => {
      const departments = {
        computer: '计算机学院',
        business: '商学院',
        design: '设计学院'
      }
      return departments[category] || '未分类学院'
    }
    
    // 评论数据
    const comments = ref([
      {
        id: 1,
        avatar: '👤',
        author: '研究生挣M001',
        time: '2天前',
        content: '已经在备考二遍了，讲解寿命清晰，特别是关于电视和视频的讲评，移学谢阳月阳！感谢王道田的协作者们认认，以人为刚能高于上班课程学生们！',
        likes: 1472
      },
      {
        id: 2,
        avatar: '👤',
        author: '计算机爱好小陈',
        time: '3天前',
        content: '我听的安全卸载了，操作系统成绩出迈了对考研中心以以考察专家理？我都是跟做题的，做题还发动分的问题分，重要特别理解是如果？',
        likes: 356
      },
      {
        id: 3,
        avatar: '👤',
        author: '程序员小王',
        time: '1周前',
        content: '作为已经上了的的群组，回头来看这套视频依然很感谢，真的带来量！服装上过个正能讲课的问题，对天奋业评的无的成就了我优，模式大学好好坚，不事只是教方才是便那学过。',
        likes: 2856
      }
    ])
    
    // 视频URL列表 - 使用国内可访问的视频源
    const videoUrls = {
      computer: [
        // 国内可访问的视频源
        'https://sf1-cdn-tos.huoshanstatic.com/obj/media-fe/xgplayer_doc_video/mp4/xgplayer-demo-360p.mp4',
        'https://sf1-cdn-tos.huoshanstatic.com/obj/media-fe/xgplayer_doc_video/mp4/xgplayer-demo-360p.mp4',
        'https://media.w3.org/2010/05/video/movie_300.mp4',
        'https://media.w3.org/2010/05/sintel/trailer.mp4',
        'https://media.w3.org/2010/05/bunny/trailer.mp4',
        'https://media.w3.org/2010/05/video/movie_300.mp4',
        'https://media.w3.org/2010/05/sintel/trailer.mp4',
        'https://media.w3.org/2010/05/bunny/trailer.mp4',
        'https://media.w3.org/2010/05/video/movie_300.mp4',
        'https://media.w3.org/2010/05/sintel/trailer.mp4'
      ],
      business: [
        'https://media.w3.org/2010/05/sintel/trailer.mp4',
        'https://media.w3.org/2010/05/bunny/trailer.mp4',
        'https://media.w3.org/2010/05/video/movie_300.mp4',
        'https://media.w3.org/2010/05/sintel/trailer.mp4',
        'https://media.w3.org/2010/05/bunny/trailer.mp4',
        'https://media.w3.org/2010/05/video/movie_300.mp4',
        'https://media.w3.org/2010/05/sintel/trailer.mp4',
        'https://media.w3.org/2010/05/bunny/trailer.mp4',
        'https://media.w3.org/2010/05/video/movie_300.mp4',
        'https://media.w3.org/2010/05/sintel/trailer.mp4'
      ],
      design: [
        'https://media.w3.org/2010/05/sintel/trailer.mp4',
        'https://media.w3.org/2010/05/bunny/trailer.mp4',
        'https://media.w3.org/2010/05/video/movie_300.mp4',
        'https://media.w3.org/2010/05/sintel/trailer.mp4',
        'https://media.w3.org/2010/05/bunny/trailer.mp4',
        'https://media.w3.org/2010/05/video/movie_300.mp4',
        'https://media.w3.org/2010/05/sintel/trailer.mp4',
        'https://media.w3.org/2010/05/bunny/trailer.mp4',
        'https://media.w3.org/2010/05/video/movie_300.mp4',
        'https://media.w3.org/2010/05/sintel/trailer.mp4'
      ]
    }
    
    // DOM 引用
    const videoElement = ref(null)
    const videoContainer = ref(null)
    
    // 计算属性
    const playPauseIcon = computed(() => 
      isPlaying.value ? 'fa fa-pause' : 'fa fa-play'
    )
    
    const progressPercentage = computed(() => {
      if (duration.value > 0) {
        return (currentTime.value / duration.value) * 100
      }
      return 0
    })
    
    const sortedComments = computed(() => {
      if (sortBy.value === 'hot') {
        return [...comments.value].sort((a, b) => b.likes - a.likes)
      }
      return comments.value
    })
    
    // 方法
    // 从课程信息获取类别
    const getCategoryFromCourse = () => {
      const savedCourse = localStorage.getItem('selectedCourse')
      if (savedCourse) {
        try {
          const courseData = JSON.parse(savedCourse)
          return courseData.category || 'computer'
        } catch (error) {
          return 'computer'
        }
      }
      return 'computer'
    }
    
    // 加载课程信息
    const loadCourseData = () => {
      const savedCourse = localStorage.getItem('selectedCourse')
      if (savedCourse) {
        try {
          const courseData = JSON.parse(savedCourse)
          console.log('从首页传递的课程数据:', courseData) // 调试用

          // 更新课程信息
          course.value.id = courseData.id || course.value.id
          course.value.title = courseData.title || course.value.title
          course.value.description = courseData.description || course.value.description

          // 根据类别设置课程信息
          const category = courseData.category || 'computer'
          setCourseDetailsByCategory(category)

          // 设置课程简介标题
          setIntroTitle(category, courseData.title)

          // 关键：从首页数据中获取老师信息
          if (courseData.teacher) {
            // 直接使用首页传递的老师名字
            instructor.value.name = courseData.teacher

            // 根据课程类型设置老师信息
            if (category === 'computer') {
              instructor.value.description = '计算机教育专家，专注编程和计算机基础教学'
              instructor.value.department = '计算机学院'
            } else if (category === 'business') {
              instructor.value.description = '商业分析专家，拥有多年企业咨询经验'
              instructor.value.department = '商学院'
            } else {
              instructor.value.description = '设计专家，拥有丰富的创意设计经验'
              instructor.value.department = '设计学院'
            }

            // 生成用户ID（简单处理，移除特殊字符）
            instructor.value.userId = `teacher_${courseData.teacher.replace(/[^\w\u4e00-\u9fa5]/g, '_')}`

            // 根据观看量估算粉丝数
            if (courseData.views) {
              const viewsStr = courseData.views
              let viewsNum = 0

              if (viewsStr.includes('万')) {
                viewsNum = parseFloat(viewsStr) * 10000
              } else if (viewsStr.includes('千')) {
                viewsNum = parseFloat(viewsStr) * 1000
              } else {
                viewsNum = parseInt(viewsStr) || 0
              }

              // 假设5%的观看者成为粉丝
              const fans = Math.floor(viewsNum * 0.05)
              if (fans >= 10000) {
                instructor.value.fans = `${(fans / 10000).toFixed(1)}万`
              } else if (fans >= 1000) {
                instructor.value.fans = `${(fans / 1000).toFixed(1)}千`
              } else {
                instructor.value.fans = fans.toString()
              }
            } else {
              instructor.value.fans = '1.2万'
            }

            // 设置头像（使用老师名字生成不同的随机头像）
            const nameHash = courseData.teacher.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
            instructor.value.avatar = `https://picsum.photos/48/48?random=${nameHash}`
          }

        } catch (error) {
          console.error('解析课程数据失败:', error)
          setDefaultCourseDetails()
        }
      } else {
        setDefaultCourseDetails()
      }
    }
    
    // 设置课程简介标题
    const setIntroTitle = (category, courseTitle) => {
      const introTitles = {
        computer: `【${courseTitle}】欢迎你我，青春无悔！来和大咖朋友交朋友吧啦！`,
        business: `【${courseTitle}】实战演练，数据驱动！一起探索商业分析的奥秘！`,
        design: `【${courseTitle}】创意无限，设计未来！开启你的设计之旅！`
      }
      
      course.value.introTitle = introTitles[category] || `【${courseTitle}】欢迎你我，青春无悔！来和大咖朋友交朋友吧啦！`
    }
    
    // 根据类别设置课程详情
    const setCourseDetailsByCategory = (category) => {
      // 设置面包屑导航
      if (category === 'computer') {
        categoryId.value = '2'
        categoryName.value = '编程开发'
      } else if (category === 'business') {
        categoryId.value = '5'
        categoryName.value = '商业管理'
      } else {
        categoryId.value = '6'
        categoryName.value = '设计创意'
      }
      
      // 设置课程标签
      const tagsByCategory = {
        computer: ['操作系统', '考研', '教育', '计算机', '王道', '考研专题', '计算机基础', '系统编程'],
        business: ['商业分析', '数据分析', '数据驱动', '决策支持', '商业智能', '市场分析', '企业战略'],
        design: ['UI设计', 'UX设计', '用户体验', '交互设计', '界面设计', '原型设计', '设计思维']
      }
      
      course.value.tags = tagsByCategory[category] || course.value.tags
      
      // 设置讲师信息
      setInstructorByCategory(category)
    }
    
    // 根据类别设置讲师信息
    const setInstructorByCategory = (category) => {
      // 如果已经有老师信息（从首页传递的），就不要覆盖
      if (instructor.value.name && instructor.value.name !== '') {
        console.log('使用首页传递的老师信息:', instructor.value.name)
        return
      }

      // 只有在没有老师信息时才使用默认值
      const instructorsByCategory = {
        computer: {
          name: '王道计算机',
          fans: '123.0万',
          description: '计算机教育专家，专注操作系统和计算机基础教学15年，培养了大量计算机专业人才。',
          userId: 'teacher_wangdao',
          department: '计算机学院'
        },
        business: {
          name: '李商业分析师',
          fans: '89.5万',
          description: '资深商业分析师，拥有10年企业咨询和数据分析经验，擅长数据驱动决策。',
          userId: 'teacher_business_li',
          department: '商学院'
        },
        design: {
          name: '张设计师',
          fans: '156.3万',
          description: '知名UI/UX设计师，曾任多家互联网公司设计总监，设计作品获得多项国际大奖。',
          userId: 'teacher_design_zhang',
          department: '设计学院'
        }
      }

      const instructorInfo = instructorsByCategory[category] || instructorsByCategory.computer
      Object.assign(instructor.value, instructorInfo)
    }
    
    // 设置默认课程详情
    const setDefaultCourseDetails = () => {
      const category = 'computer'
      setCourseDetailsByCategory(category)
      setIntroTitle(category, course.value.title)
    }
    
    // 获取章节名称
    const getChapterName = (sectionId) => {
      const category = getCategoryFromCourse()
      const chapters = {
        computer: {
          section1: '操作系统引论',
          section2: '进程管理',
          section3: '处理机调度',
          section4: '存储器管理',
          section5: '设备管理'
        },
        business: {
          section1: '商业分析导论',
          section2: '数据收集',
          section3: '统计分析',
          section4: '预测建模',
          section5: '商业决策'
        },
        design: {
          section1: '设计基础',
          section2: '用户研究',
          section3: '交互设计',
          section4: '视觉设计',
          section5: '原型制作'
        }
      }
      
      return chapters[category]?.[sectionId] || ''
    }
    
    // 获取视频标题
    const getVideoTitle = (index) => {
      const category = getCategoryFromCourse()
      const titles = {
        computer: [
          '操作系统概述',
          '进程概念',
          '处理机调度',
          '进程通信',
          '死锁处理',
          '内存管理',
          '文件系统',
          '设备管理',
          '操作系统接口',
          '系统安全'
        ],
        business: [
          '商业分析定义',
          '数据收集方法',
          '描述性统计',
          '预测模型',
          '数据可视化',
          '商业报告',
          '案例分析',
          '战略规划',
          '决策支持',
          '绩效评估'
        ],
        design: [
          '设计思维',
          '用户研究',
          '信息架构',
          '交互模式',
          '视觉设计',
          '原型工具',
          '设计评审',
          '用户体验',
          '界面设计',
          '设计交付'
        ]
      }
      
      return titles[category]?.[index - 1] || `课程内容 ${index}`
    }
    
    // 获取习题标题
    const getExerciseTitle = (index) => {
      const category = getCategoryFromCourse()
      const titles = {
        computer: [
          '操作系统基础',
          '进程管理练习',
          '调度算法应用',
          '死锁问题解决',
          '内存管理实践',
          '文件系统操作',
          '设备管理练习',
          '系统接口应用',
          '安全机制实践',
          '综合案例分析'
        ],
        business: [
          '商业分析基础',
          '数据收集练习',
          '统计分析应用',
          '模型构建实践',
          '报告撰写练习',
          '案例研究分析',
          '战略规划练习',
          '决策模拟实践',
          '绩效评估应用',
          '综合商业分析'
        ],
        design: [
          '设计思维练习',
          '用户研究实践',
          '交互设计任务',
          '视觉设计练习',
          '原型制作实践',
          '设计评审练习',
          '用户体验测试',
          '界面设计任务',
          '设计交付练习',
          '综合设计项目'
        ]
      }
      
      return titles[category]?.[index - 1] || `基础练习 ${index}`
    }
    
    // 获取视频时长
    const getVideoDuration = (index) => {
      const durations = ['45:20', '38:45', '52:10', '41:25', '48:30', '44:15', '50:20', '39:40', '47:30', '43:20']
      return durations[index - 1] || '45:00'
    }
    
    // 初始化视频播放 - 修改：在页面加载时初始化第一集视频
    const initFirstVideo = () => {
      const category = getCategoryFromCourse()
      const videoList = videoUrls[category] || videoUrls.computer
      
      // 设置初始视频URL
      currentVideoUrl.value = videoList[0]
      hasStartedPlaying.value = false // 初始时不显示视频，等待用户点击
    }
    
    // 播放视频 - 修改：添加参数处理，用于章节导航点击
    const playVideo = (index, title) => {
      const category = getCategoryFromCourse()
      const videoList = videoUrls[category] || videoUrls.computer
      
      // 设置当前视频索引
      currentVideoIndex.value = index
      
      // 设置视频URL（循环使用视频列表）
      const videoIndex = (index - 1) % videoList.length
      currentVideoUrl.value = videoList[videoIndex]
      
      // 更新课程标题为当前视频标题
      if (title) {
        course.value.title = title
      }
      
      // 标记已开始播放
      hasStartedPlaying.value = true
      
      // 开始播放
      setTimeout(() => {
        if (videoElement.value) {
          videoElement.value.load()
          videoElement.value.play().then(() => {
            isPlaying.value = true
          }).catch(error => {
            console.error('视频播放失败:', error)
            showNotification('视频播放失败，请重试')
          })
        }
      }, 100)
      
      showNotification(`正在播放：${title || getVideoTitle(index)}`)
    }
    
    // 修改：处理视频播放器点击事件
    const handleVideoPlayerClick = () => {
      // 如果是第一次点击（还没有开始播放）
      if (!hasStartedPlaying.value) {
        // 初始化并播放第一集视频
        playVideo(1, course.value.title)
      } else {
        // 如果已经开始播放，则切换播放/暂停
        togglePlay()
      }
    }
    
    // 跳转到习题系列页面 - 修复路由参数问题
    const goToExerciseSeries = (seriesId) => {
      const category = getCategoryFromCourse()
      const courseTitle = course.value.title

      // 根据seriesId获取对应的习题标题
      let exerciseTitle = ''
      const chapterNumber = seriesId.split('_')[1] // 提取章号
      const sectionNumber = seriesId.split('_')[2] // 提取节号

      if (chapterNumber && sectionNumber) {
        // 根据章节号获取对应的习题标题
        const videoIndex = (parseInt(chapterNumber) - 1) * 2 + parseInt(sectionNumber)
        exerciseTitle = getExerciseTitle(videoIndex)
      } else {
        exerciseTitle = '课后习题集'
      }

      // 完整的习题集标题
      const fullTitle = `${chapterNumber}.${sectionNumber} 课后习题集：${exerciseTitle}`

      // 保存习题信息到localStorage，供ExerciseSeries页面使用
      const exerciseInfo = {
        seriesId: seriesId,
        courseTitle: courseTitle,
        courseId: course.value.id,
        category: category,
        title: fullTitle, // 传递完整的标题
        exerciseTitle: exerciseTitle // 单独传递习题标题
      }

      localStorage.setItem('currentExercise', JSON.stringify(exerciseInfo))

      // 跳转到习题系列页面，传递正确的seriesId参数
      router.push({
        name: 'ExerciseSeries',
        params: {
          courseId: course.value.id,
          seriesId: seriesId
        },
        query: {
          title: fullTitle, // 在query中也传递标题
          category: category,
          exerciseTitle: exerciseTitle
        }
      })
    }
    
    // 跳转到老师空间
    const goToTeacherSpace = (teacher) => {
      const teacherInfo = {
        name: teacher.name,
        userId: teacher.userId,
        department: teacher.department,
        avatar: teacher.avatar,
        description: teacher.description
      }
      
      localStorage.setItem('currentTeacherInfo', JSON.stringify(teacherInfo))
      
      router.push({
        path: '/teacher-space',
        query: {
          teacherId: teacher.userId,
          teacherName: teacher.name
        }
      })
    }
    
    // 视频播放相关方法 - 修改：简化播放逻辑，参考第一个视频
    const togglePlay = () => {
      if (!videoElement.value) return
      
      if (videoElement.value.paused) {
        videoElement.value.play().then(() => {
          isPlaying.value = true
        }).catch(error => {
          console.error('播放失败:', error)
          showNotification('播放失败，请重试')
        })
      } else {
        videoElement.value.pause()
        isPlaying.value = false
      }
    }
    
    const updateProgress = () => {
      if (!videoElement.value) return
      currentTime.value = videoElement.value.currentTime
    }
    
    const onVideoLoaded = () => {
      if (videoElement.value) {
        duration.value = videoElement.value.duration
      }
    }
    
    const onVideoEnded = () => {
      isPlaying.value = false
      if (autoPlay.value) {
        nextVideo()
      }
    }
    
    const handleVideoError = (error) => {
      console.error('视频加载错误:', error)
      showNotification('视频加载失败，请检查网络连接或刷新页面')
    }
    
    const seekToTime = (event) => {
      if (!videoElement.value || !duration.value) return
      
      const rect = event.currentTarget.getBoundingClientRect()
      const clickPosition = event.clientX - rect.left
      const percentage = clickPosition / rect.width
      
      videoElement.value.currentTime = percentage * duration.value
    }
    
    // 全屏功能
    const toggleFullscreenV2 = () => {
      if (!videoContainer.value) return
      
      if (!isFullscreenV2.value) {
        enterFullscreen()
      } else {
        exitFullscreen()
      }
    }
    
    const enterFullscreen = () => {
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
      
      document.body.classList.add('video-fullscreen-active')
    }
    
    const exitFullscreen = () => {
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
      
      document.body.classList.remove('video-fullscreen-active')
    }
    
    const handleFullscreenChange = () => {
      isFullscreenV2.value = !!document.fullscreenElement
      if (!isFullscreenV2.value) {
        document.body.classList.remove('video-fullscreen-active')
      }
    }
    
    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
    
    const prevVideo = () => {
      if (currentVideoIndex.value > 1) {
        playVideo(currentVideoIndex.value - 1, getVideoTitle(currentVideoIndex.value - 1))
      } else {
        showNotification('已经是第一集了')
      }
    }
    
    const nextVideo = () => {
      if (currentVideoIndex.value < 10) {
        playVideo(currentVideoIndex.value + 1, getVideoTitle(currentVideoIndex.value + 1))
      } else {
        showNotification('已经是最后一集了')
      }
    }
    
    // 关注/取消关注讲师
    const toggleFollow = () => {
      isFollowing.value = !isFollowing.value
      saveFollowData()
      showNotification(isFollowing.value ? '已关注讲师' : '已取消关注')
    }
    
    const saveFollowData = () => {
      const currentUser = JSON.parse(localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser') || '{}')
      const userId = currentUser.userId || 'default'
      const followedTeachers = JSON.parse(localStorage.getItem(`user_${userId}_followedTeachers`) || '[]')
      
      const teacherData = {
        id: Date.now(),
        userId: instructor.value.userId,
        name: instructor.value.name,
        department: instructor.value.department,
        avatar: instructor.value.avatar,
        followedAt: new Date().toISOString().split('T')[0]
      }

      if (isFollowing.value) {
        const existingIndex = followedTeachers.findIndex(t => t.userId === teacherData.userId)
        if (existingIndex === -1) {
          followedTeachers.push(teacherData)
          localStorage.setItem(`user_${userId}_followedTeachers`, JSON.stringify(followedTeachers))
          
          window.dispatchEvent(new StorageEvent('storage', {
            key: 'userFollowedTeachers',
            newValue: JSON.stringify(followedTeachers)
          }))
          
          window.dispatchEvent(new CustomEvent('followUpdated'))
        }
      } else {
        const updatedTeachers = followedTeachers.filter(t => t.userId !== teacherData.userId)
        localStorage.setItem('userFollowedTeachers', JSON.stringify(updatedTeachers))
        
        window.dispatchEvent(new StorageEvent('storage', {
          key: 'userFollowedTeachers',
          newValue: JSON.stringify(updatedTeachers)
        }))
        
        window.dispatchEvent(new CustomEvent('followUpdated'))
      }
    }
    
    // 加载关注状态
    const loadFollowStatus = () => {
      const currentUser = JSON.parse(localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser') || '{}')
      const userId = currentUser.userId || 'default'
      const followedTeachers = JSON.parse(localStorage.getItem(`user_${userId}_followedTeachers`) || '[]')

      const isTeacherFollowed = followedTeachers.some(teacher => teacher.userId === instructor.value.userId)
      isFollowing.value = isTeacherFollowed
    }
    
    const toggleLike = () => {
      isLiked.value = !isLiked.value
      likeCount.value += isLiked.value ? 1 : -1

      const currentUser = JSON.parse(localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser') || '{}')
      const userId = currentUser.userId || 'default'
      const likes = JSON.parse(localStorage.getItem(`user_${userId}_likes`) || '[]')

      const likeData = {
        id: `like_${course.value.id}_${Date.now()}`,
        courseId: course.value.id,
        courseName: course.value.title,
        teacher: instructor.value.name,
        likedAt: new Date().toISOString().split('T')[0] + ' ' + 
                new Date().toTimeString().split(' ')[0].substring(0, 5)
      }

      if (isLiked.value) {
        if (!likes.find(l => l.courseId === course.value.id)) {
          likes.push(likeData)
        }
      } else {
        const index = likes.findIndex(l => l.courseId === course.value.id)
        if (index !== -1) {
          likes.splice(index, 1)
        }
      }

      localStorage.setItem(`user_${userId}_likes`, JSON.stringify(likes))

      window.dispatchEvent(new StorageEvent('storage', {
        key: 'userLikes',
        newValue: JSON.stringify(likes)
      }))

      showNotification(isLiked.value ? '已点赞' : '已取消点赞')
    }
    
    const toggleFavorite = () => {
      isFavorited.value = !isFavorited.value
      favoriteCount.value += isFavorited.value ? 1 : -1

      const currentUser = JSON.parse(localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser') || '{}')
      const userId = currentUser.userId || 'default'
      const favorites = JSON.parse(localStorage.getItem(`user_${userId}_favorites`) || '[]')

      const favoriteData = {
        id: course.value.id,
        name: course.value.title,
        teacher: instructor.value.name,
        status: 'ongoing',
        collectedAt: new Date().toISOString().split('T')[0],
        category: getCategoryFromCourse(),
        description: course.value.description
      }

      if (isFavorited.value) {
        if (!favorites.find(f => f.id === favoriteData.id)) {
          favorites.push(favoriteData)
        }
      } else {
        const index = favorites.findIndex(f => f.id === favoriteData.id)
        if (index !== -1) {
          favorites.splice(index, 1)
        }
      }

      localStorage.setItem(`user_${userId}_favorites`, JSON.stringify(favorites))

      window.dispatchEvent(new StorageEvent('storage', {
        key: 'userFavorites',
        newValue: JSON.stringify(favorites)
      }))

      showNotification(isFavorited.value ? '已收藏' : '已取消收藏')
    }

    const toggleFavoriteWithRedirect = () => {
      toggleFavorite()

      if (isFavorited.value) {
        setTimeout(() => {
          if (confirm('收藏成功！是否前往收藏管理页面查看？')) {
            goToFavorites()
          }
        }, 500)
      }
    }
    
    const goToFavorites = () => {
      router.push('/favorites-management?tab=collection')
    }

    const saveHistoryData = () => {
      const currentUser = JSON.parse(localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser') || '{}')
      const userId = currentUser.userId || 'default'
      const history = JSON.parse(localStorage.getItem(`user_${userId}_history`) || '[]')

      const historyData = {
        id: `history_${course.value.id}_${Date.now()}`,
        courseId: course.value.id,
        courseName: course.value.title,
        watchedAt: new Date().toISOString().split('T')[0] + ' ' + 
                   new Date().toTimeString().split(' ')[0].substring(0, 5),
        progress: duration.value > 0 ? Math.floor((currentTime.value / duration.value) * 100) : 0
      }

      const existingIndex = history.findIndex(h => h.courseId === course.value.id)

      if (existingIndex !== -1) {
        history[existingIndex] = historyData
      } else {
        history.push(historyData)
      }

      const recentHistory = history.slice(-20)
      localStorage.setItem(`user_${userId}_history`, JSON.stringify(recentHistory))

      window.dispatchEvent(new StorageEvent('storage', {
        key: 'userHistory',
        newValue: JSON.stringify(recentHistory)
      }))
    }
    
    const likeComment = (commentId) => {
      const comment = comments.value.find(c => c.id === commentId)
      if (comment) {
        comment.likes += 1
      }
    }
    
    const showReplyBox = (commentId) => {
      showNotification('回复功能开发中')
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
    
    const loadMoreComments = () => {
      showNotification('加载更多评论功能开发中')
    }
    
    const toggleSection = (section) => {
      if (section === 'section1') {
        section1Open.value = !section1Open.value
      } else if (section === 'section2') {
        section2Open.value = !section2Open.value
      }
    }
    
    const toggleOtherSection = (sectionId) => {
      openSections.value[sectionId] = !openSections.value[sectionId]
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
    
    const initFontAwesome = () => {
      if (!document.querySelector('link[href*="font-awesome"]')) {
        const link = document.createElement('link')
        link.rel = 'stylesheet'
        link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
        document.head.appendChild(link)
      }
    }
    
    // 监听键盘快捷键
    const handleKeyDown = (event) => {
      if (event.key === 'f' || event.key === 'F') {
        event.preventDefault()
        toggleFullscreenV2()
      }
      if (event.key === 'Escape' && isFullscreenV2.value) {
        toggleFullscreenV2()
      }
      if (event.key === ' ' && event.target.tagName !== 'TEXTAREA' && event.target.tagName !== 'INPUT') {
        event.preventDefault()
        togglePlay()
      }
    }
    
    // 生命周期钩子
    onMounted(() => {
      initFontAwesome()
      
      // 加载课程数据
      loadCourseData()
      
      // 初始化第一集视频
      initFirstVideo()

      console.log('当前课程ID:', course.value.id)
      console.log('当前老师信息:', instructor.value) // 添加调试信息

      // 添加事件监听器
      document.addEventListener('fullscreenchange', handleFullscreenChange)
      document.addEventListener('keydown', handleKeyDown)

      // 检查用户是否已登录
      const user = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
      if (!user) {
        router.push('/login')
      }

      // 加载关注状态
      loadFollowStatus()

      // 检查当前课程是否已收藏和已点赞
      const currentUser = JSON.parse(localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser') || '{}')
      const userId = currentUser.userId || 'default'
      const favorites = JSON.parse(localStorage.getItem(`user_${userId}_favorites`) || '[]')
      const courseId = course.value.id
      isFavorited.value = favorites.some(f => f.id === courseId)

      const likes = JSON.parse(localStorage.getItem(`user_${userId}_likes`) || '[]')
      isLiked.value = likes.some(l => l.courseId === courseId)

      // 在组件卸载时清理
      onBeforeUnmount(() => {
        document.removeEventListener('fullscreenchange', handleFullscreenChange)
        document.removeEventListener('keydown', handleKeyDown)
      })

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
      // 移除事件监听器
      document.removeEventListener('fullscreenchange', handleFullscreenChange)
      document.removeEventListener('keydown', handleKeyDown)
    })

    // 从路由参数中获取老师信息
    if (route.query.teacher) {
      instructor.value.name = route.query.teacher
    }

    // 如果本地存储中有老师信息，使用它
    const savedCourse = localStorage.getItem('selectedCourse')
    if (savedCourse) {
      try {
        const courseData = JSON.parse(savedCourse)
        if (courseData.teacher && !instructor.value.name) {
          instructor.value.name = courseData.teacher
        }
      } catch (error) {
        console.error('解析课程数据失败:', error)
      }
    }
    
    return {
      // 状态
      categoryId,
      categoryName,
      isPlaying,
      currentTime,
      duration,
      isFullscreenV2,
      currentVideoIndex,
      currentVideoUrl,
      hasStartedPlaying, // 添加：暴露给模板
      isLiked,
      likeCount,
      isFavorited,
      favoriteCount,
      isFollowing,
      activeTab,
      sortBy,
      autoPlay,
      newComment,
      section1Open,
      section2Open,
      openSections,
      
      // 数据
      course,
      courseTitle,
      instructor,
      comments,
      
      // 计算属性
      playPauseIcon,
      progressPercentage,
      sortedComments,
      
      // DOM 引用
      videoElement,
      videoContainer,
      
      // 方法
      getChapterName,
      getVideoTitle,
      getExerciseTitle,
      getVideoDuration,
      playVideo,
      handleVideoPlayerClick, // 添加：处理视频播放器点击
      goToExerciseSeries,
      goToTeacherSpace,
      togglePlay,
      updateProgress,
      onVideoLoaded,
      onVideoEnded,
      handleVideoError,
      seekToTime,
      toggleFullscreenV2,
      formatTime,
      prevVideo,
      nextVideo,
      toggleLike,
      toggleFavorite,
      toggleFavoriteWithRedirect,
      goToFavorites,
      toggleFollow,
      likeComment,
      showReplyBox,
      submitComment,
      loadMoreComments,
      toggleSection,
      toggleOtherSection
    }
  }
}
</script>

<style scoped>
/* 修复视频播放器样式 */
.video-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.video-element {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background-color: #000;
}

/* 其他原有样式保持不变 */
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

/* 面包屑导航 */
.breadcrumb {
  padding: 15px 0;
  font-size: 14px;
  color: #666;
}

.breadcrumb a {
  color: #666;
  text-decoration: none;
}

.breadcrumb a:hover {
  color: #1890ff;
}

/* 主布局 */
.main-layout {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 20px;
  margin-bottom: 40px;
}

/* 视频容器 */
.video-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  position: relative;
  transition: all 0.3s ease;
}

/* 全屏模式下的样式 */
:fullscreen .video-container {
  border-radius: 0;
  box-shadow: none;
  background: #000;
}

:fullscreen body {
  background: #000;
}

.video-player {
  position: relative;
  width: 100%;
  height: 500px;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
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
  position: relative;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  position: relative;
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

/* 新全屏按钮样式 */
.fullscreen-btn {
  position: relative;
  overflow: hidden;
  transition: transform 0.2s;
}

.fullscreen-btn:hover {
  transform: scale(1.1);
}

.fullscreen-icon-wrapper {
  position: relative;
  width: 20px;
  height: 20px;
}

.fullscreen-icon-wrapper i {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fullscreen-icon-wrapper i.hidden {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.8);
}

/* 进度条 */
.progress-container {
  flex-grow: 1;
  position: relative;
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
  opacity: 0;
  transition: opacity 0.2s;
}

.progress-container:hover .progress-handle {
  opacity: 1;
}

.time-display {
  color: white;
  font-size: 0.9rem;
  min-width: 100px;
  text-align: center;
  font-family: monospace;
}

/* 视频详情 */
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
  position: relative;
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
}

.author-avatar:hover {
  opacity: 0.8;
}

.author-name {
  font-weight: 600;
  font-size: 15px;
}

.author-date {
  font-size: 12px;
  color: #999;
}

.follow-btn {
  padding: 8px 20px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.follow-btn:hover {
  background: #40a9ff;
  transform: translateY(-1px);
}

.video-stats {
  display: flex;
  gap: 20px;
  align-items: center;
  font-size: 14px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  transition: color 0.2s;
  padding: 8px 12px;
  border-radius: 6px;
}

.stat-item:hover {
  background: #f5f5f5;
  color: #1890ff;
}

.stat-item .fa-heart:hover {
  color: #f5222d;
}

.stat-item .fa-star:hover {
  color: #faad14;
}

.stat-item .fa-bookmark:hover {
  color: #1890ff;
}

/* 标签页 */
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
  transition: color 0.3s ease;
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

/* 课程简介 */
.course-intro {
  background: white;
  padding: 20px;
  border-radius: 12px;
  margin-top: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.course-intro h3 {
  font-size: 18px;
  margin-bottom: 12px;
  color: #333;
  font-weight: 600;
}

.course-intro p {
  font-size: 14px;
  line-height: 1.8;
  color: #666;
  margin-bottom: 15px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag {
  padding: 6px 12px;
  background: #f0f0f0;
  border-radius: 20px;
  font-size: 13px;
  color: #666;
  transition: all 0.3s ease;
}

.tag:hover {
  background: #1890ff;
  color: white;
}

/* 评论区 */
.comments-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  margin-top: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.comments-header h3 {
  font-size: 18px;
  font-weight: 600;
}

.comment-sort {
  display: flex;
  gap: 15px;
  font-size: 14px;
}

.comment-sort span {
  cursor: pointer;
  color: #666;
  position: relative;
  padding: 4px 0;
  transition: color 0.3s ease;
}

.comment-sort span:hover {
  color: #1890ff;
}

.comment-sort span.active {
  color: #1890ff;
  font-weight: 500;
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

.comment-input-box {
  margin-bottom: 25px;
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
  transition: border-color 0.3s ease;
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

.submit-comment-btn {
  padding: 8px 24px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.submit-comment-btn:hover {
  background: #40a9ff;
  transform: translateY(-1px);
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
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
  font-size: 18px;
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
  font-size: 14px;
  color: #333;
}

.comment-time {
  font-size: 13px;
  color: #999;
}

.comment-content p {
  font-size: 14px;
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
  display: flex;
  align-items: center;
  gap: 4px;
}

.comment-stats span:hover {
  color: #1890ff;
}

.load-more {
  text-align: center;
  margin-top: 30px;
}

.load-more-btn {
  padding: 10px 30px;
  border: 1px solid #e0e0e0;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.load-more-btn:hover {
  background: #f9f9f9;
  border-color: #1890ff;
  color: #1890ff;
}

/* 右侧课程导航栏 */
.right-column-nav {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 课程信息卡片 */
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
  transition: all 0.3s ease;
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
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.enter-space-btn:hover {
  background: #1890ff;
  color: white;
}

/* 课程章节导航 */
.course-navigation {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

/* 课程样式 */
.course-section-title {
  @apply font-medium text-gray-600 py-3 px-4 border-b border-gray-200;
}

.course-item {
  @apply flex items-center gap-3 px-4 py-2.5 hover:bg-primary/5 cursor-pointer transition-colors text-sm;
}

.course-item.active {
  @apply bg-primary/10 text-primary font-medium;
}

.course-item-icon {
  @apply w-5 h-5 flex items-center justify-center rounded;
}

.course-item-video {
  @apply bg-primary/10 text-primary;
}

.course-item-exercise {
  @apply bg-success/10 text-success;
}

/* 响应式设计 */
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
  
  .comment-sort {
    gap: 10px;
  }
}

/* 全屏模式下的特殊样式 */
body.video-fullscreen-active {
  overflow: hidden;
}

:fullscreen .video-controls {
  background-color: rgba(0, 0, 0, 0.95);
}

:fullscreen .video-player {
  height: calc(100vh - 60px);
}

:fullscreen .control-btn:hover {
  background-color: rgba(255, 255, 255, 0.15);
  transform: scale(1.1);
}

/* 全屏按钮动画效果 */
.fullscreen-btn:active {
  transform: scale(0.95);
}

.fullscreen-btn::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 159, 67, 0.3) 0%, transparent 70%);
  transform: translate(-50%, -50%) scale(0);
  border-radius: 50%;
  opacity: 0;
  transition: transform 0.3s, opacity 0.3s;
}

.fullscreen-btn:active::after {
  transform: translate(-50%, -50%) scale(1.5);
  opacity: 1;
}
</style>