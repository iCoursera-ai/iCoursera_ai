<template>
  <header class="bg-white py-4 px-6 md:px-8 shadow-sm sticky top-0 z-30 border-b border-gray-200">
    <div class="container mx-auto flex justify-between items-center">
      <!-- 左侧Logo区域 -->
      <div class="flex items-center gap-2 cursor-pointer" @click="$router.push('/')">
        <div class="bg-primary text-white p-1.5 rounded-md">
          <i class="fa fa-graduation-cap"></i>
        </div>
        <span class="text-lg font-semibold text-dark">BGarea</span>
      </div>

      <!-- 中间导航按钮区域 -->
      <div class="hidden md:flex items-center gap-6">
        <button @click="$router.push('/')" class="text-black hover:text-primary text-sm font-medium transition-colors duration-200 flex items-center gap-1">
          首页
        </button>
        <button @click="$router.push('/personal-info')" class="text-black hover:text-primary text-sm font-medium transition-colors duration-200 flex items-center gap-1">
          用户中心
        </button>
        <button @click="$router.push('/login')" class="text-black hover:text-primary text-sm font-medium transition-colors duration-200 flex items-center gap-1">
          登录界面
        </button>
        <button @click="$router.push('/article-management')" class="text-black hover:text-primary text-sm font-medium transition-colors duration-200 flex items-center gap-1">
          稿件管理界面
        </button>
      </div>

      <!-- 右侧用户操作区域 -->
      <div class="flex items-center gap-4">
        <!-- 搜索框 -->
        <div class="relative hidden md:block">
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="搜索课程、讲师..." 
            class="w-48 px-4 py-2 pl-10 rounded-md border border-gray-300 focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none transition-all duration-200 text-sm"
            @keypress.enter="handleSearch"
          >
          <i class="fa fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
        </div>
        
        <!-- 移动端搜索按钮 -->
        <button @click="showMobileSearch = !showMobileSearch" class="md:hidden text-secondary hover:text-primary text-sm font-medium transition-colors duration-200 flex items-center gap-1">
          <i class="fa fa-search"></i>
        </button>
        
        <!-- 用户菜单 -->
        <div class="flex items-center gap-4">
          <div v-if="isLoggedIn" class="relative" id="userMenuContainer">
            <button @click="toggleUserMenu" class="flex items-center gap-2 hover:text-primary transition-colors">
              <i class="fa fa-user-circle-o text-lg"></i>
              <span class="hidden md:inline">{{ currentUser.username }}</span>
            </button>
            <div v-if="showUserMenu" class="absolute right-0 mt-2 w-40 bg-white rounded-md shadow-lg py-2 z-50 border border-gray-100">
              <router-link to="/personal-info" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors" @click="hideUserMenu">
                个人中心
              </router-link>
              <button @click="logout" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                退出登录
              </button>
            </div>
          </div>
          <div v-else class="flex items-center gap-4">
            <router-link to="/login" class="text-primary hover:text-primary/80 font-medium transition-colors">登录</router-link>
            <router-link to="/register" class="bg-primary hover:bg-primary/90 text-white px-4 py-1.5 rounded-md font-medium transition-colors">注册</router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 移动端搜索框 -->
    <div v-if="showMobileSearch" class="absolute top-full left-0 right-0 bg-white p-4 shadow-lg border-t z-40">
      <div class="relative">
        <input 
          type="text" 
          v-model="mobileSearchQuery"
          placeholder="搜索课程、讲师..." 
          class="w-full px-4 py-2 pl-10 rounded-md border border-gray-300 focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none transition-all duration-200 text-sm"
          @keypress.enter="handleMobileSearch"
        >
        <i class="fa fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
        <button @click="showMobileSearch = false" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-primary">
          <i class="fa fa-times"></i>
        </button>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      searchQuery: '',
      mobileSearchQuery: '',
      showMobileSearch: false,
      showUserMenu: false,
      currentUser: null,
      isLoggedIn: false,
      userMenuTimeout: null
    }
  },
  mounted() {
    this.checkLoginStatus()
    this.setupClickOutsideListener()
  },
  methods: {
    handleSearch() {
      if (this.searchQuery.trim()) {
        // 跳转到搜索页面并传递搜索参数
        this.$router.push({
          path: '/search',
          query: { 
            q: this.searchQuery.trim(),
            from: 'header'
          }
        })
      }
    },
    
    handleMobileSearch() {
      if (this.mobileSearchQuery.trim()) {
        // 跳转到搜索页面并传递搜索参数
        this.$router.push({
          path: '/search',
          query: { 
            q: this.mobileSearchQuery.trim(),
            from: 'mobile_header'
          }
        })
        this.showMobileSearch = false
      }
    },
    
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu
      // 清除之前的定时器
      if (this.userMenuTimeout) {
        clearTimeout(this.userMenuTimeout)
        this.userMenuTimeout = null
      }
    },
    
    showUserMenuNow() {
      if (this.userMenuTimeout) {
        clearTimeout(this.userMenuTimeout)
      }
      this.showUserMenu = true
    },
    
    hideUserMenu() {
      // 延迟隐藏，给用户时间移到菜单上
      this.userMenuTimeout = setTimeout(() => {
        this.showUserMenu = false
      }, 200)
    },
    
    checkLoginStatus() {
      const user = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
      if (user) {
        this.currentUser = JSON.parse(user)
        this.isLoggedIn = true
      }
    },
    
    logout() {
      localStorage.removeItem('bgareaCurrentUser')
      sessionStorage.removeItem('bgareaCurrentUser')
      this.isLoggedIn = false
      this.currentUser = null
      this.showUserMenu = false
      this.$router.push('/')
    },
    
    setupClickOutsideListener() {
      // 点击页面其他地方时关闭用户菜单
      document.addEventListener('click', (event) => {
        const userMenuContainer = document.getElementById('userMenuContainer')
        if (userMenuContainer && !userMenuContainer.contains(event.target)) {
          this.showUserMenu = false
        }
      })
    }
  }
}
</script>

<style scoped>
/* 为整个用户菜单容器添加悬停效果 */
#userMenuContainer:hover .fa-user-circle-o {
  color: #165DFF;
}

/* 确保下拉菜单有足够的空间 */
.absolute {
  min-width: 160px;
}
</style>