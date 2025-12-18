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

      <!-- 中间搜索框区域 - 只在非搜索页面显示 -->
      <div v-if="!isSearchPage" class="flex-1 mx-6 md:mx-10 lg:mx-16">
        <div class="relative max-w-2xl mx-auto">
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="搜索课程、讲师..." 
            class="w-full px-4 py-2.5 pl-4 pr-12 rounded-md border-none bg-gray-100 hover:bg-gray-200 focus:bg-white focus:outline-none transition-all duration-200 text-sm"
            @keypress.enter="handleSearch"
          >
          <!-- 搜索按钮（右侧） -->
          <button 
            @click="handleSearch"
            class="absolute right-0 top-0 h-full w-10 flex items-center justify-center text-gray-500 hover:text-primary transition-colors"
          >
            <i class="fa fa-search"></i>
          </button>
        </div>
      </div>

      <!-- 如果是在搜索页面，这里留空以保持布局 -->
      <div v-else class="flex-1"></div>

      <!-- 右侧用户操作区域 -->
      <div class="flex items-center gap-4">
        <!-- 移动端搜索按钮 - 只在非搜索页面显示 -->
        <button 
          v-if="!isSearchPage"
          @click="showMobileSearch = !showMobileSearch" 
          class="md:hidden text-secondary hover:text-primary text-sm font-medium transition-colors duration-200 flex items-center gap-1"
        >
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

    <!-- 移动端搜索框 - 只在非搜索页面显示 -->
    <div v-if="showMobileSearch && !isSearchPage" class="absolute top-full left-0 right-0 bg-white p-4 shadow-lg border-t z-40">
      <div class="relative">
        <input 
          type="text" 
          v-model="mobileSearchQuery"
          placeholder="搜索课程、讲师..." 
          class="w-full px-4 py-3 pl-4 pr-12 rounded-md border-none bg-gray-100 hover:bg-gray-200 focus:bg-white focus:outline-none transition-all duration-200 text-sm"
          @keypress.enter="handleMobileSearch"
        >
        <!-- 移动端搜索按钮（右侧） -->
        <button 
          @click="handleMobileSearch"
          class="absolute right-0 top-0 h-full w-8 flex items-center justify-center text-gray-500 hover:text-primary transition-colors"
        >
          <i class="fa fa-search"></i>
        </button>
        <!-- 移动端关闭按钮 -->
        <button @click="showMobileSearch = false" class="absolute right-12 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-primary">
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
      userMenuTimeout: null,
      isSearchPage: false // 新增：判断是否在搜索页面
    }
  },
  watch: {
    // 监听路由变化
    '$route'(to) {
      this.checkPageType(to)
    }
  },
  mounted() {
    this.checkLoginStatus()
    this.setupClickOutsideListener()
    // 初始化时检查当前页面类型
    this.checkPageType(this.$route)
  },
  beforeUnmount() {
    // 清理事件监听器
    if (this.userMenuTimeout) {
      clearTimeout(this.userMenuTimeout)
    }
  },
  methods: {
    // 检查当前页面类型
    checkPageType(route) {
      this.isSearchPage = route.path === '/search'
    },
    
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
        this.mobileSearchQuery = ''
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
        try {
          this.currentUser = JSON.parse(user)
          this.isLoggedIn = true
        } catch (error) {
          console.error('解析用户数据失败:', error)
          this.clearUserData()
        }
      }
    },
    
    logout() {
      this.clearUserData()
      this.$router.push('/')
      window.dispatchEvent(new CustomEvent('user-auth-change'))
    },
    
    clearUserData() {
      localStorage.removeItem('bgareaCurrentUser')
      sessionStorage.removeItem('bgareaCurrentUser')
      this.isLoggedIn = false
      this.currentUser = null
      this.showUserMenu = false
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

/* 搜索框样式优化 */
input::placeholder {
  color: #9CA3AF;
}

/* 移除所有蓝色边框效果 */
input:focus {
  --tw-ring-offset-shadow: none;
  --tw-ring-shadow: none;
  box-shadow: none;
}

/* 搜索按钮样式优化 */
button[class*="absolute"]:hover {
  background-color: transparent;
}

/* 当在搜索页面时，右侧区域可能需要调整 */
.flex-1 {
  transition: all 0.3s ease;
}
</style>