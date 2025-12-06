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
        <!-- 左侧表单区 -->
        <div>
          <div class="bg-white rounded-xl p-6 md:p-8 card-shadow max-w-md mx-auto w-full">
            <div class="text-center mb-6">
              <h2 class="text-xl font-bold text-dark mb-1">欢迎回来</h2>
              <p class="text-sm text-secondary">请登录您的账户</p>
            </div>

            <form @submit.prevent="handleLogin" class="space-y-4">
              <div>
                <label for="email" class="block text-sm font-medium text-gray-700 mb-1">电子邮件</label>
                <input type="email" id="email" v-model="form.email" 
                       :class="['input-field', errors.email ? 'input-error' : '']" 
                       placeholder="请输入您的电子邮件">
                <p v-if="errors.email" class="text-xs text-red-500 mt-1">{{ errors.email }}</p>
              </div>

              <div>
                <label for="password" class="block text-sm font-medium text-gray-700 mb-1">密码</label>
                <div class="relative">
                  <input :type="showPassword ? 'text' : 'password'" id="password" v-model="form.password"
                         :class="['input-field pr-10', errors.password ? 'input-error' : '']" 
                         placeholder="请输入您的密码">
                  <button type="button" @click="showPassword = !showPassword" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600">
                    <i :class="showPassword ? 'fa fa-eye' : 'fa fa-eye-slash'"></i>
                  </button>
                </div>
                <p v-if="errors.password" class="text-xs text-red-500 mt-1">{{ errors.password }}</p>
              </div>

              <div class="flex items-center justify-between text-sm">
                <label class="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" v-model="form.rememberMe" class="rounded text-primary focus:ring-primary h-4 w-4">
                  <span class="text-secondary">记住我</span>
                </label>
                <a href="#" class="text-link">忘记密码?</a>
              </div>

              <button type="submit" :disabled="loading" class="btn-primary">
                <span v-if="loading">
                  <i class="fa fa-spinner fa-spin mr-2"></i> 登录中...
                </span>
                <span v-else>登录账户</span>
              </button>

              <div class="relative flex items-center my-4">
                <div class="flex-grow border-t border-gray-200"></div>
                <span class="flex-shrink mx-4 text-gray-400 text-sm">或者</span>
                <div class="flex-grow border-t border-gray-200"></div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <button type="button" @click="handleThirdPartyLogin('google')" class="social-btn">
                  <i class="fa fa-google text-red-500"></i>
                  <span>使用Google登录</span>
                </button>
                <button type="button" @click="handleThirdPartyLogin('wechat')" class="social-btn">
                  <i class="fa fa-weixin text-green-500"></i>
                  <span>使用微信登录</span>
                </button>
              </div>
            </form>

            <div class="text-center mt-6 text-sm">
              <span class="text-secondary">还没有账户? </span>
              <router-link to="/register" class="text-link font-medium">立即注册</router-link>
            </div>
          </div>
        </div>

        <!-- 右侧图片区 -->
        <div>
          <div class="relative rounded-lg overflow-hidden shadow-lg">
            <img src="https://picsum.photos/600/400?random=22" alt="学习场景" class="w-full h-auto object-cover rounded-lg">
            <div class="absolute bottom-4 left-4 right-4 bg-white/95 backdrop-blur-sm p-4 rounded-lg shadow-md max-w-xs">
              <h3 class="font-semibold text-dark mb-2">加入BGarea</h3>
              <p class="text-sm text-secondary mb-2">探索5000+精品课程</p>
              <ul class="text-sm space-y-1">
                <li class="flex items-center gap-1.5">
                  <i class="fa fa-check text-green-500 text-xs"></i>
                  <span>免费学习优质课程</span>
                </li>
                <li class="flex items-center gap-1.5">
                  <i class="fa fa-check text-green-500 text-xs"></i>
                  <span>与名师实时互动</span>
                </li>
                <li class="flex items-center gap-1.5">
                  <i class="fa fa-check text-green-500 text-xs"></i>
                  <span>个性化学习体验</span>
                </li>
              </ul>
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
  name: 'Login',
  components: {
    Footer
  },
  data() {
    return {
      form: {
        email: '',
        password: '',
        rememberMe: false
      },
      errors: {},
      loading: false,
      showPassword: false
    }
  },
  methods: {
    validateForm() {
      this.errors = {}
      
      if (!this.form.email) {
        this.errors.email = '请输入电子邮件'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.form.email)) {
        this.errors.email = '请输入有效的电子邮件地址'
      }
      
      if (!this.form.password) {
        this.errors.password = '请输入密码'
      } else if (this.form.password.length < 8) {
        this.errors.password = '密码长度不能少于8位'
      }
      
      return Object.keys(this.errors).length === 0
    },
    
    async handleLogin() {
      if (!this.validateForm()) return
      
      this.loading = true
      
      try {
        // 模拟API请求
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        const users = JSON.parse(localStorage.getItem('bgareaUsers') || '[]')
        const user = users.find(u => u.email === this.form.email && u.password === this.form.password)
        
        if (user) {
          // 登录成功
          if (this.form.rememberMe) {
            localStorage.setItem('bgareaCurrentUser', JSON.stringify(user))
          } else {
            sessionStorage.setItem('bgareaCurrentUser', JSON.stringify(user))
          }
          
          // 显示成功提示
          this.showToast('登录成功！', 'success')

          // 检查用户偏好设置状态
          const preferencesCompleted = localStorage.getItem('preferencesCompleted') === 'true'
          const preferencesSkipped = localStorage.getItem('preferencesSkipped') === 'true'
          
          // 如果用户是新用户或没有偏好设置记录，则跳转到偏好设置页面
          if (!preferencesCompleted && !preferencesSkipped) {
            setTimeout(() => {
              this.$router.push('/preferences-setup')
            }, 1500)
          } else {
            // 否则跳转到首页
            setTimeout(() => {
              this.$router.push('/')
            }, 1500)
          }
        } else {
          this.errors.password = '邮箱或密码错误'
          this.showToast('邮箱或密码错误，请重试', 'error')
        }
      } catch (error) {
        console.error('登录失败:', error)
        this.showToast('登录失败，请重试', 'error')
      } finally {
        this.loading = false
      }
    },
    
    handleThirdPartyLogin(provider) {
      this.showToast(`${provider === 'google' ? 'Google' : '微信'}登录功能暂未开放`, 'error')
    },
    
    showToast(message, type = 'success') {
      // 这里可以添加Toast组件逻辑
      alert(message)
    }
  },
  mounted() {
    // 检查是否有注册成功的提示
    if (this.$route.query.registered === 'true') {
      this.showToast('注册成功，请登录您的账户', 'success')
    }
    
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