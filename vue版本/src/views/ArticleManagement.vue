<template>
  <div class="font-inter bg-gray-50 min-h-screen flex flex-col">
    <Header />
    
    <div class="flex flex-1">
      <!-- 侧边栏导航 -->
      <aside class="w-64 bg-white border-r border-gray-200 flex-shrink-0 h-[calc(100vh-5rem)] sticky top-[5rem] overflow-y-auto z-30">
        <nav class="py-4 space-y-1">
          <!-- 教师管理 -->
          <div class="sidebar-group">
            <div class="sidebar-parent active" @click="toggleSubmenu('dashboard')">
              <div class="sidebar-parent-content">
                <i class="fa fa-tachometer sidebar-icon"></i>
                <span>教师管理</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200"></i>
            </div>
            <div id="submenu-dashboard" class="bg-gray-50" :class="{'hidden': activeSubmenu !== 'dashboard'}">
              <div class="sidebar-child" @click="goToTeacherDashboard">
                <i class="fa fa-circle-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">工作台</span>
              </div>
              <!-- <div class="sidebar-child active" @click="goToPage('/article-management')">
                <i class="fa fa-file-text-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">稿件管理</span>
              </div> -->
            </div>
          </div>

          <!-- 管理员管理
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
          </div> -->
             
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
              <div 
                class="sidebar-child" 
                @click="goToPersonalCenter('user-info')"
              >
                <i class="fa fa-id-card-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">用户信息</span>
              </div>
              <div 
                class="sidebar-child" 
                @click="goToPersonalCenter('user-settings')"
              >
                <i class="fa fa-cog text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">用户设置</span>
              </div>
            </div>
          </div>
        </nav>
      </aside>

      <!-- 主内容区域 -->
      <main class="flex-1 overflow-y-auto p-6" style="max-height: calc(100vh - 5rem);">
        <!-- 面包屑导航 -->
        <div class="text-sm text-secondary mb-6">
          <span>用户中心</span>
          <i class="fa fa-angle-right mx-1 text-gray-400"></i>
          <span>教师管理</span>
          <i class="fa fa-angle-right mx-1 text-gray-400"></i>
          <span class="text-dark font-medium">稿件管理</span>
        </div>

        <!-- 稿件管理内容 -->
        <div class="space-y-6">
          <!-- 页面标题区域 -->
          <div class="mb-2">
            <h1 class="text-xl font-bold text-gray-800 mb-1">稿件管理</h1>
            <p class="text-gray-500 text-sm">管理课程相关视频文件的上传、发布与下载操作</p>
          </div>

          <!-- 新增稿件区域 -->
          <div class="card p-4 card-shadow">
            <h2 class="text-base font-semibold text-gray-800 mb-4">新增稿件</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <!-- 上传区域 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">选择课程</label>
                <div 
                  @click="triggerFileInput"
                  @dragover.prevent="dragover = true"
                  @dragleave.prevent="dragover = false"
                  @drop.prevent="handleDrop"
                  :class="[
                    'upload-area',
                    dragover ? 'active' : '',
                    uploadForm.previewImage ? 'has-preview' : ''
                  ]"
                >
                  <div v-if="uploadForm.previewImage" class="mb-4">
                    <img :src="uploadForm.previewImage" alt="预览图" class="w-32 h-32 object-cover rounded mx-auto">
                  </div>
                  <p class="text-gray-500 mb-2">{{ uploadForm.file ? uploadForm.file.name : '点击或拖拽图片文件到此处上传' }}</p>
                  <p class="text-xs text-gray-400 mb-4">支持png格式，单个文件不超过25MB</p>
                  <input 
                    type="file" 
                    ref="fileInput"
                    @change="handleFileSelect"
                    accept="image/png" 
                    class="hidden"
                  >
                  <button class="px-3 py-1 bg-primary text-white rounded text-sm">选择文件</button>
                </div>
              </div>
              
              <!-- 课程简介 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">课程简介</label>
                <textarea 
                  v-model="uploadForm.description" 
                  class="input-field h-32" 
                  placeholder="输入课程简介（将显示给学员）"
                ></textarea>
              </div>
              
              <!-- 课程信息 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">课程节数</label>
                <input 
                  v-model="uploadForm.chapterCount" 
                  type="text" 
                  class="input-field mb-4" 
                  placeholder="输入章节数"
                >
                <input 
                  v-model="uploadForm.title" 
                  type="text" 
                  class="input-field mb-4" 
                  placeholder="输入课程标题（将显示给学员）"
                >
                <button 
                  @click="handleUpload"
                  :disabled="!canUpload"
                  :class="[
                    'btn-primary w-full',
                    !canUpload ? 'opacity-50 cursor-not-allowed' : ''
                  ]"
                >
                  {{ uploading ? '上传中...' : '开始上传' }}
                </button>
              </div>
            </div>
          </div>

          <!-- 稿件管理列区域 -->
          <div class="card p-4 card-shadow">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-base font-semibold text-gray-800">稿件管理列</h2>
              <div class="relative">
                <input 
                  v-model="searchQuery" 
                  type="text" 
                  class="input-field w-48 pr-8 text-sm" 
                  placeholder="输入时间，课程名等"
                  @keyup.enter="handleSearch"
                >
                <button @click="handleSearch" class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500">
                  <i class="fa fa-search"></i>
                </button>
              </div>
            </div>

            <!-- 表格区域 -->
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-gray-200">
                    <th class="text-left py-2 px-1 font-medium text-gray-700">预览图</th>
                    <th class="text-left py-2 px-1 font-medium text-gray-700">文件信息</th>
                    <th class="text-left py-2 px-1 font-medium text-gray-700">章节数</th>
                    <th class="text-left py-2 px-1 font-medium text-gray-700">文件大小</th>
                    <th class="text-left py-2 px-1 font-medium text-gray-700">上传时间</th>
                    <th class="text-left py-2 px-1 font-medium text-gray-700">状态</th>
                    <th class="text-left py-2 px-1 font-medium text-gray-700">操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="file in paginatedFiles" :key="file.id" class="border-b border-gray-200 hover:bg-gray-50">
                    <!-- 预览图列 - 点击跳转到编辑界面 -->
                    <td class="py-3 px-1">
                      <div 
                        class="w-8 h-8 bg-gray-200 rounded cursor-pointer hover:opacity-80 transition-opacity"
                        @click="goToVideoUpload(file.id)"
                        title="点击编辑稿件"
                      ></div>
                    </td>
                    
                    <!-- 文件信息列 - 点击跳转到编辑界面 -->
                    <td class="py-3 px-1">
                      <div 
                        class="cursor-pointer hover:text-primary transition-colors"
                        @click="goToVideoUpload(file.id)"
                      >
                        <p class="font-medium text-gray-800">{{ file.title }}</p>
                        <p class="text-xs text-gray-500">时长: {{ file.duration }}</p>
                      </div>
                    </td>
                    
                    <!-- 章节数列 - 点击跳转到编辑界面 -->
                    <td 
                      class="py-3 px-1 cursor-pointer hover:text-primary transition-colors"
                      @click="goToVideoUpload(file.id)"
                      title="点击编辑稿件"
                    >
                      {{ file.chapter }}
                    </td>
                    
                    <!-- 文件大小列 - 不点击 -->
                    <td class="py-3 px-1">{{ file.size }}</td>
                    
                    <!-- 上传时间列 - 不点击 -->
                    <td class="py-3 px-1">{{ file.time }}</td>
                    
                    <!-- 状态列 - 点击跳转到编辑界面 -->
                    <td 
                      class="py-3 px-1 cursor-pointer"
                      @click="goToVideoUpload(file.id)"
                      title="点击编辑稿件"
                    >
                      <span :class="getStatusBadgeClass(file.status)">
                        {{ file.statusText }}
                      </span>
                    </td>
                    
                    <!-- 操作按钮列 -->
                    <td class="py-3 px-1">
                      <!-- 预览按钮 - 点击打开预览面板 -->
                      <button 
                        @click="previewFile(file)" 
                        class="text-primary hover:underline mr-2"
                        title="预览稿件详情"
                      >
                        预览
                      </button>
                      <template v-if="file.status === 'published'">
                        <button 
                          @click="downloadFile(file)" 
                          class="text-red-500 hover:underline"
                          title="下载文件"
                        >
                          下载
                        </button>
                      </template>
                      <template v-else-if="file.status === 'draft'">
                        <button 
                          @click="publishFile(file)" 
                          class="text-green-500 hover:underline"
                          title="发布稿件"
                        >
                          发布
                        </button>
                      </template>
                      <template v-else-if="file.status === 'pending'">
                        <button 
                          @click="cancelReview(file)" 
                          class="text-gray-500 hover:underline"
                          title="取消审核"
                        >
                          取消
                        </button>
                      </template>
                      <template v-else-if="file.status === 'unpublished'">
                        <button 
                          @click="republishFile(file)" 
                          class="text-blue-500 hover:underline mr-2"
                          title="重新发布"
                        >
                          重新发布
                        </button>
                        <button 
                          @click="deleteFile(file)" 
                          class="text-red-500 hover:underline"
                          title="删除稿件"
                        >
                          删除
                        </button>
                      </template>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- 分页区域 -->
            <div class="flex justify-between items-center mt-4 text-sm">
              <p class="text-gray-500">显示{{ startIndex + 1 }}至{{ endIndex }}条，共{{ filteredFiles.length }}条</p>
              <div class="flex gap-1">
                <button 
                  v-for="page in totalPages" 
                  :key="page"
                  @click="goToPage(page)"
                  :class="[
                    'page-btn w-6 h-6 flex items-center justify-center rounded',
                    currentPage === page ? 'bg-primary text-white' : 'hover:bg-gray-200'
                  ]"
                >
                  {{ page }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- 文件详情预览区域 -->
    <div 
      v-if="showPreviewPanel" 
      class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-40"
      @click.self="closePreviewPanel"
    >
      <div class="bg-white rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-lg font-semibold text-gray-800">文件详情</h3>
          <button @click="closePreviewPanel" class="text-gray-400 hover:text-gray-600">
            <i class="fa fa-times"></i>
          </button>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="text-center">
            <img :src="previewFileData.image || 'https://picsum.photos/400/300'" alt="预览图" class="w-full max-w-xs h-48 object-cover rounded mx-auto mb-4">
            <div class="flex gap-2 justify-center">
              <button @click="goToVideoUpload(previewFileData.id)" class="px-4 py-2 bg-primary text-white rounded text-sm hover:bg-primary/90">
                <i class="fa fa-edit mr-1"></i> 编辑稿件
              </button>
              <button @click="downloadFile(previewFileData)" class="px-4 py-2 border border-primary text-primary rounded text-sm hover:bg-primary/5">
                <i class="fa fa-download mr-1"></i> 下载文件
              </button>
            </div>
          </div>
          
          <div class="space-y-4">
            <div>
              <h4 class="text-xl font-medium text-gray-800 mb-1">{{ previewFileData.title }}</h4>
              <div class="flex flex-wrap gap-2 mt-2">
                <span class="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-100 text-gray-700">
                  <i class="fa fa-clock-o mr-1"></i> {{ previewFileData.duration }}
                </span>
                <span class="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-100 text-gray-700">
                  <i class="fa fa-file mr-1"></i> {{ previewFileData.size }}
                </span>
                <span :class="getStatusPanelClass(previewFileData.status)" class="inline-flex items-center px-2 py-1 rounded text-xs">
                  <i :class="getStatusIcon(previewFileData.status)" class="mr-1"></i>
                  {{ getStatusPanelText(previewFileData.status) }}
                </span>
              </div>
            </div>
            
            <div class="space-y-2">
              <h5 class="text-sm font-medium text-gray-700">基本信息</h5>
              <div class="grid grid-cols-2 gap-3">
                <div class="bg-gray-50 p-3 rounded">
                  <p class="text-xs text-gray-500">章节数</p>
                  <p class="text-sm font-medium">{{ previewFileData.chapter }}</p>
                </div>
                <div class="bg-gray-50 p-3 rounded">
                  <p class="text-xs text-gray-500">上传时间</p>
                  <p class="text-sm font-medium">{{ previewFileData.time }}</p>
                </div>
                <div class="bg-gray-50 p-3 rounded">
                  <p class="text-xs text-gray-500">文件格式</p>
                  <p class="text-sm font-medium">MP4</p>
                </div>
                <div class="bg-gray-50 p-3 rounded">
                  <p class="text-xs text-gray-500">更新时间</p>
                  <p class="text-sm font-medium">{{ previewFileData.updateTime }}</p>
                </div>
              </div>
            </div>
            
            <div>
              <h5 class="text-sm font-medium text-gray-700 mb-2">课程简介</h5>
              <div class="bg-gray-50 p-3 rounded text-sm text-gray-600">
                <p>{{ previewFileData.desc }}</p>
              </div>
            </div>
            
            <!-- 操作按钮组 -->
            <div class="flex gap-3 pt-4">
              <button 
                @click="goToVideoUpload(previewFileData.id)"
                class="flex-1 px-4 py-2.5 bg-primary text-white rounded-md text-sm font-medium hover:bg-primary/90 transition-colors flex items-center justify-center gap-2"
              >
                <i class="fa fa-pencil"></i>
                <span>编辑稿件</span>
              </button>
              <button 
                @click="closePreviewPanel"
                class="flex-1 px-4 py-2.5 border border-gray-300 text-gray-700 rounded-md text-sm font-medium hover:bg-gray-50 transition-colors flex items-center justify-center gap-2"
              >
                <i class="fa fa-times"></i>
                <span>关闭预览</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 提示框组件 -->
    <div :class="['toast', toastClass, showToast ? 'show' : '']" v-if="showToast">
      <i :class="toastIcon"></i>
      <span>{{ toastMessage }}</span>
    </div>

    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'ArticleManagement',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      activeSubmenu: 'dashboard',
      currentUser: null,
      // 文件数据
      fileData: [
        { 
          id: 1, 
          title: 'JavaScript基础语法讲解', 
          duration: '15:30', 
          chapter: '一章', 
          size: '256 MB', 
          time: '2025-10-15 09:23', 
          updateTime: '2025-10-15 10:10',
          status: 'published', 
          statusText: '已发',
          desc: '本课程详细讲解JavaScript基础语法，包括变量、数据类型、运算符、流程控制等核心知识点，适合零基础入门的学员学习。通过实例演示和练习，帮助学员快速掌握JavaScript编程基础。'
        },
        { 
          id: 2, 
          title: 'DOM元素操作实战', 
          duration: '20:58', 
          chapter: '二章', 
          size: '384 MB', 
          time: '2025-10-18 14:56',
          updateTime: '2025-10-18 15:30',
          status: 'draft', 
          statusText: '未发',
          desc: '深入讲解DOM元素的各种操作方法，包括元素的查找、创建、修改、删除等，结合实际项目案例，让学员掌握如何通过JavaScript操作网页元素，实现动态交互效果。'
        },
        { 
          id: 3, 
          title: 'Promise异步编程详解', 
          duration: '18:45', 
          chapter: '三章', 
          size: '312 MB', 
          time: '2025-10-20 11:32',
          updateTime: '2025-10-20 12:15',
          status: 'pending', 
          statusText: '审核',
          desc: '详细介绍Promise异步编程模式，包括Promise的基本用法、链式调用、错误处理等，帮助学员理解异步编程的核心思想，解决回调地狱问题，提升代码质量和可维护性。'
        },
        { 
          id: 4, 
          title: 'vue3基础入门', 
          duration: '25:10', 
          chapter: '四章', 
          size: '420 MB', 
          time: '2025-10-12 08:45',
          updateTime: '2025-10-12 09:30',
          status: 'unpublished', 
          statusText: '已下架',
          desc: '从零开始学习Vue3框架，包括Composition API、响应式原理、组件开发等核心内容，通过实战案例帮助学员快速掌握Vue3的使用方法，为后续开发大型前端项目打下基础。'
        },
        { 
          id: 5, 
          title: 'React Hooks实战', 
          duration: '22:30', 
          chapter: '五章', 
          size: '378 MB', 
          time: '2025-10-22 15:40',
          updateTime: '2025-10-22 16:20',
          status: 'draft', 
          statusText: '未发',
          desc: '详细讲解React Hooks的使用方法，包括useState、useEffect、useContext等常用Hook，帮助学员简化组件逻辑，提高开发效率，掌握现代React开发模式。'
        },
        { 
          id: 6, 
          title: 'TypeScript类型系统', 
          duration: '19:15', 
          chapter: '六章', 
          size: '296 MB', 
          time: '2025-10-25 10:18',
          updateTime: '2025-10-25 11:05',
          status: 'published', 
          statusText: '已发',
          desc: '深入讲解TypeScript的类型系统，包括基本类型、接口、泛型、类型守卫等核心概念，帮助学员提升代码的可读性和可维护性，减少运行时错误。'
        },
        { 
          id: 7, 
          title: 'WebPack打包优化', 
          duration: '28:40', 
          chapter: '七章', 
          size: '412 MB', 
          time: '2025-10-28 13:25',
          updateTime: '2025-10-28 14:10',
          status: 'pending', 
          statusText: '审核',
          desc: '介绍WebPack的高级配置和优化技巧，包括代码分割、懒加载、Tree Shaking、缓存优化等，帮助学员提升项目构建速度和运行性能。'
        },
        { 
          id: 8, 
          title: '性能优化实战', 
          duration: '24:50', 
          chapter: '八章', 
          size: '388 MB', 
          time: '2025-10-30 09:45',
          updateTime: '2025-10-30 10:30',
          status: 'unpublished', 
          statusText: '已下架',
          desc: '分享前端性能优化的实用技巧，包括网络优化、渲染优化、代码优化等方面，通过实际案例演示如何提升网页加载速度和用户体验。'
        }
      ],
      // 上传表单
      uploadForm: {
        file: null,
        previewImage: null,
        title: '',
        description: '',
        chapterCount: '',
        imageFile: null
      },
      dragover: false,
      uploading: false,
      // 搜索和筛选
      searchQuery: '',
      // 分页
      currentPage: 1,
      pageSize: 4,
      // 预览面板
      showPreviewPanel: false,
      previewFileData: {},
      // 提示框
      showToast: false,
      toastType: '',
      toastMessage: '',
      toastTimeout: null
    }
  },
  computed: {
    // 是否可以上传
    canUpload() {
      return this.uploadForm.file && 
             this.uploadForm.title.trim() !== '' && 
             this.uploadForm.description.trim() !== '' && 
             this.uploadForm.chapterCount.trim() !== '' &&
             !this.uploading
    },
    // 过滤后的文件
    filteredFiles() {
      if (!this.searchQuery.trim()) {
        return this.fileData
      }
      
      const query = this.searchQuery.toLowerCase()
      return this.fileData.filter(file => 
        file.title.toLowerCase().includes(query) ||
        file.time.includes(query) ||
        file.chapter.includes(query) ||
        file.statusText.includes(query)
      )
    },
    // 分页计算
    totalPages() {
      return Math.ceil(this.filteredFiles.length / this.pageSize)
    },
    paginatedFiles() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredFiles.slice(start, end)
    },
    startIndex() {
      return (this.currentPage - 1) * this.pageSize
    },
    endIndex() {
      const end = this.startIndex + this.pageSize
      return Math.min(end, this.filteredFiles.length)
    },
    // 提示框样式
    toastClass() {
      switch(this.toastType) {
        case 'success': return 'toast-success'
        case 'warning': return 'toast-warning'
        case 'error': return 'toast-error'
        default: return ''
      }
    },
    toastIcon() {
      switch(this.toastType) {
        case 'success': return 'fa fa-check-circle text-green-500'
        case 'warning': return 'fa fa-exclamation-circle text-orange-500'
        case 'error': return 'fa fa-times-circle text-red-500'
        default: return ''
      }
    }
  },
  mounted() {
    this.checkLoginStatus()
  },
  methods: {
    // 侧边栏导航方法
    toggleSubmenu(submenu) {
      this.activeSubmenu = this.activeSubmenu === submenu ? null : submenu
    },

    goToPage(path) {
      this.$router.push(path)
    },

    goToTeacherDashboard() {
      this.$router.push('/teacher-dashboard')
    },

    
    goToFavorites(tab) {
      this.$router.push({
        path: '/favorites-management',
        query: { tab }
      })
    },

    goToPersonalCenter(page = 'user-info') {
      this.$router.push({ 
        path: '/personal-information',
        query: { page }
      })
    },

    goToVideoAnalysis(videoId) {
      this.$router.push({ 
        path: '/video-analysis',
        query: { videoId }
      })
    },

    goToWorkEngine() {
      this.$router.push('/work-engine')
    },
    
    goToCourseManagement() {
      this.$router.push('/course-management')
    },
    
    goToUserManagement() {
      this.$router.push('/user-management')
    },

    goToTeacherDashboard() {
    this.$router.push('/teacher-dashboard')
    },
    
    // 检查登录状态
    checkLoginStatus() {
      const user = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
      if (user) {
        this.currentUser = JSON.parse(user)
      }
    },
    
    // 跳转到视频上传/编辑页面
    goToVideoUpload(fileId) {
      // 跳转到视频上传页面，传递稿件ID
      this.$router.push({
        path: '/video-upload',
        query: { fileId: fileId }
      })
    },
    
    // 预览文件 - 打开预览面板
    previewFile(file) {
      this.previewFileData = file
      this.showPreviewPanel = true
    },
    
    closePreviewPanel() {
      this.showPreviewPanel = false
    },
    
    // 文件选择
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    
    handleFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        if (file.type !== 'image/png') {
          this.showToastMessage('error', '请上传PNG格式的图片文件')
          return
        }
        
        if (file.size > 25 * 1024 * 1024) {
          this.showToastMessage('error', '文件大小不能超过25MB')
          return
        }
        
        this.uploadForm.file = file
        this.uploadForm.imageFile = file
        
        const reader = new FileReader()
        reader.onload = (e) => {
          this.uploadForm.previewImage = e.target.result
        }
        reader.readAsDataURL(file)
      }
    },
    
    handleDrop(event) {
      this.dragover = false
      const file = event.dataTransfer.files[0]
      if (file) {
        const input = this.$refs.fileInput
        const dataTransfer = new DataTransfer()
        dataTransfer.items.add(file)
        input.files = dataTransfer.files
        this.handleFileSelect({ target: input })
      }
    },
    
    // 上传处理
    async handleUpload() {
      if (!this.canUpload) return
      
      this.uploading = true
      
      try {
        // 模拟上传延迟
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        // 创建新文件记录
        const newFile = {
          id: Date.now(),
          title: this.uploadForm.title,
          duration: '00:00',
          chapter: this.uploadForm.chapterCount + '章',
          size: '0 MB',
          time: new Date().toLocaleString('zh-CN', { 
            year: 'numeric', 
            month: '2-digit', 
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
          }),
          updateTime: new Date().toLocaleString('zh-CN', { 
            year: 'numeric', 
            month: '2-digit', 
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
          }),
          status: 'pending',
          statusText: '审核',
          desc: this.uploadForm.description
        }
        
        this.fileData.unshift(newFile)
        this.showToastMessage('success', '课程稿件已成功上传，等待审核')
        
        // 重置表单
        this.uploadForm = {
          file: null,
          previewImage: null,
          title: '',
          description: '',
          chapterCount: '',
          imageFile: null
        }
        
        if (this.$refs.fileInput) {
          this.$refs.fileInput.value = ''
        }
        
        // 重置到第一页
        this.currentPage = 1
      } catch (error) {
        this.showToastMessage('error', '上传失败，请重试')
      } finally {
        this.uploading = false
      }
    },
    
    // 搜索
    handleSearch() {
      this.currentPage = 1
      if (this.searchQuery.trim()) {
        this.showToastMessage('success', `找到${this.filteredFiles.length}条匹配稿件`)
      }
    },
    
    // 分页
    goToPage(page) {
      this.currentPage = page
    },
    
    // 状态徽章
    getStatusBadgeClass(status) {
      switch(status) {
        case 'published': return 'badge-published'
        case 'draft': return 'badge-draft'
        case 'pending': return 'badge-pending'
        case 'unpublished': return 'badge-unpublished'
        default: return ''
      }
    },
    
    // 状态面板样式
    getStatusPanelClass(status) {
      switch(status) {
        case 'published': return 'bg-green-100 text-green-700'
        case 'draft': return 'bg-gray-100 text-gray-700'
        case 'pending': return 'bg-orange-100 text-orange-700'
        case 'unpublished': return 'bg-red-100 text-red-700'
        default: return ''
      }
    },
    
    getStatusIcon(status) {
      switch(status) {
        case 'published': return 'fa fa-check'
        case 'draft': return 'fa fa-edit'
        case 'pending': return 'fa fa-clock-o'
        case 'unpublished': return 'fa fa-times'
        default: return ''
      }
    },
    
    getStatusPanelText(status) {
      switch(status) {
        case 'published': return '已发布'
        case 'draft': return '草稿'
        case 'pending': return '审核中'
        case 'unpublished': return '已下架'
        default: return ''
      }
    },
    
    // 文件操作
    downloadFile(file) {
      this.showToastMessage('success', '文件已开始下载，请稍后')
    },
    
    publishFile(file) {
      if (confirm('确认发布？发布后文件将对学员可见，是否继续？')) {
        const index = this.fileData.findIndex(f => f.id === file.id)
        if (index !== -1) {
          this.fileData[index].status = 'published'
          this.fileData[index].statusText = '已发'
          this.showToastMessage('success', '文件已成功发布')
        }
      }
    },
    
    cancelReview(file) {
      if (confirm('确认取消？取消后文件将回到草稿状态，是否继续？')) {
        const index = this.fileData.findIndex(f => f.id === file.id)
        if (index !== -1) {
          this.fileData[index].status = 'draft'
          this.fileData[index].statusText = '未发'
          this.showToastMessage('success', '已取消审核，文件回到草稿状态')
        }
      }
    },
    
    republishFile(file) {
      if (confirm('确认重新发布？重新发布后文件将再次对学员可见，是否继续？')) {
        const index = this.fileData.findIndex(f => f.id === file.id)
        if (index !== -1) {
          this.fileData[index].status = 'published'
          this.fileData[index].statusText = '已发'
          this.showToastMessage('success', '文件已成功重新发布')
        }
      }
    },
    
    deleteFile(file) {
      if (confirm('确认删除？删除后文件将无法恢复，是否继续？')) {
        const index = this.fileData.findIndex(f => f.id === file.id)
        if (index !== -1) {
          this.fileData.splice(index, 1)
          this.showToastMessage('success', '文件已成功删除')
          if (this.paginatedFiles.length === 0 && this.currentPage > 1) {
            this.currentPage = Math.max(1, this.currentPage - 1)
          }
        }
      }
    },
    
    // 提示框
    showToastMessage(type, message) {
      this.toastType = type
      this.toastMessage = message
      this.showToast = true
      
      if (this.toastTimeout) {
        clearTimeout(this.toastTimeout)
      }
      
      this.toastTimeout = setTimeout(() => {
        this.showToast = false
      }, 3000)
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

/* 链接样式 */
.text-link {
  @apply text-primary hover:text-primary/80 transition-colors duration-200 cursor-pointer;
}

/* 稿件管理样式 */
.btn-primary {
  @apply bg-primary hover:bg-primary/90 text-white font-medium py-2.5 rounded-md transition-all duration-200;
}
.btn-secondary {
  @apply bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2.5 rounded-md transition-all duration-200;
}
.input-field {
  @apply w-full px-4 py-2.5 rounded-md border border-gray-300 focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none transition-all duration-200;
}
.upload-area {
  @apply border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary/50 transition-all duration-200 cursor-pointer;
}
.upload-area.active {
  @apply border-primary bg-primary/5;
}
.upload-area.has-preview {
  @apply p-4;
}
.badge-published {
  @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800;
}
.badge-draft {
  @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800;
}
.badge-pending {
  @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800;
}
.badge-unpublished {
  @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800;
}
.toast {
  @apply fixed top-4 right-4 px-4 py-3 rounded-md shadow-lg flex items-center gap-2 z-50 transition-all duration-300 transform translate-y-[-100px] opacity-0;
}
.toast.show {
  @apply translate-y-0 opacity-100;
}
.toast-success {
  @apply bg-green-50 text-green-800 border border-green-200;
}
.toast-warning {
  @apply bg-orange-50 text-orange-800 border border-orange-200;
}
.toast-error {
  @apply bg-red-50 text-red-800 border border-red-200;
}
.page-btn {
  @apply cursor-pointer;
}

/* 新增样式 */
.cursor-pointer {
  cursor: pointer;
}

/* 悬停效果 */
.hover\:text-primary:hover {
  color: #165DFF;
}

.hover\:opacity-80:hover {
  opacity: 0.8;
}

/* 预览面板按钮样式 */
button[title="预览稿件详情"] {
  @apply text-sm font-medium;
}
</style>