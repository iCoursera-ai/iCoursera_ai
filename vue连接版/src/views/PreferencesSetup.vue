<template>
  <div class="font-inter bg-gray-50 min-h-screen flex items-center justify-center p-4">
    <div class="max-w-4xl w-full">
      <!-- 主内容卡片 -->
      <div class="bg-white rounded-2xl card-shadow overflow-hidden">
        <!-- 头部 -->
        <div class="bg-gradient-to-r from-primary/10 to-blue-50 p-8 border-b">
          <div class="flex items-center gap-3 mb-4">
            <div class="bg-primary text-white p-2 rounded-md">
              <i class="fa fa-graduation-cap"></i>
            </div>
            <h1 class="text-2xl font-bold text-dark">BGarea</h1>
          </div>
          <h2 class="text-xl font-bold text-dark mb-2">定制您的学习体验</h2>
          <p class="text-gray-600">告诉我们您的偏好，我们将为您推荐更相关的内容</p>
        </div>
        
        <!-- 偏好选择区域 -->
        <div class="p-8 space-y-10">
          <!-- 学习领域偏好 -->
          <div class="space-y-4">
            <div class="flex items-start justify-between">
              <div>
                <h3 class="font-semibold text-lg text-dark">您感兴趣的领域是？</h3>
                <p class="text-sm text-gray-600 mt-1">选择您最感兴趣的学习领域（可多选）</p>
              </div>
              <span class="text-xs bg-primary/10 text-primary px-2 py-1 rounded">必选</span>
            </div>
            <div class="flex flex-wrap gap-3">
              <div 
                v-for="field in fields" 
                :key="field.value"
                class="preference-chip"
                :class="{ 'selected': userPreferences.field.includes(field.value) }"
                @click="togglePreference('field', field.value)"
              >
                <i :class="field.icon"></i>{{ field.label }}
              </div>
            </div>
          </div>
          
          <!-- 学习目标偏好 -->
          <div class="space-y-4">
            <div class="flex items-start justify-between">
              <div>
                <h3 class="font-semibold text-lg text-dark">您的学习目标是？</h3>
                <p class="text-sm text-gray-600 mt-1">明确目标有助于推荐合适的课程</p>
              </div>
              <span class="text-xs bg-primary/10 text-primary px-2 py-1 rounded">必选</span>
            </div>
            <div class="flex flex-wrap gap-3">
              <div 
                v-for="goal in goals" 
                :key="goal.value"
                class="preference-chip"
                :class="{ 'selected': userPreferences.goal.includes(goal.value) }"
                @click="togglePreference('goal', goal.value)"
              >
                <i :class="goal.icon"></i>{{ goal.label }}
              </div>
            </div>
          </div>
        </div>
        
        <!-- 底部操作栏 -->
        <div class="border-t bg-gray-50 p-8">
          <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
            <div class="text-sm text-gray-600">
              <i class="fa fa-info-circle mr-1"></i>
              已选择 <span class="font-medium text-primary">{{ selectedCount }}</span> 个偏好
            </div>
            <div class="flex gap-3 w-full sm:w-auto">
              <button 
                @click="handleSkip" 
                class="flex-1 sm:flex-none px-6 py-3 text-gray-700 font-medium rounded-md border border-gray-300 hover:bg-gray-50 transition-all duration-200"
              >
                跳过，稍后设置
              </button>
              <button 
                @click="handleSubmit" 
                :disabled="!canSubmit"
                class="flex-1 sm:flex-none px-6 py-3 bg-primary text-white font-medium rounded-md hover:bg-primary/90 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                :title="!canSubmit ? '请至少选择一个学习领域和学习目标' : ''"
              >
                完成设置，开始学习
              </button>
            </div>
          </div>
          <p class="text-xs text-gray-500 text-center mt-4">
            您可以随时在"账户设置"中修改这些偏好
          </p>
        </div>
      </div>
      
      <!-- 返回登录链接 -->
      <div class="text-center mt-6">
        <button 
          @click="goBack" 
          class="text-primary hover:text-primary/80 text-sm font-medium inline-flex items-center gap-1"
        >
          <i class="fa fa-arrow-left"></i> 返回登录页面
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  import { authService } from '@/service/auth'

  export default {
    name: 'PreferencesSetup',
    data() {
      return {
        userPreferences: {
          field: [],
          goal: []
        },
        fields: [
          { value: 'programming', label: '编程开发', icon: 'fa fa-code mr-2' },
          { value: 'ai', label: '人工智能', icon: 'fa fa-paint-brush mr-2' },
          { value: 'business', label: '商业管理', icon: 'fa fa-line-chart mr-2' },
          { value: 'data-science', label: '数据科学', icon: 'fa fa-database mr-2' },
          { value: 'language', label: '语言学习', icon: 'fa fa-language mr-2' },
          { value: 'marketing', label: '市场营销', icon: 'fa fa-bullhorn mr-2' },
          { value: 'Design-creativity', label: '设计创意', icon: 'fa fa-user-plus mr-2'},
          { value: 'academic', label: '学术教育', icon: 'fa fa-book mr-2' }
        ],
        goals: [
          { value: 'career-skill', label: '职业技能', icon: 'fa fa-briefcase mr-2' },
          { value: 'upgrade', label: '职场提升', icon: 'fa fa-wrench mr-2' },
          { value: 'exam', label: '考研考证', icon: 'fa fa-certificate mr-2' },
          { value: 'hobby', label: '生活兴趣', icon: 'fa fa-heart mr-2' },
          { value: 'teacher-growth', label: '教师成长', icon: 'fa fa-graduation-cap mr-2' },
          { value: 'entrepreneurship', label: '创业指导', icon: 'fa fa-rocket mr-2' },
          { value: 'student-zone', label: '学生专区', icon: 'fa fa-rocket mr-2' },
        ],
        loading: false
      }
    },
    computed: {
      selectedCount() {
        return Object.values(this.userPreferences).reduce((total, arr) => total + arr.length, 0)
      },
      canSubmit() {
        return this.userPreferences.field.length > 0 && this.userPreferences.goal.length > 0
      }
    },
    methods: {
      togglePreference(category, value) {
        const index = this.userPreferences[category].indexOf(value)
        if (index > -1) {
          this.userPreferences[category].splice(index, 1)
        } else {
          this.userPreferences[category].push(value)
        }
      },
      
      handleSkip() {
        if (confirm('跳过偏好设置？您可以在稍后的账户设置中重新设置。')) {
          // 存储空的偏好设置
          localStorage.setItem('userPreferences', JSON.stringify({}))
          localStorage.setItem('preferencesSkipped', 'true')
          localStorage.setItem('preferencesCompleted', 'false')
          
          // 跳转到首页
          this.$router.push('/')
        }
      },
      
      async handleSubmit() {
        this.loading = true
        try {
          // 1. 合并field和goal
          const allPreferences = [
            ...this.userPreferences.field,
            ...this.userPreferences.goal
          ]
          const favoriteDomain = allPreferences.join(',')
          console.log('favoriteDomain:', favoriteDomain)
          
          // 2. 获取用户信息
          const userStr = localStorage.getItem('bgareaCurrentUser')
          const user = userStr ? JSON.parse(userStr) : null
          console.log('用户信息:', user)
          console.log('user_id:', user?.user_id)
          
          if (user && user.user_id) {
            // 3. 调用API更新数据库
            const response = await authService.updateUserPreferences(
              user.user_id,
              favoriteDomain
            )
            console.log('API响应:', response)
            
            // 4. 更新本地用户信息
            user.favorite_domain = favoriteDomain
            localStorage.setItem('bgareaCurrentUser', JSON.stringify(user))
            
            // 5. 保存偏好标记
            localStorage.setItem('preferencesCompleted', 'true')
            
            // 6. 显示成功消息
            alert('偏好设置已保存！即将为您推荐个性化内容。')
            
            // 7. 跳转到首页
            console.log('跳转到首页')
            this.$router.push('/')
          } else {
            console.error('没有用户信息或user_id')
            alert('用户信息异常')
          }
          
        } catch (error) {
          console.error('保存失败:', error)
          alert('保存失败，请重试')
        } finally {
          this.loading = false
        }
      },
      
      goBack() {
        // 清除登录状态
        localStorage.removeItem('bgareaCurrentUser')
        sessionStorage.removeItem('bgareaCurrentUser')
        this.$router.push('/login')
      },
      
      // 检查是否已有偏好设置
      checkExistingPreferences() {
        const preferencesCompleted = localStorage.getItem('preferencesCompleted')
        const preferencesSkipped = localStorage.getItem('preferencesSkipped')
        
        // 如果用户已经完成或跳过了偏好设置，直接跳转到首页
        if (preferencesCompleted === 'true' || preferencesSkipped === 'true') {
          this.$router.push('/')
        }
      }
    },
    mounted() {
      this.checkExistingPreferences()
    }
  }
</script>

<style scoped>
.card-shadow {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.02);
}

.preference-chip {
  @apply px-4 py-2 rounded-full border border-gray-300 text-gray-700 bg-white hover:bg-gray-50 transition-all duration-200 cursor-pointer;
}
.preference-chip.selected {
  @apply bg-primary text-white border-primary;
}
</style>