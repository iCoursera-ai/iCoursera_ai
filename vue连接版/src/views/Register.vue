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
import { authService } from '@/service/auth'

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
        const response = await authService.register(
          this.form.username,
          this.form.email,
          this.form.password
        )
        
        if (response.data.code === 200) {
          // 注册成功
          await this.handleRegisterSuccess(response.data.data)
        } else {
          // 注册失败
          await this.handleRegisterError(response.data)
        }
      } catch (error) {
        // 网络错误或其他异常
        await this.handleNetworkError(error)
      } finally {
        this.loading = false
      }
    },
    handleRegisterSuccess(userData) {
      localStorage.clear()
      sessionStorage.clear()

      if (userData.token) {
        localStorage.setItem('token', userData.token)
        localStorage.setItem('bgareaCurrentUser', JSON.stringify(userData.user))
      }
      window.dispatchEvent(new CustomEvent('user-auth-change'))
      this.showToast('注册成功！请设置学习偏好', 'success')
      // 3. 直接跳转到偏好设置页面
      setTimeout(() => {
        this.$router.push('/preferences-setup')
      }, 1000)
    },
    handleRegisterError(responseData) {
      const { code, msg } = responseData
      
      // 清空之前的错误
      this.errors = {}
      
      // 根据错误消息判断具体原因
      if (msg.includes('用户名已存在')) {
        this.errors.username = '用户名已存在'
        this.showToast('该用户名已被占用，请尝试其他用户名', 'error')
        
      } else if (msg.includes('邮箱已被注册')) {
        this.errors.email = '邮箱已被注册'
        this.showToast('该邮箱已被注册，请使用其他邮箱', 'error')
        
      } else if (msg.includes('邮箱格式不正确')) {
        this.errors.email = '邮箱格式不正确'
        this.showToast('请输入有效的邮箱地址（如：user@example.com）', 'error')
        
      } else if (msg.includes('密码强度不足')) {
        this.errors.password = '密码强度不足'
        // 显示具体的密码要求
        const passwordMsg = msg.replace('密码强度不足:', '').trim()
        this.showToast(`密码要求：${passwordMsg || '需包含字母和数字，长度8-20位'}`, 'error')
        
      } else if (msg.includes('不能为空')) {
        // 判断是哪个字段为空
        if (msg.includes('用户名') && !this.form.username) {
          this.errors.username = '用户名不能为空'
        }
        if (msg.includes('邮箱') && !this.form.email) {
          this.errors.email = '邮箱不能为空'
        }
        if (msg.includes('密码') && !this.form.password) {
          this.errors.password = '密码不能为空'
        }
        this.showToast('请填写所有必填项', 'error')
        
      } else if (msg.includes('注册失败:')) {
        // 数据库错误或其他服务器错误
        this.errors.submit = '服务器错误'
        this.showToast('注册失败，请稍后重试', 'error')
        console.error('服务器错误详情:', msg)
        
      } else {
        // 其他未知错误
        this.errors.submit = msg
        this.showToast(msg || '注册失败', 'error')
      }
      
      // 如果有错误，自动聚焦到第一个错误字段
      this.focusFirstErrorField()
    },
    // 聚焦到第一个错误字段
    focusFirstErrorField() {
      this.$nextTick(() => {
        if (this.errors.username && this.$refs.usernameInput) {
          this.$refs.usernameInput.focus()
        } else if (this.errors.email && this.$refs.emailInput) {
          this.$refs.emailInput.focus()
        } else if (this.errors.password && this.$refs.passwordInput) {
          this.$refs.passwordInput.focus()
        }
      })
    },
    // 处理网络错误
    handleNetworkError(error) {
      console.error('网络错误:', error)
      
      if (error.response) {
        // 服务器响应了错误
        const { status, data } = error.response
        
        switch (status) {
          case 429:
            this.showToast('请求过于频繁，请稍后再试', 'error')
            break
          case 503:
            this.showToast('服务器维护中，请稍后再试', 'error')
            break
          default:
            this.showToast(`服务器错误 (${status})，请稍后重试`, 'error')
        }
      } else if (error.request) {
        // 请求发送了但没有响应
        this.showToast('网络连接失败，请检查网络后重试', 'error')
      } else {
        // 其他错误
        this.showToast('注册失败，请重试', 'error')
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
        console.log('push/')
        this.$router.push('/')
      }
    }
  }
}
</script>