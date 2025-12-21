<template>
  <div class="font-inter bg-gray-50 min-h-screen flex flex-col">
    <Header />
    
    <div class="flex flex-1">
      <!-- 侧边栏导航 -->
      <aside class="w-64 bg-white border-r border-gray-200 flex-shrink-0 fixed top-[5rem] left-0 h-[calc(100vh-5rem)] overflow-y-auto z-30">
        <nav class="py-4 space-y-1 px-4">
          <!-- 工作台 - 只有教师认证用户才显示 -->
          <div v-if="isTeacherCertified" class="sidebar-group">
            <div class="sidebar-parent" :class="{ 'active': activePage === 'dashboard' }" @click="goToTeacherDashboard">
              <div class="sidebar-parent-content">
                <i class="fa fa-tachometer sidebar-icon"></i>
                <span>工作台</span>
              </div>
            </div>
          </div>
          
          <!-- 我的收藏 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" :class="{ 'active': activePage === 'favorites' }" @click="goToFavorites('collection')">
              <div class="sidebar-parent-content">
                <i class="fa fa-book sidebar-icon"></i>
                <span>我的收藏</span>
              </div>
            </div>
          </div>
          
          <!-- 点赞 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" :class="{ 'active': activePage === 'likes' }" @click="goToFavorites('likes')">
              <div class="sidebar-parent-content">
                <i class="fa fa-thumbs-up sidebar-icon"></i>
                <span>点赞</span>
              </div>
            </div>
          </div>
          
          <!-- 历史记录 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" :class="{ 'active': activePage === 'history' }" @click="goToFavorites('history')">
              <div class="sidebar-parent-content">
                <i class="fa fa-history sidebar-icon"></i>
                <span>历史记录</span>
              </div>
            </div>
          </div>
          
          <!-- 用户信息 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" :class="{ 'active': activePage === 'user-info' }" @click="switchPage('user-info')">
              <div class="sidebar-parent-content">
                <i class="fa fa-id-card-o sidebar-icon"></i>
                <span>用户信息</span>
              </div>
            </div>
          </div>
          
          <!-- 用户设置 -->
          <div class="sidebar-group">
            <div class="sidebar-parent" :class="{ 'active': activePage === 'user-settings' }" @click="switchPage('user-settings')">
              <div class="sidebar-parent-content">
                <i class="fa fa-cog sidebar-icon"></i>
                <span>用户设置</span>
              </div>
            </div>
          </div>
        </nav>
      </aside>

      <!-- 主内容区域 -->
      <main class="flex-1 overflow-y-auto p-6 ml-64" style="max-height: calc(100vh - 5rem);">
        <div class="p-6">
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
                    <h2 class="text-2xl font-bold text-dark mb-2">{{ userData.username }}</h2>
                    <!-- 显示真实姓名（如果已认证） -->
                    <div v-if="userData.realnameStatus === '已认证' && userData.realname" class="mb-3">
                      <span class="px-2 py-1 bg-primary/10 text-primary text-sm rounded">实名：{{ userData.realname }}</span>
                    </div>
                    <div class="flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-secondary">
                      <div class="flex items-center gap-1">
                        <i class="fa fa-graduation-cap text-primary"></i>
                        <span>{{ userData.school || '未设置' }}</span>
                      </div>
                      <div class="flex items-center gap-1">
                        <i class="fa fa-map-marker text-primary"></i>
                        <span>{{ userData.location || '未设置' }}</span>
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
                      v-if="myCourses.length > 6"
                      class="text-link text-sm hover:underline flex items-center gap-1"
                      @click="toggleExpandCourses"
                    >
                      {{ showAllCourses ? '收起' : '查看更多' }}
                      <i class="fa" :class="showAllCourses ? 'fa-angle-up' : 'fa-angle-down'"></i>
                    </button>
                  </div>
                  
                  <!-- 空状态 -->
                  <div v-if="myCourses.length === 0" class="text-center py-12 text-gray-500">
                    <i class="fa fa-book text-4xl mb-4"></i>
                    <p class="text-sm">暂无课程</p>
                    <p class="text-xs mt-1">开始学习或创建课程吧</p>
                  </div>

                  <!-- 课程网格 -->
                  <div
                    v-else
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
                        <div v-if="!teacher.avatar || teacher.avatar === '👤'" 
                             class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-purple-600 flex items-center justify-center text-white">
                          {{ getTeacherInitials(teacher.name) }}
                        </div>
                        <img v-else :src="teacher.avatar" :alt="teacher.name" class="w-10 h-10 rounded-full">
                        <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white"></div>
                      </div>
                      <div class="flex-1">
                        <div class="font-medium text-dark">{{ teacher.name }}</div>
                        <div class="text-xs text-secondary">{{ teacher.department || '未设置学院' }}</div>
                      </div>
                      <button 
                        class="text-xs px-2 py-1 rounded text-primary hover:bg-primary/10 transition-colors"
                        @click.stop="unfollowTeacher(teacher.userId)"
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
                  
                  <div class="flex-1 grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">用户名</div>
                      <div class="flex items-center gap-2">
                        <span class="font-medium text-dark">{{ userData.username }}</span>
                        <button class="text-link text-sm hover:underline" @click="showEditModal('username')">修改</button>
                      </div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">账号ID</div>
                      <div class="font-medium text-dark">{{ userData.userId }}</div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">实名认证</div>
                      <div class="flex items-center gap-2">
                        <span :class="realnameStatusClass">{{ userData.realnameStatus }}</span>
                        <button v-if="userData.realnameStatus === '未认证'" 
                                class="text-link text-sm hover:underline" 
                                @click="showRealnameCertModal">
                          去认证
                        </button>
                      </div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">真实姓名</div>
                      <div class="flex items-center gap-2">
                        <span class="font-medium text-dark">{{ userData.realname || '未认证' }}</span>
                        <!-- 已认证用户才能修改真实姓名 -->
                        <button v-if="userData.realnameStatus === '已认证'" 
                                class="text-link text-sm hover:underline" 
                                @click="showEditModal('realname')">
                          修改
                        </button>
                      </div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">手机号码</div>
                      <div class="flex items-center gap-2">
                        <span class="font-medium text-dark">{{ userData.phone || '未绑定' }}</span>
                        <!-- 手机号码通过安全设置绑定，这里不显示修改按钮 -->
                      </div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">位置</div>
                      <div class="flex items-center gap-1">
                        <span class="font-medium text-dark">{{ userData.location || '未设置' }}</span>
                        <button class="text-link text-sm hover:underline" @click="showEditModal('location')">修改</button>
                      </div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">学校</div>
                      <div class="flex items-center gap-1">
                        <span class="font-medium text-dark">{{ userData.school || '未设置' }}</span>
                        <button class="text-link text-sm hover:underline" @click="showEditModal('school')">修改</button>
                      </div>
                    </div>
                    
                    <div>
                      <div class="text-sm font-medium text-gray-700 mb-1">教师资格认证</div>
                      <div class="flex items-center gap-2">
                        <span :class="teacherCertStatusClass" class="font-medium">{{ userData.teacherCertStatus }}</span>
                        <button v-if="userData.teacherCertStatus === '未认证'" 
                                class="text-link text-sm hover:underline" 
                                @click="showCertificationModal">
                          去认证
                        </button>
                      </div>
                    </div>
                    
                    <div class="md:col-span-2">
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
                      <div class="text-sm text-secondary">
                        {{ userData.phone ? `已绑定: ${maskedPhone}` : '未绑定手机，绑定手机可以用来找回密码、接收通知等。' }}
                      </div>
                    </div>
                    <button class="btn-text px-4 py-2 rounded-md" @click="showPhoneBindingModal">绑定</button>
                  </div>
                  
                  <div class="flex justify-between items-center py-3">
                    <div>
                      <div class="font-medium text-dark mb-1">安全邮箱</div>
                      <div class="text-sm text-secondary">
                        {{ userData.email ? `已绑定: ${userData.email}` : '未设置邮箱，绑定邮箱可以用来找回密码、接收通知等。' }}
                      </div>
                    </div>
                    <button class="btn-text px-4 py-2 rounded-md" @click="showEditModal('email')">设置</button>
                  </div>
                </div>
                
                <!-- 教师认证内容 -->
                <div v-if="activeTab === 'teacher'" class="space-y-8">
                  <div class="mb-8 relative">
                    <!-- 前往认证按钮 -->
                    <div v-if="userData.teacherCertStatus === '未认证'" class="absolute top-0 right-0">
                      <button class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90 transition-colors" @click="showCertificationModal">
                        <i class="fa fa-pencil mr-2"></i>前往认证
                      </button>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-dark mb-4">教师实名认证</h3>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <!-- 认证状态显示 -->
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">认证状态</div>
                        <div :class="teacherCertStatusClass" class="font-medium">{{ userData.teacherCertStatus }}</div>
                      </div>
                      
                      <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="text-sm text-secondary mb-1">认证时间</div>
                        <div class="font-medium text-dark">{{ teacherCertInfo.certTime || '未认证' }}</div>
                      </div>
                      
                      <!-- 其他认证信息，认证后才显示 -->
                      <template v-if="userData.teacherCertStatus === '已认证' || userData.teacherCertStatus === '审核中'">
                        <div class="p-4 bg-gray-50 rounded-lg">
                          <div class="text-sm text-secondary mb-1">账号类型</div>
                          <div class="font-medium text-dark">{{ teacherCertInfo.accountType || '未填写' }}</div>
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
                      </template>
                    </div>
                    
                    <!-- 认证提示 -->
                    <div v-if="userData.teacherCertStatus === '未认证'" class="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                      <div class="flex items-start">
                        <i class="fa fa-info-circle text-blue-500 mt-1 mr-3"></i>
                        <div>
                          <h4 class="font-medium text-blue-800 mb-1">教师认证说明</h4>
                          <p class="text-sm text-blue-700">
                            通过教师认证后，您将获得以下权限：<br>
                            1. 发布和管理课程<br>
                            2. 获得教师工作台<br>
                            3. 创建和管理班级<br>
                            4. 获得官方认证标识
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- 实名认证模态框 -->
    <div v-if="showRealnameModal" class="modal">
      <div class="modal-content max-w-md">
        <div class="modal-header">
          <h3 class="text-lg font-semibold">实名认证</h3>
          <button @click="closeRealnameModal" class="text-gray-500 hover:text-gray-700">
            <i class="fa fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">真实姓名</label>
              <input type="text" v-model="realnameForm.name" class="input-field" placeholder="请输入您的真实姓名">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">身份证号码</label>
              <input type="text" v-model="realnameForm.idCard" class="input-field" placeholder="请输入您的身份证号码">
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeRealnameModal" class="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50">取消</button>
          <button @click="submitRealnameCert" class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90">提交认证</button>
        </div>
      </div>
    </div>

    <!-- 手机绑定模态框 -->
    <div v-if="showPhoneModal" class="modal">
      <div class="modal-content max-w-md">
        <div class="modal-header">
          <h3 class="text-lg font-semibold">{{ userData.phone ? '修改手机' : '绑定手机' }}</h3>
          <button @click="closePhoneModal" class="text-gray-500 hover:text-gray-700">
            <i class="fa fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">手机号码</label>
              <input type="text" v-model="phoneForm.phone" class="input-field" placeholder="请输入您的手机号码">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">验证码</label>
              <div class="flex gap-2">
                <input type="text" v-model="phoneForm.verificationCode" class="input-field flex-1" placeholder="请输入验证码">
                <button @click="sendVerificationCode" :disabled="codeSending" class="px-3 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 disabled:opacity-50">
                  {{ codeSending ? `${countdown}秒后重发` : '获取验证码' }}
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closePhoneModal" class="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50">取消</button>
          <button @click="submitPhoneBinding" class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90">确认{{ userData.phone ? '修改' : '绑定' }}</button>
        </div>
      </div>
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
import { isTestAccount, getTestAccountData } from '@/data/mockData.js'

export default {
  name: 'PersonalInformation',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      activePage: 'user-info', // 默认显示用户信息
      activeTab: 'security',
      showModal: false,
      showAllCourses: false,
      showCertModal: false,
      showRealnameModal: false,
      showPhoneModal: false,
      codeSending: false,
      countdown: 60,
      countdownTimer: null,
      
      // 用户数据从注册信息加载
      userData: {
        username: '',
        realname: '',
        realnameStatus: '未认证',
        userId: '',
        phone: '',
        location: '',
        school: '',
        followers: 0,
        courses: 0,
        avatar: 'https://picsum.photos/200/200?random=1',
        signature: '',
        email: '',
        teacherCertStatus: '未认证'
      },
      
      // 实名认证表单
      realnameForm: {
        name: '',
        idCard: ''
      },
      
      // 手机绑定表单
      phoneForm: {
        phone: '',
        verificationCode: ''
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
      
      // 我的课程数据 - 通过 loadCoursesData 方法加载
      myCourses: [],
      // 我的关注老师 - 从localStorage加载
      followedTeachers: [],
      
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
    isTeacherCertified() {
      return this.userData.teacherCertStatus === '已认证'
    },
    realnameStatusClass() {
      return this.userData.realnameStatus === '已认证' ? 'text-success font-medium' : 'text-danger font-medium'
    },
    teacherCertStatusClass() {
      return this.userData.teacherCertStatus === '已认证' ? 'text-success' : 
             this.userData.teacherCertStatus === '审核中' ? 'text-warning' : 'text-danger'
    },
    maskedPhone() {
      if (!this.userData.phone) return ''
      return this.userData.phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
    },
    displayedCourses() {
      return this.showAllCourses ? this.myCourses : this.myCourses.slice(0, 6)
    }
  },
  mounted() {
    // 检查URL参数，确定显示哪个页面
    const urlParams = new URLSearchParams(window.location.search)
    const page = urlParams.get('page')
    if (page && (page === 'user-info' || page === 'user-settings')) {
      this.activePage = page
    }

    this.loadUserData()
    this.loadCoursesData()
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
    // 获取老师姓名首字母
    getTeacherInitials(name) {
      if (!name) return '老'
      const chineseName = name.trim()
      if (chineseName.length >= 2) {
        return chineseName.substring(0, 2)
      }
      return chineseName || '老'
    },

    // 跳转到工作台
    goToTeacherDashboard() {
      this.$router.push('/teacher-dashboard')
    },

    // 跳转到收藏管理
    goToFavorites(tab) {
      this.$router.push({
        path: '/favorites-management',
        query: { tab }
      })
    },

    // 切换页面（用户信息/用户设置）
    switchPage(page) {
      this.activePage = page
      // 更新URL参数
      const url = new URL(window.location)
      url.searchParams.set('page', page)
      window.history.replaceState({}, '', url)
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
      // 确保老师信息完整
      const teacherInfo = {
        name: teacher.name,
        userId: teacher.userId,
        department: teacher.department || '未设置学院',
        avatar: teacher.avatar || '👤',
        description: teacher.description || `${teacher.name} - 老师`,
        fans: teacher.fans || '0'
      }
      
      console.log('跳转老师信息:', teacherInfo)
      
      // 保存到localStorage
      localStorage.setItem('currentTeacherInfo', JSON.stringify(teacherInfo))
      
      // 跳转到教师空间
      this.$router.push({
        path: '/teacher-space',
        query: {
          teacherId: teacher.userId,
          teacherName: teacher.name
        }
      })
    },
    
    // 取消关注老师
    unfollowTeacher(teacherUserId) {
      if (confirm('确定要取消关注这位老师吗？')) {
        const storedUser = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
        const userId = storedUser ? JSON.parse(storedUser).userId || JSON.parse(storedUser).email : 'default'
        
        // 使用用户特定的键名
        const userSpecificKey = `userFollowedTeachers_${userId}`
        const currentFollowed = JSON.parse(localStorage.getItem(userSpecificKey) || '[]')
        
        // 过滤掉要取消关注的老师
        const updatedTeachers = currentFollowed.filter(teacher => teacher.userId !== teacherUserId)
        
        // 保存更新后的列表
        localStorage.setItem(userSpecificKey, JSON.stringify(updatedTeachers))
        
        // 更新本地数据
        this.followedTeachers = updatedTeachers
        
        // 触发更新事件
        window.dispatchEvent(new StorageEvent('storage', {
          key: userSpecificKey,
          newValue: JSON.stringify(updatedTeachers)
        }))
        
        window.dispatchEvent(new CustomEvent('followUpdated'))
        
        alert('已取消关注')
      }
    },
    
    // 加载用户数据
    loadUserData() {
      const storedUser = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')

      if (storedUser) {
        const user = JSON.parse(storedUser)

        // 根据是否是测试账号设置粉丝数和课程数
        let followers = 0
        let courses = 0
        if (isTestAccount(user.email)) {
          followers = user.followers || 15200
          courses = user.courses || 20
        }

        this.userData = {
          username: user.username || '',
          realname: user.realname || '',
          realnameStatus: user.realnameStatus || '未认证',
          userId: user.userId || '',
          phone: user.phone || '',
          location: user.location || '',
          school: user.school || '',
          followers: followers,
          courses: courses,
          // 优先从 sessionStorage 获取头像，如果不存在则使用默认
          avatar: sessionStorage.getItem('userAvatar_' + user.userId) ||
                  user.avatar ||
                  'https://picsum.photos/200/200?random=1',
          signature: user.signature || '',
          email: user.email || '',
          teacherCertStatus: user.teacherCertStatus || '未认证'
        }

        // 保存到 userData（不包含大图片）
        const userDataToStore = { ...this.userData }
        // 移除 base64 头像数据
        delete userDataToStore.avatar
        localStorage.setItem('bgareaUserData', JSON.stringify(userDataToStore))
      }
    },

    // 加载课程数据
    loadCoursesData() {
      const storedUser = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
      if (storedUser) {
        const user = JSON.parse(storedUser)
        if (isTestAccount(user.email)) {
          const data = getTestAccountData()
          this.myCourses = data.courses.slice(0, 12).map(course => ({
            id: course.id,
            title: course.name,
            image: course.avatar,
            subject: course.tag
          }))
        } else {
          this.myCourses = []
        }
      }
    },
    
    // 加载关注的老师
    loadFollowedTeachers() {
      const storedUser = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
      const userId = storedUser ? JSON.parse(storedUser).userId || JSON.parse(storedUser).email : 'default'
      
      // 使用用户特定的键名
      const userSpecificKey = `userFollowedTeachers_${userId}`
      const followed = localStorage.getItem(userSpecificKey)

      if (followed) {
        this.followedTeachers = JSON.parse(followed)
        
        // 确保每个老师都有完整的字段
        this.followedTeachers = this.followedTeachers.map(teacher => ({
          id: teacher.id || Date.now(),
          userId: teacher.userId || `teacher_${teacher.name}_${Date.now()}`,
          name: teacher.name,
          department: teacher.department || '未设置学院',
          avatar: teacher.avatar || '👤',
          description: teacher.description || `${teacher.name} - 老师`,
          fans: teacher.fans || '0'
        }))
      } else {
        this.followedTeachers = []
      }
      
      console.log('加载的关注老师:', this.followedTeachers)
    },
    
    // 处理storage事件，用于接收来自视频播放器的关注更新
    handleStorageEvent(event) {
      if (event.key && event.key.startsWith('userFollowedTeachers_')) {
        this.loadFollowedTeachers()
      }
    },
    
    // 加载教师认证信息
    loadTeacherCertInfo() {
      const storedCertInfo = localStorage.getItem('teacherCertificationInfo')
      if (storedCertInfo) {
        this.teacherCertInfo = JSON.parse(storedCertInfo)
      }
    },
    
    // 显示实名认证模态框
    showRealnameCertModal() {
      this.showRealnameModal = true
    },
    
    // 关闭实名认证模态框
    closeRealnameModal() {
      this.showRealnameModal = false
      this.realnameForm.name = ''
      this.realnameForm.idCard = ''
    },
    
    // 提交实名认证
    submitRealnameCert() {
      if (!this.realnameForm.name.trim()) {
        alert('请输入真实姓名')
        return
      }
      
      if (!this.realnameForm.idCard.trim() || !/^\d{17}[\dXx]$/.test(this.realnameForm.idCard)) {
        alert('请输入有效的身份证号码')
        return
      }
      
      // 更新用户数据
      this.userData.realname = this.realnameForm.name
      this.userData.realnameStatus = '已认证'
      
      // 更新本地存储
      this.updateUserData()
      
      alert('实名认证提交成功！')
      this.closeRealnameModal()
    },
    
    // 显示手机绑定模态框
    showPhoneBindingModal() {
      this.phoneForm.phone = this.userData.phone || ''
      this.showPhoneModal = true
    },
    
    // 关闭手机绑定模态框
    closePhoneModal() {
      this.showPhoneModal = false
      this.phoneForm.phone = ''
      this.phoneForm.verificationCode = ''
    },
    
    // 发送验证码
    sendVerificationCode() {
      if (!this.phoneForm.phone || !/^1[3-9]\d{9}$/.test(this.phoneForm.phone)) {
        alert('请输入有效的手机号码')
        return
      }
      
      this.codeSending = true
      this.countdown = 60
      
      // 模拟发送验证码
      console.log(`发送验证码到: ${this.phoneForm.phone}`)
      
      this.countdownTimer = setInterval(() => {
        this.countdown--
        if (this.countdown <= 0) {
          clearInterval(this.countdownTimer)
          this.codeSending = false
        }
      }, 1000)
      
      alert('验证码已发送，请注意查收')
    },
    
    // 提交手机绑定
    submitPhoneBinding() {
      if (!this.phoneForm.phone || !/^1[3-9]\d{9}$/.test(this.phoneForm.phone)) {
        alert('请输入有效的手机号码')
        return
      }
      
      if (!this.phoneForm.verificationCode.trim()) {
        alert('请输入验证码')
        return
      }
      
      // 模拟验证码验证
      if (this.phoneForm.verificationCode !== '123456') {
        alert('验证码错误，请输入123456进行测试')
        return
      }
      
      // 更新用户数据
      this.userData.phone = this.phoneForm.phone
      
      // 更新本地存储
      this.updateUserData()
      
      alert(`手机号码${this.userData.phone ? '修改' : '绑定'}成功！`)
      this.closePhoneModal()
    },
    
    // 更新用户数据到本地存储
    updateUserData() {
      // 创建不包含大图片的副本
      const userDataToStore = { ...this.userData }

      // 检查是否是 base64 图片（如果是，则不存储到 localStorage）
      if (this.userData.avatar && this.userData.avatar.startsWith('data:image')) {
        // 这是 base64 图片，保存到 sessionStorage
        sessionStorage.setItem('userAvatar_' + this.userData.userId, this.userData.avatar)
        // 从要存储的数据中移除
        userDataToStore.avatar = 'custom_avatar' // 只存储一个标记
      }

      // 更新 bgareaUserData（不包含大图片）
      localStorage.setItem('bgareaUserData', JSON.stringify(userDataToStore))
      
      // 同时更新bgareaCurrentUser和bgareaUsers中的对应数据
      const storedUser = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
      if (storedUser) {
        const user = JSON.parse(storedUser)
        const users = JSON.parse(localStorage.getItem('bgareaUsers') || '[]')
        const userIndex = users.findIndex(u => u.userId === user.userId)
        
        if (userIndex > -1) {
          // 更新用户列表
          Object.keys(this.userData).forEach(key => {
            users[userIndex][key] = this.userData[key]
          })
          localStorage.setItem('bgareaUsers', JSON.stringify(users))
          
          // 更新当前用户
          Object.keys(this.userData).forEach(key => {
            user[key] = this.userData[key]
          })
          
          if (localStorage.getItem('bgareaCurrentUser')) {
            localStorage.setItem('bgareaCurrentUser', JSON.stringify(user))
          } else {
            sessionStorage.setItem('bgareaCurrentUser', JSON.stringify(user))
          }
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

        // 更新本地存储
        this.updateUserData()

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

      // 限制文件大小（例如最大 500KB）
      const maxSize = 1024 * 1024 // 500KB
      if (file.size > maxSize) {
        alert('头像图片不能超过 1MB')
        return
      }

      // 创建缩略图或压缩图片
      this.compressImage(file, (compressedDataUrl) => {
        this.userData.avatar = compressedDataUrl
        // 注意：这里不再存储完整图片到 localStorage
        // 只更新用户信息的引用
        this.updateUserDataWithAvatarRef(file.name)
        alert('头像上传成功！')
      })
    },

    // 压缩图片
    compressImage(file, callback) {
      const reader = new FileReader()
      reader.onload = (e) => {
        const img = new Image()
        img.onload = () => {
          const canvas = document.createElement('canvas')

          // 设置最大尺寸
          const maxWidth = 200
          const maxHeight = 200
          let width = img.width
          let height = img.height

          if (width > height) {
            if (width > maxWidth) {
              height *= maxWidth / width
              width = maxWidth
            }
          } else {
            if (height > maxHeight) {
              width *= maxHeight / height
              height = maxHeight
            }
          }

          canvas.width = width
          canvas.height = height

          const ctx = canvas.getContext('2d')
          ctx.drawImage(img, 0, 0, width, height)

          // 转换为较低质量的 base64
          const compressedDataUrl = canvas.toDataURL('image/jpeg', 0.7)
          callback(compressedDataUrl)
        }
        img.src = e.target.result
      }
      reader.readAsDataURL(file)
    },

    // 更新用户数据（不存储完整图片）
    updateUserDataWithAvatarRef(avatarFileName) {
      // 只存储头像引用信息，不存储完整的base64
      const userDataToStore = {
        ...this.userData,
        avatar: avatarFileName // 或使用一个引用标识
      }

      // 同时保存压缩后的图片到 sessionStorage（会话期间有效）
      sessionStorage.setItem('userAvatar_' + this.userData.userId, this.userData.avatar)

      // 更新主要用户数据（不包含大图片）
      localStorage.setItem('bgareaUserData', JSON.stringify(userDataToStore))

      // 更新当前用户信息
      const storedUser = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
      if (storedUser) {
        const user = JSON.parse(storedUser)
        const users = JSON.parse(localStorage.getItem('bgareaUsers') || '[]')
        const userIndex = users.findIndex(u => u.userId === user.userId)

        if (userIndex > -1) {
          // 更新用户列表（只存储引用）
          users[userIndex].avatar = avatarFileName
          localStorage.setItem('bgareaUsers', JSON.stringify(users))

          // 更新当前用户
          user.avatar = avatarFileName

          if (localStorage.getItem('bgareaCurrentUser')) {
            localStorage.setItem('bgareaCurrentUser', JSON.stringify(user))
          } else {
            sessionStorage.setItem('bgareaCurrentUser', JSON.stringify(user))
          }
        }
      }
    },
    
    // 自动保存签名
    saveSignatureAuto() {
      // 清除之前的定时器
      if (this.signatureSaveTimer) {
        clearTimeout(this.signatureSaveTimer)
      }
      
      // 设置新的定时器，延迟1秒保存
      this.signatureSaveTimer = setTimeout(() => {
        this.updateUserData()
        console.log('签名已自动保存')
      }, 1000)
    },
    
    // 显示教师认证模态框
    showCertificationModal() {
      // 如果已有认证信息，填充到表单
      if (this.teacherCertInfo.status === '已认证' || this.teacherCertInfo.status === '审核中') {
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
      this.updateUserData()
      
      alert('认证信息已提交，正在审核中...')
      this.closeCertModal()
      
      // 10秒后自动认证通过
      setTimeout(() => {
        this.teacherCertInfo.status = '已认证'
        this.userData.teacherCertStatus = '已认证'
        
        localStorage.setItem('teacherCertificationInfo', JSON.stringify(this.teacherCertInfo))
        this.updateUserData()
        
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
.text-warning {
  color: #f59e0b;
}
</style>