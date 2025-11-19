<template>
  <div class="course-card" @click="handleClick">
    <div class="course-card-image">
      <img 
        :src="course.image" 
        :alt="course.title"
        @error="handleImageError"
      >
      <div v-if="course.featured" class="featured-badge">精选</div>
      <div v-if="course.isNew" class="new-badge">新</div>
    </div>
    
    <div class="course-card-content">
      <h3 class="course-title">{{ course.title }}</h3>
      <p class="course-instructor">{{ course.instructor }}</p>
      
      <div class="course-rating">
        <div class="rating-stars">
          <i v-for="n in 5" :key="n" :class="getStarClass(n)"></i>
        </div>
        <span class="rating-value">{{ course.rating }}</span>
        <span class="rating-count">({{ course.ratingCount }})</span>
      </div>
      
      <div class="course-meta">
        <span class="course-level" :class="course.level">{{ getLevelText(course.level) }}</span>
        <span class="course-duration">{{ course.duration }}</span>
        <span class="course-students">{{ course.studentCount }} 名学生</span>
      </div>
      
      <p class="course-description">{{ course.description }}</p>
      
      <div class="course-tags" v-if="course.tags && course.tags.length > 0">
        <span v-for="tag in course.tags.slice(0, 3)" :key="tag" class="tag">{{ tag }}</span>
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
      <button class="btn btn-primary btn-enroll" @click.stop="enrollCourse">
        {{ course.price === 0 ? '立即学习' : '立即购买' }}
      </button>
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
    handleClick() {
      this.$emit('click', this.course.id)
    },
    
    enrollCourse() {
      this.$emit('enroll', this.course.id)
    },
    
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
    },
    
    handleImageError(event) {
      // 图片加载失败时使用默认图片
      event.target.src = this.getDefaultImage(this.course.category)
    },
    
    getDefaultImage(category) {
      const defaultImages = {
        'technology': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=300&h=160&fit=crop',
        'data-science': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=300&h=160&fit=crop',
        'business': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=300&h=160&fit=crop',
        'design': 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=300&h=160&fit=crop',
        'marketing': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=300&h=160&fit=crop',
        'health': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=300&h=160&fit=crop'
      }
      return defaultImages[category] || 'https://images.unsplash.com/photo-1496171367470-9ed9a91ea931?w=300&h=160&fit=crop'
    }
  }
}
</script>

<style scoped>
.course-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
}

.course-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.course-card-image {
  position: relative;
  height: 160px;
  overflow: hidden;
}

.course-card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.course-card:hover .course-card-image img {
  transform: scale(1.05);
}

.featured-badge, .new-badge {
  position: absolute;
  top: 10px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 500;
  color: white;
}

.featured-badge {
  left: 10px;
  background: var(--warning);
}

.new-badge {
  right: 10px;
  background: var(--success);
}

.course-card-content {
  padding: 20px;
}

.course-title {
  font-size: 1.1rem;
  margin-bottom: 8px;
  color: var(--text);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-instructor {
  color: var(--text-light);
  font-size: 0.9rem;
  margin-bottom: 12px;
}

.course-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.rating-stars {
  color: var(--warning);
}

.rating-value {
  font-weight: 500;
  color: var(--text);
}

.rating-count {
  color: var(--text-light);
  font-size: 0.8rem;
}

.course-meta {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.course-level, .course-duration, .course-students {
  padding: 4px 8px;
  background: var(--secondary);
  border-radius: 4px;
  font-size: 0.8rem;
  color: var(--text-light);
}

.course-level.beginner {
  background: #e8f5e8;
  color: var(--success);
}

.course-level.intermediate {
  background: #fff3cd;
  color: var(--warning);
}

.course-level.advanced {
  background: #f8d7da;
  color: var(--danger);
}

.course-description {
  color: var(--text-light);
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag {
  padding: 2px 8px;
  background: var(--secondary);
  border-radius: 12px;
  font-size: 0.7rem;
  color: var(--text-light);
}

.course-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-top: 1px solid var(--border);
  background: var(--secondary);
}

.course-price {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-free {
  font-weight: 600;
  color: var(--success);
  font-size: 1.1rem;
}

.price-current {
  font-weight: 600;
  color: var(--text);
  font-size: 1.1rem;
}

.price-original {
  color: var(--text-light);
  text-decoration: line-through;
  font-size: 0.9rem;
}

.btn-enroll {
  padding: 8px 16px;
  font-size: 0.9rem;
}

@media (max-width: 480px) {
  .course-card-footer {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }
  
  .btn-enroll {
    width: 100%;
  }
}
</style>