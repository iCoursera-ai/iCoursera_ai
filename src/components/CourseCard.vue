<template>
  <div class="course-card" @click="$emit('click')">
    <div class="course-card-image">
      <img :src="course.image" :alt="course.title">
      <div v-if="course.featured" class="featured-badge">推荐</div>
      <div v-if="course.isNew" class="new-badge">新课程</div>
    </div>
    <div class="course-card-content">
      <h3 class="course-title">{{ course.title }}</h3>
      <p class="course-instructor">{{ course.instructor }}</p>
      <div class="course-rating">
        <div class="rating-stars">
          <i v-for="n in 5" :key="n" :class="getStarClass(n)"></i>
        </div>
        <span class="rating-value">{{ course.rating }}</span>
        <span class="rating-count">({{ course.ratingCount }} 评价)</span>
      </div>
      <div class="course-meta">
        <span class="course-level" :class="course.level">{{ getLevelText(course.level) }}</span>
        <span class="course-duration">{{ course.duration }}</span>
      </div>
      <p class="course-description">{{ course.description }}</p>
      <div v-if="course.tags && course.tags.length" class="course-tags">
        <span v-for="tag in course.tags" :key="tag" class="tag">{{ tag }}</span>
      </div>
    </div>
    <div class="course-card-footer">
      <div class="course-price">
        <span v-if="course.price === 0" class="price-free">免费</span>
        <template v-else>
          <span class="price-current">¥{{ course.price }}</span>
          <span v-if="course.originalPrice" class="price-original">¥{{ course.originalPrice }}</span>
        </template>
      </div>
      <button class="btn btn-primary btn-enroll">立即学习</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseCard',
  props: {
    course: {
      type: Object,
      required: true
    }
  },
  methods: {
    getStarClass(n) {
      const rating = this.course.rating
      if (n <= Math.floor(rating)) return 'fas fa-star'
      if (n === Math.ceil(rating) && rating % 1 >= 0.5) return 'fas fa-star-half-alt'
      return 'far fa-star'
    },
    getLevelText(level) {
      const levels = {
        'beginner': '初级',
        'intermediate': '中级',
        'advanced': '高级'
      }
      return levels[level] || level
    }
  }
}
</script>