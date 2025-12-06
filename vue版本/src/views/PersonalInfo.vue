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
              <div class="sidebar-child active">
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
            <!-- 修改这部分代码 -->
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
                    <a href="#" class="text-link text-sm hover:underline">查看更多</a>
                  </div>
                  
                  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                    <!-- 课程卡片 -->
                    <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow bg-white" v-for="course in myCourses" :key="course.id">
                      <div class="text-dark font-medium mb-2">{{ course.title }}</div>
                      <div class="text-sm text-secondary mb-3">{{ course.subject }}</div>
                      <div class="flex -space-x-2">
                        <img v-for="student in course.students" :key="student" :src="student" alt="学员" class="w-7 h-7 rounded-full border border-white">
                        <div class="w-7 h-7 rounded-full bg-gray-100 border border-white flex items-center justify-center text-xs text-secondary">+{{ course.extraStudents }}</div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- 我的关注 -->
                <div class="card p-6 card-shadow">
                  <h3 class="text-lg font-semibold text-dark mb-6">我的关注</h3>
                  
                  <div class="space-y-4">
                    <div v-for="teacher in followedTeachers" :key="teacher.id" class="flex items-center gap-3">
                      <img :src="teacher.avatar" :alt="teacher.name" class="w-10 h-10 rounded-full">
                      <div class="flex-1">
                        <div class="font-medium text-dark">{{ teacher.name }}</div>
                        <div class="text-xs text-secondary">{{ teacher.department }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 我的签名 -->
              <div class="card p-6 card-shadow">
                <h3 class="text-lg font-semibold text-dark mb-4">我的签名</h3>
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
                      <div class="text-sm font-medium text-gray-700 mb-1">粉丝数</div>
                      <div class="font-medium text-dark">{{ userData.followers }}</div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">发布课程数</div>
                      <div class="font-medium text-dark">{{ userData.courses }}</div>
                    </div>
                    
                    <div class="md:col-span-3">
                      <div class="text-sm font-medium text-gray-700 mb-1">个人简介</div>
                      <textarea v-model="userData.bio" class="input-field" rows="3" placeholder="请输入个人简介"></textarea>
                      <button class="btn btn-primary mt-2 px-4 py-2 rounded-md" @click="saveBio">保存简介</button>
                    </div>
                    
                    <div class="md:col-span-3">
                      <div class="text-sm font-medium text-gray-700 mb-1">我的签名</div>
                      <textarea v-model="userData.signature" class="input-field" rows="2" placeholder="请输入签名"></textarea>
                      <button class="btn btn-primary mt-2 px-4 py-2 rounded-md" @click="saveSignature">保存签名</button>
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
                      <div class="font-medium text-dark mb-1">密保问题</div>
                      <div class="text-sm text-secondary">您暂未设置密保问题。密保问题可以有效的保护账号的安全。</div>
                    </div>
                    <button class="btn-text px-4 py-2 rounded-md" @click="showDevelopmentAlert">设置</button>
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
                  <div class="mb-8">
                    <h3 class="text-lg font-semibold text-dark mb-4">教师实名认证</h3>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">账号类型</div>
                        <div class="font-medium text-dark">企业账号</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">认证状态</div>
                        <div class="text-success font-medium">已认证</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">认证时间</div>
                        <div class="font-medium text-dark">2018-10-06</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">教师姓名</div>
                        <div class="font-medium text-dark">李机皮</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">教师学位</div>
                        <div class="font-medium text-dark">教授</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">法人认证号码</div>
                        <div class="font-medium text-dark">131****3246</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">学校名称</div>
                        <div class="font-medium text-dark">浙江工商大学</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">企业证件类型</div>
                        <div class="font-medium text-dark">企业营业执照</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">组织机构代码</div>
                        <div class="font-medium text-dark">5***9</div>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h3 class="text-lg font-semibold text-dark mb-4">记录</h3>
                    
                    <div class="overflow-x-auto">
                      <table class="w-full">
                        <thead>
                          <tr class="bg-gray-50 text-left text-sm text-secondary">
                            <th class="px-4 py-3 rounded-l-lg">课程UID</th>
                            <th class="px-4 py-3">审核课程</th>
                            <th class="px-4 py-3">当前状态</th>
                            <th class="px-4 py-3">创建时间</th>
                            <th class="px-4 py-3 rounded-r-lg">操作</th>
                          </tr>
                        </thead>
                        <tbody class="text-sm">
                          <tr class="border-b border-gray-100 bg-white" v-for="record in teacherRecords" :key="record.id">
                            <td class="px-4 py-3 text-dark">{{ record.id }}</td>
                            <td class="px-4 py-3 text-dark">{{ record.course }}</td>
                            <td class="px-4 py-3">
                              <span class="flex items-center gap-1">
                                <span class="w-2 h-2 rounded-full" :class="record.statusClass"></span>
                                <span>{{ record.status }}</span>
                              </span>
                            </td>
                            <td class="px-4 py-3 text-secondary">{{ record.createdAt }}</td>
                            <td class="px-4 py-3">
                              <div class="flex gap-3">
                                <a href="#" class="text-link hover:underline">查看</a>
                                <a v-if="record.status === '审核中'" href="#" class="text-link hover:underline">撤回</a>
                              </div>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    
                    <div class="flex justify-between items-center mt-4 text-sm">
                      <div class="text-secondary">共{{ teacherRecords.length }}条</div>
                      <div class="flex items-center gap-2">
                        <button class="w-8 h-8 flex items-center justify-center rounded border border-gray-200 text-secondary hover:border-primary hover:text-primary transition-colors">
                          <i class="fa fa-angle-left"></i>
                        </button>
                        <button class="w-8 h-8 flex items-center justify-center rounded bg-primary text-white">51</button>
                        <button class="w-8 h-8 flex items-center justify-center rounded border border-gray-200 text-secondary hover:border-primary hover:text-primary transition-colors">
                          <i class="fa fa-angle-right"></i>
                        </button>
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
                    
                    <!-- 学习方式偏好 -->
                    <div class="space-y-4">
                      <h3 class="font-semibold text-dark mb-1">您偏好的学习方式是？</h3>
                      <div class="flex flex-wrap gap-3">
                        <div 
                          v-for="method in preferencesOptions.method" 
                          :key="method.value"
                          class="preference-chip"
                          :class="{ 'selected': selectedPreferences.method.includes(method.value) }"
                          @click="togglePreference('method', method.value)"
                        >
                          <i :class="method.icon"></i> {{ method.label }}
                        </div>
                      </div>
                    </div>
                    
                    <!-- 学习时长偏好 -->
                    <div class="space-y-4">
                      <h3 class="font-semibold text-dark mb-1">您每周的学习时间是？</h3>
                      <div class="flex flex-wrap gap-3">
                        <div 
                          v-for="duration in preferencesOptions.duration" 
                          :key="duration.value"
                          class="preference-chip"
                          :class="{ 'selected': selectedPreferences.duration.includes(duration.value) }"
                          @click="togglePreference('duration', duration.value)"
                        >
                          {{ duration.label }}
                        </div>
                      </div>
                    </div>
                    
                    <!-- 难度级别偏好 -->
                    <div class="space-y-4">
                      <h3 class="font-semibold text-dark mb-1">您偏好的课程难度是？</h3>
                      <div class="flex flex-wrap gap-3">
                        <div 
                          v-for="difficulty in preferencesOptions.difficulty" 
                          :key="difficulty.value"
                          class="preference-chip"
                          :class="{ 'selected': selectedPreferences.difficulty.includes(difficulty.value) }"
                          @click="togglePreference('difficulty', difficulty.value)"
                        >
                          {{ difficulty.label }}
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

    <!-- 模态框 -->
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
        bio: '',
        signature: '啊啊啊啊啊啊啊啊啊啊啊，摆烂摆烂',
        email: ''
      },
      myCourses: [
        { id: 1, title: '操作系统', subject: 'Arco Design System', students: [
          'https://picsum.photos/32/32?random=10',
          'https://picsum.photos/32/32?random=11',
          'https://picsum.photos/32/32?random=12'
        ], extraStudents: 5 },
        { id: 2, title: '互联网', subject: 'Arco Design System', students: [
          'https://picsum.photos/32/32?random=13',
          'https://picsum.photos/32/32?random=14',
          'https://picsum.photos/32/32?random=15'
        ], extraStudents: 8 },
        { id: 3, title: '操作系统', subject: 'Arco Design System', students: [
          'https://picsum.photos/32/32?random=16',
          'https://picsum.photos/32/32?random=17',
          'https://picsum.photos/32/32?random=18'
        ], extraStudents: 3 },
        { id: 4, title: '操作系统', subject: 'Arco Design System', students: [
          'https://picsum.photos/32/32?random=19',
          'https://picsum.photos/32/32?random=20',
          'https://picsum.photos/32/32?random=21'
        ], extraStudents: 6 },
        { id: 5, title: '操作系统', subject: 'Arco Design System', students: [
          'https://picsum.photos/32/32?random=22',
          'https://picsum.photos/32/32?random=23',
          'https://picsum.photos/32/32?random=24'
        ], extraStudents: 7 },
        { id: 6, title: '操作系统', subject: 'Arco Design System', students: [
          'https://picsum.photos/32/32?random=25',
          'https://picsum.photos/32/32?random=26',
          'https://picsum.photos/32/32?random=27'
        ], extraStudents: 4 }
      ],
      followedTeachers: [
        { id: 1, name: '汪老师', department: '计算机学院', avatar: 'https://picsum.photos/48/48?random=30' },
        { id: 2, name: '董老师', department: '信息工程学院', avatar: 'https://picsum.photos/48/48?random=31' },
        { id: 3, name: '沈老师', department: '软件学院', avatar: 'https://picsum.photos/48/48?random=32' },
        { id: 4, name: '何老师', department: '数据科学系', avatar: 'https://picsum.photos/48/48?random=33' }
      ],
      teacherRecords: [
        { id: 232, course: '操作系统', status: '审核中', statusClass: 'bg-primary', createdAt: '2021-02-28 10:30' },
        { id: 254, course: '计算机网络', status: '已通过', statusClass: 'bg-success', createdAt: '2021-02-28 10:30' }
      ],
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
        ],
        method: [
          { value: 'video', label: '视频课程', icon: 'fa fa-video-camera mr-2' },
          { value: 'text', label: '图文教程', icon: 'fa fa-file-text mr-2' },
          { value: 'interactive', label: '互动练习', icon: 'fa fa-mouse-pointer mr-2' },
          { value: 'live', label: '直播授课', icon: 'fa fa-desktop mr-2' },
          { value: 'project', label: '项目实战', icon: 'fa fa-code-fork mr-2' },
          { value: 'one-on-one', label: '一对一辅导', icon: 'fa fa-users mr-2' }
        ],
        duration: [
          { value: '1-3', label: '1-3小时' },
          { value: '3-5', label: '3-5小时' },
          { value: '5-10', label: '5-10小时' },
          { value: '10-15', label: '10-15小时' },
          { value: '15+', label: '15小时以上' }
        ],
        difficulty: [
          { value: 'beginner', label: '初级入门' },
          { value: 'intermediate', label: '中级进阶' },
          { value: 'advanced', label: '高级精通' },
          { value: 'mixed', label: '混合难度' }
        ]
      },
      selectedPreferences: {
        field: [],
        goal: [],
        method: [],
        duration: [],
        difficulty: []
      },
      editField: '',
      modalTitle: '',
      modalLabel: '',
      modalInputValue: '',
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
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
        
        // 学习方式
        if (parsed.method && parsed.method.length > 0) {
          const methodDisplay = parsed.method.map(m => {
            const method = this.preferencesOptions.method.find(opt => opt.value === m)
            return method ? method.label : m
          }).join('、')
          html += `<div><span class="font-medium">学习方式:</span> ${methodDisplay}</div>`
        }
        
        // 学习时长
        if (parsed.duration && parsed.duration.length > 0) {
          const durationDisplay = parsed.duration.map(d => {
            const duration = this.preferencesOptions.duration.find(opt => opt.value === d)
            return duration ? duration.label : d
          }).join('、')
          html += `<div><span class="font-medium">学习时长:</span> ${durationDisplay}</div>`
        }
        
        // 难度级别
        if (parsed.difficulty && parsed.difficulty.length > 0) {
          const difficultyDisplay = parsed.difficulty.map(d => {
            const difficulty = this.preferencesOptions.difficulty.find(opt => opt.value === d)
            return difficulty ? difficulty.label : d
          }).join('、')
          html += `<div><span class="font-medium">课程难度:</span> ${difficultyDisplay}</div>`
        }
        
        html += '</div>'
        return html
      } catch (e) {
        console.error('解析偏好设置失败:', e)
        return ''
      }
    }
  },
  mounted() {
    this.loadUserData()
    this.loadPreferences()
  },
  methods: {
    toggleSubmenu(submenu) {
      this.activeSubmenu = this.activeSubmenu === submenu ? null : submenu
    },

    switchPage(page) {
    this.activePage = page
    // 确保子菜单是展开状态
    this.activeSubmenu = 'user-center'
    },

    showDevelopmentAlert() {
    alert('密保问题设置功能开发中');
    },

    showAlert(message) {
    alert(message);
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
          avatar: user.avatar || this.userData.avatar
        }
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
        
        // 更新本地存储
        localStorage.setItem('bgareaUserData', JSON.stringify(this.userData))
        
        // 更新当前登录信息中的用户名
        if (this.editField === 'username') {
          const storedUser = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
          if (storedUser) {
            const user = JSON.parse(storedUser)
            user.username = value
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
    
    saveBio() {
      localStorage.setItem('bgareaUserData', JSON.stringify(this.userData))
      alert('个人简介已保存！')
    },
    
    saveSignature() {
      localStorage.setItem('bgareaUserData', JSON.stringify(this.userData))
      alert('签名已保存！')
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
</style>