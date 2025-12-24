<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- 使用Header组件 -->
    <Header />
    
    <!-- 主内容容器 -->
    <div class="flex flex-1">
      <!-- 左侧章节导航 -->
      <aside class="w-56 bg-white border-r border-gray-200 p-4 h-[calc(100vh-64px)] sticky top-16">
        <!-- 章节列表容器 -->
        <div class="space-y-1">
          <!-- 动态生成章节 -->
          <div v-for="(chapter, index) in chapters" :key="chapter.id" class="chapter-group">
            <div 
              :class="[
                'chapter-item flex items-center justify-between py-1.5 cursor-pointer',
                activeChapterId === chapter.id ? 'active' : ''
              ]"
              @click="toggleChapter(chapter)"
            >
              <span>{{ chapter.name }}</span>
              <i 
                :class="[
                  'fa text-xs transition-transform duration-200',
                  chapter.expanded ? 'fa-chevron-down rotate-180 text-primary' : 'fa-chevron-down text-gray-400'
                ]"
              ></i>
            </div>
            
            <!-- 章节内容 -->
            <div v-show="chapter.expanded" class="chapter-children space-y-1 mt-1">
              <!-- 视频内容 -->
              <div 
                v-for="video in chapter.videos" 
                :key="video.id"
                :class="[
                  'sub-item pl-4 py-1.5 text-sm cursor-pointer transition-colors duration-200',
                  activeContentId === video.id && activeContentType === 'video' ? 'active' : ''
                ]"
                @click="selectContent(video, 'video')"
              >
                {{ chapter.name.slice(1, 3) }}.{{ video.order }}视频
              </div>
              
              <!-- 习题内容 -->
              <div 
                v-for="exercise in chapter.exercises" 
                :key="exercise.id"
                :class="[
                  'sub-item pl-4 py-1.5 text-sm cursor-pointer transition-colors duration-200',
                  activeContentId === exercise.id && activeContentType === 'exercise' ? 'active' : ''
                ]"
                @click="selectContent(exercise, 'exercise')"
              >
                {{ chapter.name.slice(1, 3) }}.{{ exercise.order }}习题
              </div>
              
              <!-- 添加按钮 -->
              <div 
                class="add-btn pl-4 py-1.5 text-sm cursor-pointer transition-colors duration-200 text-primary"
                @click="addContentToChapter(chapter.id, 'video')"
              >
                <i class="fa fa-plus-circle text-xs mr-1"></i>添加视频
              </div>
              <div 
                class="add-btn pl-4 py-1.5 text-sm cursor-pointer transition-colors duration-200 text-primary"
                @click="addContentToChapter(chapter.id, 'exercise')"
              >
                <i class="fa fa-plus-circle text-xs mr-1"></i>添加习题
              </div>
            </div>
          </div>
          
          <!-- 添加新章节按钮 -->
          <div 
            class="add-btn mt-4 py-1.5 text-sm cursor-pointer transition-colors duration-200 text-primary"
            @click="addNewChapter"
          >
            <i class="fa fa-plus-circle text-xs mr-1"></i>添加新章节
          </div>
        </div>
      </aside>

      <!-- 右侧内容区域 -->
      <main class="flex-1 p-6">
        <!-- 视频上传界面 -->
        <div 
          v-if="activeContentType === 'video'" 
          id="video-upload-panel" 
          class="bg-white rounded-lg p-6 shadow-sm"
        >
          <!-- 页面标题 -->
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-xl font-bold text-gray-800">{{ activeVideo ? `${activeVideo.title} - 上传内容` : '上传视频内容' }}</h1>
            <div class="flex gap-3">
              <button 
                class="px-4 py-2 text-primary border border-primary rounded-md text-sm hover:bg-primary/5 transition-colors"
                @click="previewVideo"
              >
                预览
              </button>
              <button 
                class="px-4 py-2 bg-primary text-white rounded-md text-sm hover:bg-primary/90 transition-colors"
                @click="saveVideo"
              >
                保存
              </button>
            </div>
          </div>

          <!-- 视频标题 -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">视频标题</label>
            <input 
              type="text" 
              class="input-field" 
              v-model="videoForm.title"
              placeholder="请输入视频标题"
            >
          </div>

          <!-- 视频文件上传 -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">视频文件</label>
            <div 
              class="upload-area"
              @click="triggerVideoUpload"
              @dragover.prevent="videoDragover = true"
              @dragleave.prevent="videoDragover = false"
              @drop.prevent="handleVideoDrop"
              :class="{ 'border-primary bg-primary/5': videoDragover }"
            >
              <p class="text-gray-500 mb-2">
                {{ videoForm.videoFile ? videoForm.videoFile.name : '点击或拖拽视频文件到此处上传' }}
              </p>
              <p class="text-xs text-gray-400">支持格式：MP4、AVI、MOV<br>最大2GB，时长≤2小时</p>
              <input 
                type="file" 
                ref="videoFileInput"
                @change="handleVideoFileSelect"
                accept="video/*"
                class="hidden"
              >
            </div>
          </div>

          <!-- 视频描述 -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">视频描述</label>
            <textarea 
              class="input-field min-h-[80px]" 
              v-model="videoForm.description"
              placeholder="请输入视频简介..."
            ></textarea>
          </div>

          <!-- 视频封面 -->
          <div class="mb-8">
            <label class="block text-sm font-medium text-gray-700 mb-2">视频封面</label>
            <div class="flex items-center gap-4">
              <div 
                v-if="videoForm.coverPreview"
                class="w-20 h-20 rounded overflow-hidden border border-gray-300"
              >
                <img :src="videoForm.coverPreview" class="w-full h-full object-cover">
              </div>
              <div 
                v-else
                class="w-20 h-20 bg-gray-200 rounded flex items-center justify-center border border-gray-300 cursor-pointer"
                @click="triggerCoverUpload"
              >
                <span class="text-sm text-gray-500">选择图片</span>
              </div>
              <div>
                <p class="text-xs text-gray-500">建议尺寸：1200x675px</p>
                <p class="text-xs text-gray-500">格式：JPG、PNG</p>
                <input 
                  type="file" 
                  ref="coverFileInput"
                  @change="handleCoverFileSelect"
                  accept="image/*"
                  class="hidden"
                >
              </div>
            </div>
          </div>

          <!-- 分割线 -->
          <div class="border-t border-dashed border-gray-300 my-6"></div>

          <!-- 视频标签 -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">视频标签</label>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="(tag, index) in videoForm.tags" 
                :key="index"
                class="inline-flex items-center px-3 py-1 rounded-full bg-primary/10 text-primary text-xs"
              >
                {{ tag }}
                <button 
                  class="ml-1 text-primary hover:text-primary/80"
                  @click="removeVideoTag(index)"
                >
                  <i class="fa fa-times"></i>
                </button>
              </span>
              <input 
                type="text" 
                v-model="newTag"
                @keyup.enter="addVideoTag"
                placeholder="添加标签..."
                class="inline-flex items-center px-3 py-1 rounded-full bg-gray-100 text-gray-700 text-xs outline-none min-w-[80px]"
              >
            </div>
          </div>

          <!-- 视频设置 -->
          <div class="mb-6">
            <h3 class="text-base font-medium text-gray-800 mb-4">视频设置</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-800">允许下载</p>
                  <p class="text-xs text-gray-500">学员可下载该视频</p>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="videoForm.allowDownload">
                  <span class="slider"></span>
                </label>
              </div>
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-800">需要观看完整</p>
                  <p class="text-xs text-gray-500">只允许学员完整观看后进行后续操作</p>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="videoForm.requireComplete">
                  <span class="slider"></span>
                </label>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">视频时长（秒）</label>
                <input 
                  type="number" 
                  class="input-field w-32" 
                  v-model="videoForm.duration"
                  min="0"
                >
              </div>
            </div>
          </div>

          <!-- 底部提示 -->
          <div class="mt-8 text-sm text-gray-500">
            <i class="fa fa-info-circle mr-1"></i>
            如需上传习题内容，请在左侧导航栏中选择对应的习题
          </div>
        </div>

        <!-- 习题上传界面 -->
        <div 
          v-else 
          id="exercise-upload-panel" 
          class="bg-white rounded-lg p-6 shadow-sm"
        >
          <!-- 页面标题 -->
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-xl font-bold text-gray-800">{{ activeExercise ? activeExercise.title : '上传习题内容' }}</h1>
            <p class="text-xs text-gray-500">上传题目时请选择章节节点（支持单选/多选）</p>
          </div>

          <!-- 题目信息区域 -->
          <div class="space-y-6">
            <div>
              <h3 class="text-base font-medium text-gray-800 mb-3">题目信息</h3>
              
              <!-- 题目类型 -->
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">题目类型</label>
                <select class="input-field w-40" v-model="exerciseForm.type">
                  <option value="single">单选题</option>
                  <option value="multiple">多选题</option>
                  <option value="judge">判断题</option>
                  <option value="fill">填空题</option>
                  <option value="short">简答题</option>
                </select>
              </div>

              <!-- 题目内容 -->
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">题目内容</label>
                <textarea 
                  class="input-field min-h-[80px]" 
                  v-model="exerciseForm.content"
                  placeholder="请输入题目内容..."
                ></textarea>
              </div>

              <!-- 选项区域 -->
              <div class="mb-4" v-if="showOptions">
                <label class="block text-sm font-medium text-gray-700 mb-2">选项（至少2个）</label>
                <div id="options-container" class="space-y-2">
                  <div 
                    v-for="(option, index) in exerciseForm.options" 
                    :key="index"
                    class="option-item"
                  >
                    <span class="w-6 text-center">{{ String.fromCharCode(65 + index) }}</span>
                    <input 
                      type="text" 
                      class="option-input" 
                      v-model="exerciseForm.options[index]"
                      placeholder="输入选项内容"
                    >
                  </div>
                </div>
                <button 
                  class="text-primary text-sm mt-2"
                  @click="addOption"
                  v-if="exerciseForm.options.length < 6"
                >
                  <i class="fa fa-plus-circle text-xs"></i> 添加选项
                </button>
              </div>

              <!-- 正确答案 -->
              <div class="mb-4" v-if="showOptions">
                <label class="block text-sm font-medium text-gray-700 mb-2">正确答案</label>
                <div class="flex gap-4">
                  <label 
                    v-for="(option, index) in exerciseForm.options" 
                    :key="index"
                    class="answer-label"
                  >
                    <input 
                      type="checkbox" 
                      v-model="exerciseForm.correctAnswers"
                      :value="String.fromCharCode(65 + index)"
                      :multiple="exerciseForm.type === 'multiple'"
                    >
                    <span>{{ String.fromCharCode(65 + index) }}</span>
                  </label>
                </div>
              </div>

              <!-- 题目分数 -->
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">题目分数</label>
                <input 
                  type="number" 
                  class="input-field w-20" 
                  v-model="exerciseForm.score"
                  min="0"
                >
              </div>

              <!-- 做题时长 -->
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">做题时长（分钟）</label>
                <input 
                  type="number" 
                  class="input-field w-20" 
                  v-model="exerciseForm.timeLimit"
                  min="0"
                >
                <p class="text-xs text-gray-500 mt-1">设置学员完成该题的时间，未完成则跳时</p>
              </div>

              <!-- 题目解析 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">题目解析（可选）</label>
                <textarea 
                  class="input-field min-h-[80px]" 
                  v-model="exerciseForm.analysis"
                  placeholder="简要说明题目考点和解题思路..."
                ></textarea>
              </div>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex justify-end gap-3 mt-8">
            <button 
              class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md text-sm hover:bg-gray-50 transition-colors"
              @click="resetExerciseForm"
            >
              取消
            </button>
            <button 
              class="px-4 py-2 bg-primary text-white rounded-md text-sm hover:bg-primary/90 transition-colors"
              @click="saveExercise"
            >
              保存题目
            </button>
          </div>

          <!-- 已上传题目列表 -->
          <div class="mt-8">
            <h3 class="text-base font-medium text-gray-800 mb-3">已上传题目</h3>
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-gray-200">
                    <th class="text-left py-2 px-1 font-medium text-gray-700">题目</th>
                    <th class="text-left py-2 px-1 font-medium text-gray-700">类型</th>
                    <th class="text-left py-2 px-1 font-medium text-gray-700">分数</th>
                    <th class="text-left py-2 px-1 font-medium text-gray-700">时长</th>
                    <th class="text-left py-2 px-1 font-medium text-gray-700">操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="exercise in existingExercises" 
                    :key="exercise.id"
                    class="border-b border-gray-200 hover:bg-gray-50"
                  >
                    <td class="py-3 px-1 max-w-xs truncate">{{ exercise.content }}</td>
                    <td class="py-3 px-1">{{ getExerciseTypeText(exercise.type) }}</td>
                    <td class="py-3 px-1">{{ exercise.score }}分</td>
                    <td class="py-3 px-1">{{ exercise.timeLimit }}分钟</td>
                    <td class="py-3 px-1">
                      <button 
                        class="text-primary hover:underline mr-2"
                        @click="editExercise(exercise)"
                      >
                        编辑
                      </button>
                      <button 
                        class="text-red-500 hover:underline"
                        @click="deleteExercise(exercise.id)"
                      >
                        删除
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- 提示框组件 -->
    <div :class="['toast', toastClass, showToast ? 'show' : '']" v-if="showToast">
      <i :class="toastIcon"></i>
      <span>{{ toastMessage }}</span>
    </div>

    <!-- 使用Footer组件 -->
    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'VideoUpload',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      // 从URL参数获取的稿件ID
      fileId: null,
      // 章节数据
      chapters: [
        {
          id: 1,
          name: '第1章',
          expanded: false,
          videos: [
            { id: 1, title: '1.1视频', order: 1, content: null },
            { id: 2, title: '1.2视频', order: 2, content: null }
          ],
          exercises: [
            { id: 1, title: '1.1习题', order: 1, content: null }
          ]
        },
        {
          id: 2,
          name: '第2章',
          expanded: false,
          videos: [
            { id: 3, title: '2.1视频', order: 1, content: null }
          ],
          exercises: [
            { id: 2, title: '2.1习题', order: 1, content: null }
          ]
        },
        {
          id: 3,
          name: '第3章',
          expanded: false,
          videos: [
            { id: 4, title: '3.1视频', order: 1, content: null }
          ],
          exercises: [
            { id: 3, title: '3.1习题', order: 1, content: null }
          ]
        },
        {
          id: 4,
          name: '第4章',
          expanded: true,
          videos: [
            { id: 5, title: '4.1视频', order: 1, content: null }
          ],
          exercises: [
            { 
              id: 4, 
              title: '4.1习题', 
              order: 1, 
              content: {
                id: 1,
                type: 'single',
                content: '以下哪个是JavaScript的基本数据类型？',
                options: ['String', 'Object', 'Function', 'Array'],
                correctAnswers: ['A'],
                score: 5,
                timeLimit: 5,
                analysis: 'JavaScript的基本数据类型包括：String、Number、Boolean、Null、Undefined、Symbol、BigInt。Object、Function、Array都是引用类型。'
              }
            }
          ]
        }
      ],
      // 当前选中的章节和内容
      activeChapterId: 4,
      activeContentId: 4,
      activeContentType: 'exercise',
      // 视频表单数据
      videoForm: {
        title: '视频4.1',
        videoFile: null,
        description: '',
        coverFile: null,
        coverPreview: null,
        tags: ['基础知识'],
        allowDownload: false,
        requireComplete: true,
        duration: 900
      },
      newTag: '',
      videoDragover: false,
      // 习题表单数据
      exerciseForm: {
        id: null,
        type: 'single',
        content: '以下哪个是JavaScript的基本数据类型？',
        options: ['String', 'Object', 'Function', 'Array'],
        correctAnswers: ['A'],
        score: 5,
        timeLimit: 5,
        analysis: 'JavaScript的基本数据类型包括：String、Number、Boolean、Null、Undefined、Symbol、BigInt。Object、Function、Array都是引用类型。'
      },
      // 现有习题列表
      existingExercises: [
        {
          id: 1,
          type: 'single',
          content: '以下哪个是JavaScript的基本数据类型？',
          options: ['String', 'Object', 'Function', 'Array'],
          correctAnswers: ['A'],
          score: 5,
          timeLimit: 5,
          analysis: 'JavaScript的基本数据类型包括：String、Number、Boolean、Null、Undefined、Symbol、BigInt。Object、Function、Array都是引用类型。'
        }
      ],
      // 提示框
      showToast: false,
      toastType: '',
      toastMessage: '',
      toastTimeout: null
    }
  },
  computed: {
    // 当前选中的视频
    activeVideo() {
      const chapter = this.chapters.find(c => c.id === this.activeChapterId)
      if (!chapter) return null
      return chapter.videos.find(v => v.id === this.activeContentId)
    },
    // 当前选中的习题
    activeExercise() {
      const chapter = this.chapters.find(c => c.id === this.activeChapterId)
      if (!chapter) return null
      return chapter.exercises.find(e => e.id === this.activeContentId)
    },
    // 是否显示选项区域
    showOptions() {
      return ['single', 'multiple', 'judge'].includes(this.exerciseForm.type)
    },
    // 提示框样式
    toastClass() {
      switch(this.toastType) {
        case 'success': return 'toast-success'
        case 'warning': return 'toast-warning'
        case 'error': return 'toast-error'
        default: return ''
      }
    },
    toastIcon() {
      switch(this.toastType) {
        case 'success': return 'fa fa-check-circle text-green-500'
        case 'warning': return 'fa fa-exclamation-circle text-orange-500'
        case 'error': return 'fa fa-times-circle text-red-500'
        default: return ''
      }
    }
  },
  mounted() {
    // 从URL参数获取稿件ID
    this.fileId = this.$route.query.fileId
    
    // 如果有稿件ID，可以加载对应的数据
    if (this.fileId) {
      this.loadFileData(this.fileId)
    }
    
    // 默认展开第一个章节
    if (this.chapters.length > 0) {
      const firstChapter = this.chapters[0]
      firstChapter.expanded = true
    }
  },
  methods: {
    // 显示提示框
    showToastMessage(type, message) {
      this.toastType = type
      this.toastMessage = message
      this.showToast = true
      
      if (this.toastTimeout) {
        clearTimeout(this.toastTimeout)
      }
      
      this.toastTimeout = setTimeout(() => {
        this.showToast = false
      }, 3000)
    },
    
    // 加载稿件数据
    loadFileData(fileId) {
      // 这里应该从API加载对应稿件的数据
      console.log('加载稿件ID:', fileId)
      // 模拟加载数据
      // TODO: 调用API获取稿件详情
    },
    
    // 切换章节展开/收起
    toggleChapter(chapter) {
      chapter.expanded = !chapter.expanded
      if (chapter.expanded) {
        this.activeChapterId = chapter.id
      }
    },
    
    // 选择内容
    selectContent(content, type) {
      this.activeContentId = content.id
      this.activeContentType = type
      
      // 如果是视频，加载视频数据
      if (type === 'video' && content.content) {
        this.loadVideoForm(content.content)
      }
      // 如果是习题，加载习题数据
      else if (type === 'exercise' && content.content) {
        this.loadExerciseForm(content.content)
      } else {
        this.resetForms()
      }
    },
    
    // 加载视频表单数据
    loadVideoForm(videoData) {
      this.videoForm = {
        title: videoData.title || '新视频',
        videoFile: videoData.videoFile || null,
        description: videoData.description || '',
        coverFile: videoData.coverFile || null,
        coverPreview: videoData.coverPreview || null,
        tags: videoData.tags || ['基础知识'],
        allowDownload: videoData.allowDownload || false,
        requireComplete: videoData.requireComplete || true,
        duration: videoData.duration || 900
      }
    },
    
    // 加载习题表单数据
    loadExerciseForm(exerciseData) {
      this.exerciseForm = {
        id: exerciseData.id,
        type: exerciseData.type || 'single',
        content: exerciseData.content || '',
        options: [...(exerciseData.options || ['', ''])],
        correctAnswers: [...(exerciseData.correctAnswers || [])],
        score: exerciseData.score || 5,
        timeLimit: exerciseData.timeLimit || 5,
        analysis: exerciseData.analysis || ''
      }
    },
    
    // 重置表单
    resetForms() {
      this.videoForm = {
        title: this.activeVideo ? this.activeVideo.title : '新视频',
        videoFile: null,
        description: '',
        coverFile: null,
        coverPreview: null,
        tags: ['基础知识'],
        allowDownload: false,
        requireComplete: true,
        duration: 900
      }
      
      this.exerciseForm = {
        id: null,
        type: 'single',
        content: '',
        options: ['', ''],
        correctAnswers: [],
        score: 5,
        timeLimit: 5,
        analysis: ''
      }
    },
    
    // 重置习题表单
    resetExerciseForm() {
      this.exerciseForm = {
        id: null,
        type: 'single',
        content: '',
        options: ['', ''],
        correctAnswers: [],
        score: 5,
        timeLimit: 5,
        analysis: ''
      }
    },
    
    // 添加内容到章节
    addContentToChapter(chapterId, type) {
      const chapter = this.chapters.find(c => c.id === chapterId)
      if (!chapter) return
      
      if (type === 'video') {
        const order = chapter.videos.length + 1
        const newVideo = {
          id: Date.now(),
          title: `${chapter.name.slice(1, 3)}.${order}视频`,
          order,
          content: null
        }
        chapter.videos.push(newVideo)
        // 自动选中新添加的视频
        this.selectContent(newVideo, 'video')
      } else {
        const order = chapter.exercises.length + 1
        const newExercise = {
          id: Date.now(),
          title: `${chapter.name.slice(1, 3)}.${order}习题`,
          order,
          content: null
        }
        chapter.exercises.push(newExercise)
        // 自动选中新添加的习题
        this.selectContent(newExercise, 'exercise')
      }
      
      // 修复：使用自定义提示框方法
      this.showToastMessage('success', `已添加新${type === 'video' ? '视频' : '习题'}`)
    },
    
    // 添加新章节
    addNewChapter() {
      const newChapterNum = this.chapters.length + 1
      const newChapter = {
        id: Date.now(),
        name: `第${newChapterNum}章`,
        expanded: true,
        videos: [],
        exercises: []
      }
      
      this.chapters.push(newChapter)
      this.activeChapterId = newChapter.id
      this.showToastMessage('success', `已添加新章节：${newChapter.name}`)
    },
    
    // 添加视频标签
    addVideoTag() {
      if (this.newTag.trim() && !this.videoForm.tags.includes(this.newTag.trim())) {
        this.videoForm.tags.push(this.newTag.trim())
        this.newTag = ''
      }
    },
    
    // 移除视频标签
    removeVideoTag(index) {
      this.videoForm.tags.splice(index, 1)
    },
    
    // 添加习题选项
    addOption() {
      if (this.exerciseForm.options.length < 6) {
        this.exerciseForm.options.push('')
      }
    },
    
    // 触发视频文件选择
    triggerVideoUpload() {
      this.$refs.videoFileInput.click()
    },
    
    // 处理视频文件选择
    handleVideoFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        this.videoForm.videoFile = file
      }
    },
    
    // 处理视频文件拖放
    handleVideoDrop(event) {
      this.videoDragover = false
      const file = event.dataTransfer.files[0]
      if (file) {
        this.videoForm.videoFile = file
      }
    },
    
    // 触发封面文件选择
    triggerCoverUpload() {
      this.$refs.coverFileInput.click()
    },
    
    // 处理封面文件选择
    handleCoverFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        this.videoForm.coverFile = file
        this.videoForm.coverPreview = URL.createObjectURL(file)
      }
    },
    
    // 预览视频
    previewVideo() {
      if (!this.videoForm.videoFile) {
        this.showToastMessage('warning', '请先上传视频文件')
        return
      }
      
      // 在实际应用中，这里应该打开视频预览窗口
      this.showToastMessage('success', '视频预览功能开发中')
    },
    
    // 保存视频
    saveVideo() {
      if (!this.videoForm.title.trim()) {
        this.showToastMessage('warning', '请输入视频标题')
        return
      }
      
      if (!this.videoForm.videoFile) {
        this.showToastMessage('warning', '请上传视频文件')
        return
      }
      
      // 保存视频数据到当前选中的内容
      const chapter = this.chapters.find(c => c.id === this.activeChapterId)
      if (chapter) {
        const video = chapter.videos.find(v => v.id === this.activeContentId)
        if (video) {
          video.content = { ...this.videoForm }
          this.showToastMessage('success', '视频内容已保存')
        }
      }
    },
    
    // 保存习题
    saveExercise() {
      if (!this.exerciseForm.content.trim()) {
        this.showToastMessage('warning', '请输入题目内容')
        return
      }
      
      if (this.showOptions) {
        const validOptions = this.exerciseForm.options.filter(opt => opt.trim())
        if (validOptions.length < 2) {
          this.showToastMessage('warning', '至少需要2个有效选项')
          return
        }
        
        if (this.exerciseForm.correctAnswers.length === 0) {
          this.showToastMessage('warning', '请选择正确答案')
          return
        }
      }
      
      const exerciseData = { ...this.exerciseForm }
      
      if (this.exerciseForm.id) {
        // 更新现有习题
        const index = this.existingExercises.findIndex(e => e.id === this.exerciseForm.id)
        if (index !== -1) {
          this.existingExercises[index] = exerciseData
        }
      } else {
        // 添加新习题
        exerciseData.id = Date.now()
        this.existingExercises.push(exerciseData)
      }
      
      // 保存到当前选中的内容
      const chapter = this.chapters.find(c => c.id === this.activeChapterId)
      if (chapter) {
        const exercise = chapter.exercises.find(e => e.id === this.activeContentId)
        if (exercise) {
          exercise.content = exerciseData
        }
      }
      
      this.showToastMessage('success', '习题已保存')
      this.resetExerciseForm()
    },
    
    // 编辑习题
    editExercise(exercise) {
      this.loadExerciseForm(exercise)
    },
    
    // 删除习题
    deleteExercise(id) {
      if (confirm('确定要删除这个题目吗？')) {
        const index = this.existingExercises.findIndex(e => e.id === id)
        if (index !== -1) {
          this.existingExercises.splice(index, 1)
          this.showToastMessage('success', '题目已删除')
        }
      }
    },
    
    // 获取习题类型文本
    getExerciseTypeText(type) {
      const typeMap = {
        single: '单选题',
        multiple: '多选题',
        judge: '判断题',
        fill: '填空题',
        short: '简答题'
      }
      return typeMap[type] || '未知类型'
    }
  }
}
</script>

<style scoped>
/* 继承HTML文件中的样式 */


/* 自定义滚动条 */
.sticky {
  position: -webkit-sticky;
  position: sticky;
}

/* 旋转动画 */
.rotate-180 {
  transform: rotate(180deg);
}


</style>