<template>
  <div 
    class="teacher-card"
    :class="{ 'cursor-pointer': clickable }"
    @click="handleClick"
  >
    <!-- 头像区域 -->
    <div class="teacher-avatar-container relative group">
      <img 
        :src="teacher.avatar" 
        :alt="teacher.name"
        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
      >
      <!-- 遮罩层 -->
      <div class="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-all duration-300 flex items-center justify-center">
        <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          <div class="flex gap-2">
            <button @click.stop="viewProfile" class="w-8 h-8 rounded-full bg-white/80 flex items-center justify-center hover:bg-white">
              <i class="fa fa-user text-gray-700 text-sm"></i>
            </button>
            <button @click.stop="sendMessage" class="w-8 h-8 rounded-full bg-white/80 flex items-center justify-center hover:bg-white">
              <i class="fa fa-envelope text-gray-700 text-sm"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 教师信息 -->
    <div class="mt-3 text-center">
      <h4 class="text-base font-medium text-dark">{{ teacher.name }}</h4>
      <p class="text-sm text-gray-500 mt-1">{{ teacher.university }}</p>
      <p class="text-base text-primary mt-0.5 font-medium">{{ teacher.major }}</p>
      
      <!-- 标签 -->
      <div v-if="teacher.tags && teacher.tags.length > 0" class="flex flex-wrap justify-center gap-1 mt-2">
        <span 
          v-for="tag in teacher.tags" 
          :key="tag"
          class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full"
        >
          {{ tag }}
        </span>
      </div>
      
      <!-- 评分和课程数 -->
      <div v-if="teacher.rating || teacher.courseCount" class="flex items-center justify-center gap-3 mt-2">
        <div v-if="teacher.rating" class="flex items-center gap-1">
          <div class="flex text-yellow-400">
            <i v-for="i in 5" :key="i" class="fa fa-star text-xs"></i>
          </div>
          <span class="text-xs text-gray-600">{{ teacher.rating }}</span>
        </div>
        
        <div v-if="teacher.courseCount" class="flex items-center gap-1 text-gray-600">
          <i class="fa fa-video-camera text-xs"></i>
          <span class="text-xs">{{ teacher.courseCount }}门课程</span>
        </div>
      </div>
      
      <!-- 简介 -->
      <p v-if="teacher.bio && teacher.bio.length > 0" class="text-xs text-gray-500 mt-2 line-clamp-2">
        {{ teacher.bio }}
      </p>
      
      <!-- 关注按钮 -->
      <button 
        v-if="showFollowButton"
        @click.stop="toggleFollow"
        :class="[
          'mt-3 px-4 py-1.5 text-sm rounded-full transition-all duration-200',
          isFollowing 
            ? 'bg-primary/10 text-primary border border-primary/20 hover:bg-primary/20' 
            : 'bg-primary text-white hover:bg-primary/90'
        ]"
      >
        <i v-if="isFollowing" class="fa fa-check mr-1"></i>
        {{ isFollowing ? '已关注' : '关注' }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TeacherCard',
  props: {
    teacher: {
      type: Object,
      required: true,
      default: () => ({
        id: null,
        name: '',
        avatar: '',
        university: '',
        major: '',
        tags: [],
        rating: 0,
        courseCount: 0,
        bio: ''
      })
    },
    showFollowButton: {
      type: Boolean,
      default: true
    },
    clickable: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      isFollowing: false
    }
  },
  methods: {
    handleClick() {
      if (this.clickable) {
        this.$emit('click', this.teacher)
        this.$router.push(`/teacher/${this.teacher.id}`)
      }
    },
    
    viewProfile() {
      this.$emit('view-profile', this.teacher)
      this.$router.push(`/teacher/${this.teacher.id}`)
    },
    
    sendMessage() {
      this.$emit('send-message', this.teacher)
      // 这里可以跳转到消息页面或显示消息对话框
    },
    
    toggleFollow() {
      this.isFollowing = !this.isFollowing
      
      // 更新本地存储
      let following = JSON.parse(localStorage.getItem('bgareaFollowing') || '[]')
      
      if (this.isFollowing) {
        if (!following.some(item => item.id === this.teacher.id)) {
          following.push({
            id: this.teacher.id,
            name: this.teacher.name,
            avatar: this.teacher.avatar,
            followTime: new Date().getTime()
          })
        }
      } else {
        following = following.filter(item => item.id !== this.teacher.id)
      }
      
      localStorage.setItem('bgareaFollowing', JSON.stringify(following))
      this.$emit('follow-change', { teacher: this.teacher, isFollowing: this.isFollowing })
    }
  },
  mounted() {
    // 检查是否已关注
    const following = JSON.parse(localStorage.getItem('bgareaFollowing') || '[]')
    this.isFollowing = following.some(item => item.id === this.teacher.id)
  }
}
</script>

<style scoped>
.teacher-card {
  @apply flex flex-col items-center text-center w-44 bg-white border border-transparent rounded-lg p-4 shadow-sm hover:shadow-md transition-all duration-300;
}

.teacher-avatar-container {
  @apply w-36 h-52 bg-gray-200 rounded-lg overflow-hidden mb-5;
}
</style>