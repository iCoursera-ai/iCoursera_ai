<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-header">
          <div class="logo">
            <i class="fas fa-graduation-cap"></i>
            BGarea
          </div>
          <h1>创建账户</h1>
          <p>开始您的学习之旅</p>
        </div>
        
        <form class="auth-form" @submit.prevent="handleRegister">
          <div class="form-row">
            <div class="form-group">
              <label for="firstName">名字</label>
              <input 
                type="text" 
                id="firstName"
                v-model="form.firstName"
                class="form-control" 
                placeholder="名字" 
                required
              >
            </div>
            <div class="form-group">
              <label for="lastName">姓氏</label>
              <input 
                type="text" 
                id="lastName"
                v-model="form.lastName"
                class="form-control" 
                placeholder="姓氏" 
                required
              >
            </div>
          </div>
          
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
              placeholder="至少8个字符" 
              required
              @input="checkPasswordStrength"
            >
            <div class="password-strength">
              <div class="strength-bar" :style="{ width: passwordStrength + '%', background: passwordStrengthColor }"></div>
              <span class="strength-text">{{ passwordStrengthText }}</span>
            </div>
          </div>
          
          <div class="form-group">
            <label for="confirmPassword">确认密码</label>
            <input 
              type="password" 
              id="confirmPassword"
              v-model="form.confirmPassword"
              class="form-control" 
              placeholder="再次输入密码" 
              required
            >
          </div>
          
          <div class="form-group">
            <label class="checkbox">
              <input type="checkbox" v-model="form.agreeTerms" required>
              <span class="checkmark"></span>
              我同意 <a href="#">服务条款</a> 和 <a href="#">隐私政策</a>
            </label>
          </div>
          
          <div class="form-group">
            <label class="checkbox">
              <input type="checkbox" v-model="form.newsletter">
              <span class="checkmark"></span>
              我希望接收学习资源和优惠信息
            </label>
          </div>
          
          <button type="submit" class="btn btn-primary btn-auth" :disabled="loading">
            {{ loading ? '注册中...' : '创建账户' }}
          </button>
        </form>
        
        <div class="auth-divider">
          <span>或</span>
        </div>
        
        <div class="social-login">
          <button class="btn btn-social btn-google" @click="socialRegister('google')">
            <i class="fab fa-google"></i>
            使用 Google 注册
          </button>
          <button class="btn btn-social btn-wechat" @click="socialRegister('wechat')">
            <i class="fab fa-weixin"></i>
            使用微信注册
          </button>
        </div>
        
        <div class="auth-footer">
          <p>已有账户？ <router-link to="/login">立即登录</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Register',
  data() {
    return {
      form: {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '',
        agreeTerms: false,
        newsletter: true
      },
      loading: false,
      passwordStrength: 0,
      passwordStrengthColor: '#dc3545',
      passwordStrengthText: '密码强度：弱'
    }
  },
  methods: {
    ...mapActions(['register']),
    async handleRegister() {
      if (this.form.password !== this.form.confirmPassword) {
        this.$notify({
          type: 'error',
          title: '注册失败',
          message: '密码不匹配'
        })
        return
      }
      
      if (this.form.password.length < 8) {
        this.$notify({
          type: 'error',
          title: '注册失败',
          message: '密码长度至少8个字符'
        })
        return
      }
      
      if (!this.form.agreeTerms) {
        this.$notify({
          type: 'error',
          title: '注册失败',
          message: '请同意服务条款和隐私政策'
        })
        return
      }
      
      this.loading = true
      
      try {
        await this.register(this.form)
        this.$router.push('/profile')
        
        this.$notify({
          type: 'success',
          title: '注册成功',
          message: '欢迎加入 BGarea！'
        })
      } catch (error) {
        this.$notify({
          type: 'error',
          title: '注册失败',
          message: error.message
        })
      } finally {
        this.loading = false
      }
    },
    checkPasswordStrength() {
      const password = this.form.password
      let strength = 0
      
      if (password.length >= 8) strength += 25
      if (/[A-Z]/.test(password)) strength += 25
      if (/[0-9]/.test(password)) strength += 25
      if (/[^A-Za-z0-9]/.test(password)) strength += 25
      
      this.passwordStrength = strength
      
      if (strength < 50) {
        this.passwordStrengthColor = '#dc3545'
        this.passwordStrengthText = '密码强度：弱'
      } else if (strength < 75) {
        this.passwordStrengthColor = '#ffc107'
        this.passwordStrengthText = '密码强度：中'
      } else {
        this.passwordStrengthColor = '#28a745'
        this.passwordStrengthText = '密码强度：强'
      }
    },
    socialRegister(provider) {
      this.$notify({
        type: 'info',
        title: '第三方注册',
        message: `${provider} 注册功能将在完整版本中实现`
      })
    }
  }
}
</script>