<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-header">
          <div class="logo">
            <i class="fas fa-graduation-cap"></i>
            BGarea
          </div>
          <h1>欢迎回来</h1>
          <p>请登录您的账户</p>
        </div>
        
        <form class="auth-form" @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="email">电子邮件</label>
            <input 
              type="email" 
              id="email"
              v-model="form.email"
              class="form-control" 
              placeholder="请输入您的电子邮件" 
              required
            >
          </div>
          
          <div class="form-group">
            <label for="password">密码</label>
            <input 
              type="password" 
              id="password"
              v-model="form.password"
              class="form-control" 
              placeholder="请输入您的密码" 
              required
            >
          </div>
          
          <div class="form-options">
            <label class="checkbox">
              <input type="checkbox" v-model="form.remember">
              <span class="checkmark"></span>
              记住我
            </label>
            <router-link to="/forgot-password" class="forgot-password">忘记密码？</router-link>
          </div>
          
          <button type="submit" class="btn btn-primary btn-auth" :disabled="loading">
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>
        
        <div class="auth-divider">
          <span>或</span>
        </div>
        
        <div class="social-login">
          <button class="btn btn-social btn-google" @click="socialLogin('google')">
            <i class="fab fa-google"></i>
            使用 Google 登录
          </button>
          <button class="btn btn-social btn-wechat" @click="socialLogin('wechat')">
            <i class="fab fa-weixin"></i>
            使用微信登录
          </button>
        </div>
        
        <div class="auth-footer">
          <p>还没有账户？ <router-link to="/register">立即注册</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        email: '',
        password: '',
        remember: false
      },
      loading: false
    }
  },
  methods: {
    ...mapActions(['login']),
    async handleLogin() {
      this.loading = true
      
      try {
        const user = await this.login(this.form)
        
        if (user.role === 'admin') {
          this.$router.push('/admin')
        } else {
          this.$router.push('/profile')
        }
        
        this.$notify({
          type: 'success',
          title: '登录成功',
          message: `欢迎回来！您的身份是：${user.role === 'admin' ? '管理员' : '普通用户'}`
        })
      } catch (error) {
        this.$notify({
          type: 'error',
          title: '登录失败',
          message: error.message
        })
      } finally {
        this.loading = false
      }
    },
    socialLogin(provider) {
      this.$notify({
        type: 'info',
        title: '第三方登录',
        message: `${provider} 登录功能将在完整版本中实现`
      })
    }
  }
}
</script>