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

              <div class="text-center mt-6 text-sm">
                <span class="text-secondary">还没有账户? </span>
                <router-link to="/register" class="text-link font-medium">立即注册</router-link>
              </div>
            </form>
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
import { authService } from '@/service/auth'

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
        // 1. 调用真实API（不再是模拟）
        const response = await authService.login(
          this.form.email,
          this.form.password
        )
        
        if (response.data.code === 200) {

          localStorage.clear()
          sessionStorage.clear()
          // 2. 正确提取数据（针对你的数据结构）
          const data = response.data.data
          const token = data.token
          
          // 3. 构建 user 对象
          const user = {
            user_id: data.user_id,
            username: data.username,
            email: this.form.email,           // 后端没返回，用表单的
            favorite_domain: data.favorite_domain,
            login_time: data.login_time
          }
          
          // 4. 根据"记住我"选项保存
          if (this.form.rememberMe) {
            localStorage.setItem('token', token)
            localStorage.setItem('bgareaCurrentUser', JSON.stringify(user))
          } else {
            sessionStorage.setItem('token', token)
            sessionStorage.setItem('bgareaCurrentUser', JSON.stringify(user))
          }
          
          // 5. 发送登录事件
          window.dispatchEvent(new CustomEvent('user-auth-change'))
          
          // 6. 检查偏好设置状态
          const preferencesCompleted = localStorage.getItem('preferencesCompleted') === 'true'
          const preferencesSkipped = localStorage.getItem('preferencesSkipped') === 'true'
          
          this.showToast('登录成功！', 'success')
          
          // 7. 跳转
          if (!preferencesCompleted && !preferencesSkipped) {
            setTimeout(() => {
              this.$router.push('/preferences-setup')
            }, 1500)
          } else {
            setTimeout(() => {
              this.$router.push('/')
            }, 1500)
          }
          
        } else {
          this.errors.password = response.data.msg
          this.showToast(response.data.msg, 'error')
        }
        
      } catch (error) {
        console.error('登录失败:', error)
        this.showToast('登录失败，请重试', 'error')
      } finally {
        this.loading = false
      }
    },
    
    showToast(message, type = 'success') {
      // 这里可以添加Toast组件逻辑
      alert(message)
    },

     checkRegistrationSuccess() {
      if (this.$route.query.registered === 'true') {
        this.showToast('注册成功，请登录您的账户', 'success')
        
        // 可选：清除URL参数，防止刷新后重复显示
        this.$router.replace({ query: {} })
      }
    },
  
    // 检查自动跳转
    checkAutoRedirect() {
      try {
        const userStr = localStorage.getItem('bgareaCurrentUser') || 
                      sessionStorage.getItem('bgareaCurrentUser')
        
        if (userStr) {
          const user = JSON.parse(userStr)
          
          // 验证用户数据格式
          if (user && user.id) {
            console.log('用户已登录，自动跳转', user.username)
            
            // 检查偏好设置
            const prefCompleted = localStorage.getItem('preferencesCompleted') === 'true'
            const prefSkipped = localStorage.getItem('preferencesSkipped') === 'true'
            
            // 显示提示
            this.showToast(`欢迎回来，${user.username}！`, 'info')
            
            // 延迟跳转
            setTimeout(() => {
              if (!prefCompleted && !prefSkipped) {
                this.$router.push('/preferences-setup')
              } else {
                this.$router.push('/')
              }
            }, 1500)
          }
        }
      } catch (error) {
        console.warn('用户数据解析失败:', error)
        // 清除无效数据
        localStorage.removeItem('bgareaCurrentUser')
        sessionStorage.removeItem('bgareaCurrentUser')
      }
    }
  },
  mounted() {
    console.log('登录页面加载完成')
    
    // 1. 检查注册成功提示
    this.checkRegistrationSuccess()
    
    // 2. 检查是否已登录
    this.checkAutoRedirect()
  },

  
}
</script>