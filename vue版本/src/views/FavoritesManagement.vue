<!-- FavoritesManagement.vue -->
<template>
  <div class="font-inter bg-gray-50 min-h-screen flex flex-col">
    <!-- 使用Header组件 -->
    <Header />
    
    <div class="flex flex-1">
      <!-- 侧边栏导航 -->
      <aside class="w-64 bg-white border-r border-gray-200 flex-shrink-0 h-[calc(100vh-5rem)] sticky top-[5rem] overflow-y-auto z-30">
        <nav class="py-4 space-y-1">
          <!-- 教师管理 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" @click="toggleSubmenu('teacher')">
              <div class="sidebar-parent-content">
                <i class="fa fa-tachometer sidebar-icon"></i>
                <span>教师管理</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200" :class="{'rotate-icon': activeSubmenu === 'teacher'}"></i>
            </div>
            <div id="submenu-teacher" class="bg-gray-50" :class="{'hidden': activeSubmenu !== 'teacher'}">
              <div class="sidebar-child" @click="goToWorkEngine">
                <i class="fa fa-circle-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">工作台</span>
              </div>
            </div>
          </div>

          <!-- 管理员管理 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" @click="toggleSubmenu('admin')">
              <div class="sidebar-parent-content">
                <i class="fa fa-user-secret sidebar-icon"></i>
                <span>管理员管理</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200" :class="{'rotate-icon': activeSubmenu === 'admin'}"></i>
            </div>
            <div id="submenu-admin" class="bg-gray-50" :class="{'hidden': activeSubmenu !== 'admin'}">
              <div class="sidebar-child" @click="goToCourseManagement">
                <i class="fa fa-circle-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">课程管理</span>
              </div>
              <div class="sidebar-child" @click="goToUserManagement">
                <i class="fa fa-circle-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">用户管理</span>
              </div>
            </div>
          </div>
          
          <!-- 收藏管理（当前激活） -->
          <div class="sidebar-group">
            <div class="sidebar-parent active" @click="toggleSubmenu('favorites')">
              <div class="sidebar-parent-content">
                <i class="fa fa-heart sidebar-icon"></i>
                <span>收藏管理</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200 rotate-icon"></i>
            </div>
            <div id="submenu-favorites" class="bg-gray-50" :class="{'hidden': activeSubmenu !== 'favorites'}">
              <div class="sidebar-child active" @click="switchTab('collection')">
                <i class="fa fa-book text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">我的收藏</span>
              </div>
              <div class="sidebar-child" @click="switchTab('likes')">
                <i class="fa fa-thumbs-up text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">点赞</span>
              </div>
              <div class="sidebar-child" @click="switchTab('history')">
                <i class="fa fa-history text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">历史记录</span>
              </div>
            </div>
          </div>
          
          <!-- 个人中心 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" @click="toggleSubmenu('user-center')">
              <div class="sidebar-parent-content">
                <i class="fa fa-user-circle-o sidebar-icon"></i>
                <span>个人中心</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200" :class="{'rotate-icon': activeSubmenu === 'user-center'}"></i>
            </div>
            <div id="submenu-user-center" class="bg-gray-50" :class="{'hidden': activeSubmenu !== 'user-center'}">
              <div class="sidebar-child" @click="goToPersonalInfo">
                <i class="fa fa-id-card-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">用户信息</span>
              </div>
              <div class="sidebar-child" @click="goToUserSettings">
                <i class="fa fa-cog text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">用户设置</span>
              </div>
            </div>
          </div>
        </nav>
      </aside>

      <!-- 主内容区域 -->
      <main class="flex-1 overflow-y-auto p-6">
        <div class="p-6">
          <!-- 面包屑导航 -->
          <div class="text-sm text-secondary mb-6">
            <span>用户中心</span>
            <i class="fa fa-angle-right mx-1 text-gray-400"></i>
            <span>收藏管理</span>
            <i class="fa fa-angle-right mx-1 text-gray-400"></i>
            <span class="text-dark font-medium">{{ breadcrumbCurrent }}</span>
          </div>

          <!-- 收藏管理页面 -->
          <div class="card p-6 card-shadow">
            <!-- 页面标题和批量操作 -->
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
              <div>
                <h3 class="text-lg font-semibold text-dark">{{ pageTitle }}</h3>
                <p class="text-sm text-secondary mt-1">{{ pageDescription }}</p>
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
                     @click="switchTab('collection')">
                  我的收藏
                </div>
                <div class="favorite-tab" :class="{ 'active': currentTab === 'likes' }" 
                     @click="switchTab('likes')">
                  点赞
                </div>
                <div class="favorite-tab" :class="{ 'active': currentTab === 'history' }" 
                     @click="switchTab('history')">
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
                          :class="selectedCategory === 'all' ? 'bg-primary/10 text-primary' : 'hover:bg-gray-100 text-gray-500'"
                          @click="filterCategory('all')">
                    全部课程
                  </button>
                  <button v-for="category in courseCategories" 
                          :key="category.value"
                          class="px-3 py-1 rounded text-sm"
                          :class="selectedCategory === category.value ? 'bg-primary/10 text-primary' : 'hover:bg-gray-100 text-gray-500'"
                          @click="filterCategory(category.value)">
                    {{ category.label }}
                  </button>
                </div>
              </div>
              
              <!-- 课程表格 -->
              <div class="overflow-x-auto" v-if="filteredCourses.length > 0">
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
                    <tr v-for="course in filteredCourses" 
                        :key="course.id"
                        class="border-b border-gray-200 table-row-hover">
                      <td class="py-3 px-2 text-gray-500">{{ course.id }}</td>
                      <td class="py-3 px-2">{{ course.name }}</td>
                      <td class="py-3 px-2">{{ course.teacher }}</td>
                      <td class="py-3 px-2">
                        <span :class="getStatusClass(course.status)" class="text-xs">
                          {{ getStatusText(course.status) }}
                        </span>
                      </td>
                      <td class="py-3 px-2 text-gray-500">{{ course.collectedAt }}</td>
                      <td class="py-3 px-2">
                        <button class="text-primary hover:text-primary/80 text-sm" 
                                @click="removeCourse(course.id)">
                          取消收藏
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              <!-- 空状态 -->
              <div v-else class="text-center py-12">
                <i class="fa fa-heart text-4xl text-gray-300 mb-4"></i>
                <h4 class="text-lg font-medium text-dark mb-2">暂无收藏内容</h4>
                <p class="text-secondary mb-6">您还没有收藏任何内容，快去发现您感兴趣的课程吧！</p>
                <button class="btn-primary max-w-xs mx-auto" @click="goToHomepage">
                  <i class="fa fa-compass mr-2"></i>去首页看看
                </button>
              </div>
              
              <!-- 分页区域 -->
              <div v-if="filteredCourses.length > 0" class="flex justify-between items-center mt-6">
                <div class="text-sm text-secondary">
                  共 <span>{{ filteredCourses.length }}</span> 条收藏
                </div>
                <div class="flex items-center gap-2">
                  <button class="w-8 h-8 flex items-center justify-center rounded border border-gray-200 text-secondary hover:border-primary hover:text-primary transition-colors"
                          @click="prevPage">
                    <i class="fa fa-angle-left"></i>
                  </button>
                  <button class="w-8 h-8 flex items-center justify-center rounded bg-primary text-white">1</button>
                  <button class="w-8 h-8 flex items-center justify-center rounded border border-gray-200 text-secondary hover:border-primary hover:text-primary transition-colors"
                          @click="nextPage">
                    <i class="fa fa-angle-right"></i>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- 点赞页面 -->
            <div v-if="currentTab === 'likes'" class="space-y-4">
              <div class="text-center py-12">
                <i class="fa fa-thumbs-up text-4xl text-gray-300 mb-4"></i>
                <h4 class="text-lg font-medium text-dark mb-2">您还没有点赞内容</h4>
                <p class="text-secondary mb-6">去浏览课程，给喜欢的内容点赞吧！</p>
                <button class="btn-primary max-w-xs mx-auto" @click="goToHomepage">
                  <i class="fa fa-compass mr-2"></i>去首页看看
                </button>
              </div>
            </div>
            
            <!-- 历史记录页面 -->
            <div v-if="currentTab === 'history'" class="space-y-4">
              <div class="text-center py-12">
                <i class="fa fa-history text-4xl text-gray-300 mb-4"></i>
                <h4 class="text-lg font-medium text-dark mb-2">您还没有浏览历史</h4>
                <p class="text-secondary mb-6">浏览课程后，这里会显示您的观看记录</p>
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
    <div v-if="toastMessage" class="toast-message fixed top-6 right-6 bg-dark text-white px-4 py-2 rounded-md shadow-lg z-50 animate-fade-in">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script>
// 引入Header和Footer组件
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
      // 侧边栏状态
      activeSubmenu: 'favorites',
      
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
      
      // 收藏的课程数据
      courses: [
        { 
          id: 'CS202501', 
          name: '计算机网络与通信', 
          teacher: '徐冠雷', 
          status: 'ongoing', 
          collectedAt: '2025-11-28',
          category: 'network'
        },
        { 
          id: 'MG202501', 
          name: '软件项目管理', 
          teacher: '徐斌', 
          status: 'ended', 
          collectedAt: '2025-10-15',
          category: 'management'
        },
        { 
          id: 'LI202501', 
          name: '中国现代文学', 
          teacher: '张明', 
          status: 'ongoing', 
          collectedAt: '2025-11-05',
          category: 'literature'
        },
        { 
          id: 'AI202501', 
          name: '机器学习基础', 
          teacher: '李华', 
          status: 'ongoing', 
          collectedAt: '2025-11-12',
          category: 'ai'
        },
        { 
          id: 'NE202501', 
          name: '网络安全技术', 
          teacher: '王强', 
          status: 'ended', 
          collectedAt: '2025-09-30',
          category: 'computer'
        }
      ],
      
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
      }
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
    
    // 过滤后的课程
    filteredCourses() {
      if (this.selectedCategory === 'all') {
        return this.courses
      }
      return this.courses.filter(course => course.category === this.selectedCategory)
    },
    
    // 是否有项目
    hasItems() {
      if (this.currentTab === 'collection') {
        return this.filteredCourses.length > 0
      }
      return false
    }
  },
  mounted() {
    // 从URL参数获取标签
    const urlParams = new URLSearchParams(window.location.search)
    const targetTab = urlParams.get('tab')
    
    // 如果URL参数指定了标签，则切换到对应标签
    if (targetTab && ['collection', 'likes', 'history'].includes(targetTab)) {
      this.currentTab = targetTab
      this.updateSidebarActive()
    }
  },
  methods: {
    // 侧边栏切换
    toggleSubmenu(submenu) {
      this.activeSubmenu = this.activeSubmenu === submenu ? null : submenu
    },
    
    // 更新侧边栏激活状态
    updateSidebarActive() {
      // 更新侧边栏子菜单激活状态
      const sidebarChildren = document.querySelectorAll('#submenu-favorites .sidebar-child')
      sidebarChildren.forEach(child => {
        child.classList.remove('active')
      })
      
      // 根据当前标签激活对应侧边栏项
      if (this.currentTab === 'collection') {
        const collectionItem = document.querySelector('#submenu-favorites .sidebar-child:nth-child(1)')
        if (collectionItem) collectionItem.classList.add('active')
      } else if (this.currentTab === 'likes') {
        const likesItem = document.querySelector('#submenu-favorites .sidebar-child:nth-child(2)')
        if (likesItem) likesItem.classList.add('active')
      } else if (this.currentTab === 'history') {
        const historyItem = document.querySelector('#submenu-favorites .sidebar-child:nth-child(3)')
        if (historyItem) historyItem.classList.add('active')
      }
    },
    
    // 切换标签页
    switchTab(tab) {
      this.currentTab = tab
      this.selectedCategory = 'all' // 重置筛选
      this.updateSidebarActive()
      
      // 更新URL参数
      const url = new URL(window.location)
      url.searchParams.set('tab', tab)
      window.history.replaceState({}, '', url)
    },
    
    // 过滤课程分类
    filterCategory(category) {
      this.selectedCategory = category
    },
    
    // 获取状态样式
    getStatusClass(status) {
      const classes = {
        'ongoing': 'text-success',
        'ended': 'text-warning'
      }
      return classes[status] || 'text-secondary'
    },
    
    // 获取状态文本
    getStatusText(status) {
      const texts = {
        'ongoing': '进行中',
        'ended': '已结束'
      }
      return texts[status] || status
    },
    
    // 移除课程
    removeCourse(id) {
      if (confirm('确定要取消收藏吗？')) {
        this.courses = this.courses.filter(course => course.id !== id)
        this.showToast('已取消收藏')
      }
    },
    
    // 批量操作
    handleBatchAction() {
      if (!this.hasItems) return
      
      const actionText = this.batchButtonText.replace('批量', '')
      if (confirm(`确定要${actionText}吗？`)) {
        if (this.currentTab === 'collection') {
          // 清空收藏
          this.courses = []
        }
        
        this.showToast(`${actionText}成功`)
      }
    },
    
    // 分页
    prevPage() {
      console.log('上一页')
      // 这里可以添加分页逻辑
    },
    
    nextPage() {
      console.log('下一页')
      // 这里可以添加分页逻辑
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
    },
    
    goToPersonalInfo() {
      this.$router.push('/personal-info')
    },
    
    goToUserSettings() {
      this.$router.push('/personal-info#settings')
    },
    
    goToWorkEngine() {
      this.$router.push('/work-engine')
    },
    
    goToCourseManagement() {
      this.$router.push('/course-management')
    },
    
    goToUserManagement() {
      this.$router.push('/user-management')
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
.sidebar-group {
  @apply mb-2;
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
  @apply w-full bg-primary hover:bg-primary/90 text-white font-medium py-2.5 rounded-md transition-all duration-200 transform hover:scale-[1.01] active:scale-[0.99] focus:outline-none focus:ring-2 focus:ring-primary/50;
}
.btn-text {
  @apply text-primary hover:bg-primary/10 transition-all duration-200;
}

/* 输入框样式 */
.input-field {
  @apply w-full px-4 py-2.5 rounded-md border border-gray-300 focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none transition-all duration-200;
}

/* 链接样式 */
.text-link {
  @apply text-primary hover:text-primary/80 transition-colors duration-200 cursor-pointer;
}

/* 收藏标签页样式 */
.favorite-tab {
  @apply px-4 py-2 text-sm font-medium transition-all duration-200 cursor-pointer;
}
.favorite-tab.active {
  @apply text-primary border-b-2 border-primary;
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