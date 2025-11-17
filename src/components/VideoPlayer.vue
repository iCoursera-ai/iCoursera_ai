<template>
  <div class="video-player-component">
    <div class="video-wrapper">
      <video 
        ref="videoElement"
        :src="videoSrc"
        :poster="poster"
        @timeupdate="handleTimeUpdate"
        @loadedmetadata="handleLoadedMetadata"
        @play="handlePlay"
        @pause="handlePause"
        @ended="handleEnded"
      >
        <source :src="videoSrc" type="video/mp4">
        您的浏览器不支持 HTML5 视频。
      </video>
      
      <div class="video-controls" v-show="showControls">
        <div class="progress-bar" @click="handleProgressClick">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
          <div class="progress-handle" :style="{ left: progress + '%' }"></div>
        </div>
        
        <div class="control-buttons">
          <button class="control-btn" @click="togglePlay">
            <i :class="isPlaying ? 'fas fa-pause' : 'fas fa-play'"></i>
          </button>
          
          <div class="time-display">
            {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
          </div>
          
          <button class="control-btn" @click="toggleMute">
            <i :class="isMuted ? 'fas fa-volume-mute' : 'fas fa-volume-up'"></i>
          </button>
          
          <input 
            type="range" 
            min="0" 
            max="1" 
            step="0.1" 
            v-model="volume"
            class="volume-slider"
          >
          
          <button class="control-btn" @click="toggleFullscreen">
            <i :class="isFullscreen ? 'fas fa-compress' : 'fas fa-expand'"></i>
          </button>
        </div>
      </div>
      
      <div class="play-overlay" v-show="!isPlaying && showPlayOverlay" @click="togglePlay">
        <i class="fas fa-play"></i>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VideoPlayer',
  props: {
    videoSrc: {
      type: String,
      required: true
    },
    poster: {
      type: String,
      default: ''
    },
    autoplay: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isPlaying: false,
      isMuted: false,
      isFullscreen: false,
      currentTime: 0,
      duration: 0,
      volume: 1,
      progress: 0,
      showControls: true,
      showPlayOverlay: true,
      controlsTimeout: null
    }
  },
  mounted() {
    this.setupEventListeners()
    if (this.autoplay) {
      this.playVideo()
    }
  },
  beforeUnmount() {
    this.removeEventListeners()
  },
  methods: {
    setupEventListeners() {
      document.addEventListener('fullscreenchange', this.handleFullscreenChange)
      document.addEventListener('keydown', this.handleKeydown)
      this.$refs.videoElement.addEventListener('click', this.togglePlay)
    },
    removeEventListeners() {
      document.removeEventListener('fullscreenchange', this.handleFullscreenChange)
      document.removeEventListener('keydown', this.handleKeydown)
      if (this.$refs.videoElement) {
        this.$refs.videoElement.removeEventListener('click', this.togglePlay)
      }
    },
    playVideo() {
      this.$refs.videoElement.play()
    },
    pauseVideo() {
      this.$refs.videoElement.pause()
    },
    togglePlay() {
      if (this.isPlaying) {
        this.pauseVideo()
      } else {
        this.playVideo()
      }
    },
    toggleMute() {
      this.isMuted = !this.isMuted
      this.$refs.videoElement.muted = this.isMuted
    },
    toggleFullscreen() {
      if (!this.isFullscreen) {
        if (this.$el.requestFullscreen) {
          this.$el.requestFullscreen()
        }
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen()
        }
      }
    },
    handleTimeUpdate() {
      this.currentTime = this.$refs.videoElement.currentTime
      this.progress = (this.currentTime / this.duration) * 100
    },
    handleLoadedMetadata() {
      this.duration = this.$refs.videoElement.duration
    },
    handlePlay() {
      this.isPlaying = true
      this.showPlayOverlay = false
    },
    handlePause() {
      this.isPlaying = false
      this.showPlayOverlay = true
    },
    handleEnded() {
      this.isPlaying = false
      this.showPlayOverlay = true
      this.$emit('video-ended')
    },
    handleFullscreenChange() {
      this.isFullscreen = !!document.fullscreenElement
    },
    handleKeydown(event) {
      if (event.code === 'Space') {
        event.preventDefault()
        this.togglePlay()
      }
    },
    handleProgressClick(event) {
      const progressBar = event.currentTarget
      const clickPosition = event.offsetX
      const width = progressBar.offsetWidth
      const percentage = clickPosition / width
      
      this.$refs.videoElement.currentTime = percentage * this.duration
    },
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    },
    hideControls() {
      this.showControls = false
    },
    showControlsWithTimeout() {
      this.showControls = true
      clearTimeout(this.controlsTimeout)
      this.controlsTimeout = setTimeout(() => {
        if (this.isPlaying) {
          this.showControls = false
        }
      }, 3000)
    }
  },
  watch: {
    volume(newVolume) {
      this.$refs.videoElement.volume = newVolume
      this.isMuted = newVolume === 0
    }
  }
}
</script>

<style scoped>
.video-player-component {
  position: relative;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
}

.video-wrapper {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
}

.video-wrapper video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000;
}

.video-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  padding: 20px;
  color: white;
  transition: opacity 0.3s;
}

.progress-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  margin-bottom: 15px;
  cursor: pointer;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: var(--primary);
  border-radius: 2px;
  transition: width 0.1s;
}

.progress-handle {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 12px;
  height: 12px;
  background: var(--primary);
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s;
}

.progress-bar:hover .progress-handle {
  opacity: 1;
}

.control-buttons {
  display: flex;
  align-items: center;
  gap: 15px;
}

.control-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.time-display {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  margin: 0 10px;
}

.volume-slider {
  width: 80px;
  cursor: pointer;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: opacity 0.3s;
}

.play-overlay i {
  font-size: 4rem;
  color: white;
  opacity: 0.8;
}

.play-overlay:hover i {
  opacity: 1;
}
</style>