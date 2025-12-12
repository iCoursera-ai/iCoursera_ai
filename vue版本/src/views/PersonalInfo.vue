<template>
  <div class="font-inter bg-gray-50 min-h-screen flex flex-col">
    <Header />
    
    <div class="flex flex-1">
      <!-- 侧边栏导航 -->
      <aside class="w-64 bg-white border-r border-gray-200 flex-shrink-0 h-[calc(100vh-5rem)] sticky top-[5rem] overflow-y-auto z-30">
        <nav class="py-4 space-y-1">
          <!-- 教师管理 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" @click="goToTeacherDashboard">
              <div class="sidebar-parent-content">
                <i class="fa fa-tachometer sidebar-icon"></i>
                <span>教师管理</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200"></i>
            </div>
            <div id="submenu-dashboard" class="bg-gray-50" :class="{'hidden': activeSubmenu !== 'dashboard'}">
              <div class="sidebar-child">
                <i class="fa fa-circle-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">工作台</span>
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
            <div class="sidebar-parent active" @click="toggleSubmenu('user-center')">
              <div class="sidebar-parent-content">
                <i class="fa fa-user-circle-o sidebar-icon"></i>
                <span>个人中心</span>
              </div>
              <i class="fa fa-angle-right text-xs transition-transform duration-200" :class="{'rotate-icon': activeSubmenu === 'user-center'}"></i>
            </div>
            <div id="submenu-user-center" class="bg-gray-50" :class="{'hidden': activeSubmenu !== 'user-center'}">
              <div 
                class="sidebar-child" 
                :class="{ 'active': activePage === 'user-info' }"
                @click="switchPage('user-info')"
              >
                <i class="fa fa-id-card-o text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">用户信息</span>
              </div>
              <div 
                class="sidebar-child" 
                :class="{ 'active': activePage === 'user-settings' }"
                @click="switchPage('user-settings')"
              >
                <i class="fa fa-cog text-xs sidebar-icon"></i>
                <span class="sidebar-child-text">用户设置</span>
              </div>
            </div>
          </div>
        </nav>
      </aside>

      <!-- 主内容区域 -->
      <main class="flex-1 overflow-y-auto" style="max-height: calc(100vh - 5rem);">
        <div class="p-6">
          <!-- 面包屑导航 -->
          <div class="text-sm text-secondary mb-6">
            <span>用户中心</span>
            <i class="fa fa-angle-right mx-1 text-gray-400"></i>
            <span>个人中心</span>
            <i class="fa fa-angle-right mx-1 text-gray-400"></i>
            <span class="text-dark font-medium">{{ breadcrumbCurrent }}</span>
          </div>

          <!-- 页面内容容器 -->
          <div class="space-y-6">
            <!-- 用户信息页面 -->
            <div v-if="activePage === 'user-info'" class="space-y-6">
              <!-- 用户资料卡片 -->
              <div class="card p-6 card-shadow">
                <div class="flex flex-col md:flex-row items-center md:items-start gap-6">
                  <div class="relative">
                    <div class="w-24 h-24 rounded-full overflow-hidden border-4 border-white shadow-sm">
                      <img :src="userData.avatar" alt="用户头像" class="w-full h-full object-cover">
                    </div>
                  </div>
                  
                  <div class="text-center md:text-left flex-1">
                    <h2 class="text-2xl font-bold text-dark mb-2">{{ userData.realname }}</h2>
                    <div class="flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-secondary">
                      <div class="flex items-center gap-1">
                        <i class="fa fa-graduation-cap text-primary"></i>
                        <span>{{ userData.school }}</span>
                      </div>
                      <div class="flex items-center gap-1">
                        <i class="fa fa-map-marker text-primary"></i>
                        <span>{{ userData.location }}</span>
                      </div>
                      <div class="flex items-center gap-1">
                        <i class="fa fa-star text-yellow-500"></i>
                        <span>粉丝数: <span>{{ userData.followers }}</span></span>
                      </div>
                      <div class="flex items-center gap-1">
                        <i class="fa fa-book text-primary"></i>
                        <span>发布课程: <span>{{ userData.courses }}</span></span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 课程和关注区域 -->
              <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- 我的课程 -->
                <div class="lg:col-span-2 card p-6 card-shadow">
                  <div class="flex justify-between items-center mb-6">
                    <h3 class="text-lg font-semibold text-dark">我的课程</h3>
                    <button 
                      class="text-link text-sm hover:underline flex items-center gap-1"
                      @click="toggleExpandCourses"
                    >
                      {{ showAllCourses ? '收起' : '查看更多' }}
                      <i class="fa" :class="showAllCourses ? 'fa-angle-up' : 'fa-angle-down'"></i>
                    </button>
                  </div>
                  
                  <!-- 课程网格 -->
                  <div 
                    class="grid gap-4 transition-all duration-300"
                    :class="showAllCourses ? 'grid-cols-1 sm:grid-cols-2 md:grid-cols-3' : 'grid-cols-1 sm:grid-cols-2 md:grid-cols-3 max-h-[400px] overflow-hidden'"
                  >
                    <!-- 课程卡片 - 使用主页视频样式 -->
                    <div 
                      v-for="course in displayedCourses" 
                      :key="course.id"
                      class="bg-white rounded-lg overflow-hidden cursor-pointer hover:shadow-lg transition-all duration-300 group video-card"
                      @click="goToCourse(course)"
                    >
                      <!-- 视频封面 - 16:9比例 -->
                      <div class="relative" style="aspect-ratio: 16/9;">
                        <img 
                          :src="course.image" 
                          :alt="course.title" 
                          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        >
                        <!-- 播放按钮 -->
                        <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/20">
                          <div class="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                            <i class="fa fa-play text-white text-lg"></i>
                          </div>
                        </div>
                      </div>
                      <!-- 只显示课程名字 -->
                      <div class="p-3">
                        <h4 class="text-sm font-medium line-clamp-2 group-hover:text-primary transition-colors">
                          {{ course.title }}
                        </h4>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- 我的关注 -->
                <div class="card p-6 card-shadow">
                  <div class="flex justify-between items-center mb-6">
                    <h3 class="text-lg font-semibold text-dark">我的关注</h3>
                    <span class="text-sm text-secondary">{{ followedTeachers.length }}位老师</span>
                  </div>
                  
                  <div class="space-y-4">
                    <div 
                      v-for="teacher in followedTeachers" 
                      :key="teacher.id" 
                      class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                      @click="goToTeacherSpace(teacher)"
                    >
                      <div class="relative">
                        <img :src="teacher.avatar" :alt="teacher.name" class="w-10 h-10 rounded-full">
                        <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white"></div>
                      </div>
                      <div class="flex-1">
                        <div class="font-medium text-dark">{{ teacher.name }}</div>
                        <div class="text-xs text-secondary">{{ teacher.department }}</div>
                      </div>
                      <button 
                        class="text-xs px-2 py-1 rounded text-primary hover:bg-primary/10 transition-colors"
                        @click.stop="unfollowTeacher(teacher.id)"
                      >
                        取消关注
                      </button>
                    </div>
                    
                    <!-- 空状态 -->
                    <div v-if="followedTeachers.length === 0" class="text-center py-8 text-gray-500">
                      <i class="fa fa-user-friends text-3xl mb-3"></i>
                      <p class="text-sm">暂无关注的老师</p>
                      <p class="text-xs mt-1">去视频页面关注喜欢的老师吧</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 我的简介 -->
              <div class="card p-6 card-shadow">
                <h3 class="text-lg font-semibold text-dark mb-4">我的简介</h3>
                <div class="text-xl text-dark py-8 border-t border-b border-gray-200">
                  {{ userData.signature }}
                </div>
              </div>
            </div>
            
            <!-- 用户设置页面 -->
            <div v-if="activePage === 'user-settings'" class="space-y-6">
              <!-- 基本信息 -->
              <div class="card p-6 card-shadow">
                <div class="flex flex-col md:flex-row gap-8">
                  <div class="flex flex-col items-center md:items-start">
                    <div class="w-24 h-24 rounded-full overflow-hidden border-4 border-white shadow-sm mb-3">
                      <img :src="userData.avatar" alt="用户头像" class="w-full h-full object-cover">
                    </div>
                    <button class="btn-text text-sm flex items-center gap-1 px-4 py-2 rounded-md" @click="triggerAvatarUpload">
                      <i class="fa fa-upload"></i>
                      <span>更换头像</span>
                    </button>
                    <input type="file" ref="avatarInput" class="hidden" accept="image/*" @change="handleAvatarUpload">
                  </div>
                  
                  <div class="flex-1 grid grid-cols-1 md:grid-cols-3 gap-x-6 gap-y-4">
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">用户名</div>
                      <div class="flex items-center gap-2">
                        <span class="font-medium text-dark">{{ userData.username }}</span>
                        <button class="text-link text-sm hover:underline" @click="showEditModal('username')">修改</button>
                      </div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">实名认证</div>
                      <div class="flex items-center gap-2">
                        <span class="text-success font-medium">{{ userData.realnameStatus }}</span>
                        <button class="text-link text-sm hover:underline" @click="showEditModal('realname')">修改</button>
                      </div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">真实姓名</div>
                      <div class="flex items-center gap-2">
                        <span class="font-medium text-dark">{{ userData.realname }}</span>
                        <button class="text-link text-sm hover:underline" @click="showEditModal('realname')">修改</button>
                      </div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">账号ID</div>
                      <div class="font-medium text-dark">{{ userData.userId }}</div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">手机号码</div>
                      <div class="flex items-center gap-2">
                        <span class="font-medium text-dark">{{ userData.phone }}</span>
                        <button class="text-link text-sm hover:underline" @click="showEditModal('phone')">修改</button>
                      </div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">位置</div>
                      <div class="flex items-center gap-1">
                        <span class="font-medium text-dark">{{ userData.location }}</span>
                        <button class="text-link text-sm hover:underline" @click="showEditModal('location')">修改</button>
                      </div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">学校</div>
                      <div class="flex items-center gap-1">
                        <span class="font-medium text-dark">{{ userData.school }}</span>
                        <button class="text-link text-sm hover:underline" @click="showEditModal('school')">修改</button>
                      </div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">教师资格认证</div>
                      <div class="flex items-center gap-2">
                        <span :class="teacherCertStatusClass" class="font-medium">{{ teacherCertStatus }}</span>
                      </div>
                    </div>
                    
                    <div class="md:col-span-3">
                      <div class="text-sm font-medium text-gray-700 mb-1">我的简介</div>
                      <textarea v-model="userData.signature" class="input-field" rows="2" placeholder="请输入签名" @input="saveSignatureAuto"></textarea>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 安全设置、教师认证和偏好设置 -->
              <div class="card p-6 card-shadow">
                <!-- 标签切换 -->
                <div class="border-b border-gray-200 mb-6">
                  <div class="flex">
                    <button 
                      class="px-4 py-2 border-b-2 font-medium" 
                      :class="activeTab === 'security' ? 'text-primary border-primary' : 'text-secondary hover:text-primary'"
                      @click="activeTab = 'security'"
                    >
                      安全设置
                    </button>
                    <button 
                      class="px-4 py-2 border-b-2 font-medium" 
                      :class="activeTab === 'teacher' ? 'text-primary border-primary' : 'text-secondary hover:text-primary'"
                      @click="activeTab = 'teacher'"
                    >
                      教师认证
                    </button>
                    <button 
                      class="px-4 py-2 border-b-2 font-medium" 
                      :class="activeTab === 'preferences' ? 'text-primary border-primary' : 'text-secondary hover:text-primary'"
                      @click="activeTab = 'preferences'; loadPreferences()"
                    >
                      偏好设置
                    </button>
                  </div>
                </div>
                
                <!-- 安全设置内容 -->
                <div v-if="activeTab === 'security'" class="space-y-6">
                  <div class="flex justify-between items-center py-3 border-b border-gray-100">
                    <div>
                      <div class="font-medium text-dark mb-1">登录密码</div>
                      <div class="text-sm text-secondary">已设置。密码至少6位字符，支持数字、字母和除空格外的特殊字符，且必须同时包含数字和大小写字母。</div>
                    </div>
                    <button class="btn-text px-4 py-2 rounded-md" @click="showEditModal('password')">修改</button>
                  </div>
                  
                  <div class="flex justify-between items-center py-3 border-b border-gray-100">
                    <div>
                      <div class="font-medium text-dark mb-1">安全手机</div>
                      <div class="text-sm text-secondary">已绑定: <span>{{ maskedPhone }}</span></div>
                    </div>
                    <button class="btn-text px-4 py-2 rounded-md" @click="showEditModal('phone')">修改</button>
                  </div>
                  
                  <div class="flex justify-between items-center py-3">
                    <div>
                      <div class="font-medium text-dark mb-1">安全邮箱</div>
                      <div class="text-sm text-secondary">您暂未设置邮箱，绑定邮箱可以用来找回密码、接收通知等。</div>
                    </div>
                    <button class="btn-text px-4 py-2 rounded-md" @click="showEditModal('email')">设置</button>
                  </div>
                </div>
                
                <!-- 教师认证内容 -->
                <div v-if="activeTab === 'teacher'" class="space-y-8">
                  <div class="mb-8 relative">
                    <!-- 前往认证按钮 -->
                    <div class="absolute top-0 right-0">
                      <button class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90 transition-colors" @click="showCertificationModal">
                        <i class="fa fa-pencil mr-2"></i>前往认证
                      </button>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-dark mb-4">教师实名认证</h3>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">账号类型</div>
                        <div class="font-medium text-dark">{{ teacherCertInfo.accountType || '未填写' }}</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">认证状态</div>
                        <div :class="teacherCertStatusClass" class="font-medium">{{ teacherCertStatus }}</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">认证时间</div>
                        <div class="font-medium text-dark">{{ teacherCertInfo.certTime || '未认证' }}</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">教师姓名</div>
                        <div class="font-medium text-dark">{{ teacherCertInfo.teacherName || '未填写' }}</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">教师学位</div>
                        <div class="font-medium text-dark">{{ teacherCertInfo.teacherDegree || '未填写' }}</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">法人认证号码</div>
                        <div class="font-medium text-dark">{{ teacherCertInfo.legalPersonId || '未填写' }}</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">学校名称</div>
                        <div class="font-medium text-dark">{{ teacherCertInfo.schoolName || '未填写' }}</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">企业证件类型</div>
                        <div class="font-medium text-dark">{{ teacherCertInfo.certificateType || '未填写' }}</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">组织机构代码</div>
                        <div class="font-medium text-dark">{{ teacherCertInfo.organizationCode || '未填写' }}</div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- 偏好设置内容 -->
                <div v-if="activeTab === 'preferences'">
                  <div class="mb-6">
                    <div class="flex justify-between items-center mb-4">
                      <h3 class="text-lg font-semibold text-dark">学习偏好设置</h3>
                      <div class="text-sm text-secondary">
                        已选择 <span class="font-medium text-primary">{{ selectedPreferencesCount }}</span> 个偏好
                      </div>
                    </div>
                    <p class="text-sm text-secondary mb-6">根据您的偏好，我们将为您推荐更相关的内容</p>
                  </div>
                  
                  <div class="space-y-8">
                    <!-- 学习领域偏好 -->
                    <div class="space-y-4">
                      <div class="flex items-start justify-between">
                        <div>
                          <h3 class="font-semibold text-dark mb-1">您感兴趣的领域是？</h3>
                          <p class="text-sm text-gray-600">选择您最感兴趣的学习领域（可多选）</p>
                        </div>
                        <span class="text-xs bg-primary/10 text-primary px-2 py-1 rounded">必选</span>
                      </div>
                      <div class="flex flex-wrap gap-3">
                        <div 
                          v-for="field in preferencesOptions.field" 
                          :key="field.value"
                          class="preference-chip"
                          :class="{ 'selected': selectedPreferences.field.includes(field.value) }"
                          @click="togglePreference('field', field.value)"
                        >
                          <i :class="field.icon"></i> {{ field.label }}
                        </div>
                      </div>
                    </div>
                    
                    <!-- 学习目标偏好 -->
                    <div class="space-y-4">
                      <div class="flex items-start justify-between">
                        <div>
                          <h3 class="font-semibold text-dark mb-1">您的学习目标是？</h3>
                          <p class="text-sm text-gray-600">明确目标有助于推荐合适的课程</p>
                        </div>
                        <span class="text-xs bg-primary/10 text-primary px-2 py-1 rounded">必选</span>
                      </div>
                      <div class="flex flex-wrap gap-3">
                        <div 
                          v-for="goal in preferencesOptions.goal" 
                          :key="goal.value"
                          class="preference-chip"
                          :class="{ 'selected': selectedPreferences.goal.includes(goal.value) }"
                          @click="togglePreference('goal', goal.value)"
                        >
                          <i :class="goal.icon"></i> {{ goal.label }}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="mt-8 pt-6 border-t border-gray-200 flex justify-between items-center">
                    <div class="text-sm text-gray-600">
                      您可以随时修改这些偏好设置
                    </div>
                    <div class="flex gap-3">
                      <button 
                        @click="resetPreferences" 
                        class="px-5 py-2.5 text-gray-700 font-medium rounded-md border border-gray-300 hover:bg-gray-50 transition-all duration-200"
                      >
                        重置选择
                      </button>
                      <button 
                        @click="savePreferences" 
                        :disabled="!canSavePreferences"
                        class="px-5 py-2.5 bg-primary text-white font-medium rounded-md hover:bg-primary/90 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        保存偏好设置
                      </button>
                    </div>
                  </div>
                  
                  <!-- 当前偏好展示 -->
                  <div v-if="currentPreferencesDisplay" class="mt-6 p-4 bg-gray-50 rounded-lg">
                    <h4 class="font-medium text-dark mb-2">当前设置的学习偏好：</h4>
                    <div v-html="currentPreferencesDisplay"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- 修改信息模态框 -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="text-lg font-semibold">{{ modalTitle }}</h3>
          <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
            <i class="fa fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <input type="hidden" v-model="editField">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ modalLabel }}</label>
            <input 
              v-if="editField !== 'password'" 
              type="text" 
              v-model="modalInputValue" 
              class="input-field" 
              :placeholder="`请输入新的${modalLabel}`"
            >
            <div v-else class="mt-4 space-y-3">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">原密码</label>
                <input type="password" v-model="oldPassword" class="input-field">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">新密码</label>
                <input type="password" v-model="newPassword" class="input-field">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">确认新密码</label>
                <input type="password" v-model="confirmPassword" class="input-field">
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeModal" class="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50">取消</button>
          <button @click="saveEdit" class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90">保存</button>
        </div>
      </div>
    </div>

    <!-- 教师认证模态框 -->
    <div v-if="showCertModal" class="modal">
      <div class="modal-content max-w-2xl">
        <div class="modal-header">
          <h3 class="text-lg font-semibold">教师实名认证</h3>
          <button @click="closeCertModal" class="text-gray-500 hover:text-gray-700">
            <i class="fa fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">账号类型</label>
                <input type="text" v-model="certForm.accountType" class="input-field" placeholder="请输入账号类型">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">教师姓名</label>
                <input type="text" v-model="certForm.teacherName" class="input-field" placeholder="请输入教师姓名">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">教师学位</label>
                <input type="text" v-model="certForm.teacherDegree" class="input-field" placeholder="请输入教师学位">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">法人认证号码</label>
                <input type="text" v-model="certForm.legalPersonId" class="input-field" placeholder="请输入法人认证号码">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">学校名称</label>
                <input type="text" v-model="certForm.schoolName" class="input-field" placeholder="请输入学校名称">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">企业证件类型</label>
                <input type="text" v-model="certForm.certificateType" class="input-field" placeholder="请输入企业证件类型">
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">组织机构代码</label>
                <input type="text" v-model="certForm.organizationCode" class="input-field" placeholder="请输入组织机构代码">
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeCertModal" class="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50">取消</button>
          <button @click="submitCertification" class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90">确认认证</button>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'PersonalInformation',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      activeSubmenu: 'user-center',
      activePage: 'user-info',
      activeTab: 'security',
      showModal: false,
      showAllCourses: false,
      showCertModal: false,
      userData: {
        username: 'dsfuis',
        realname: '谷名',
        realnameStatus: '已认证',
        userId: '2489372598',
        phone: '13800138000',
        location: '北京',
        school: '北京理工大学',
        followers: 5000,
        courses: 20,
        avatar: 'https://picsum.photos/200/200?random=1',
        signature: '啊啊啊啊啊啊啊啊啊啊啊，摆烂摆烂',
        email: '',
        teacherCertStatus: '未认证'
      },
      // 教师认证信息
      teacherCertInfo: {
        accountType: '',
        certTime: '',
        teacherName: '',
        teacherDegree: '',
        legalPersonId: '',
        schoolName: '',
        certificateType: '',
        organizationCode: '',
        status: '未认证'
      },
      // 教师认证表单
      certForm: {
        accountType: '',
        teacherName: '',
        teacherDegree: '',
        legalPersonId: '',
        schoolName: '',
        certificateType: '',
        organizationCode: ''
      },
      // 我的课程数据 - 使用主页视频样式
      myCourses: [
        { 
          id: 1, 
          title: '操作系统', 
          image: 'https://picsum.photos/400/225?random=100',
          subject: '计算机基础'
        },
        { 
          id: 2, 
          title: '互联网原理与应用', 
          image: 'https://picsum.photos/400/225?random=101',
          subject: '网络技术'
        },
        { 
          id: 3, 
          title: '数据结构与算法', 
          image: 'https://picsum.photos/400/225?random=102',
          subject: '编程基础'
        },
        { 
          id: 4, 
          title: '数据库系统原理', 
          image: 'https://picsum.photos/400/225?random=103',
          subject: '数据管理'
        },
        { 
          id: 5, 
          title: '计算机网络', 
          image: 'https://picsum.photos/400/225?random=104',
          subject: '网络工程'
        },
        { 
          id: 6, 
          title: '软件工程', 
          image: 'https://picsum.photos/400/225?random=105',
          subject: '软件开发'
        },
        { 
          id: 7, 
          title: '人工智能基础', 
          image: 'https://picsum.photos/400/225?random=106',
          subject: '人工智能'
        },
        { 
          id: 8, 
          title: '机器学习入门', 
          image: 'https://picsum.photos/400/225?random=107',
          subject: '机器学习'
        },
        { 
          id: 9, 
          title: 'Web前端开发', 
          image: 'https://picsum.photos/400/225?random=108',
          subject: '前端技术'
        },
        { 
          id: 10, 
          title: '移动应用开发', 
          image: 'https://picsum.photos/400/225?random=109',
          subject: '移动开发'
        },
        { 
          id: 11, 
          title: '云计算基础', 
          image: 'https://picsum.photos/400/225?random=110',
          subject: '云计算'
        },
        { 
          id: 12, 
          title: '网络安全技术', 
          image: 'https://picsum.photos/400/225?random=111',
          subject: '网络安全'
        }
      ],
      // 我的关注老师 - 从localStorage加载
      followedTeachers: [],
      preferencesOptions: {
        field: [
          { value: 'programming', label: '编程开发', icon: 'fa fa-code mr-2' },
          { value: 'design', label: '设计艺术', icon: 'fa fa-paint-brush mr-2' },
          { value: 'business', label: '商业管理', icon: 'fa fa-line-chart mr-2' },
          { value: 'data-science', label: '数据科学', icon: 'fa fa-database mr-2' },
          { value: 'language', label: '语言学习', icon: 'fa fa-language mr-2' },
          { value: 'marketing', label: '市场营销', icon: 'fa fa-bullhorn mr-2' },
          { value: 'personal-growth', label: '个人成长', icon: 'fa fa-user-plus mr-2' },
          { value: 'academic', label: '学术教育', icon: 'fa fa-book mr-2' }
        ],
        goal: [
          { value: 'career', label: '职业发展', icon: 'fa fa-briefcase mr-2' },
          { value: 'skill-upgrade', label: '技能提升', icon: 'fa fa-wrench mr-2' },
          { value: 'exam', label: '考试认证', icon: 'fa fa-certificate mr-2' },
          { value: 'hobby', label: '兴趣爱好', icon: 'fa fa-heart mr-2' },
          { value: 'school', label: '学业辅助', icon: 'fa fa-graduation-cap mr-2' },
          { value: 'entrepreneurship', label: '创业指导', icon: 'fa fa-rocket mr-2' }
        ]
      },
      selectedPreferences: {
        field: [],
        goal: []
      },
      editField: '',
      modalTitle: '',
      modalLabel: '',
      modalInputValue: '',
      oldPassword: '',
      newPassword: '',
      confirmPassword: '',
      signatureSaveTimer: null
    }
  },
  computed: {
    breadcrumbCurrent() {
      return this.activePage === 'user-info' ? '用户信息' : '用户设置'
    },
    maskedPhone() {
      return this.userData.phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
    },
    selectedPreferencesCount() {
      return Object.values(this.selectedPreferences).reduce((total, arr) => total + arr.length, 0)
    },
    canSavePreferences() {
      return this.selectedPreferences.field.length > 0 && this.selectedPreferences.goal.length > 0
    },
    currentPreferencesDisplay() {
      const saved = localStorage.getItem('userPreferences')
      if (!saved) return ''
      
      try {
        const parsed = JSON.parse(saved)
        if (Object.keys(parsed).length === 0) return ''
        
        let html = '<div class="space-y-2">'
        
        // 领域偏好
        if (parsed.field && parsed.field.length > 0) {
          const fieldDisplay = parsed.field.map(f => {
            const field = this.preferencesOptions.field.find(opt => opt.value === f)
            return field ? field.label : f
          }).join('、')
          html += `<div><span class="font-medium">学习领域:</span> ${fieldDisplay}</div>`
        }
        
        // 目标偏好
        if (parsed.goal && parsed.goal.length > 0) {
          const goalDisplay = parsed.goal.map(g => {
            const goal = this.preferencesOptions.goal.find(opt => opt.value === g)
            return goal ? goal.label : g
          }).join('、')
          html += `<div><span class="font-medium">学习目标:</span> ${goalDisplay}</div>`
        }
        
        html += '</div>'
        return html
      } catch (e) {
        console.error('解析偏好设置失败:', e)
        return ''
      }
    },
    displayedCourses() {
      return this.showAllCourses ? this.myCourses : this.myCourses.slice(0, 6)
    },
    teacherCertStatus() {
      return this.teacherCertInfo.status === '已认证' ? '已认证' : '未认证'
    },
    teacherCertStatusClass() {
      return this.teacherCertInfo.status === '已认证' ? 'text-success' : 'text-danger'
    }
  },
  mounted() {
    this.loadUserData()
    this.loadPreferences()
    this.loadFollowedTeachers()
    this.loadTeacherCertInfo()
    
    // 监听关注更新事件
    window.addEventListener('storage', this.handleStorageEvent)
    // 监听自定义事件（同页面内更新）
    window.addEventListener('followUpdated', this.loadFollowedTeachers)
  },
  beforeUnmount() {
    window.removeEventListener('storage', this.handleStorageEvent)
    window.removeEventListener('followUpdated', this.loadFollowedTeachers)
  },
  methods: {
    toggleSubmenu(submenu) {
      this.activeSubmenu = this.activeSubmenu === submenu ? null : submenu
    },

    switchPage(page) {
      this.activePage = page
      this.activeSubmenu = 'user-center'
    },

    goToTeacherDashboard() {
      this.$router.push('/teacher-dashboard')
    },

    goToFavorites() {
      this.$router.push('/favorites-management')
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

    goToPage(path) {
      this.$router.push(path)
    },

    // 加载用户数据
    loadUserData() {
      const storedUserData = localStorage.getItem('bgareaUserData')
      const storedUser = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
      
      if (storedUserData) {
        this.userData = JSON.parse(storedUserData)
      } else if (storedUser) {
        const user = JSON.parse(storedUser)
        this.userData = {
          ...this.userData,
          username: user.username || this.userData.username,
          realname: user.realname || this.userData.realname,
          userId: user.userId || this.userData.userId,
          phone: user.phone || this.userData.phone,
          location: user.location || this.userData.location,
          school: user.school || this.userData.school,
          avatar: user.avatar || this.userData.avatar,
          teacherCertStatus: user.teacherCertStatus || this.userData.teacherCertStatus
        }
      }
    },
    
    // 加载教师认证信息
    loadTeacherCertInfo() {
      const storedCertInfo = localStorage.getItem('teacherCertificationInfo')
      if (storedCertInfo) {
        this.teacherCertInfo = JSON.parse(storedCertInfo)
      }
    },
    
    // 加载关注的老师
    loadFollowedTeachers() {
      const followed = localStorage.getItem('userFollowedTeachers')
      if (followed) {
        this.followedTeachers = JSON.parse(followed)
      } else {
        // 默认关注的老师
        this.followedTeachers = [
          { 
            id: 1, 
            name: '汪老师', 
            department: '计算机学院', 
            avatar: 'https://picsum.photos/48/48?random=30',
            userId: 'teacher_001'
          },
          { 
            id: 2, 
            name: '董老师', 
            department: '信息工程学院', 
            avatar: 'https://picsum.photos/48/48?random=31',
            userId: 'teacher_002'
          },
          { 
            id: 3, 
            name: '沈老师', 
            department: '软件学院', 
            avatar: 'https://picsum.photos/48/48?random=32',
            userId: 'teacher_003'
          },
          { 
            id: 4, 
            name: '何老师', 
            department: '数据科学系', 
            avatar: 'https://picsum.photos/48/48?random=33',
            userId: 'teacher_004'
          }
        ]
        localStorage.setItem('userFollowedTeachers', JSON.stringify(this.followedTeachers))
      }
    },
    
    // 处理storage事件，用于接收来自视频播放器的关注更新
    handleStorageEvent(event) {
      if (event.key === 'userFollowedTeachers') {
        this.loadFollowedTeachers()
      }
    },
    
    // 跳转到课程详情页
    goToCourse(course) {
      this.$router.push({
        name: 'VideoPlayer',
        params: { courseId: course.id }
      })
    },
    
    // 切换课程展开/收起
    toggleExpandCourses() {
      this.showAllCourses = !this.showAllCourses
    },
    
    // 跳转到老师空间
    goToTeacherSpace(teacher) {
      // 这里先实现跳转，但暂不做老师空间页面
      this.$router.push({
        path: '/teacher-space',
        query: { teacherId: teacher.userId, teacherName: teacher.name }
      })
    },
    
    // 取消关注老师
    unfollowTeacher(teacherId) {
      if (confirm('确定要取消关注这位老师吗？')) {
        this.followedTeachers = this.followedTeachers.filter(teacher => teacher.id !== teacherId)
        localStorage.setItem('userFollowedTeachers', JSON.stringify(this.followedTeachers))
        alert('已取消关注')
      }
    },
    
    showEditModal(field) {
      this.editField = field
      const fieldLabels = {
        'username': '用户名',
        'realname': '真实姓名',
        'phone': '手机号码',
        'location': '位置',
        'school': '学校',
        'password': '密码',
        'email': '邮箱'
      }
      
      this.modalLabel = fieldLabels[field] || field
      this.modalTitle = '修改' + this.modalLabel
      
      if (field !== 'password') {
        this.modalInputValue = this.userData[field] || ''
      } else {
        this.oldPassword = ''
        this.newPassword = ''
        this.confirmPassword = ''
      }
      
      this.showModal = true
    },
    
    closeModal() {
      this.showModal = false
      this.editField = ''
      this.modalInputValue = ''
      this.oldPassword = ''
      this.newPassword = ''
      this.confirmPassword = ''
    },
    
    saveEdit() {
      if (this.editField === 'password') {
        if (!this.oldPassword || !this.newPassword || !this.confirmPassword) {
          alert('请填写所有密码字段')
          return
        }

        if (this.newPassword !== this.confirmPassword) {
          alert('新密码与确认密码不一致')
          return
        }

        if (this.newPassword.length < 6) {
          alert('密码长度至少6位')
          return
        }

        // 验证原密码是否正确
        const currentUser = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
        if (currentUser) {
          const user = JSON.parse(currentUser)

          // 从用户列表中查找当前用户
          const users = JSON.parse(localStorage.getItem('bgareaUsers') || '[]')
          const userIndex = users.findIndex(u => u.email === user.email || u.userId === user.userId)

          if (userIndex > -1) {
            // 检查原密码是否匹配
            if (users[userIndex].password !== this.oldPassword) {
              // 如果没有密码字段，或者密码不匹配，检查是否从用户对象获取
              if (user.password && user.password !== this.oldPassword) {
                alert('原密码错误')
                return
              }
            }

            // 更新用户列表中的密码
            users[userIndex].password = this.newPassword

            // 更新当前登录用户的密码
            user.password = this.newPassword

            // 保存更新后的用户列表
            localStorage.setItem('bgareaUsers', JSON.stringify(users))

            // 保存更新后的当前用户
            if (localStorage.getItem('bgareaCurrentUser')) {
              localStorage.setItem('bgareaCurrentUser', JSON.stringify(user))
            } else {
              sessionStorage.setItem('bgareaCurrentUser', JSON.stringify(user))
            }

            alert('密码修改成功！下次登录请使用新密码。')
            this.closeModal()
            return
          }
        }

        // 如果没有找到用户，尝试其他方式
        alert('密码修改成功！')
        this.closeModal()
      } else {
        const value = this.modalInputValue.trim()
        if (!value) {
          alert('请输入有效值')
          return
        }

        if (this.editField === 'phone' && !/^1[3-9]\d{9}$/.test(value)) {
          alert('请输入有效的手机号码')
          return
        }

        // 更新用户数据
        this.userData[this.editField] = value

        // 更新本地存储中的用户数据
        localStorage.setItem('bgareaUserData', JSON.stringify(this.userData))

        // 同时更新用户列表中的对应字段
        const currentUser = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
        if (currentUser) {
          const user = JSON.parse(currentUser)
          const users = JSON.parse(localStorage.getItem('bgareaUsers') || '[]')
          const userIndex = users.findIndex(u => u.email === user.email || u.userId === user.userId)

          if (userIndex > -1) {
            // 更新用户列表中的对应字段
            users[userIndex][this.editField] = value

            // 如果是用户名，还需要更新其他引用
            if (this.editField === 'username') {
              users[userIndex].username = value
              user.username = value
            }

            // 保存更新后的用户列表
            localStorage.setItem('bgareaUsers', JSON.stringify(users))

            // 保存更新后的当前用户
            if (localStorage.getItem('bgareaCurrentUser')) {
              localStorage.setItem('bgareaCurrentUser', JSON.stringify(user))
            } else {
              sessionStorage.setItem('bgareaCurrentUser', JSON.stringify(user))
            }
          }
        }

        alert('修改成功！')
        this.closeModal()
      }
    },
    
    triggerAvatarUpload() {
      this.$refs.avatarInput.click()
    },
    
    handleAvatarUpload(event) {
      const file = event.target.files[0]
      if (!file) return
      
      if (!file.type.startsWith('image/')) {
        alert('请选择图片文件')
        return
      }
      
      const reader = new FileReader()
      reader.onload = (e) => {
        this.userData.avatar = e.target.result
        localStorage.setItem('bgareaUserData', JSON.stringify(this.userData))
        alert('头像上传成功！')
      }
      reader.readAsDataURL(file)
    },
    
    // 自动保存签名
    saveSignatureAuto() {
      // 清除之前的定时器
      if (this.signatureSaveTimer) {
        clearTimeout(this.signatureSaveTimer)
      }
      
      // 设置新的定时器，延迟1秒保存
      this.signatureSaveTimer = setTimeout(() => {
        localStorage.setItem('bgareaUserData', JSON.stringify(this.userData))
        console.log('签名已自动保存')
      }, 1000)
    },
    
    loadPreferences() {
      const saved = localStorage.getItem('userPreferences')
      if (saved) {
        try {
          const parsed = JSON.parse(saved)
          Object.keys(this.selectedPreferences).forEach(category => {
            this.selectedPreferences[category] = parsed[category] || []
          })
        } catch (e) {
          console.error('加载偏好设置失败:', e)
        }
      }
    },
    
    togglePreference(category, value) {
      const index = this.selectedPreferences[category].indexOf(value)
      if (index > -1) {
        this.selectedPreferences[category].splice(index, 1)
      } else {
        this.selectedPreferences[category].push(value)
      }
    },
    
    resetPreferences() {
      if (confirm('确定要重置所有偏好选择吗？')) {
        Object.keys(this.selectedPreferences).forEach(key => {
          this.selectedPreferences[key] = []
        })
      }
    },
    
    savePreferences() {
      // 收集所有选中的偏好
      const selectedPreferences = {}
      Object.keys(this.selectedPreferences).forEach(category => {
        if (this.selectedPreferences[category].length > 0) {
          selectedPreferences[category] = this.selectedPreferences[category]
        }
      })
      
      // 保存到localStorage
      localStorage.setItem('userPreferences', JSON.stringify(selectedPreferences))
      localStorage.setItem('preferencesCompleted', 'true')
      
      // 模拟保存过程
      setTimeout(() => {
        alert('偏好设置已保存！')
      }, 500)
    },
    
    // 显示教师认证模态框
    showCertificationModal() {
      // 如果已有认证信息，填充到表单
      if (this.teacherCertInfo.status === '已认证') {
        Object.keys(this.certForm).forEach(key => {
          if (this.teacherCertInfo[key]) {
            this.certForm[key] = this.teacherCertInfo[key]
          }
        })
      }
      this.showCertModal = true
    },
    
    // 关闭教师认证模态框
    closeCertModal() {
      this.showCertModal = false
      // 重置表单
      Object.keys(this.certForm).forEach(key => {
        this.certForm[key] = ''
      })
    },
    
    // 提交教师认证
    submitCertification() {
      // 验证必填字段
      const requiredFields = ['accountType', 'teacherName', 'teacherDegree', 'legalPersonId', 'schoolName', 'certificateType', 'organizationCode']
      const missingFields = requiredFields.filter(field => !this.certForm[field]?.trim())
      
      if (missingFields.length > 0) {
        alert('请填写所有认证信息')
        return
      }
      
      // 更新教师认证信息
      const currentDate = new Date()
      const formattedDate = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(currentDate.getDate()).padStart(2, '0')}`
      
      this.teacherCertInfo = {
        ...this.certForm,
        certTime: formattedDate,
        status: '审核中'
      }
      
      // 保存到本地存储
      localStorage.setItem('teacherCertificationInfo', JSON.stringify(this.teacherCertInfo))
      
      // 更新用户数据中的教师资格认证状态
      this.userData.teacherCertStatus = '审核中'
      localStorage.setItem('bgareaUserData', JSON.stringify(this.userData))
      
      alert('认证信息已提交，正在审核中...')
      this.closeCertModal()
      
      // 10秒后自动认证通过
      setTimeout(() => {
        this.teacherCertInfo.status = '已认证'
        this.userData.teacherCertStatus = '已认证'
        
        localStorage.setItem('teacherCertificationInfo', JSON.stringify(this.teacherCertInfo))
        localStorage.setItem('bgareaUserData', JSON.stringify(this.userData))
        
        alert('教师实名认证已通过！')
      }, 10000)
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

/* 偏好设置样式 */
.preference-chip {
  @apply px-4 py-2 rounded-full border border-gray-300 text-gray-700 bg-white hover:bg-gray-50 transition-all duration-200 cursor-pointer;
}
.preference-chip.selected {
  @apply bg-primary text-white border-primary;
}

/* 模态框样式 */
.modal {
  @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4;
}
.modal-content {
  @apply bg-white rounded-lg shadow-xl w-full max-w-md;
}
.modal-header {
  @apply flex justify-between items-center p-4 border-b;
}
.modal-body {
  @apply p-4;
}
.modal-footer {
  @apply p-4 border-t flex justify-end gap-3;
}

/* 视频卡片样式（与主页一致） */
.video-card {
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.video-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

/* 我的关注样式 */
.hover\:bg-gray-50:hover {
  background-color: #f9fafb;
}

/* 状态颜色 */
.text-success {
  color: #10b981;
}
.text-danger {
  color: #ef4444;
}
</style>