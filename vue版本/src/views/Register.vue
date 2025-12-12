<template>
  <div class="min-h-screen flex flex-col">
    <header class="bg-white py-4 px-6 md:px-12 shadow-sm">
      <div class="container mx-auto flex justify-between items-center">
        <div class="flex items-center gap-2">
          <div class="bg-primary text-white p-1.5 rounded-md">
            <i class="fa fa-graduation-cap"></i>
          </div>
          <span class="text-lg font-semibold text-dark">BGarea</span>
        </div>
        <button @click="$router.push('/')" class="text-primary hover:text-primary/80 text-sm font-medium transition-colors duration-200 flex items-center gap-1">
          <i class="fa fa-home"></i> 返回首页
        </button>
      </div>
    </header>

    <main class="flex-grow flex items-center justify-center px-4 py-12 md:py-20">
      <div class="container mx-auto max-w-6xl grid md:grid-cols-2 gap-8 md:gap-12 items-center">
        <!-- 左侧图片区域 -->
        <div>
          <div class="relative rounded-lg overflow-hidden shadow-lg">
            <img src="https://picsum.photos/600/400?random=23" alt="学习场景" class="w-full h-auto object-cover rounded-lg">
            <div class="absolute bottom-4 left-4 right-4 bg-white/95 backdrop-blur-sm p-4 rounded-lg shadow-md max-w-xs">
              <h3 class="font-semibold text-dark mb-2">立即开始</h3>
              <p class="text-sm text-secondary mb-2">免费学习3500+精品课程</p>
              <ul class="text-sm space-y-1">
                <li class="flex items-center gap-1.5">
                  <i class="fa fa-star text-yellow-500 text-xs"></i>
                  <span>顶尖师资团队</span>
                </li>
                <li class="flex items-center gap-1.5">
                  <i class="fa fa-check-circle text-primary text-xs"></i>
                  <span>高质量在线课程</span>
                </li>
                <li class="flex items-center gap-1.5">
                  <i class="fa fa-road text-purple-500 text-xs"></i>
                  <span>个性化学习路径</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- 右侧注册表单 -->
        <div>
          <div class="bg-white rounded-xl p-6 md:p-8 card-shadow max-w-md mx-auto w-full">
            <div class="text-center mb-6">
              <h2 class="text-xl font-bold text-dark mb-1">创建新账户</h2>
              <p class="text-sm text-secondary">注册成为BGarea用户，享受优质教育资源</p>
            </div>

            <form @submit.prevent="handleRegister" class="space-y-4">
              <div>
                <label for="username" class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
                <input type="text" id="username" v-model="form.username"
                       :class="['input-field', errors.username ? 'input-error' : '']" 
                       placeholder="请设置用户名">
                <p class="text-xs text-gray-500 mt-1">2-20个字符，支持中文、数字和下划线</p>
                <p v-if="errors.username" class="text-xs text-red-500 mt-1">{{ errors.username }}</p>
              </div>

              <div>
                <label for="email" class="block text-sm font-medium text-gray-700 mb-1">邮箱地址</label>
                <input type="email" id="email" v-model="form.email"
                       :class="['input-field', errors.email ? 'input-error' : '']" 
                       placeholder="请输入邮箱地址">
                <p v-if="errors.email" class="text-xs text-red-500 mt-1">{{ errors.email }}</p>
              </div>

              <div>
                <label for="password" class="block text-sm font-medium text-gray-700 mb-1">设置密码</label>
                <div class="relative">
                  <input :type="showPassword ? 'text' : 'password'" id="password" v-model="form.password"
                         :class="['input-field pr-10', errors.password ? 'input-error' : '']" 
                         placeholder="请设置密码">
                  <button type="button" @click="showPassword = !showPassword" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600">
                    <i :class="showPassword ? 'fa fa-eye' : 'fa fa-eye-slash'"></i>
                  </button>
                </div>
                <p class="text-xs text-gray-500 mt-1">密码长度8-20位，包含字母和数字</p>
                <p v-if="errors.password" class="text-xs text-red-500 mt-1">{{ errors.password }}</p>
              </div>

              <div>
                <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">确认密码</label>
                <input type="password" id="confirmPassword" v-model="form.confirmPassword"
                       :class="['input-field', errors.confirmPassword ? 'input-error' : '']" 
                       placeholder="请再次输入密码">
                <p v-if="errors.confirmPassword" class="text-xs text-red-500 mt-1">{{ errors.confirmPassword }}</p>
              </div>

              <div class="flex items-start mt-2">
                <input type="checkbox" id="agreeTerms" v-model="form.agreeTerms" class="mt-1 h-4 w-4 rounded text-primary focus:ring-primary">
                <label for="agreeTerms" class="ml-2 text-sm text-secondary">
                  我已阅读并同意 <a href="#" class="text-link">服务条款</a> 和 <a href="#" class="text-link">隐私政策</a>
                </label>
                <p v-if="errors.agreeTerms" class="text-xs text-red-500 mt-1 ml-6">请同意服务条款和隐私政策</p>
              </div>

              <button type="submit" :disabled="loading" class="btn-primary mt-2">
                <span v-if="loading">
                  <i class="fa fa-spinner fa-spin mr-2"></i> 注册中...
                </span>
                <span v-else>注册账户</span>
              </button>
            </form>

            <div class="text-center mt-6 text-sm">
              <span class="text-secondary">已有账户? </span>
              <router-link to="/login" class="text-link font-medium">立即登录</router-link>
            </div>
          </div>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script>
import Footer from '@/components/Footer.vue'

export default {
  name: 'Register',
  components: {
    Footer
  },
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        agreeTerms: false
      },
      errors: {},
      loading: false,
      showPassword: false
    }
  },
  methods: {
    validateForm() {
      this.errors = {}
      
      // 验证用户名
      if (!this.form.username) {
        this.errors.username = '请输入用户名'
      } else if (this.form.username.length < 2 || this.form.username.length > 20) {
        this.errors.username = '用户名长度必须在2-20个字符之间'
      } else if (!/^[\u4e00-\u9fa5a-zA-Z0-9_]+$/.test(this.form.username)) {
        this.errors.username = '用户名只能包含中文、字母、数字和下划线'
      }
      
      // 验证邮箱
      if (!this.form.email) {
        this.errors.email = '请输入邮箱地址'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.form.email)) {
        this.errors.email = '请输入有效的电子邮件地址'
      }
      
      // 验证密码
      if (!this.form.password) {
        this.errors.password = '请设置密码'
      } else if (this.form.password.length < 8 || this.form.password.length > 20) {
        this.errors.password = '密码长度必须在8-20位之间'
      } else if (!/(?=.*[a-zA-Z])(?=.*\d)/.test(this.form.password)) {
        this.errors.password = '密码必须包含字母和数字'
      }
      
      // 验证确认密码
      if (!this.form.confirmPassword) {
        this.errors.confirmPassword = '请再次输入密码'
      } else if (this.form.confirmPassword !== this.form.password) {
        this.errors.confirmPassword = '两次输入的密码不一致'
      }
      
      // 验证服务条款
      if (!this.form.agreeTerms) {
        this.errors.agreeTerms = true
      }
      
      return Object.keys(this.errors).length === 0
    },
    
    async handleRegister() {
      if (!this.validateForm()) return
      
      this.loading = true
      
      try {
        // 模拟API请求
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        const users = JSON.parse(localStorage.getItem('bgareaUsers') || '[]')
        const userExists = users.some(u => u.email === this.form.email)
        
        if (userExists) {
          this.errors.email = '该邮箱已被注册'
          this.showToast('该邮箱已被注册，请使用其他邮箱', 'error')
        } else {
          // 注册成功 - 创建新用户对象
          const newUser = {
            id: Date.now().toString(),
            username: this.form.username,
            email: this.form.email,
            password: this.form.password, // 确保密码被存储
            realname: '',
            realnameStatus: '未认证',
            userId: Date.now().toString().slice(-8),
            phone: '',
            location: '',
            school: '',
            followers: 0,
            courses: 0,
            avatar: 'https://picsum.photos/200/200?random=1',
            bio: '',
            signature: '',
            isNewUser: true,
            hasPreferences: false,
            registerTime: new Date().toISOString()
          }
          
          // 保存用户到列表
          users.push(newUser)
          localStorage.setItem('bgareaUsers', JSON.stringify(users))
          
          // 自动登录
          if (true) { // 默认记住我
            localStorage.setItem('bgareaCurrentUser', JSON.stringify(newUser))
          } else {
            sessionStorage.setItem('bgareaCurrentUser', JSON.stringify(newUser))
          }
          
          // 发送登录状态变化事件
          window.dispatchEvent(new CustomEvent('user-auth-change'))

          // 清除之前的偏好设置记录，确保新用户需要设置偏好
          localStorage.removeItem('preferencesCompleted')
          localStorage.removeItem('preferencesSkipped')
          localStorage.removeItem('userPreferences')
          
          this.showToast('注册成功！请设置您的学习偏好。', 'success')
          
          // 跳转到偏好设置页面
          setTimeout(() => {
            this.$router.push('/preferences-setup')
          }, 1500)
        }
      } catch (error) {
        console.error('注册失败:', error)
        this.showToast('注册失败，请重试', 'error')
      } finally {
        this.loading = false
      }
    },
    
    showToast(message, type = 'success') {
      // 这里可以添加Toast组件逻辑
      alert(message)
    }
  },
  mounted() {
    // 如果用户已登录，直接跳转到相应页面
    const currentUser = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
    if (currentUser) {
      const preferencesCompleted = localStorage.getItem('preferencesCompleted') === 'true'
      const preferencesSkipped = localStorage.getItem('preferencesSkipped') === 'true'
      
      if (!preferencesCompleted && !preferencesSkipped) {
        this.$router.push('/preferences-setup')
      } else {
        this.$router.push('/')
      }
    }
  }
}
</script>