<template>
  <div class="upload-section">
    <div class="section-header">
      <h2>上传新视频</h2>
      <p>分享您的知识，帮助更多人学习</p>
    </div>
    
    <form class="upload-form" @submit.prevent="handleVideoUpload">
      <div class="form-row">
        <div class="form-group">
          <label for="video-title">视频标题 *</label>
          <input 
            type="text" 
            id="video-title"
            v-model="uploadForm.title"
            class="form-control" 
            placeholder="输入吸引人的视频标题" 
            required
          >
        </div>
        <div class="form-group">
          <label for="video-category">分类 *</label>
          <select 
            id="video-category"
            v-model="uploadForm.category"
            class="form-control" 
            required
          >
            <option value="">选择分类</option>
            <option value="technology">技术</option>
            <option value="data-science">数据科学</option>
            <option value="business">商业</option>
            <option value="design">设计</option>
            <option value="marketing">市场营销</option>
            <option value="personal-development">个人发展</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label for="video-description">视频描述 *</label>
        <textarea 
          id="video-description"
          v-model="uploadForm.description"
          class="form-control" 
          placeholder="详细描述视频内容，包括学习目标和适合人群..." 
          rows="4" 
          required
        ></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="video-level">难度级别</label>
          <select 
            id="video-level"
            v-model="uploadForm.level"
            class="form-control"
          >
            <option value="beginner">初级</option>
            <option value="intermediate">中级</option>
            <option value="advanced">高级</option>
          </select>
        </div>
        <div class="form-group">
          <label for="video-duration">视频时长（分钟）</label>
          <input 
            type="number" 
            id="video-duration"
            v-model="uploadForm.duration"
            class="form-control" 
            placeholder="例如：45" 
            min="1"
          >
        </div>
      </div>

      <div class="form-group">
        <label for="video-tags">标签</label>
        <input 
          type="text" 
          id="video-tags"
          v-model="uploadForm.tags"
          class="form-control" 
          placeholder="用逗号分隔标签，例如：Python,机器学习,数据分析"
        >
        <div class="form-hint">添加相关标签可以帮助更多学习者发现您的视频</div>
      </div>

      <div class="upload-area">
        <div class="upload-box" @click="triggerVideoUpload" :class="{ 'has-file': uploadForm.videoFile }">
          <i class="fas fa-cloud-upload-alt"></i>
          <h3>上传视频文件</h3>
          <p>支持 MP4, MOV, AVI 格式，最大 2GB</p>
          <input 
            type="file" 
            ref="videoFileInput"
            accept=".mp4,.mov,.avi" 
            style="display: none;"
            @change="handleVideoFileSelect"
          >
          <button type="button" class="btn btn-outline">
            选择文件
          </button>
          <div class="file-info" v-if="uploadForm.videoFile">
            <div class="file-details">
              <i class="fas fa-file-video"></i>
              <div>
                <div class="file-name">{{ uploadForm.videoFile.name }}</div>
                <div class="file-size">{{ formatFileSize(uploadForm.videoFile.size) }}</div>
              </div>
              <button type="button" class="btn-remove" @click="removeVideoFile">
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="upload-box" @click="triggerThumbnailUpload" :class="{ 'has-file': uploadForm.thumbnailFile }">
          <i class="fas fa-image"></i>
          <h3>上传缩略图</h3>
          <p>建议尺寸 1280x720px，支持 JPG, PNG 格式</p>
          <input 
            type="file" 
            ref="thumbnailFileInput"
            accept=".jpg,.jpeg,.png" 
            style="display: none;"
            @change="handleThumbnailFileSelect"
          >
          <button type="button" class="btn btn-outline">
            选择图片
          </button>
          <div class="file-info" v-if="uploadForm.thumbnailFile">
            <div class="file-details">
              <i class="fas fa-image"></i>
              <div>
                <div class="file-name">{{ uploadForm.thumbnailFile.name }}</div>
                <div class="file-size">{{ formatFileSize(uploadForm.thumbnailFile.size) }}</div>
              </div>
              <button type="button" class="btn-remove" @click="removeThumbnailFile">
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="upload-options">
        <h4>发布选项</h4>
        <div class="form-row">
          <div class="form-group">
            <label for="video-price">价格（元）</label>
            <input 
              type="number" 
              id="video-price"
              v-model="uploadForm.price"
              class="form-control" 
              placeholder="0 表示免费"
              min="0"
            >
          </div>
          <div class="form-group">
            <label for="video-schedule">发布时间</label>
            <select id="video-schedule" v-model="uploadForm.schedule" class="form-control">
              <option value="immediately">立即发布</option>
              <option value="schedule">定时发布</option>
            </select>
          </div>
        </div>
        <div class="form-group" v-if="uploadForm.schedule === 'schedule'">
          <label for="schedule-date">发布时间</label>
          <input 
            type="datetime-local" 
            id="schedule-date"
            v-model="uploadForm.scheduleDate"
            class="form-control"
          >
        </div>
      </div>

      <div class="form-group">
        <label class="checkbox">
          <input type="checkbox" v-model="uploadForm.agreeTerms" required>
          <span class="checkmark"></span>
          我确认拥有上传内容的版权，并同意 <a href="#">内容上传协议</a>
        </label>
      </div>

      <div class="form-actions">
        <button type="button" class="btn btn-outline" @click="resetUploadForm">重置</button>
        <button type="submit" class="btn btn-primary" :disabled="!canSubmitUpload || uploading">
          <i class="fas fa-upload"></i> {{ uploading ? '上传中...' : '上传视频' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'UploadVideoSection',
  data() {
    return {
      uploadForm: {
        title: '',
        category: '',
        description: '',
        level: 'intermediate',
        duration: null,
        tags: '',
        videoFile: null,
        thumbnailFile: null,
        price: 0,
        schedule: 'immediately',
        scheduleDate: '',
        agreeTerms: false
      },
      uploading: false
    }
  },
  computed: {
    canSubmitUpload() {
      return (
        this.uploadForm.title &&
        this.uploadForm.category &&
        this.uploadForm.description &&
        this.uploadForm.videoFile &&
        this.uploadForm.agreeTerms
      )
    }
  },
  methods: {
    triggerVideoUpload() {
      this.$refs.videoFileInput.click()
    },
    triggerThumbnailUpload() {
      this.$refs.thumbnailFileInput.click()
    },
    handleVideoFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        // 验证文件类型和大小
        const validTypes = ['video/mp4', 'video/quicktime', 'video/x-msvideo']
        const maxSize = 2 * 1024 * 1024 * 1024 // 2GB
        
        if (!validTypes.includes(file.type)) {
          alert('请选择 MP4, MOV 或 AVI 格式的视频文件')
          return
        }
        
        if (file.size > maxSize) {
          alert('视频文件大小不能超过 2GB')
          return
        }
        
        this.uploadForm.videoFile = file
      }
    },
    handleThumbnailFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        // 验证文件类型
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png']
        const maxSize = 10 * 1024 * 1024 // 10MB
        
        if (!validTypes.includes(file.type)) {
          alert('请选择 JPG 或 PNG 格式的图片文件')
          return
        }
        
        if (file.size > maxSize) {
          alert('缩略图文件大小不能超过 10MB')
          return
        }
        
        this.uploadForm.thumbnailFile = file
      }
    },
    removeVideoFile() {
      this.uploadForm.videoFile = null
      this.$refs.videoFileInput.value = ''
    },
    removeThumbnailFile() {
      this.uploadForm.thumbnailFile = null
      this.$refs.thumbnailFileInput.value = ''
    },
    resetUploadForm() {
      this.uploadForm = {
        title: '',
        category: '',
        description: '',
        level: 'intermediate',
        duration: null,
        tags: '',
        videoFile: null,
        thumbnailFile: null,
        price: 0,
        schedule: 'immediately',
        scheduleDate: '',
        agreeTerms: false
      }
      this.removeVideoFile()
      this.removeThumbnailFile()
    },
    async handleVideoUpload() {
      this.uploading = true
      
      try {
        // 模拟上传过程
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        alert('视频上传成功！正在处理中...')
        this.resetUploadForm()
        this.$emit('video-uploaded')
      } catch (error) {
        alert('视频上传失败，请重试')
      } finally {
        this.uploading = false
      }
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
  }
}
</script>

<style scoped>
.upload-box.has-file {
  border-color: var(--primary);
  background: rgba(0, 86, 210, 0.02);
}

.upload-options {
  margin: 25px 0;
  padding: 20px;
  background: var(--secondary);
  border-radius: 8px;
}

.upload-options h4 {
  margin-bottom: 15px;
  color: var(--text);
}
</style>