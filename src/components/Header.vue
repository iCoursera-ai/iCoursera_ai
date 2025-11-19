<template>
  <header>
    <div class="container">
      <div class="navbar">
        <div class="logo" @click="$router.push('/')">
          <i class="fas fa-graduation-cap"></i>
          BGarea
        </div>
        <ul class="nav-links">
          <li><router-link to="/">首页</router-link></li>
          <li><router-link to="/courses">课程</router-link></li>
          <li><a href="#">专项课程</a></li>
          <li><a href="#">学位</a></li>
        </ul>
        <div class="user-actions">
          <button v-if="!isLoggedIn" class="btn btn-outline" @click="$router.push('/login')">登录</button>
          <button v-if="!isLoggedIn" class="btn btn-primary" @click="$router.push('/register')">注册</button>
          
          <button v-if="user?.role === 'admin'" class="btn btn-primary" @click="$router.push('/admin')">
            <i class="fas fa-user-shield"></i> 管理
          </button>
          
          <button v-if="isLoggedIn" class="btn btn-outline" @click="$router.push('/profile')">
            <i class="fas fa-user"></i> 个人中心
          </button>
          
          <button v-if="isLoggedIn" class="btn btn-outline" @click="logout">
            <i class="fas fa-sign-out-alt"></i> 退出
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'Header',
  computed: {
    ...mapState(['user', 'isLoggedIn'])
  },
  methods: {
    ...mapActions(['logout']),
    handleLogout() {
      if (confirm('确定要退出登录吗？')) {
        this.logout()
        this.$router.push('/')
      }
    }
  }
}
</script>