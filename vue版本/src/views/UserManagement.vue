<!-- views/UserManagement.vue -->
<template>
  <div class="font-inter bg-gray-50 min-h-screen flex flex-col">
    <Header />
    
    <div class="flex flex-1">
      <!-- 侧边栏导航 -->
      <aside class="w-64 bg-white border-r border-gray-200 flex-shrink-0 h-[calc(100vh-5rem)] sticky top-[5rem] overflow-y-auto z-30">
        <nav class="py-4 space-y-1">
          <!-- 教师管理 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" @click="goToPage('/work-engine')">
              <div class="sidebar-parent-content">
                <i class="fa fa-tachometer sidebar-icon"></i>
                <span>教师管理</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200"></i>
            </div>
          </div>

          <!-- 管理员管理 -->
          <div class="sidebar-group">
            <div class="sidebar-parent active" @click="toggleSubmenu('admin')">
              <div class="sidebar-parent-content">
                <i class="fa fa-user-secret sidebar-icon"></i>
                <span>管理员管理</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200" :class="{'rotate-icon': activeSubmenu === 'admin'}"></i>
            </div>
            <div id="submenu-admin" class="bg-gray-50" :class="{'hidden': activeSubmenu !== 'admin'}">
              <div class="sidebar-child" @click="goToPage('/course-management')">
                <i class="fa fa-circle-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">课程管理</span>
              </div>
              <div class="sidebar-child active" @click="goToPage('/user-management')">
                <i class="fa fa-circle-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">用户管理</span>
              </div>
            </div>
          </div>
             
          <!-- 收藏管理 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" @click="toggleSubmenu('favorites')">
              <div class="sidebar-parent-content">
                <i class="fa fa-heart sidebar-icon"></i>
                <span>收藏管理</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200" :class="{'rotate-icon': activeSubmenu === 'favorites'}"></i>
            </div>
            <div id="submenu-favorites" class="bg-gray-50" :class="{'hidden': activeSubmenu !== 'favorites'}">
              <div class="sidebar-child" @click="goToFavorites('my-collection')">
                <i class="fa fa-book text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">我的收藏</span>
              </div>
              <div class="sidebar-child" @click="goToFavorites('likes')">
                <i class="fa fa-thumbs-up text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">点赞</span>
              </div>
              <div class="sidebar-child" @click="goToFavorites('history')">
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
              <div class="sidebar-child" @click="goToPage('/personal-information')">
                <i class="fa fa-id-card-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">用户信息</span>
              </div>
              <div class="sidebar-child" @click="goToPage('/personal-information?tab=settings')">
                <i class="fa fa-cog text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">用户设置</span>
              </div>
            </div>
          </div>
        </nav>
      </aside>

      <!-- 主内容区域（用户管理UI） -->
      <main class="flex-1 overflow-y-auto p-6">
        <div class="p-6">
          <!-- 面包屑导航 -->
          <div class="text-sm text-secondary mb-6">
            <span>用户中心</span>
            <i class="fa fa-angle-right mx-1 text-gray-400"></i>
            <span>管理员管理</span>
            <i class="fa fa-angle-right mx-1 text-gray-400"></i>
            <span class="text-dark font-medium">用户管理</span>
          </div>

          <!-- 用户管理页面 -->
          <div class="card p-6 card-shadow">
            <h3 class="text-lg font-semibold text-dark mb-6">用户管理</h3>
            
            <!-- 搜索筛选区域 -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <div>
                <label class="block text-sm text-gray-500 mb-1">实际姓名</label>
                <input 
                  type="text" 
                  placeholder="请输入实际姓名" 
                  class="input-field"
                  v-model="searchParams.realName"
                  @keyup.enter="searchUsers"
                >
              </div>
              <div>
                <label class="block text-sm text-gray-500 mb-1">状态</label>
                <select class="input-field" v-model="searchParams.status">
                  <option value="">全部</option>
                  <option value="举报中">举报中</option>
                  <option value="教师申请">教师申请</option>
                  <option value="正常">正常</option>
                </select>
              </div>
              <div>
                <label class="block text-sm text-gray-500 mb-1">当前身份</label>
                <select class="input-field" v-model="searchParams.role">
                  <option value="">全部</option>
                  <option value="教师">教师</option>
                  <option value="学生">学生</option>
                </select>
              </div>
              <div class="flex items-end">
                <button class="btn-primary" @click="searchUsers">
                  <i class="fa fa-search mr-1"></i>查询
                </button>
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm text-gray-500 mb-1">开始日期</label>
                  <input type="date" class="input-field" v-model="searchParams.startDate">
                </div>
                <div>
                  <label class="block text-sm text-gray-500 mb-1">结束日期</label>
                  <input type="date" class="input-field" v-model="searchParams.endDate">
                </div>
              </div>
              <div>
                <label class="block text-sm text-gray-500 mb-1">用户名称</label>
                <input 
                  type="text" 
                  placeholder="请输入用户名" 
                  class="input-field"
                  v-model="searchParams.username"
                  @keyup.enter="searchUsers"
                >
              </div>
              <div>
                <label class="block text-sm text-gray-500 mb-1">用户编号</label>
                <input 
                  type="text" 
                  placeholder="请输入编号" 
                  class="input-field"
                  v-model="searchParams.userId"
                  @keyup.enter="searchUsers"
                >
              </div>
            </div>
            
            <div class="flex justify-end gap-4 mb-6">
              <button class="btn border border-gray-300 hover:bg-gray-50 transition-all duration-200 flex items-center gap-1" @click="resetSearch">
                <i class="fa fa-refresh"></i>重置
              </button>
              <button class="btn border border-gray-300 hover:bg-gray-50 transition-all duration-200 flex items-center gap-1" @click="exportData">
                <i class="fa fa-download"></i>下载
              </button>
            </div>
            
            <!-- 用户列表 -->
            <div class="overflow-x-auto">
              <table class="w-full border-collapse">
                <thead>
                  <tr class="bg-gray-50 text-left text-sm text-secondary">
                    <th class="px-4 py-3">用户编号</th>
                    <th class="px-4 py-3">用户名称</th>
                    <th class="px-4 py-3">内容体裁</th>
                    <th class="px-4 py-3">作者</th>
                    <th class="px-4 py-3">状态</th>
                    <th class="px-4 py-3">注册时间</th>
                    <th class="px-4 py-3">当前身份</th>
                    <th class="px-4 py-3">操作</th>
                  </tr>
                </thead>
                <tbody class="text-sm">
                  <tr 
                    v-for="user in paginatedUsers" 
                    :key="user.id"
                    class="border-b border-gray-100 bg-white hover:bg-gray-50 transition-colors"
                  >
                    <td class="px-4 py-3 text-dark">{{ user.id }}</td>
                    <td class="px-4 py-3 text-dark">{{ user.name }}</td>
                    <td class="px-4 py-3 text-dark">{{ user.contentType }}</td>
                    <td class="px-4 py-3 text-dark">{{ user.author }}</td>
                    <td class="px-4 py-3">
                      <span 
                        class="px-2 py-1 rounded text-xs"
                        :class="getStatusClass(user.status)"
                      >
                        {{ user.status }}
                      </span>
                    </td>
                    <td class="px-4 py-3 text-secondary">{{ user.registerTime }}</td>
                    <td class="px-4 py-3 text-dark">{{ user.role }}</td>
                    <td class="px-4 py-3">
                      <a href="#" class="text-link hover:underline" @click.prevent="viewUserDetail(user)">查看</a>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- 分页区域 -->
            <div class="flex justify-between items-center mt-6">
              <div class="text-sm text-secondary">共{{ totalItems }}条</div>
              <div class="flex items-center gap-2">
                <button 
                  class="w-8 h-8 flex items-center justify-center rounded border border-gray-200 text-secondary hover:border-primary hover:text-primary transition-colors"
                  @click="changePage(currentPage - 1)"
                  :disabled="currentPage === 1"
                >
                  <i class="fa fa-angle-left"></i>
                </button>
                
                <!-- 页码按钮 -->
                <template v-for="page in visiblePages" :key="page">
                  <button 
                    v-if="page === 'ellipsis'"
                    class="w-8 h-8 flex items-center justify-center text-gray-400"
                    disabled
                  >
                    ...
                  </button>
                  <button 
                    v-else
                    class="w-8 h-8 flex items-center justify-center rounded border border-gray-200 transition-colors"
                    :class="{
                      'bg-primary text-white border-primary': page === currentPage,
                      'text-secondary hover:border-primary hover:text-primary': page !== currentPage
                    }"
                    @click="changePage(page)"
                  >
                    {{ page }}
                  </button>
                </template>
                
                <button 
                  class="w-8 h-8 flex items-center justify-center rounded border border-gray-200 text-secondary hover:border-primary hover:text-primary transition-colors"
                  @click="changePage(currentPage + 1)"
                  :disabled="currentPage === totalPages"
                >
                  <i class="fa fa-angle-right"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'UserManagement',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      activeSubmenu: 'admin',
      searchParams: {
        realName: '',
        status: '',
        role: '',
        startDate: '',
        endDate: '',
        username: '',
        userId: ''
      },
      users: [
        { id: 232, name: '每日推荐视频集', contentType: '操作系统', author: '张三', status: '举报中', registerTime: '2021-02-28 10:30', role: '教师' },
        { id: 254, name: '每日推荐视频集', contentType: '操作系统', author: '李四', status: '教师申请', registerTime: '2021-02-28 10:30', role: '学生' },
        { id: 46, name: '每日推荐视频集', contentType: '操作系统', author: '王五', status: '举报中', registerTime: '2021-02-28 10:30', role: '教师' },
        { id: 577, name: '每日推荐视频集', contentType: '操作系统', author: '赵六', status: '正常', registerTime: '2021-02-28 10:30', role: '学生' },
        { id: 233, name: '每日推荐视频集', contentType: '操作系统', author: '钱七', status: '正常', registerTime: '2021-02-28 10:30', role: '学生' },
        { id: 255, name: '每日推荐视频集', contentType: '操作系统', author: '孙八', status: '正常', registerTime: '2021-02-28 10:30', role: '教师' },
        { id: 47, name: '每日推荐视频集', contentType: '操作系统', author: '周九', status: '正常', registerTime: '2021-02-28 10:30', role: '教师' },
        { id: 578, name: '每日推荐视频集', contentType: '操作系统', author: '吴十', status: '正常', registerTime: '2021-02-28 10:30', role: '学生' },
        { id: 234, name: '每日推荐视频集', contentType: '操作系统', author: '郑十一', status: '正常', registerTime: '2021-02-28 10:30', role: '学生' },
        { id: 256, name: '每日推荐视频集', contentType: '操作系统', author: '王十二', status: '正常', registerTime: '2021-02-28 10:30', role: '教师' },
        // 添加更多用户数据
        { id: 579, name: '每日推荐视频集', contentType: '操作系统', author: '刘十三', status: '正常', registerTime: '2021-03-01 10:30', role: '学生' },
        { id: 235, name: '每日推荐视频集', contentType: '操作系统', author: '陈十四', status: '教师申请', registerTime: '2021-03-01 10:30', role: '学生' },
        { id: 257, name: '每日推荐视频集', contentType: '操作系统', author: '林十五', status: '举报中', registerTime: '2021-03-01 10:30', role: '教师' }
      ],
      filteredUsers: [],
      currentPage: 1,
      itemsPerPage: 10
    }
  },
  computed: {
    totalItems() {
      return this.filteredUsers.length
    },
    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage)
    },
    paginatedUsers() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredUsers.slice(start, end)
    },
    visiblePages() {
      const pages = []
      const maxVisible = 7
      
      if (this.totalPages <= maxVisible) {
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i)
        }
      } else {
        let start = Math.max(1, this.currentPage - 3)
        let end = Math.min(this.totalPages, start + maxVisible - 1)
        
        if (end - start + 1 < maxVisible) {
          start = Math.max(1, end - maxVisible + 1)
        }
        
        if (start > 1) {
          pages.push(1)
          if (start > 2) pages.push('ellipsis')
        }
        
        for (let i = start; i <= end; i++) {
          pages.push(i)
        }
        
        if (end < this.totalPages) {
          if (end < this.totalPages - 1) pages.push('ellipsis')
          pages.push(this.totalPages)
        }
      }
      
      return pages
    }
  },
  mounted() {
    this.filteredUsers = [...this.users]
  },
  methods: {
    toggleSubmenu(submenu) {
      this.activeSubmenu = this.activeSubmenu === submenu ? null : submenu
    },
    
    goToPage(path) {
      this.$router.push(path)
    },
    
    goToFavorites(tab) {
      this.$router.push({
        path: '/favorites-management',
        query: { tab }
      })
    },
    
    getStatusClass(status) {
      switch (status) {
        case '举报中':
          return 'bg-red-100 text-red-800'
        case '教师申请':
          return 'bg-yellow-100 text-yellow-800'
        case '正常':
          return 'bg-green-100 text-green-800'
        default:
          return 'bg-gray-100 text-gray-800'
      }
    },
    
    searchUsers() {
      this.filteredUsers = this.users.filter(user => {
        const matchesRealName = !this.searchParams.realName || 
          user.author.toLowerCase().includes(this.searchParams.realName.toLowerCase())
        
        const matchesStatus = !this.searchParams.status || 
          user.status === this.searchParams.status
        
        const matchesRole = !this.searchParams.role || 
          user.role === this.searchParams.role
        
        const matchesUsername = !this.searchParams.username || 
          user.name.toLowerCase().includes(this.searchParams.username.toLowerCase())
        
        const matchesUserId = !this.searchParams.userId || 
          user.id.toString().includes(this.searchParams.userId)
        
        return matchesRealName && matchesStatus && matchesRole && matchesUsername && matchesUserId
      })
      
      this.currentPage = 1
    },
    
    resetSearch() {
      this.searchParams = {
        realName: '',
        status: '',
        role: '',
        startDate: '',
        endDate: '',
        username: '',
        userId: ''
      }
      this.filteredUsers = [...this.users]
      this.currentPage = 1
    },
    
    exportData() {
      alert('数据导出功能开发中')
    },
    
    viewUserDetail(user) {
      alert(`查看用户详情: ${user.name} (${user.author})`)
    },
    
    changePage(page) {
      if (page < 1 || page > this.totalPages) return
      this.currentPage = page
      window.scrollTo({ top: 0, behavior: 'smooth' })
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
  @apply bg-primary hover:bg-primary/90 text-white font-medium py-2.5 rounded-md transition-all duration-200 transform hover:scale-[1.01] active:scale-[0.99] focus:outline-none focus:ring-2 focus:ring-primary/50;
}

/* 输入框样式 */
.input-field {
  @apply w-full px-4 py-2.5 rounded-md border border-gray-300 focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none transition-all duration-200;
}

/* 链接样式 */
.text-link {
  @apply text-primary hover:text-primary/80 transition-colors duration-200 cursor-pointer;
}
</style>