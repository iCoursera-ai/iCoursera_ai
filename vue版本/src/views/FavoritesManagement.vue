<template>
  <div class="font-sans bg-gray-50 min-h-screen flex flex-col">
    <!-- 使用Header组件 -->
    <Header />
    
    <div class="flex flex-1">
      <!-- 侧边栏导航 -->
      <aside class="w-64 bg-white border-r border-gray-200 flex-shrink-0 fixed top-[5rem] left-0 h-[calc(100vh-5rem)] overflow-y-auto z-30">
        <nav class="py-4 space-y-1 px-4">
          <!-- 工作台 - 只有教师认证用户才显示 -->
          <div v-if="isTeacherCertified" class="sidebar-group">
            <div class="sidebar-parent" :class="{ 'active': activeSidebar === 'dashboard' }" @click="goToTeacherDashboard">
              <div class="sidebar-parent-content">
                <i class="fa fa-tachometer sidebar-icon"></i>
                <span>工作台</span>
              </div>
            </div>
          </div>
          
          <!-- 我的收藏 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" :class="{ 'active': activeSidebar === 'collection' }" @click="switchTabAndSidebar('collection')">
              <div class="sidebar-parent-content">
                <i class="fa fa-book sidebar-icon"></i>
                <span>我的收藏</span>
              </div>
            </div>
          </div>
          
          <!-- 点赞 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" :class="{ 'active': activeSidebar === 'likes' }" @click="switchTabAndSidebar('likes')">
              <div class="sidebar-parent-content">
                <i class="fa fa-thumbs-up sidebar-icon"></i>
                <span>点赞</span>
              </div>
            </div>
          </div>
          
          <!-- 历史记录 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" :class="{ 'active': activeSidebar === 'history' }" @click="switchTabAndSidebar('history')">
              <div class="sidebar-parent-content">
                <i class="fa fa-history sidebar-icon"></i>
                <span>历史记录</span>
              </div>
            </div>
          </div>
          
          <!-- 用户信息 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" :class="{ 'active': activeSidebar === 'user-info' }" @click="goToPersonalInfo">
              <div class="sidebar-parent-content">
                <i class="fa fa-id-card-o sidebar-icon"></i>
                <span>用户信息</span>
              </div>
            </div>
          </div>
          
          <!-- 用户设置 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" :class="{ 'active': activeSidebar === 'user-settings' }" @click="goToPersonalSettings">
              <div class="sidebar-parent-content">
                <i class="fa fa-cog sidebar-icon"></i>
                <span>用户设置</span>
              </div>
            </div>
          </div>
        </nav>
      </aside>

      <!-- 主内容区域 -->
      <main class="flex-1 overflow-y-auto p-6 ml-64">
        <div class="p-6">
          <!-- 收藏管理页面 -->
          <div class="card p-6 card-shadow">
            <!-- 页面标题和批量操作 -->
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
              <div>
                <h3 class="text-lg font-semibold text-gray-900">{{ pageTitle }}</h3>
                <p class="text-sm text-gray-600 mt-1">{{ pageDescription }}</p>
              </div>
              <div class="flex items-center gap-3">
                <button class="btn border border-gray-300 hover:bg-gray-50 transition-all duration-200 flex items-center gap-1 px-4" 
                        @click="handleBatchAction"
                        :disabled="!hasItems">
                  <i class="fa fa-trash-o"></i>
                  <span>{{ batchButtonText }}</span>
                </button>
              </div>
            </div>
            
            <!-- 收藏标签页 -->
            <div class="border-b border-gray-200 mb-6">
              <div class="flex">
                <div class="favorite-tab" :class="{ 'active': currentTab === 'collection' }" 
                     @click="switchTabAndSidebar('collection')">
                  我的收藏
                </div>
                <div class="favorite-tab" :class="{ 'active': currentTab === 'likes' }" 
                     @click="switchTabAndSidebar('likes')">
                  点赞
                </div>
                <div class="favorite-tab" :class="{ 'active': currentTab === 'history' }" 
                     @click="switchTabAndSidebar('history')">
                  历史记录
                </div>
              </div>
            </div>
            
            <!-- 我的收藏页面 -->
            <div v-if="currentTab === 'collection'" class="space-y-4">
              <!-- 课程分类筛选 -->
              <div class="mb-4">
                <div class="text-sm font-medium text-gray-500 mb-2">课程分类</div>
                <div class="flex flex-wrap gap-2">
                  <button class="px-3 py-1 rounded text-sm"
                          :class="selectedCategory === 'all' ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100 text-gray-500'"
                          @click="filterCategory('all')">
                    全部课程
                  </button>
                  <button v-for="category in courseCategories" 
                          :key="category.value"
                          class="px-3 py-1 rounded text-sm"
                          :class="selectedCategory === category.value ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100 text-gray-500'"
                          @click="filterCategory(category.value)">
                    {{ category.label }}
                  </button>
                </div>
              </div>
              
              <!-- 收藏课程表格 -->
              <div class="overflow-x-auto" v-if="filteredFavorites.length > 0">
                <table class="w-full text-sm">
                  <thead>
                    <tr class="border-b border-gray-200">
                      <th class="text-left py-3 px-2 font-medium text-gray-500">课程ID</th>
                      <th class="text-left py-3 px-2 font-medium text-gray-500">课程名称</th>
                      <th class="text-left py-3 px-2 font-medium text-gray-500">授课教师</th>
                      <th class="text-left py-3 px-2 font-medium text-gray-500">课程状态</th>
                      <th class="text-left py-3 px-2 font-medium text-gray-500">收藏时间</th>
                      <th class="text-left py-3 px-2 font-medium text-gray-500">操作</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="course in filteredFavorites" 
                        :key="course.id"
                        class="border-b border-gray-200 table-row-hover">
                      <td class="py-3 px-2 text-gray-500">{{ course.id }}</td>
                      <td class="py-3 px-2 text-gray-900">{{ course.name || course.title }}</td>
                      <td class="py-3 px-2 text-gray-900">{{ course.teacher }}</td>
                      <td class="py-3 px-2">
                        <span :class="getStatusClass(course.status)" class="text-xs">
                          {{ getStatusText(course.status) }}
                        </span>
                      </td>
                      <td class="py-3 px-2 text-gray-500">{{ course.collectedAt }}</td>
                      <td class="py-3 px-2">
                        <div class="flex gap-2">
                          <button class="text-blue-600 hover:text-blue-800 text-sm px-2 py-1 border border-blue-600 rounded hover:bg-blue-50 transition-colors" 
                                  @click="goToCourseFromFavorite(course)">
                            继续学习
                          </button>
                          <button class="text-red-600 hover:text-red-800 text-sm px-2 py-1 border border-red-600 rounded hover:bg-red-50 transition-colors" 
                                  @click="removeFavorite(course.id)">
                            取消收藏
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              <!-- 空状态 -->
              <div v-else class="text-center py-12">
                <i class="fa fa-heart text-4xl text-gray-300 mb-4"></i>
                <h4 class="text-lg font-medium text-gray-900 mb-2">暂无收藏内容</h4>
                <p class="text-gray-600 mb-6">您还没有收藏任何内容，快去发现您感兴趣的课程吧！</p>
                <button class="btn-primary max-w-xs mx-auto" @click="goToHomepage">
                  <i class="fa fa-compass mr-2"></i>去首页看看
                </button>
              </div>
            </div>
            
            <!-- 点赞页面 -->
            <div v-if="currentTab === 'likes'" class="space-y-4">
              <!-- 点赞课程表格 -->
              <div class="overflow-x-auto" v-if="likes.length > 0">
                <table class="w-full text-sm">
                  <thead>
                    <tr class="border-b border-gray-200">
                      <th class="text-left py-3 px-2 font-medium text-gray-500">课程ID</th>
                      <th class="text-left py-3 px-2 font-medium text-gray-500">课程名称</th>
                      <th class="text-left py-3 px-2 font-medium text-gray-500">授课教师</th>
                      <th class="text-left py-3 px-2 font-medium text-gray-500">点赞时间</th>
                      <th class="text-left py-3 px-2 font-medium text-gray-500">操作</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="like in likes" 
                        :key="like.id"
                        class="border-b border-gray-200 table-row-hover">
                      <td class="py-3 px-2 text-gray-500">{{ like.courseId }}</td>
                      <td class="py-3 px-2 text-gray-900">{{ like.courseName }}</td>
                      <td class="py-3 px-2 text-gray-900">{{ like.teacher }}</td>
                      <td class="py-3 px-2 text-gray-500">{{ like.likedAt }}</td>
                      <td class="py-3 px-2">
                        <div class="flex gap-2">
                          <button class="text-blue-600 hover:text-blue-800 text-sm px-2 py-1 border border-blue-600 rounded hover:bg-blue-50 transition-colors" 
                                  @click="goToCourseFromLike(like)">
                            查看课程
                          </button>
                          <button class="text-red-600 hover:text-red-800 text-sm px-2 py-1 border border-red-600 rounded hover:bg-red-50 transition-colors" 
                                  @click="removeLike(like.id)">
                            取消点赞
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              <!-- 空状态 -->
              <div v-else class="text-center py-12">
                <i class="fa fa-thumbs-up text-4xl text-gray-300 mb-4"></i>
                <h4 class="text-lg font-medium text-gray-900 mb-2">您还没有点赞内容</h4>
                <p class="text-gray-600 mb-6">去浏览课程，给喜欢的内容点赞吧！</p>
                <button class="btn-primary max-w-xs mx-auto" @click="goToHomepage">
                  <i class="fa fa-compass mr-2"></i>去首页看看
                </button>
              </div>
            </div>
            
            <!-- 历史记录页面 -->
            <div v-if="currentTab === 'history'" class="space-y-4">
              <!-- 历史记录列表 -->
              <div class="space-y-3" v-if="history.length > 0">
                <div v-for="record in history" 
                     :key="record.id"
                     class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div class="flex items-start justify-between">
                    <div class="flex items-start gap-3">
                      <div class="w-10 h-10 flex items-center justify-center rounded-lg bg-blue-100">
                        <i class="fa fa-play-circle text-blue-600"></i>
                      </div>
                      <div>
                        <h4 class="font-medium text-gray-900 mb-1">{{ record.courseName }}</h4>
                        <p class="text-sm text-gray-500">授课教师: {{ record.teacher || '未知' }}</p>
                        <p class="text-sm text-gray-500 mt-1">观看时间: {{ record.watchedAt }}</p>
                        <p class="text-sm text-gray-500 mt-1">
                          观看进度: <span class="font-medium">{{ record.progress }}%</span>
                        </p>
                      </div>
                    </div>
                    <div class="flex gap-2">
                      <button class="text-xs text-blue-600 hover:text-blue-800 px-3 py-1 border border-blue-600 rounded hover:bg-blue-50 transition-colors"
                              @click="continueWatching(record)">
                        继续观看
                      </button>
                      <button class="text-xs text-red-600 hover:text-red-800 px-2 py-1 border border-red-600 rounded hover:bg-red-50 transition-colors" 
                              @click="removeHistory(record.id)">
                        删除
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 空状态 -->
              <div v-else class="text-center py-12">
                <i class="fa fa-history text-4xl text-gray-300 mb-4"></i>
                <h4 class="text-lg font-medium text-gray-900 mb-2">您还没有浏览历史</h4>
                <p class="text-gray-600 mb-6">浏览课程后，这里会显示您的观看记录</p>
                <button class="btn-primary max-w-xs mx-auto" @click="goToHomepage">
                  <i class="fa fa-compass mr-2"></i>去首页看看
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- 使用Footer组件 -->
    <Footer />

    <!-- 提示信息 -->
    <div v-if="toastMessage" class="toast-message fixed top-6 right-6 bg-gray-800 text-white px-4 py-2 rounded-md shadow-lg z-50 animate-fade-in">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'FavoritesManagement',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      // 侧边栏活动状态
      activeSidebar: 'collection',
      
      // 收藏管理相关
      currentTab: 'collection', // collection, likes, history
      selectedCategory: 'all',
      toastMessage: '',
      
      // 课程分类
      courseCategories: [
        { value: 'computer', label: '计算机科学' },
        { value: 'literature', label: '文学概论' },
        { value: 'ai', label: '人工智能' },
        { value: 'network', label: '网络通信' },
        { value: 'management', label: '项目管理' }
      ],
      
      // 从localStorage获取的数据
      favorites: [],
      likes: [],
      history: [],
      
      // 当前用户信息
      currentUser: null,
      isTeacherCertified: false,
      
      // 页面配置
      pageConfig: {
        'collection': {
          title: '我的收藏',
          description: '管理您收藏的课程内容',
          batchBtn: '批量取消收藏',
          breadcrumb: '我的收藏'
        },
        'likes': {
          title: '我的点赞',
          description: '管理您点赞的内容',
          batchBtn: '批量取消点赞',
          breadcrumb: '点赞'
        },
        'history': {
          title: '浏览历史',
          description: '查看您的课程浏览记录',
          batchBtn: '清空历史记录',
          breadcrumb: '历史记录'
        }
      },
      
      refreshInterval: null
    }
  },
  computed: {
    // 面包屑导航当前项
    breadcrumbCurrent() {
      return this.pageConfig[this.currentTab]?.breadcrumb || ''
    },
    
    // 页面标题和描述
    pageTitle() {
      return this.pageConfig[this.currentTab]?.title || ''
    },
    
    pageDescription() {
      return this.pageConfig[this.currentTab]?.description || ''
    },
    
    batchButtonText() {
      return this.pageConfig[this.currentTab]?.batchBtn || ''
    },
    
    // 过滤后的收藏课程
    filteredFavorites() {
      if (this.selectedCategory === 'all') {
        return this.favorites
      }
      return this.favorites.filter(course => course.category === this.selectedCategory)
    },
    
    // 是否有项目
    hasItems() {
      if (this.currentTab === 'collection') {
        return this.favorites.length > 0
      } else if (this.currentTab === 'likes') {
        return this.likes.length > 0
      } else if (this.currentTab === 'history') {
        return this.history.length > 0
      }
      return false
    },
    
    // 获取当前用户的storage key
    userStorageKey() {
      if (!this.currentUser || !this.currentUser.userId) {
        return 'default'
      }
      return this.currentUser.userId
    }
  },
  mounted() {
    // 从URL参数获取标签
    const urlParams = new URLSearchParams(window.location.search)
    const targetTab = urlParams.get('tab')
    
    // 如果URL参数指定了标签，则切换到对应标签
    if (targetTab && ['collection', 'likes', 'history'].includes(targetTab)) {
      this.currentTab = targetTab
      this.activeSidebar = targetTab
    }
    
    // 加载当前用户信息
    this.loadCurrentUser()
    
    // 加载用户数据
    this.loadUserData()

    // 添加数据迁移（确保旧数据可以迁移到新格式）
    this.migrateOldData()
    
    // 监听storage变化（当视频页面更新数据时）
    window.addEventListener('storage', this.handleStorageChange)
    
    // 每30秒刷新一次数据
    this.refreshInterval = setInterval(this.loadUserData, 30000)
  },
  beforeUnmount() {
    // 移除事件监听器和定时器
    window.removeEventListener('storage', this.handleStorageChange)
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval)
    }
  },
  methods: {
    // 加载当前用户信息
    loadCurrentUser() {
      try {
        const storedUser = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
        if (storedUser) {
          this.currentUser = JSON.parse(storedUser)
          this.isTeacherCertified = this.currentUser.teacherCertStatus === '已认证'
        } else {
          // 如果没有登录，跳转到登录页
          this.$router.push('/login')
        }
      } catch (error) {
        console.error('加载用户信息失败:', error)
        this.$router.push('/login')
      }
    },
    
    // 跳转到工作台
    goToTeacherDashboard() {
      this.activeSidebar = 'dashboard'
      this.$router.push('/teacher-dashboard')
    },

    // 跳转到用户信息
    goToPersonalInfo() {
      this.activeSidebar = 'user-info'
      this.$router.push({
        path: '/personal-information',
        query: { page: 'user-info' }
      })
    },

    // 跳转到用户设置
    goToPersonalSettings() {
      this.activeSidebar = 'user-settings'
      this.$router.push({
        path: '/personal-information',
        query: { page: 'user-settings' }
      })
    },

    // 切换标签页并更新侧边栏高亮
    switchTabAndSidebar(tab) {
      this.currentTab = tab
      this.activeSidebar = tab
      this.selectedCategory = 'all' // 重置筛选
      
      // 更新URL参数
      const url = new URL(window.location)
      url.searchParams.set('tab', tab)
      window.history.replaceState({}, '', url)
    },

    // 迁移旧数据到新格式
    migrateOldData() {
      if (!this.currentUser || !this.currentUser.userId) return

      // 迁移收藏数据
      const oldFavorites = JSON.parse(localStorage.getItem('userFavorites') || '[]')
      if (oldFavorites.length > 0) {
        const currentFavorites = JSON.parse(localStorage.getItem(`user_${this.userStorageKey}_favorites`) || '[]')
        // 合并数据，避免重复
        const mergedFavorites = [...currentFavorites]
        oldFavorites.forEach(item => {
          if (!mergedFavorites.some(f => f.id === item.id)) {
            mergedFavorites.push(item)
          }
        })
        localStorage.setItem(`user_${this.userStorageKey}_favorites`, JSON.stringify(mergedFavorites))
        localStorage.removeItem('userFavorites')
      }

      // 迁移点赞数据
      const oldLikes = JSON.parse(localStorage.getItem('userLikes') || '[]')
      if (oldLikes.length > 0) {
        const currentLikes = JSON.parse(localStorage.getItem(`user_${this.userStorageKey}_likes`) || '[]')
        const mergedLikes = [...currentLikes]
        oldLikes.forEach(item => {
          if (!mergedLikes.some(l => l.id === item.id)) {
            mergedLikes.push(item)
          }
        })
        localStorage.setItem(`user_${this.userStorageKey}_likes`, JSON.stringify(mergedLikes))
        localStorage.removeItem('userLikes')
      }

      // 迁移历史数据
      const oldHistory = JSON.parse(localStorage.getItem('userHistory') || '[]')
      if (oldHistory.length > 0) {
        const currentHistory = JSON.parse(localStorage.getItem(`user_${this.userStorageKey}_history`) || '[]')
        const mergedHistory = [...currentHistory]
        oldHistory.forEach(item => {
          if (!mergedHistory.some(h => h.id === item.id)) {
            mergedHistory.push(item)
          }
        })
        localStorage.setItem(`user_${this.userStorageKey}_history`, JSON.stringify(mergedHistory))
        localStorage.removeItem('userHistory')
      }
    },
    
    // 加载用户数据
    loadUserData() {
      try {
        if (!this.currentUser || !this.currentUser.userId) {
          return
        }
        
        // 使用用户特定的storage key
        const userKey = this.userStorageKey
        
        // 收藏数据 - 尝试新格式，兼容旧格式
        let favorites = JSON.parse(localStorage.getItem(`user_${userKey}_favorites`) || '[]')
        // 如果新格式为空，尝试旧格式（兼容性处理）
        if (favorites.length === 0) {
          const oldFavorites = JSON.parse(localStorage.getItem('userFavorites') || '[]')
          if (oldFavorites.length > 0) {
            favorites = oldFavorites
            // 迁移到新格式
            localStorage.setItem(`user_${userKey}_favorites`, JSON.stringify(favorites))
            localStorage.removeItem('userFavorites')
          }
        }
        this.favorites = favorites

        // 点赞数据 - 同样处理兼容性
        let likes = JSON.parse(localStorage.getItem(`user_${userKey}_likes`) || '[]')
        if (likes.length === 0) {
          const oldLikes = JSON.parse(localStorage.getItem('userLikes') || '[]')
          if (oldLikes.length > 0) {
            likes = oldLikes
            localStorage.setItem(`user_${userKey}_likes`, JSON.stringify(likes))
            localStorage.removeItem('userLikes')
          }
        }
        this.likes = likes

        // 浏览历史数据 - 同样处理兼容性
        let history = JSON.parse(localStorage.getItem(`user_${userKey}_history`) || '[]')
        if (history.length === 0) {
          const oldHistory = JSON.parse(localStorage.getItem('userHistory') || '[]')
          if (oldHistory.length > 0) {
            history = oldHistory
            localStorage.setItem(`user_${userKey}_history`, JSON.stringify(history))
            localStorage.removeItem('userHistory')
          }
        }

        // 按观看时间倒序排列
        this.history = history.sort((a, b) => {
          const dateA = new Date(a.watchedAt || 0)
          const dateB = new Date(b.watchedAt || 0)
          return dateB - dateA
        })
      } catch (error) {
        console.error('加载用户数据失败:', error)
        // 初始化为空数组
        this.favorites = []
        this.likes = []
        this.history = []
      }
    },
    
    // 处理storage变化
    handleStorageChange(event) {
      if (!this.currentUser || !this.currentUser.userId) return

      const userKey = this.userStorageKey
      if (event.key === `user_${userKey}_favorites` || 
          event.key === `user_${userKey}_likes` || 
          event.key === `user_${userKey}_history` ||
          // 同时监听旧格式的键名，确保完全兼容
          event.key === 'userFavorites' ||
          event.key === 'userLikes' ||
          event.key === 'userHistory') {
        this.loadUserData()
      }
    },
    
    // 过滤课程分类
    filterCategory(category) {
      this.selectedCategory = category
    },
    
    // 获取状态样式
    getStatusClass(status) {
      const classes = {
        'ongoing': 'text-green-600',
        'ended': 'text-yellow-600'
      }
      return classes[status] || 'text-gray-600'
    },
    
    // 获取状态文本
    getStatusText(status) {
      const texts = {
        'ongoing': '进行中',
        'ended': '已结束'
      }
      return texts[status] || status
    },
    
    // 移除收藏课程
    removeFavorite(id) {
      if (confirm('确定要取消收藏吗？')) {
        this.favorites = this.favorites.filter(course => course.id !== id)
        localStorage.setItem(`user_${this.userStorageKey}_favorites`, JSON.stringify(this.favorites))
        this.showToast('已取消收藏')
      }
    },
    
    // 移除点赞
    removeLike(id) {
      if (confirm('确定要取消点赞吗？')) {
        this.likes = this.likes.filter(like => like.id !== id)
        localStorage.setItem(`user_${this.userStorageKey}_likes`, JSON.stringify(this.likes))
        this.showToast('已取消点赞')
      }
    },
    
    // 移除历史记录
    removeHistory(id) {
      if (confirm('确定要删除这条历史记录吗？')) {
        this.history = this.history.filter(record => record.id !== id)
        localStorage.setItem(`user_${this.userStorageKey}_history`, JSON.stringify(this.history))
        this.showToast('已删除历史记录')
      }
    },
    
    // 继续观看历史记录
    continueWatching(record) {
      // 确保课程信息完整
      const courseData = record.courseData || {
        id: record.courseId,
        title: record.courseName,
        teacher: record.teacher || '未知教师',
        category: this.getCategoryFromCourseTitle(record.courseName),
        description: `${record.courseName} - 学习记录`,
        views: '已学习',
        progress: record.progress || 0
      }
      
      console.log('从历史记录跳转的课程数据:', courseData)
      localStorage.setItem('selectedCourse', JSON.stringify(courseData))
      
      this.$router.push({
        name: 'VideoPlayer',
        params: {
          courseId: record.courseId
        },
        query: {
          fromHistory: true,
          historyId: record.id
        }
      })
    },
    
    // 从收藏跳转到课程
    goToCourseFromFavorite(course) {
      // 确保课程信息完整
      const courseData = {
        id: course.id,
        title: course.name || course.title,
        teacher: course.teacher || '未知教师',
        category: course.category || this.getCategoryFromCourseTitle(course.name || course.title),
        description: course.description || `${course.name || course.title} - 收藏课程`,
        views: course.views || '0播放',
        comments: course.comments || '0',
        duration: course.duration || '00:00',
        image: course.image || 'https://picsum.photos/400/225?random=' + course.id
      }
      
      console.log('从收藏跳转的课程数据:', courseData)
      localStorage.setItem('selectedCourse', JSON.stringify(courseData))
      
      this.$router.push({
        name: 'VideoPlayer',
        params: {
          courseId: course.id
        },
        query: {
          fromFavorite: true
        }
      })
    },
    
    // 从点赞跳转到课程
    goToCourseFromLike(like) {
      const courseData = {
        id: like.courseId,
        title: like.courseName,
        teacher: like.teacher || '未知教师',
        category: this.getCategoryFromCourseTitle(like.courseName),
        description: `${like.courseName} - 点赞课程`,
        views: '已点赞'
      }
      
      console.log('从点赞跳转的课程数据:', courseData)
      localStorage.setItem('selectedCourse', JSON.stringify(courseData))
      
      this.$router.push({
        name: 'VideoPlayer',
        params: {
          courseId: like.courseId
        },
        query: {
          fromLike: true
        }
      })
    },
    
    // 根据课程标题判断类别
    getCategoryFromCourseTitle(title) {
      if (!title) return 'computer'
      
      const computerKeywords = ['编程', '代码', '算法', '计算机', 'Python', 'Java', 'Web', '前端', '后端', '操作系统']
      const businessKeywords = ['商业', '管理', '市场', '营销', '财务', '投资', 'MBA', '分析']
      const designKeywords = ['设计', 'UI', 'UX', '视觉', '创意', '美术', '插画', '平面']
      
      if (computerKeywords.some(keyword => title.includes(keyword))) {
        return 'computer'
      } else if (businessKeywords.some(keyword => title.includes(keyword))) {
        return 'business'
      } else if (designKeywords.some(keyword => title.includes(keyword))) {
        return 'design'
      }
      return 'computer'
    },
    
    // 批量操作
    handleBatchAction() {
      if (!this.hasItems) return
      
      const actionText = this.batchButtonText.replace('批量', '')
      if (confirm(`确定要${actionText}吗？`)) {
        if (this.currentTab === 'collection') {
          // 清空收藏
          this.favorites = []
          localStorage.setItem(`user_${this.userStorageKey}_favorites`, JSON.stringify(this.favorites))
          
        } else if (this.currentTab === 'likes') {
          // 清空点赞
          this.likes = []
          localStorage.setItem(`user_${this.userStorageKey}_likes`, JSON.stringify(this.likes))
          
        } else if (this.currentTab === 'history') {
          // 清空历史记录
          this.history = []
          localStorage.setItem(`user_${this.userStorageKey}_history`, JSON.stringify(this.history))
        }
        
        this.showToast(`${actionText}成功`)
      }
    },
    
    // 显示提示信息
    showToast(message) {
      this.toastMessage = message
      setTimeout(() => {
        this.toastMessage = ''
      }, 3000)
    },
    
    // 导航方法
    goToHomepage() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
/* 侧边栏样式 */
.sidebar-parent {
  @apply flex items-center justify-between px-4 py-3 text-gray-500 hover:bg-primary/5 hover:text-primary transition-all duration-200 cursor-pointer;
}
.sidebar-parent.active {
  @apply bg-primary/10 text-primary font-medium;
}
.sidebar-parent-content {
  @apply flex items-center gap-2;
}
.sidebar-child {
  @apply flex items-center px-6 py-2 text-gray-500 hover:bg-primary/5 hover:text-primary transition-all duration-200 cursor-pointer text-sm;
}
.sidebar-child.active {
  @apply bg-primary/10 text-primary font-medium;
}
.sidebar-child-text {
  @apply ml-3;
}
.sidebar-icon {
  @apply w-4 text-center;
}
.rotate-icon {
  @apply transform transition-transform duration-200 rotate-90;
}

/* 导航容器 */
nav {
  @apply py-4 space-y-1 px-4;
}

/* 卡片样式 */
.card {
  @apply bg-white rounded-lg border border-gray-200 shadow-sm;
}
.card-shadow {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.02);
}

/* 按钮样式 */
.btn {
  @apply px-3 py-1 text-sm rounded transition-all duration-200;
}
.btn-primary {
  @apply w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-md transition-all duration-200 transform hover:scale-[1.01] active:scale-[0.99] focus:outline-none focus:ring-2 focus:ring-blue-500/50;
}

/* 输入框样式 */
.input-field {
  @apply w-full px-4 py-2.5 rounded-md border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition-all duration-200;
}

/* 收藏标签页样式 */
.favorite-tab {
  @apply px-4 py-2 text-sm font-medium transition-all duration-200 cursor-pointer;
}
.favorite-tab.active {
  @apply text-blue-600 border-b-2 border-blue-600;
}

/* 表格行悬停效果 */
.table-row-hover {
  @apply hover:bg-gray-50 transition-colors duration-200;
}

/* 提示信息动画 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fadeIn 0.3s ease forwards;
}

/* 响应式隐藏 */
.hidden {
  display: none;
}
</style>