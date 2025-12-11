<template>
  <div class="min-h-screen bg-gray-100">
    <!-- 面包屑导航 -->
    <div class="container">
      <nav class="breadcrumb">
        <router-link to="/">首页</router-link> > 
        <router-link to="/courses?category=computer">计算机考研</router-link> > 
        <router-link to="/courses?category=os">操作系统</router-link> > 
        <router-link :to="`/course/${courseId}/player`" @click="goBackToVideo">返回视频</router-link> > 
        <span>{{ exerciseSeries.title }}</span>
      </nav>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="container">
      <div class="loading-container">
        <div class="loading-spinner">
          <i class="fa fa-spinner fa-spin"></i>
        </div>
        <p class="loading-text">正在加载习题集...</p>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div v-else class="container">
      <div class="main-layout">
        <!-- 左侧列 - 习题集内容 -->
        <div class="left-column">
          <!-- 习题集头部 -->
          <div class="exercise-header">
            <div class="exercise-series-info">
              <h1 class="exercise-series-title">{{ exerciseSeries.title }}</h1>
              <div class="exercise-series-meta">
                <span class="exercise-series-count">共 {{ exerciseSeries.questions.length }} 题</span>
                <span class="exercise-series-difficulty" :data-difficulty="exerciseSeries.difficulty">
                  {{ exerciseSeries.difficulty }}
                </span>
                <span class="exercise-series-points">总分: {{ exerciseSeries.totalPoints }}分</span>
              </div>
            </div>
            
            <!-- 习题进度条 -->
            <div class="series-progress">
              <div class="progress-info">
                <span>已完成 {{ answeredQuestionsCount }} / {{ exerciseSeries.questions.length }} 题</span>
                <span>{{ Math.round((answeredQuestionsCount / exerciseSeries.questions.length) * 100) }}%</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: (answeredQuestionsCount / exerciseSeries.questions.length) * 100 + '%' }"></div>
              </div>
            </div>
            
            <!-- 提交按钮 -->
            <div class="submit-header" v-if="!isSubmitted">
              <button 
                class="btn btn-primary submit-all-btn" 
                @click="submitSeries"
                :disabled="!isAllAnswered"
                :class="{ 'btn-success': isAllAnswered }"
              >
                <i class="fa fa-paper-plane"></i>
                提交全部答案 ({{ answeredQuestionsCount }}/{{ exerciseSeries.questions.length }})
              </button>
              
              <div class="submit-hint" v-if="!isAllAnswered">
                <i class="fa fa-info-circle text-blue-500"></i>
                请完成所有题目后再提交
              </div>
            </div>
            
            <!-- 提交后显示总分 -->
            <div class="score-header" v-else>
              <div class="score-display">
                <div class="score-title">本次得分</div>
                <div class="score-value">{{ seriesScore }}<span class="score-total">/{{ exerciseSeries.totalPoints }}</span></div>
                <div class="score-accuracy">正确率: {{ Math.round((correctAnswersCount / exerciseSeries.questions.length) * 100) }}%</div>
              </div>
            </div>
          </div>
          
          <!-- 所有题目列表 -->
          <div class="questions-list">
            <div 
              v-for="(question, index) in exerciseSeries.questions" 
              :key="question.id || index"
              class="question-card"
              :class="{ 
                'answered': userAnswers[index] !== null,
                'current': currentQuestionIndex === index,
                'correct': isSubmitted && userAnswers[index] !== null && checkAnswerCorrect(question, index),
                'incorrect': isSubmitted && userAnswers[index] !== null && !checkAnswerCorrect(question, index),
                'not-answered': isSubmitted && userAnswers[index] === null
              }"
              @click="scrollToQuestion(index)"
            >
              <!-- 题目头部 -->
              <div class="question-card-header">
                <div class="question-card-title">
                  <span class="question-number">第{{ index + 1 }}题</span>
                  <span class="question-points">{{ question.points }}分</span>
                  <span class="question-type">{{ question.type }}</span>
                </div>
                
                <div class="question-card-status">
                  <span v-if="userAnswers[index] !== null && !isSubmitted" class="status-answered">
                    <i class="fa fa-check-circle text-green-500"></i>
                    已作答
                  </span>
                  <span v-else-if="userAnswers[index] === null && !isSubmitted" class="status-not-answered">
                    <i class="fa fa-circle text-gray-300"></i>
                    未作答
                  </span>
                  <span v-else-if="isSubmitted && userAnswers[index] !== null && checkAnswerCorrect(question, index)" 
                        class="status-correct">
                    <i class="fa fa-check-circle text-green-500"></i>
                    {{ question.points }}分
                  </span>
                  <span v-else-if="isSubmitted && userAnswers[index] !== null && !checkAnswerCorrect(question, index)" 
                        class="status-incorrect">
                    <i class="fa fa-times-circle text-red-500"></i>
                    0分
                  </span>
                  <span v-else class="status-not-answered">
                    <i class="fa fa-times-circle text-red-500"></i>
                    未作答
                  </span>
                </div>
              </div>
              
              <!-- 题目内容 -->
              <div class="question-card-content">
                <div class="question-text">
                  {{ question.question }}
                </div>
                
                <!-- 选项 -->
                <div class="options-list">
                  <div 
                    v-for="(option, optionIndex) in question.options" 
                    :key="optionIndex"
                    class="option-item"
                    :class="{ 
                      'selected': isOptionSelected(index, optionIndex),
                      'correct-answer': isSubmitted && optionIndex === getCorrectAnswer(question),
                      'user-answer': isSubmitted && userAnswers[index] !== null && (
                        (question.type === '多选题' && Array.isArray(userAnswers[index]) && userAnswers[index].includes(optionIndex)) ||
                        (question.type !== '多选题' && userAnswers[index] === optionIndex)
                      ),
                      'wrong-answer': isSubmitted && userAnswers[index] !== null && !checkAnswerCorrect(question, index) && (
                        (question.type === '多选题' && Array.isArray(userAnswers[index]) && userAnswers[index].includes(optionIndex)) ||
                        (question.type !== '多选题' && userAnswers[index] === optionIndex)
                      )
                    }"
                    @click.stop="selectOption(index, optionIndex)"
                  >
                    <div class="option-letter">
                      {{ String.fromCharCode(65 + optionIndex) }}
                    </div>
                    <div class="option-content">
                      {{ option }}
                    </div>
                    <div class="option-status">
                      <i v-if="isSubmitted && optionIndex === getCorrectAnswer(question)" 
                         class="fa fa-check text-green-500"></i>
                      <i v-if="isSubmitted && userAnswers[index] !== null && !checkAnswerCorrect(question, index) && 
                        ((question.type === '多选题' && Array.isArray(userAnswers[index]) && userAnswers[index].includes(optionIndex)) ||
                         (question.type !== '多选题' && userAnswers[index] === optionIndex))" 
                         class="fa fa-times text-red-500"></i>
                    </div>
                  </div>
                </div>
                
                <!-- 答案解析（提交后显示） -->
                <div class="question-analysis" v-if="isSubmitted">
                  <div class="analysis-header">
                    <i class="fa fa-chart-bar text-blue-500"></i>
                    答案解析
                  </div>
                  <div class="analysis-content">
                    <p v-if="userAnswers[index] !== null">
                      <strong>你的答案：</strong>
                      <span v-if="question.type === '多选题'">
                        {{ formatMultiChoiceAnswer(userAnswers[index]) }}
                      </span>
                      <span v-else>
                        {{ String.fromCharCode(65 + userAnswers[index]) }}
                      </span>
                    </p>
                    <p v-else>
                      <strong class="text-red-500">未作答</strong>
                    </p>
                    <p>
                      <strong>正确答案：</strong>
                      <span v-if="question.type === '多选题'">
                        {{ formatMultiChoiceAnswer(getCorrectAnswer(question)) }}
                      </span>
                      <span v-else>
                        {{ String.fromCharCode(65 + getCorrectAnswer(question)) }}
                      </span>
                    </p>
                    <p class="analysis-explanation">
                      {{ question.explanation }}
                    </p>
                    <div class="knowledge-points" v-if="question.knowledgePoints && question.knowledgePoints.length > 0">
                      <strong>知识点：</strong>
                      <span class="knowledge-tag" v-for="point in question.knowledgePoints" :key="point">
                        {{ point }}
                      </span>
                    </div>
                  </div>
                </div>
                
                <!-- 提示（提交前可点击显示） -->
                <div class="question-hint" v-if="!isSubmitted">
                  <button class="hint-toggle" @click.stop="toggleHint(index)">
                    <i class="fa fa-lightbulb text-yellow-500"></i>
                    {{ showHints[index] ? '隐藏提示' : '显示提示' }}
                  </button>
                  <div class="hint-content" v-if="showHints[index]">
                    {{ question.hint }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧列 -->
        <div class="right-column">
          <!-- 课程信息卡片 -->
          <div class="course-card">
            <div class="course-card-header">
              <div class="course-author">
                <div class="course-author-avatar">👤</div>
                <div>
                  <div class="course-author-name">{{ instructor.name }}</div>
                  <div class="course-author-fans">粉丝: {{ instructor.fans }}</div>
                </div>
              </div>
              <button 
                class="follow-btn-small" 
                @click="toggleFollow"
                :class="{ 'following': isFollowing }"
              >
                {{ isFollowing ? '已关注' : '关注' }}
              </button>
            </div>
            <p class="course-description">{{ instructor.description }}</p>
            <button class="enter-space-btn" @click="goToInstructorSpace">进入空间</button>
          </div>

          <!-- 学习进度统计 -->
          <div class="progress-stats">
            <div class="progress-title">
              <i class="fa fa-chart-line"></i>
              学习进度
            </div>
            <div class="progress-bar-stats">
              <div class="progress-label">
                <span>习题完成度</span>
                <span>{{ answeredQuestionsCount }} / {{ exerciseSeries.questions.length }}</span>
              </div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill" :style="{ width: (answeredQuestionsCount / exerciseSeries.questions.length) * 100 + '%' }"></div>
              </div>
              <div class="progress-percentage">{{ Math.round((answeredQuestionsCount / exerciseSeries.questions.length) * 100) }}%</div>
            </div>
            
            <!-- 正确率统计（提交后显示） -->
            <div class="accuracy-stats" v-if="isSubmitted">
              <div class="progress-label">
                <span>正确率</span>
                <span>{{ correctAnswersCount }} / {{ exerciseSeries.questions.length }}</span>
              </div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill" :style="{ width: (correctAnswersCount / exerciseSeries.questions.length) * 100 + '%' }"></div>
              </div>
              <div class="progress-percentage">{{ Math.round((correctAnswersCount / exerciseSeries.questions.length) * 100) }}%</div>
            </div>
            
            <!-- 用时统计 -->
            <div class="time-stats" v-if="isSubmitted">
              <div class="progress-label">
                <span>答题用时</span>
                <span>{{ formatTime(timeSpent) }}</span>
              </div>
            </div>
          </div>

          <!-- 题目导航 -->
          <div class="question-navigation-card">
            <div class="nav-header">
              <h4>📝 题目导航</h4>
              <span>{{ answeredQuestionsCount }}/{{ exerciseSeries.questions.length }}</span>
            </div>
            <div class="nav-grid">
              <div 
                v-for="(question, index) in exerciseSeries.questions" 
                :key="index"
                class="nav-item"
                :class="{
                  'current': currentQuestionIndex === index,
                  'answered': userAnswers[index] !== null,
                  'correct': isSubmitted && userAnswers[index] !== null && checkAnswerCorrect(question, index),
                  'incorrect': isSubmitted && userAnswers[index] !== null && !checkAnswerCorrect(question, index),
                  'not-answered': isSubmitted && userAnswers[index] === null
                }"
                @click="scrollToQuestion(index)"
              >
                {{ index + 1 }}
              </div>
            </div>
            <div class="nav-legend">
              <div class="legend-item">
                <span class="legend-color current"></span>
                <span>当前</span>
              </div>
              <div class="legend-item">
                <span class="legend-color answered"></span>
                <span>已答</span>
              </div>
              <div class="legend-item">
                <span class="legend-color not-answered"></span>
                <span>未答</span>
              </div>
              <div class="legend-item" v-if="isSubmitted">
                <span class="legend-color correct"></span>
                <span>正确</span>
              </div>
              <div class="legend-item" v-if="isSubmitted">
                <span class="legend-color incorrect"></span>
                <span>错误</span>
              </div>
            </div>

            <div class="back-to-video-section">
              <button class="btn btn-outline back-to-video-btn" @click="goBackToVideo">
                <i class="fa fa-play-circle"></i>
                  返回视频学习
                </button>
              </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 学习反馈弹窗 -->
    <div v-if="showFeedbackModal" class="feedback-modal-overlay" @click="closeFeedbackModal">
      <div class="feedback-modal" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">
            <i class="fa" :class="feedbackIcon"></i>
            {{ feedbackTitle }}
          </h3>
          <button class="modal-close" @click="closeFeedbackModal">
            <i class="fa fa-times"></i>
          </button>
        </div>
        
        <div class="modal-content">
          <div class="feedback-score">
            <div class="score-circle" :class="feedbackScoreClass">
              <span class="score-value">{{ Math.round((seriesScore / exerciseSeries.totalPoints) * 100) }}</span>
              <div class="score-label">总分</div>
            </div>
          </div>
          
          <div class="performance-summary">
            <div class="summary-item">
              <div class="summary-icon correct">
                <i class="fa fa-check-circle"></i>
              </div>
              <div class="summary-content">
                <div class="summary-label">正确题数</div>
                <div class="summary-value">{{ correctAnswersCount }}/{{ exerciseSeries.questions.length }}</div>
              </div>
            </div>
            <div class="summary-item">
              <div class="summary-icon score">
                <i class="fa fa-star"></i>
              </div>
              <div class="summary-content">
                <div class="summary-label">获得分数</div>
                <div class="summary-value">{{ seriesScore }}/{{ exerciseSeries.totalPoints }}</div>
              </div>
            </div>
            <div class="summary-item">
              <div class="summary-icon time">
                <i class="fa fa-clock"></i>
              </div>
              <div class="summary-content">
                <div class="summary-label">答题用时</div>
                <div class="summary-value">{{ formatTime(timeSpent) }}</div>
              </div>
            </div>
          </div>
          
          <div class="feedback-message">
            <p class="message-text">{{ feedbackMessage }}</p>
          </div>
          
          <div class="feedback-suggestions">
            <h4 class="suggestions-title">
              <i class="fa fa-lightbulb"></i>
              个性化学习建议
            </h4>
            <ul class="suggestions-list">
              <li v-for="(suggestion, index) in feedbackSuggestions" :key="index">
                <i class="fa fa-check-circle"></i>
                {{ suggestion }}
              </li>
            </ul>
          </div>
          
          <div class="knowledge-mastery" v-if="knowledgePoints.length > 0">
            <h4 class="knowledge-title">
              <i class="fa fa-graduation-cap"></i>
              知识点掌握情况
            </h4>
            <div class="knowledge-list">
              <div 
                v-for="(point, index) in knowledgePoints" 
                :key="index"
                class="knowledge-item"
                :class="{ 'mastered': point.mastery >= 80, 'need-practice': point.mastery < 80 && point.mastery >= 60, 'need-review': point.mastery < 60 }"
              >
                <div class="knowledge-info">
                  <span class="knowledge-name">{{ point.name }}</span>
                  <span class="knowledge-mastery">{{ point.mastery }}%</span>
                </div>
                <div class="knowledge-progress">
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: point.mastery + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="btn btn-primary" @click="handleFeedbackAction">
            <i class="fa" :class="feedbackActionIcon"></i>
            {{ feedbackActionText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'ExerciseSeries',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // 路由参数
    const courseId = ref(route.params.courseId || 1)
    const seriesId = ref(route.params.seriesId || 'series_1_1')
    
    // 加载状态
    const isLoading = ref(true)
    
    // 习题集状态 - 设置默认值
    const exerciseSeries = ref({
      id: '',
      title: '加载中...',
      difficulty: '简单',
      totalPoints: 0,
      questions: []
    })
    
    const userAnswers = ref([])
    const showHints = ref({})
    const isSubmitted = ref(false)
    const timeSpent = ref(0)
    const startTime = ref(null)
    const currentQuestionIndex = ref(0)
    
    // 学习反馈弹窗
    const showFeedbackModal = ref(false)
    
    // 互动状态
    const isFollowing = ref(false)
    
    // 讲师数据
    const instructor = ref({
      name: '王道计算机',
      fans: '123.0万',
      description: '感谢你我是计算机专业学子...'
    })
    
    // 习题集数据
    const exerciseSeriesData = {
      'series_1_1': {
        id: 'series_1_1',
        title: '1.1 课后习题集：机器学习基本概念',
        difficulty: '简单',
        totalPoints: 50,
        questions: [
          {
            id: 1,
            question: '下列哪项不属于机器学习的主要任务类型？',
            type: '单选题',
            options: ['A. 分类', 'B. 回归', 'C. 聚类', 'D. 编译'],
            correctAnswer: 3,
            points: 10,
            hint: '机器学习主要解决分类、回归、聚类等问题，编译是编程语言处理过程。',
            explanation: '机器学习的主要任务包括分类、回归、聚类、降维等。编译是将源代码转换为机器代码的过程，属于编译器领域，不属于机器学习任务。',
            knowledgePoints: ['机器学习基本概念', '任务类型']
          },
          {
            id: 2,
            question: '机器学习中的"过拟合"指的是什么？',
            type: '单选题',
            options: [
              'A. 模型在训练集上表现很好，但在测试集上表现差',
              'B. 模型在训练集和测试集上都表现差',
              'C. 模型过于简单，无法捕捉数据特征',
              'D. 模型训练时间过长'
            ],
            correctAnswer: 0,
            points: 10,
            hint: '过拟合是模型过度学习了训练数据的噪声和细节。',
            explanation: '过拟合是指模型在训练数据上表现很好，但在未见过的测试数据上表现较差，通常是因为模型过于复杂或训练数据不足。',
            knowledgePoints: ['过拟合', '模型评估']
          },
          {
            id: 3,
            question: '监督学习和无监督学习的主要区别是什么？',
            type: '单选题',
            options: [
              'A. 是否有标签数据',
              'B. 是否使用神经网络',
              'C. 是否需要训练',
              'D. 是否有输出结果'
            ],
            correctAnswer: 0,
            points: 10,
            hint: '关注数据是否有预先标注的标签。',
            explanation: '监督学习使用有标签的数据进行训练，而无监督学习使用无标签的数据。',
            knowledgePoints: ['监督学习', '无监督学习']
          },
          {
            id: 4,
            question: '下列哪项是常见的机器学习算法？',
            type: '多选题',
            options: ['A. 决策树', 'B. 支持向量机', 'C. K-means聚类', 'D. 线性回归'],
            correctAnswer: [0, 1, 2, 3],
            points: 10,
            hint: '这些都是经典的机器学习算法。',
            explanation: '决策树、支持向量机、K-means聚类和线性回归都是常见的机器学习算法。',
            knowledgePoints: ['机器学习算法']
          },
          {
            id: 5,
            question: '机器学习的核心目标是什么？',
            type: '单选题',
            options: [
              'A. 让计算机自动从数据中学习规律',
              'B. 编写复杂的程序',
              'C. 提高计算速度',
              'D. 减少存储空间'
            ],
            correctAnswer: 0,
            points: 10,
            hint: '机器学习关注的是从数据中学习的能力。',
            explanation: '机器学习的核心目标是让计算机能够自动从数据中学习规律和模式，而不是通过明确的编程指令。',
            knowledgePoints: ['机器学习目标']
          }
        ]
      },
      'series_1_2': {
        id: 'series_1_2',
        title: '1.2 课后习题集：监督学习算法',
        difficulty: '中等',
        totalPoints: 60,
        questions: [
          {
            id: 1,
            question: '在监督学习中，以下哪种算法可以用于处理非线性分类问题？',
            type: '单选题',
            options: [
              'A. 线性回归',
              'B. 决策树',
              'C. K-近邻算法',
              'D. 支持向量机'
            ],
            correctAnswer: 3,
            points: 10,
            hint: '注意题目问的是"非线性分类问题"，线性回归主要用于回归任务。',
            explanation: '支持向量机通过核函数可以处理非线性分类问题，决策树和K-近邻算法也可以处理非线性分类，但题目问的是最适合处理非线性分类的算法。',
            knowledgePoints: ['监督学习算法', '非线性分类']
          }
        ]
      },
      'series_1_3': {
        id: 'series_1_3',
        title: '1.3 课后习题集：实际应用分析',
        difficulty: '困难',
        totalPoints: 40,
        questions: [
          {
            id: 1,
            question: '在图像识别任务中，以下哪种神经网络结构最适合？',
            type: '单选题',
            options: [
              'A. 全连接神经网络',
              'B. 循环神经网络',
              'C. 卷积神经网络',
              'D. 自编码器'
            ],
            correctAnswer: 2,
            points: 10,
            hint: '考虑不同神经网络结构的特点和适用场景。',
            explanation: '卷积神经网络（CNN）通过卷积层可以提取图像的局部特征，池化层可以减少参数数量，特别适合图像识别任务。循环神经网络更适合序列数据，自编码器用于特征学习。',
            knowledgePoints: ['深度学习', '计算机视觉']
          }
        ]
      }
    }
    
    // 计算属性 - 添加空值检查
    const answeredQuestionsCount = computed(() => {
      if (!exerciseSeries.value || !exerciseSeries.value.questions) return 0
      return userAnswers.value.filter(answer => answer !== null).length
    })
    
    const isAllAnswered = computed(() => {
      if (!exerciseSeries.value || !exerciseSeries.value.questions) return false
      return answeredQuestionsCount.value === exerciseSeries.value.questions.length
    })
    
    const correctAnswersCount = computed(() => {
      if (!exerciseSeries.value || !exerciseSeries.value.questions || !isSubmitted.value) return 0
      
      return exerciseSeries.value.questions.reduce((count, question, index) => {
        const userAnswer = userAnswers.value[index]
        if (userAnswer === null) return count
        
        return checkAnswerCorrect(question, index) ? count + 1 : count
      }, 0)
    })
    
    const seriesScore = computed(() => {
      if (!exerciseSeries.value || !exerciseSeries.value.questions || !isSubmitted.value) return 0
      
      return exerciseSeries.value.questions.reduce((score, question, index) => {
        const userAnswer = userAnswers.value[index]
        if (userAnswer === null) return score
        
        return checkAnswerCorrect(question, index) ? score + question.points : score
      }, 0)
    })
    
    const wrongQuestionsCount = computed(() => {
      if (!exerciseSeries.value || !exerciseSeries.value.questions || !isSubmitted.value) return 0
      return exerciseSeries.value.questions.length - correctAnswersCount.value
    })
    
    // 反馈弹窗计算属性 - 添加空值检查
    const feedbackTitle = computed(() => {
      if (!exerciseSeries.value || !exerciseSeries.value.questions) return '加载中...'
      const accuracy = (correctAnswersCount.value / exerciseSeries.value.questions.length) * 100
      if (accuracy >= 80) return '🎉 优秀！完成得很棒！'
      if (accuracy >= 60) return '👍 不错！继续加油！'
      return '💡 需要加强练习哦'
    })
    
    const feedbackIcon = computed(() => {
      if (!exerciseSeries.value || !exerciseSeries.value.questions) return 'fa-spinner fa-spin'
      const accuracy = (correctAnswersCount.value / exerciseSeries.value.questions.length) * 100
      if (accuracy >= 80) return 'fa-trophy'
      if (accuracy >= 60) return 'fa-check-circle'
      return 'fa-exclamation-circle'
    })
    
    const feedbackScoreClass = computed(() => {
      if (!exerciseSeries.value || !exerciseSeries.value.questions) return 'score-poor'
      const accuracy = (correctAnswersCount.value / exerciseSeries.value.questions.length) * 100
      if (accuracy >= 80) return 'score-excellent'
      if (accuracy >= 60) return 'score-good'
      return 'score-poor'
    })
    
    const feedbackMessage = computed(() => {
      if (!exerciseSeries.value || !exerciseSeries.value.questions) return '正在加载数据...'
      const accuracy = (correctAnswersCount.value / exerciseSeries.value.questions.length) * 100
      const points = seriesScore.value
      const totalPoints = exerciseSeries.value.totalPoints
      
      if (accuracy >= 90) {
        return `太出色了！你答对了${correctAnswersCount.value}题，获得了${points}/${totalPoints}分，说明你对这个知识点掌握得非常扎实！`
      } else if (accuracy >= 70) {
        return `做得不错！你答对了${correctAnswersCount.value}题，获得了${points}/${totalPoints}分，大部分知识点已经掌握，只有少量需要加强。`
      } else if (accuracy >= 50) {
        return `需要继续努力！你答对了${correctAnswersCount.value}题，获得了${points}/${totalPoints}分，建议回顾相关知识点。`
      } else {
        return `需要认真学习！你只答对了${correctAnswersCount.value}题，获得了${points}/${totalPoints}分，建议重新学习本章内容。`
      }
    })
    
    const feedbackSuggestions = computed(() => {
      if (!exerciseSeries.value || !exerciseSeries.value.questions) return []
      
      const accuracy = (correctAnswersCount.value / exerciseSeries.value.questions.length) * 100
      const suggestions = []
      
      if (accuracy >= 80) {
        suggestions.push('继续保持，可以挑战更高难度的习题')
        suggestions.push('尝试将学到的知识应用到实际项目中')
        suggestions.push('帮助其他同学解答疑问，巩固知识')
      } else if (accuracy >= 60) {
        suggestions.push('回顾错题，理解错误原因')
        suggestions.push('重新学习相关视频内容，加深理解')
        suggestions.push('多做同类型练习题，提升熟练度')
      } else {
        suggestions.push('强烈建议重新观看本章节的所有视频')
        suggestions.push('建立错题本，定期复习')
        suggestions.push('向老师或同学请教不理解的知识点')
      }
      
      // 基于用时给出建议
      const avgTimePerQuestion = timeSpent.value / exerciseSeries.value.questions.length
      if (avgTimePerQuestion > 120) {
        suggestions.push('答题速度较慢，需要提升对知识点的熟练程度')
      } else if (avgTimePerQuestion < 30) {
        suggestions.push('答题速度很快，但要注意审题的准确性')
      }
      
      // 基于难度给出建议
      if (exerciseSeries.value.difficulty === '困难') {
        suggestions.push('困难题目需要更深入的理解和更多的练习')
      }
      
      return suggestions.slice(0, 3)
    })
    
    const knowledgePoints = computed(() => {
      if (!exerciseSeries.value || !exerciseSeries.value.questions) return []
      
      const knowledgeMap = {}
      
      // 统计每个知识点的答题情况
      exerciseSeries.value.questions.forEach((question, index) => {
        const userAnswer = userAnswers.value[index]
        const isCorrect = userAnswer !== null && checkAnswerCorrect(question, index)
        
        if (question.knowledgePoints && question.knowledgePoints.length > 0) {
          question.knowledgePoints.forEach(point => {
            if (!knowledgeMap[point]) {
              knowledgeMap[point] = { total: 0, correct: 0 }
            }
            knowledgeMap[point].total += 1
            if (isCorrect) {
              knowledgeMap[point].correct += 1
            }
          })
        }
      })
      
      // 计算掌握程度
      return Object.entries(knowledgeMap).map(([name, data]) => ({
        name,
        mastery: Math.round((data.correct / data.total) * 100)
      }))
    })
    
    const feedbackActionText = computed(() => {
      return '返回视频界面'
    })
    
    const feedbackActionIcon = computed(() => {
      return 'fa-play-circle'
    })
    
    // 方法
    const checkAnswerCorrect = (question, index) => {
      const userAnswer = userAnswers.value[index]
      if (userAnswer === null) return false
      
      if (question.type === '多选题') {
        const userSet = new Set(Array.isArray(userAnswer) ? userAnswer : [userAnswer])
        const correctSet = new Set(Array.isArray(question.correctAnswer) ? question.correctAnswer : [question.correctAnswer])
        return userSet.size === correctSet.size && [...userSet].every(val => correctSet.has(val))
      }
      
      return userAnswer === question.correctAnswer
    }
    
    const getCorrectAnswer = (question) => {
      return question.correctAnswer
    }
    
    const formatMultiChoiceAnswer = (answer) => {
      if (Array.isArray(answer)) {
        return answer.map(index => String.fromCharCode(65 + index)).join('、')
      }
      return String.fromCharCode(65 + answer)
    }
    
    const isOptionSelected = (questionIndex, optionIndex) => {
      const userAnswer = userAnswers.value[questionIndex]
      if (userAnswer === null) return false
      
      if (Array.isArray(userAnswer)) {
        return userAnswer.includes(optionIndex)
      }
      
      return userAnswer === optionIndex
    }
    
    const selectOption = (questionIndex, optionIndex) => {
      if (isSubmitted.value) return
      
      const question = exerciseSeries.value.questions[questionIndex]
      
      if (question.type === '多选题') {
        // 多选题逻辑
        let currentAnswers = userAnswers.value[questionIndex]
        if (currentAnswers === null) {
          currentAnswers = []
        } else if (!Array.isArray(currentAnswers)) {
          currentAnswers = [currentAnswers]
        }
        
        if (currentAnswers.includes(optionIndex)) {
          // 取消选择
          userAnswers.value[questionIndex] = currentAnswers.filter(i => i !== optionIndex)
          if (userAnswers.value[questionIndex].length === 0) {
            userAnswers.value[questionIndex] = null
          }
        } else {
          // 添加选择
          userAnswers.value[questionIndex] = [...currentAnswers, optionIndex]
        }
      } else {
        // 单选题逻辑 - 直接替换
        userAnswers.value[questionIndex] = optionIndex
      }
      
      // 保存到本地存储
      saveProgress()
    }
    
    const toggleHint = (index) => {
      showHints.value[index] = !showHints.value[index]
    }
    
    const scrollToQuestion = (index) => {
      currentQuestionIndex.value = index
      const element = document.querySelector(`.question-card:nth-child(${index + 1})`)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' })
        // 添加高亮效果
        element.classList.add('highlight')
        setTimeout(() => {
          element.classList.remove('highlight')
        }, 1000)
      }
    }
    
    const submitSeries = () => {
      if (!isAllAnswered.value) {
        alert(`请先完成所有题目 (${answeredQuestionsCount.value}/${exerciseSeries.value.questions.length})`)
        return
      }
      
      // 计算用时
      const endTime = Date.now()
      timeSpent.value = Math.round((endTime - startTime.value) / 1000)
      
      // 标记为已提交
      isSubmitted.value = true
      
      // 保存提交状态
      saveProgress()
      
      // 显示学习反馈弹窗
      setTimeout(() => {
        showFeedbackModal.value = true
      }, 800)
    }
    
    const resetSeries = () => {
      if (confirm('确定要重新开始练习吗？这将清除所有答案。')) {
        userAnswers.value = new Array(exerciseSeries.value.questions.length).fill(null)
        showHints.value = {}
        isSubmitted.value = false
        timeSpent.value = 0
        startTime.value = Date.now()
        
        // 清除本地存储
        localStorage.removeItem(`series_${seriesId.value}_progress`)
        
        // 滚动到顶部
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }
    
    
    const handleFeedbackAction = () => {
      showFeedbackModal.value = false
      goBackToVideo()
    }
    
    const closeFeedbackModal = () => {
      showFeedbackModal.value = false
    }
    
    const goBackToVideo = () => {
      router.push(`/course/${courseId.value}/player`)
    }
    
    const goToInstructorSpace = () => {
      alert('进入讲师空间功能开发中')
    }
    
    const toggleFollow = () => {
      isFollowing.value = !isFollowing.value
      alert(isFollowing.value ? '已关注讲师' : '已取消关注')
    }
    
    const formatTime = (seconds) => {
      if (!seconds) return '0秒'
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      if (mins > 0) {
        return `${mins}分${secs}秒`
      }
      return `${secs}秒`
    }
    
    // 保存进度
    const saveProgress = () => {
      const progress = {
        userAnswers: userAnswers.value,
        showHints: showHints.value,
        isSubmitted: isSubmitted.value,
        timeSpent: timeSpent.value,
        startTime: startTime.value
      }
      localStorage.setItem(`series_${seriesId.value}_progress`, JSON.stringify(progress))
    }
    
    // 加载进度
    const loadProgress = () => {
      const savedProgress = localStorage.getItem(`series_${seriesId.value}_progress`)
      if (savedProgress) {
        try {
          const progress = JSON.parse(savedProgress)
          userAnswers.value = progress.userAnswers || []
          showHints.value = progress.showHints || {}
          isSubmitted.value = progress.isSubmitted || false
          timeSpent.value = progress.timeSpent || 0
          startTime.value = progress.startTime || Date.now()
        } catch (e) {
          console.error('加载进度失败:', e)
          userAnswers.value = new Array(exerciseSeries.value.questions.length).fill(null)
          startTime.value = Date.now()
        }
      } else {
        userAnswers.value = new Array(exerciseSeries.value.questions.length).fill(null)
        startTime.value = Date.now()
      }
    }
    
    // 初始化
    const initialize = () => {
      isLoading.value = true
      
      // 模拟数据加载延迟
      setTimeout(() => {
        // 加载习题集数据
        const seriesData = exerciseSeriesData[seriesId.value]
        if (seriesData) {
          exerciseSeries.value = seriesData
        } else {
          // 如果找不到对应的习题集，使用第一个作为默认
          exerciseSeries.value = exerciseSeriesData['series_1_1']
        }
        
        // 加载进度
        loadProgress()
        
        isLoading.value = false
      }, 300) // 300ms的加载延迟
    }
    
    // 键盘事件处理
    const handleKeydown = (event) => {
      switch (event.key) {
        case 'Escape':
          if (showFeedbackModal.value) {
            closeFeedbackModal()
          }
          break
      }
    }
    
    // 初始化Font Awesome
    const initFontAwesome = () => {
      if (!document.querySelector('link[href*="font-awesome"]')) {
        const link = document.createElement('link')
        link.rel = 'stylesheet'
        link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
        document.head.appendChild(link)
      }
    }
    
    // 生命周期钩子
    onMounted(() => {
      initFontAwesome()
      initialize()
      
      // 添加事件监听器
      document.addEventListener('keydown', handleKeydown)
    })
    
    onBeforeUnmount(() => {
      // 移除事件监听器
      document.removeEventListener('keydown', handleKeydown)
    })
    
    return {
      // 路由参数
      courseId,
      seriesId,
      
      // 状态
      isLoading,
      exerciseSeries,
      userAnswers,
      showHints,
      isSubmitted,
      timeSpent,
      currentQuestionIndex,
      showFeedbackModal,
      isFollowing,
      instructor,
      
      // 计算属性
      answeredQuestionsCount,
      isAllAnswered,
      correctAnswersCount,
      seriesScore,
      wrongQuestionsCount,
      feedbackTitle,
      feedbackIcon,
      feedbackScoreClass,
      feedbackMessage,
      feedbackSuggestions,
      knowledgePoints,
      feedbackActionText,
      feedbackActionIcon,
      
      // 方法
      checkAnswerCorrect,
      getCorrectAnswer,
      formatMultiChoiceAnswer,
      isOptionSelected,
      selectOption,
      toggleHint,
      scrollToQuestion,
      submitSeries,
      resetSeries,
      handleFeedbackAction,
      closeFeedbackModal,
      goBackToVideo,
      goToInstructorSpace,
      toggleFollow,
      formatTime
    }
  }
}
</script>

<style scoped>
/* 加载状态样式 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  background: white;
  border-radius: 12px;
  margin: 20px 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.loading-spinner {
  font-size: 48px;
  color: #1890ff;
  margin-bottom: 20px;
}

.loading-text {
  font-size: 16px;
  color: #666;
}

/* 基础样式 */
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.min-h-screen {
  min-height: 100vh;
}

.bg-gray-100 {
  background-color: #f5f5f5;
}

/* 面包屑导航 */
.breadcrumb {
  padding: 15px 0;
  font-size: 14px;
  color: #666;
}

.breadcrumb a {
  color: #666;
  text-decoration: none;
}

.breadcrumb a:hover {
  color: #1890ff;
}

/* 主布局 */
.main-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 20px;
  margin-bottom: 40px;
}

/* 习题集头部 */
.exercise-header {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.exercise-series-info {
  margin-bottom: 20px;
}

.exercise-series-title {
  font-size: 28px;
  color: #333;
  margin-bottom: 12px;
  font-weight: 600;
}

.exercise-series-meta {
  display: flex;
  gap: 15px;
  align-items: center;
  font-size: 14px;
  color: #666;
}

.exercise-series-count {
  background: #f0f0f0;
  padding: 6px 12px;
  border-radius: 20px;
}

.exercise-series-difficulty {
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 500;
}

.exercise-series-difficulty[data-difficulty="简单"] {
  background: #f6ffed;
  color: #52c41a;
}

.exercise-series-difficulty[data-difficulty="中等"] {
  background: #fff7e6;
  color: #fa8c16;
}

.exercise-series-difficulty[data-difficulty="困难"] {
  background: #fff1f0;
  color: #f5222d;
}

.exercise-series-points {
  background: #f0f9ff;
  color: #1890ff;
  padding: 6px 12px;
  border-radius: 20px;
}

/* 习题进度条 */
.series-progress {
  margin-bottom: 20px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.progress-bar {
  height: 10px;
  background: #f0f0f0;
  border-radius: 5px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #1890ff, #52c41a);
  border-radius: 5px;
  transition: width 0.5s ease;
}

/* 提交头部 */
.submit-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.submit-all-btn {
  padding: 12px 32px;
  font-size: 16px;
  border-radius: 8px;
  font-weight: 500;
}

.submit-all-btn.btn-success {
  background: #52c41a;
}

.submit-all-btn.btn-success:hover {
  background: #73d13d;
}

.submit-hint {
  color: #666;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 分数头部 */
.score-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: linear-gradient(135deg, #f6ffed, #f0f9ff);
  border-radius: 8px;
  border: 1px solid #b7eb8f;
}

.score-display {
  text-align: center;
}

.score-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.score-value {
  font-size: 36px;
  font-weight: bold;
  color: #52c41a;
}

.score-total {
  font-size: 20px;
  color: #666;
}

.score-accuracy {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

/* 题目列表 */
.questions-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.question-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.question-card.current {
  border-color: #1890ff;
  box-shadow: 0 0 0 3px rgba(24, 144, 255, 0.1);
}

.question-card.answered {
  border-left: 4px solid #1890ff;
}

.question-card.correct {
  border-left: 4px solid #52c41a;
}

.question-card.incorrect {
  border-left: 4px solid #f5222d;
}

.question-card.not-answered {
  border-left: 4px solid #ff4d4f;
}

.question-card.highlight {
  animation: highlight 1s ease;
}

@keyframes highlight {
  0%, 100% { background: white; }
  50% { background: #f0f9ff; }
}

/* 题目卡片头部 */
.question-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.question-card-title {
  display: flex;
  align-items: center;
  gap: 15px;
}

.question-number {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.question-points {
  background: #1890ff;
  color: white;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.question-type {
  background: #f0f0f0;
  color: #666;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
}

.question-card-status {
  font-size: 14px;
  font-weight: 500;
}

.status-answered {
  color: #52c41a;
}

.status-not-answered {
  color: #666;
}

.status-correct {
  color: #52c41a;
}

.status-incorrect {
  color: #f5222d;
}

/* 题目内容 */
.question-card-content {
  position: relative;
}

.question-text {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  margin-bottom: 25px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
}

/* 选项列表 */
.options-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  margin-bottom: 20px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 16px 20px;
  border: 2px solid #e8e8e8;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.option-item:hover {
  border-color: #1890ff;
  background: #f0f9ff;
}

.option-item.selected {
  border-color: #1890ff;
  background: #f0f9ff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.2);
}

.option-item.correct-answer {
  border-color: #52c41a;
  background: #f6ffed;
}

.option-item.user-answer {
  border-color: #1890ff;
  background: #f0f9ff;
}

.option-item.wrong-answer {
  border-color: #f5222d;
  background: #fff1f0;
}

.option-letter {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #f0f0f0;
  font-weight: bold;
  color: #666;
  flex-shrink: 0;
}

.option-item.selected .option-letter {
  background: #1890ff;
  color: white;
}

.option-item.correct-answer .option-letter {
  background: #52c41a;
  color: white;
}

.option-item.user-answer .option-letter {
  background: #1890ff;
  color: white;
}

.option-item.wrong-answer .option-letter {
  background: #f5222d;
  color: white;
}

.option-content {
  flex: 1;
  font-size: 15px;
  color: #333;
  line-height: 1.5;
}

.option-status {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* 答案解析 */
.question-analysis {
  background: #f6ffed;
  border: 1px solid #b7eb8f;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
}

.analysis-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
  color: #52c41a;
  margin-bottom: 12px;
  font-size: 16px;
}

.analysis-content {
  color: #333;
  line-height: 1.6;
}

.analysis-content p {
  margin-bottom: 8px;
}

.analysis-content strong {
  color: #1890ff;
}

.analysis-explanation {
  color: #666;
  font-style: italic;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #d9d9d9;
}

.knowledge-points {
  margin-top: 12px;
}

.knowledge-tag {
  display: inline-block;
  background: #f0f0f0;
  color: #666;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-right: 8px;
  margin-bottom: 4px;
}

/* 提示 */
.question-hint {
  margin-top: 20px;
}

.hint-toggle {
  background: #fff7e6;
  border: 1px solid #ffd591;
  color: #fa8c16;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.hint-toggle:hover {
  background: #ffe7ba;
}

.hint-content {
  background: #fff7e6;
  border: 1px solid #ffd591;
  border-radius: 6px;
  padding: 16px;
  margin-top: 10px;
  color: #666;
  line-height: 1.6;
}

/* 按钮样式 */
.btn {
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  border: none;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #1890ff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #40a9ff;
}

.btn-secondary {
  background: #f0f0f0;
  color: #666;
}

.btn-secondary:hover:not(:disabled) {
  background: #e0e0e0;
}

.btn-outline {
  background: white;
  color: #1890ff;
  border: 1px solid #1890ff;
}

.btn-outline:hover:not(:disabled) {
  background: #f0f9ff;
}

/* 右侧列 */
.right-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 课程信息卡片 */
.course-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.course-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.course-author {
  display: flex;
  gap: 12px;
  align-items: center;
}

.course-author-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.course-author-name {
  font-weight: 600;
  font-size: 15px;
}

.course-author-fans {
  font-size: 12px;
  color: #999;
}

.follow-btn-small {
  padding: 6px 16px;
  background: #f0f0f0;
  color: #666;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s ease;
}

.follow-btn-small.following {
  background: #1890ff;
  color: white;
}

.follow-btn-small:hover {
  transform: translateY(-1px);
}

.course-description {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
}

.enter-space-btn {
  width: 100%;
  padding: 10px;
  border: 1px solid #1890ff;
  background: white;
  color: #1890ff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.enter-space-btn:hover {
  background: #1890ff;
  color: white;
}

/* 学习进度统计 */
.progress-stats {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.progress-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  margin-bottom: 16px;
  color: #333;
  font-size: 16px;
}

.progress-bar-stats,
.accuracy-stats,
.time-stats {
  margin-bottom: 20px;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.progress-bar-bg {
  height: 8px;
  background: #e8e8e8;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #1890ff, #52c41a);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.progress-percentage {
  text-align: right;
  font-size: 14px;
  color: #1890ff;
  font-weight: bold;
}

.time-stats .progress-label {
  justify-content: space-between;
}

/* 题目导航卡片 */
.question-navigation-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.nav-header h4 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.nav-header span {
  color: #666;
  font-size: 14px;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.nav-item {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #f0f0f0;
  color: #666;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.nav-item.current {
  background: #1890ff;
  color: white;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.3);
}

.nav-item.answered {
  background: #1890ff;
  color: white;
}

.nav-item.correct {
  background: #52c41a;
  color: white;
}

.nav-item.incorrect {
  background: #f5222d;
  color: white;
}

.nav-item.not-answered {
  background: #ff4d4f;
  color: white;
}

.nav-legend {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  font-size: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.legend-color.current {
  background: #1890ff;
}

.legend-color.answered {
  background: #1890ff;
}

.legend-color.not-answered {
  background: #ff4d4f;
}

.legend-color.correct {
  background: #52c41a;
}

.legend-color.incorrect {
  background: #f5222d;
}

/* 学习反馈弹窗样式 */
.feedback-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
  animation: fadeIn 0.3s ease;
}

.feedback-modal {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.4s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.modal-title i {
  font-size: 24px;
}

.modal-title i.fa-trophy {
  color: #ffd700;
}

.modal-title i.fa-check-circle {
  color: #52c41a;
}

.modal-title i.fa-exclamation-circle {
  color: #fa8c16;
}

.modal-close {
  background: none;
  border: none;
  font-size: 20px;
  color: #999;
  cursor: pointer;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #f5f5f5;
  color: #333;
}

.modal-content {
  padding: 24px;
}

/* 总体评分 */
.feedback-score {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.score-circle {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.score-circle::before {
  content: '';
  position: absolute;
  top: -8px;
  left: -8px;
  right: -8px;
  bottom: -8px;
  border-radius: 50%;
  z-index: -1;
}

.score-circle.score-excellent {
  background: linear-gradient(135deg, #ffd700, #ffc107);
}

.score-circle.score-excellent::before {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 193, 7, 0.2));
}

.score-circle.score-good {
  background: linear-gradient(135deg, #1890ff, #40a9ff);
}

.score-circle.score-good::before {
  background: linear-gradient(135deg, rgba(24, 144, 255, 0.2), rgba(64, 169, 255, 0.2));
}

.score-circle.score-poor {
  background: linear-gradient(135deg, #fa8c16, #ffc069);
}

.score-circle.score-poor::before {
  background: linear-gradient(135deg, rgba(250, 140, 22, 0.2), rgba(255, 192, 105, 0.2));
}

.score-value {
  font-size: 36px;
  font-weight: bold;
  color: white;
}

.score-label {
  font-size: 16px;
  color: white;
  opacity: 0.9;
  margin-top: 4px;
}

/* 学习表现 */
.performance-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.summary-item {
  background: white;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  gap: 12px;
  align-items: center;
}

.summary-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.summary-icon.correct {
  background: #f6ffed;
  color: #52c41a;
}

.summary-icon.score {
  background: #f0f9ff;
  color: #1890ff;
}

.summary-icon.time {
  background: #fff7e6;
  color: #fa8c16;
}

.summary-content {
  flex: 1;
}

.summary-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.summary-value {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

/* 学习评价 */
.feedback-message {
  background: #f9f9f9;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.message-text {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  margin: 0;
  text-align: center;
}

/* 学习建议 */
.feedback-suggestions {
  background: #f0f9ff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.suggestions-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  color: #333;
  margin: 0 0 16px 0;
}

.suggestions-title i {
  color: #1890ff;
}

.suggestions-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.suggestions-list li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 12px;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.suggestions-list li:last-child {
  margin-bottom: 0;
}

.suggestions-list li i {
  color: #52c41a;
  margin-top: 2px;
  flex-shrink: 0;
}

/* 知识点掌握情况 */
.knowledge-mastery {
  background: #fff;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.knowledge-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  color: #333;
  margin: 0 0 16px 0;
}

.knowledge-title i {
  color: #722ed1;
}

.knowledge-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.knowledge-item {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 12px;
}

.knowledge-item.mastered {
  border-left: 4px solid #52c41a;
}

.knowledge-item.need-practice {
  border-left: 4px solid #fa8c16;
}

.knowledge-item.need-review {
  border-left: 4px solid #f5222d;
}

.knowledge-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.knowledge-name {
  font-weight: 500;
  color: #333;
}

.knowledge-mastery {
  font-weight: bold;
  color: #1890ff;
}

.knowledge-progress .progress-bar {
  height: 6px;
  background: #e8e8e8;
  border-radius: 3px;
  overflow: hidden;
}

.knowledge-progress .progress-fill {
  height: 100%;
  border-radius: 3px;
}

.knowledge-item.mastered .progress-fill {
  background: #52c41a;
}

.knowledge-item.need-practice .progress-fill {
  background: #fa8c16;
}

.knowledge-item.need-review .progress-fill {
  background: #f5222d;
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 0 24px 24px;
}

.modal-footer .btn {
  flex: 1;
  justify-content: center;
  padding: 12px;
}

/* 弹窗动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .main-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 15px;
  }
  
  .exercise-header {
    padding: 20px;
  }
  
  .exercise-series-title {
    font-size: 24px;
  }
  
  .exercise-series-meta {
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .submit-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
  
  .score-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .question-card {
    padding: 20px;
  }
  
  .options-list {
    grid-template-columns: 1fr;
  }
  
  .nav-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .nav-legend {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .performance-summary {
    grid-template-columns: 1fr;
  }
  
  .feedback-modal {
    margin: 20px;
  }
  
  .score-circle {
    width: 120px;
    height: 120px;
  }
  
  .score-value {
    font-size: 32px;
  }
  
  .modal-footer {
    flex-direction: column;
  }
}

/* 返回视频按钮区域 */
.back-to-video-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.back-to-video-btn {
  width: 100%;
  justify-content: center;
  padding: 12px;
}

@media (max-width: 576px) {
  .question-card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .question-card-title {
    flex-wrap: wrap;
  }
  
  .nav-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .feedback-modal {
    margin: 10px;
    border-radius: 12px;
  }
  
  .modal-header,
  .modal-content,
  .modal-footer {
    padding: 16px;
  }
}
</style>