<template>
  <div 
    :class="['video-card-hover', { 'cursor-pointer': clickable }]" 
    @click="handleClick"
  >
    <div class="relative rounded-lg overflow-hidden mb-2">
      <img 
        :src="course.image" 
        :alt="course.title" 
        class="w-full h-40 object-cover"
        :class="{ 'h-24': size === 'small', 'h-40': size === 'medium', 'h-80': size === 'large' }"
      >
      
      <!-- 徽章 -->
      <span 
        v-if="course.badge"
        :class="['absolute top-2 left-2 text-white text-xs px-2 py-0.5 rounded z-10', getBadgeClass(course.badge)]"
      >
        {{ getBadgeText(course.badge) }}
      </span>
      
      <!-- 视频时长 -->
      <span v-if="course.duration" class="video-time">
        {{ formatDuration(course.duration) }}
      </span>
      
      <!-- 播放按钮 -->
      <div v-if="showPlayButton" class="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-300 bg-black/20">
        <div class="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
          <i class="fa fa-play text-white text-lg"></i>
        </div>
      </div>
      
      <!-- 收藏按钮 -->
      <div v-if="showBookmark" class="absolute top-2 right-2 text-gray-400 hover:text-primary cursor-pointer">
        <i class="fa" :class="isBookmarked ? 'fa-bookmark text-primary' : 'fa-bookmark-o'"></i>
      </div>
    </div>
    
    <!-- 课程信息 -->
    <div :class="['px-1', { 'flex flex-col justify-center': size === 'small' }]">
      <h4 
        :class="[
          'font-medium text-dark line-clamp-1 hover:text-primary transition-colors',
          { 'text-sm': size === 'small', 'text-base': size === 'medium', 'text-xl': size === 'large' }
        ]"
      >
        {{ course.title }}
      </h4>
      
      <div v-if="course.teacher" class="text-xs text-gray-500 mt-1 flex items-center gap-1">
        <i class="fa fa-user text-gray-400"></i>
        <span>{{ course.teacher }}</span>
      </div>
      
      <p v-if="course.description && size !== 'small'" class="text-sm text-gray-600 mt-2 line-clamp-2">
        {{ course.description }}
      </p>
      
      <!-- 统计信息 -->
      <div class="flex justify-between items-center text-xs text-gray-400 mt-2">
        <div v-if="course.views" class="flex items-center gap-4">
          <span class="flex items-center gap-1">
            <i class="fa fa-eye text-gray-400"></i>
            {{ formatViews(course.views) }}
          </span>
          <span v-if="course.rating" class="flex items-center gap-1">
            <i class="fa fa-thumbs-up text-gray-400"></i>
            {{ course.rating }}
          </span>
        </div>
        
        <div v-if="course.date" class="text-gray-400">
          {{ course.date }}
        </div>
        
        <div v-if="course.category" class="text-gray-400">
          {{ course.category }}
        </div>
      </div>
      
      <!-- 评分 -->
      <div v-if="course.score" class="flex items-center gap-1 mt-1">
        <div class="flex text-yellow-400">
          <i v-for="i in 5" :key="i" class="fa" :class="i <= Math.floor(course.score) ? 'fa-star' : 'fa-star-o'"></i>
        </div>
        <span class="text-xs text-gray-500 ml-1">{{ course.score }}分</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseCard',
  props: {
    course: {
      type: Object,
      required: true,
      default: () => ({
        id: null,
        title: '',
        teacher: '',
        image: '',
        duration: '',
        views: '',
        date: '',
        category: '',
        rating: '',
        score: 0,
        description: '',
        badge: '' // 'hot', 'new', 'featured', 'recommended'
      })
    },
    size: {
      type: String,
      default: 'medium', // 'small', 'medium', 'large'
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    showPlayButton: {
      type: Boolean,
      default: true
    },
    showBookmark: {
      type: Boolean,
      default: false
    },
    clickable: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      isBookmarked: false
    }
  },
  methods: {
    handleClick() {
      if (this.clickable) {
        this.$emit('click', this.course)
        if (this.course.id) {
          this.$router.push(`/course/${this.course.id}`)
        }
      }
    },
    
    getBadgeClass(badge) {
      const badgeClasses = {
        hot: 'bg-red-500',
        new: 'bg-primary',
        featured: 'bg-green-500',
        recommended: 'bg-orange-500',
        popular: 'bg-purple-500'
      }
      return badgeClasses[badge] || 'bg-primary'
    },
    
    getBadgeText(badge) {
      const badgeTexts = {
        hot: '热门',
        new: '新品',
        featured: '精讲',
        recommended: '推荐',
        popular: '爆款'
      }
      return badgeTexts[badge] || '推荐'
    },
    
    formatDuration(duration) {
      if (typeof duration === 'number') {
        const hours = Math.floor(duration / 3600)
        const minutes = Math.floor((duration % 3600) / 60)
        const seconds = duration % 60
        
        if (hours > 0) {
          return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
        } else {
          return `${minutes}:${seconds.toString().padStart(2, '0')}`
        }
      }
      return duration
    },
    
    formatViews(views) {
      if (typeof views === 'number') {
        if (views >= 10000) {
          return (views / 10000).toFixed(1) + '万播放'
        }
        return views + '播放'
      }
      return views
    }
  },
  mounted() {
    // 检查是否已收藏
    const bookmarks = JSON.parse(localStorage.getItem('bgareaBookmarks') || '[]')
    this.isBookmarked = bookmarks.some(item => item.id === this.course.id)
  }
}
</script>

<style scoped>
.video-card-hover img {
  transition: transform 0.3s ease;
}
.video-card-hover:hover img {
  transform: scale(1.03);
}
</style>