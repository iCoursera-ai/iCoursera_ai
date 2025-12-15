<template>
  <div class="exercise-container">
    <!-- 面包屑导航 - 更简约 -->
    <div class="breadcrumb-nav">
      <router-link to="/">首页</router-link> >
      <router-link to="/courses?category=computer">计算机考研</router-link> >
      <router-link to="/courses?category=os">操作系统</router-link> >
      <span class="current">课后习题</span>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner">
        <i class="fa fa-spinner fa-spin"></i>
      </div>
      <p>加载中...</p>
    </div>

    <!-- 主要内容区域 -->
    <div v-else class="main-content">
      <div class="content-wrapper">
        <!-- 左侧题目区域 -->
        <div class="questions-area">
          <!-- 习题集头部 -->
          <div class="exercise-header">
            <div class="header-top">
              <h1 class="exercise-title">{{ exerciseSeries.title }}</h1>
              <div class="exercise-info">
                <span class="question-count">共{{ exerciseSeries.questions.length }}题</span>
                <span class="total-points">总分{{ exerciseSeries.totalPoints }}分</span>
                <span class="difficulty-tag" :class="exerciseSeries.difficulty">
                  {{ exerciseSeries.difficulty }}
                </span>
              </div>
            </div>
            
            <!-- 进度条 -->
            <div class="progress-container">
              <div class="progress-info">
                <span>已完成 {{ answeredQuestionsCount }}/{{ exerciseSeries.questions.length }}</span>
                <span>{{ Math.round((answeredQuestionsCount / exerciseSeries.questions.length) * 100) }}%</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: (answeredQuestionsCount / exerciseSeries.questions.length) * 100 + '%' }"></div>
              </div>
            </div>
            
            <!-- 操作按钮区域 -->
            <div class="action-buttons">
              <!-- 提交按钮 -->
              <div class="submit-section" v-if="!isSubmitted">
                <button 
                  class="submit-btn" 
                  @click="submitSeries"
                  :disabled="!isAllAnswered"
                  :class="{ 'active': isAllAnswered }"
                >
                  提交答案 ({{ answeredQuestionsCount }}/{{ exerciseSeries.questions.length }})
                </button>
                <div class="submit-tip" v-if="!isAllAnswered">
                  请完成所有题目
                </div>
              </div>
              
              <!-- 分数展示和重做按钮 -->
              <div class="score-section" v-else>
                <div class="score-display">
                  <span class="score-label">得分</span>
                  <span class="score-value">{{ seriesScore }}</span>
                  <span class="score-total">/{{ exerciseSeries.totalPoints }}</span>
                  <span class="accuracy">正确率: {{ Math.round((correctAnswersCount / exerciseSeries.questions.length) * 100) }}%</span>
                </div>
                <button class="redo-btn" @click="resetSeries">
                  <i class="fa fa-redo"></i>
                  重新练习
                </button>
              </div>
            </div>
          </div>
          
          <!-- 题目列表 -->
          <div class="questions-list">
            <div 
              v-for="(question, index) in exerciseSeries.questions" 
              :key="question.id || index"
              class="question-item"
              :class="{ 
                'current': currentQuestionIndex === index,
                'answered': userAnswers[index] !== null && !isSubmitted,
                'correct': isSubmitted && userAnswers[index] !== null && checkAnswerCorrect(question, index),
                'incorrect': isSubmitted && userAnswers[index] !== null && !checkAnswerCorrect(question, index)
              }"
              :id="'question-' + index"
            >
              <!-- 题目头部 -->
              <div class="question-header">
                <div class="question-meta">
                  <span class="question-number">第{{ index + 1 }}题</span>
                  <span class="question-points">{{ question.points }}分</span>
                  <span class="question-type">{{ question.type }}</span>
                </div>
                <div class="question-status">
                  <span v-if="userAnswers[index] !== null && !isSubmitted" class="status-answered">
                    已答
                  </span>
                  <span v-else-if="isSubmitted && userAnswers[index] !== null && checkAnswerCorrect(question, index)" 
                        class="status-correct">
                    正确 +{{ question.points }}分
                  </span>
                  <span v-else-if="isSubmitted && userAnswers[index] !== null && !checkAnswerCorrect(question, index)" 
                        class="status-incorrect">
                    错误
                  </span>
                  <span v-else class="status-not-answered">
                    未答
                  </span>
                </div>
              </div>
              
              <!-- 题目内容 -->
              <div class="question-content">
                <div class="question-text">
                  {{ question.question }}
                </div>
                
                <!-- 选项 -->
                <div class="options">
                  <div 
                    v-for="(option, optionIndex) in question.options" 
                    :key="optionIndex"
                    class="option"
                    :class="{ 
                      'selected': isOptionSelected(index, optionIndex),
                      'correct': isSubmitted && optionIndex === getCorrectAnswer(question),
                      'wrong': isSubmitted && userAnswers[index] !== null && !checkAnswerCorrect(question, index) && (
                        (question.type === '多选题' && Array.isArray(userAnswers[index]) && userAnswers[index].includes(optionIndex)) ||
                        (question.type !== '多选题' && userAnswers[index] === optionIndex)
                      )
                    }"
                    @click="selectOption(index, optionIndex)"
                  >
                    <div class="option-letter">
                      {{ String.fromCharCode(65 + optionIndex) }}
                    </div>
                    <div class="option-text">
                      {{ option }}
                    </div>
                  </div>
                </div>
                
                <!-- 答案解析 -->
                <div class="answer-analysis" v-if="isSubmitted">
                  <div class="analysis-header">
                    <i class="fa fa-chart-bar"></i>
                    答案解析
                  </div>
                  <div class="analysis-content">
                    <div class="answer-info">
                      <span>你的答案：<strong>{{ getFormattedAnswer(question, index) }}</strong></span>
                      <span>正确答案：<strong class="correct-answer">{{ getFormattedCorrectAnswer(question) }}</strong></span>
                    </div>
                    <div class="explanation">
                      {{ question.explanation }}
                    </div>
                    <div class="knowledge-points" v-if="question.knowledgePoints && question.knowledgePoints.length > 0">
                      <span>知识点：</span>
                      <span class="point-tag" v-for="point in question.knowledgePoints" :key="point">
                        {{ point }}
                      </span>
                    </div>
                  </div>
                </div>
                
                <!-- 提示 -->
                <div class="hint-section" v-if="!isSubmitted">
                  <div class="hint-toggle" @click="toggleHint(index)">
                    <i class="fa fa-lightbulb"></i>
                    {{ showHints[index] ? '隐藏提示' : '显示提示' }}
                  </div>
                  <div class="hint-content" v-if="showHints[index]">
                    {{ question.hint }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧功能区 - 添加sticky使其跟随滚动 -->
        <div class="sidebar">
          <!-- 题目导航 -->
          <div class="nav-card">
            <div class="nav-header">
              <h3>题目导航</h3>
              <span>{{ answeredQuestionsCount }}/{{ exerciseSeries.questions.length }}</span>
            </div>
            <div class="nav-buttons">
              <button 
                v-for="(question, index) in exerciseSeries.questions" 
                :key="index"
                class="nav-btn"
                :class="{
                  'current': currentQuestionIndex === index,
                  'answered': userAnswers[index] !== null && !isSubmitted,
                  'correct': isSubmitted && userAnswers[index] !== null && checkAnswerCorrect(question, index),
                  'incorrect': isSubmitted && userAnswers[index] !== null && !checkAnswerCorrect(question, index),
                  'not-answered': userAnswers[index] === null
                }"
                @click="scrollToQuestion(index)"
              >
                {{ index + 1 }}
              </button>
            </div>
            
            <div class="nav-legends">
              <div class="legend">
                <span class="color-box current"></span>
                <span>当前</span>
              </div>
              <div class="legend">
                <span class="color-box answered"></span>
                <span>已答</span>
              </div>
              <div class="legend">
                <span class="color-box not-answered"></span>
                <span>未答</span>
              </div>
              <div v-if="isSubmitted" class="legend">
                <span class="color-box correct"></span>
                <span>正确</span>
              </div>
              <div v-if="isSubmitted" class="legend">
                <span class="color-box incorrect"></span>
                <span>错误</span>
              </div>
            </div>

            <!-- 操作按钮组 -->
            <div class="action-buttons-sidebar">
              <button class="back-btn" @click="goBackToVideo">
                <i class="fa fa-arrow-left"></i>
                返回视频
              </button>
              <button class="redo-btn-sidebar" @click="resetSeries" v-if="isSubmitted">
                <i class="fa fa-redo"></i>
                重做
              </button>
            </div>
          </div>

          <!-- 统计信息 -->
          <div class="stats-card">
            <div class="stats-header">
              <i class="fa fa-chart-line"></i>
              <span>学习统计</span>
            </div>
            <div class="stats-content">
              <div class="stat-item">
                <span class="stat-label">完成度</span>
                <div class="stat-progress">
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: (answeredQuestionsCount / exerciseSeries.questions.length) * 100 + '%' }"></div>
                  </div>
                  <span class="stat-value">{{ Math.round((answeredQuestionsCount / exerciseSeries.questions.length) * 100) }}%</span>
                </div>
              </div>
              
              <div class="stat-item" v-if="isSubmitted">
                <span class="stat-label">正确率</span>
                <div class="stat-progress">
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: (correctAnswersCount / exerciseSeries.questions.length) * 100 + '%' }"></div>
                  </div>
                  <span class="stat-value">{{ Math.round((correctAnswersCount / exerciseSeries.questions.length) * 100) }}%</span>
                </div>
              </div>
              
              <div class="stat-item" v-if="isSubmitted">
                <span class="stat-label">用时</span>
                <span class="stat-value">{{ formatTime(timeSpent) }}</span>
              </div>
              
              <!-- 重做提示 -->
              <div class="redo-hint" v-if="isSubmitted">
                <i class="fa fa-info-circle"></i>
                点击"重做"按钮可重新练习
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 提交反馈 -->
    <div v-if="showFeedbackModal" class="feedback-modal" @click="closeFeedbackModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>
            <i :class="feedbackIcon"></i>
            {{ feedbackTitle }}
          </h3>
          <button class="close-btn" @click="closeFeedbackModal">
            <i class="fa fa-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="score-display-modal">
            <div class="score-circle" :class="feedbackScoreClass">
              <span class="score">{{ Math.round((seriesScore / exerciseSeries.totalPoints) * 100) }}</span>
              <span class="score-label">分</span>
            </div>
          </div>
          
          <div class="performance-stats">
            <div class="stat-item-modal">
              <div class="stat-icon correct">
                <i class="fa fa-check"></i>
              </div>
              <div class="stat-info">
                <div class="stat-name">正确</div>
                <div class="stat-value">{{ correctAnswersCount }}/{{ exerciseSeries.questions.length }}</div>
              </div>
            </div>
            <div class="stat-item-modal">
              <div class="stat-icon score">
                <i class="fa fa-star"></i>
              </div>
              <div class="stat-info">
                <div class="stat-name">得分</div>
                <div class="stat-value">{{ seriesScore }}/{{ exerciseSeries.totalPoints }}</div>
              </div>
            </div>
            <div class="stat-item-modal">
              <div class="stat-icon time">
                <i class="fa fa-clock"></i>
              </div>
              <div class="stat-info">
                <div class="stat-name">用时</div>
                <div class="stat-value">{{ formatTime(timeSpent) }}</div>
              </div>
            </div>
          </div>
          
          <div class="feedback-message">
            {{ feedbackMessage }}
          </div>
          
          <div class="suggestions">
            <h4><i class="fa fa-lightbulb"></i> 学习建议</h4>
            <ul>
              <li v-for="(suggestion, index) in feedbackSuggestions" :key="index">
                <i class="fa fa-circle"></i>
                {{ suggestion }}
              </li>
            </ul>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="confirm-btn" @click="handleFeedbackAction">
            {{ feedbackActionText }}
          </button>
          <button class="redo-modal-btn" @click="handleRedoFromModal">
            <i class="fa fa-redo"></i>
            重新练习
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
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
    
    // 习题集状态
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
    
    // 反馈弹窗
    const showFeedbackModal = ref(false)
    
    // 习题集数据（保持不变）
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
      }
    }
    
    // 计算属性
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
    
    // 反馈弹窗计算属性
    const feedbackTitle = computed(() => {
      if (!exerciseSeries.value || !exerciseSeries.value.questions) return '提交完成'
      const accuracy = (correctAnswersCount.value / exerciseSeries.value.questions.length) * 100
      if (accuracy >= 80) return '优秀！'
      if (accuracy >= 60) return '良好！'
      return '加油！'
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
      if (!exerciseSeries.value || !exerciseSeries.value.questions) return ''
      const accuracy = (correctAnswersCount.value / exerciseSeries.value.questions.length) * 100
      
      if (accuracy >= 90) {
        return '你的表现非常出色！对知识点掌握得很扎实。'
      } else if (accuracy >= 70) {
        return '做得不错！大部分知识点已经掌握。'
      } else if (accuracy >= 50) {
        return '继续努力！建议回顾相关知识点。'
      } else {
        return '需要认真学习！建议重新学习本章内容。'
      }
    })
    
    const feedbackSuggestions = computed(() => {
      if (!exerciseSeries.value || !exerciseSeries.value.questions) return []
      
      const accuracy = (correctAnswersCount.value / exerciseSeries.value.questions.length) * 100
      const suggestions = []
      
      if (accuracy >= 80) {
        suggestions.push('可以挑战更高难度的题目')
        suggestions.push('尝试将知识应用到实际中')
        suggestions.push('帮助其他同学巩固知识')
      } else if (accuracy >= 60) {
        suggestions.push('回顾错题，理解错误原因')
        suggestions.push('重新学习相关视频内容')
        suggestions.push('多做练习题提升熟练度')
      } else {
        suggestions.push('建议重新观看本章节视频')
        suggestions.push('建立错题本定期复习')
        suggestions.push('向老师请教不理解的知识点')
      }
      
      return suggestions.slice(0, 3)
    })
    
    const feedbackActionText = computed(() => {
      return '返回学习'
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
    
    const getFormattedAnswer = (question, index) => {
      const userAnswer = userAnswers.value[index]
      if (userAnswer === null) return '未作答'
      
      if (question.type === '多选题') {
        if (Array.isArray(userAnswer)) {
          return userAnswer.map(index => String.fromCharCode(65 + index)).join('、')
        }
      }
      return String.fromCharCode(65 + userAnswer)
    }
    
    const getFormattedCorrectAnswer = (question) => {
      const correctAnswer = getCorrectAnswer(question)
      if (question.type === '多选题') {
        if (Array.isArray(correctAnswer)) {
          return correctAnswer.map(index => String.fromCharCode(65 + index)).join('、')
        }
      }
      return String.fromCharCode(65 + correctAnswer)
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
        let currentAnswers = userAnswers.value[questionIndex]
        if (currentAnswers === null) {
          currentAnswers = []
        } else if (!Array.isArray(currentAnswers)) {
          currentAnswers = [currentAnswers]
        }
        
        if (currentAnswers.includes(optionIndex)) {
          userAnswers.value[questionIndex] = currentAnswers.filter(i => i !== optionIndex)
          if (userAnswers.value[questionIndex].length === 0) {
            userAnswers.value[questionIndex] = null
          }
        } else {
          userAnswers.value[questionIndex] = [...currentAnswers, optionIndex]
        }
      } else {
        userAnswers.value[questionIndex] = optionIndex
      }
      
      saveProgress()
    }
    
    const toggleHint = (index) => {
      showHints.value[index] = !showHints.value[index]
    }
    
    const scrollToQuestion = (index) => {
      currentQuestionIndex.value = index
      const element = document.getElementById(`question-${index}`)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }
    
    const submitSeries = () => {
      if (!isAllAnswered.value) {
        alert(`请先完成所有题目 (${answeredQuestionsCount.value}/${exerciseSeries.value.questions.length})`)
        return
      }
      
      const endTime = Date.now()
      timeSpent.value = Math.round((endTime - startTime.value) / 1000)
      
      isSubmitted.value = true
      saveProgress()
      
      setTimeout(() => {
        showFeedbackModal.value = true
      }, 500)
    }
    
    // 重做功能
    const resetSeries = () => {
      if (confirm('确定要重新开始练习吗？这将清除所有答案。')) {
        // 重置所有状态
        userAnswers.value = new Array(exerciseSeries.value.questions.length).fill(null)
        showHints.value = {}
        isSubmitted.value = false
        timeSpent.value = 0
        startTime.value = Date.now()
        currentQuestionIndex.value = 0
        showFeedbackModal.value = false
        
        // 清除本地存储的进度
        localStorage.removeItem(`series_${seriesId.value}_progress`)
        
        // 滚动到顶部
        window.scrollTo({ top: 0, behavior: 'smooth' })
        
        // 保存重置后的状态
        saveProgress()
      }
    }
    
    // 从弹窗重做
    const handleRedoFromModal = () => {
      showFeedbackModal.value = false
      resetSeries()
    }
    
    const handleFeedbackAction = () => {
      showFeedbackModal.value = false
    }
    
    const closeFeedbackModal = () => {
      showFeedbackModal.value = false
    }
    
    const goBackToVideo = () => {
      router.push(`/course/${courseId.value}/player`)
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
    
    // 保存和加载进度
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
          resetToInitial()
        }
      } else {
        resetToInitial()
      }
    }
    
    // 重置到初始状态
    const resetToInitial = () => {
      userAnswers.value = new Array(exerciseSeries.value.questions.length).fill(null)
      startTime.value = Date.now()
    }
    
    // 初始化
    const initialize = () => {
      isLoading.value = true
      
      setTimeout(() => {
        const seriesData = exerciseSeriesData[seriesId.value]
        if (seriesData) {
          exerciseSeries.value = seriesData
        } else {
          exerciseSeries.value = exerciseSeriesData['series_1_1']
        }
        
        loadProgress()
        isLoading.value = false
      }, 300)
    }
    
    // 键盘事件
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
    
    // 生命周期
    onMounted(() => {
      initFontAwesome()
      initialize()
      document.addEventListener('keydown', handleKeydown)
    })
    
    onBeforeUnmount(() => {
      document.removeEventListener('keydown', handleKeydown)
    })
    
    return {
      // 状态
      isLoading,
      exerciseSeries,
      userAnswers,
      showHints,
      isSubmitted,
      timeSpent,
      currentQuestionIndex,
      showFeedbackModal,
      
      // 计算属性
      answeredQuestionsCount,
      isAllAnswered,
      correctAnswersCount,
      seriesScore,
      feedbackTitle,
      feedbackIcon,
      feedbackScoreClass,
      feedbackMessage,
      feedbackSuggestions,
      feedbackActionText,
      
      // 方法
      checkAnswerCorrect,
      getCorrectAnswer,
      getFormattedAnswer,
      getFormattedCorrectAnswer,
      isOptionSelected,
      selectOption,
      toggleHint,
      scrollToQuestion,
      submitSeries,
      resetSeries,
      handleRedoFromModal,
      handleFeedbackAction,
      closeFeedbackModal,
      goBackToVideo,
      formatTime
    }
  }
}
</script>

<style scoped>
/* 基础样式 */
.exercise-container {
  background: #f5f5f5;
  min-height: 100vh;
}

/* 面包屑导航 */
.breadcrumb-nav {
  padding: 15px 20px;
  background: white;
  border-bottom: 1px solid #e8e8e8;
  font-size: 14px;
  color: #666;
}

.breadcrumb-nav a {
  color: #666;
  text-decoration: none;
}

.breadcrumb-nav a:hover {
  color: #1890ff;
}

.breadcrumb-nav .current {
  color: #333;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  background: white;
  margin: 20px;
  border-radius: 8px;
}

.loading-spinner {
  font-size: 36px;
  color: #1890ff;
  margin-bottom: 15px;
}

.loading-state p {
  color: #666;
}

/* 主内容区域 */
.main-content {
  padding: 20px;
}

.content-wrapper {
  display: flex;
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* 左侧题目区域 */
.questions-area {
  flex: 1;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

/* 习题集头部 */
.exercise-header {
  padding: 20px;
  border-bottom: 1px solid #e8e8e8;
}

.header-top {
  margin-bottom: 15px;
}

.exercise-title {
  font-size: 18px;
  color: #333;
  margin: 0 0 10px 0;
  font-weight: 600;
}

.exercise-info {
  display: flex;
  gap: 15px;
  align-items: center;
  font-size: 13px;
  color: #666;
}

.question-count, .total-points {
  background: #f0f0f0;
  padding: 2px 8px;
  border-radius: 10px;
}

.difficulty-tag {
  padding: 2px 10px;
  border-radius: 10px;
  font-size: 12px;
}

.difficulty-tag.简单 {
  background: #e6f7ff;
  color: #1890ff;
}

.difficulty-tag.中等 {
  background: #fff7e6;
  color: #fa8c16;
}

.difficulty-tag.困难 {
  background: #fff1f0;
  color: #f5222d;
}

/* 进度条 */
.progress-container {
  margin-bottom: 15px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #666;
  margin-bottom: 5px;
}

.progress-bar {
  height: 6px;
  background: #f0f0f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #1890ff;
  border-radius: 3px;
  transition: width 0.3s;
}

/* 操作按钮区域 */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* 提交按钮 */
.submit-section {
  display: flex;
  align-items: center;
  gap: 15px;
}

.submit-btn {
  padding: 10px 24px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  color: #666;
  cursor: not-allowed;
  font-size: 14px;
  transition: all 0.3s;
  font-weight: 500;
}

.submit-btn.active {
  background: #1890ff;
  color: white;
  cursor: pointer;
}

.submit-btn.active:hover {
  background: #40a9ff;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.3);
}

.submit-tip {
  font-size: 13px;
  color: #999;
}

/* 分数展示和重做按钮 */
.score-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #e6f7ff;
  padding: 15px;
  border-radius: 6px;
  border: 1px solid #91d5ff;
}

.score-display {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
}

.score-label {
  color: #666;
}

.score-value {
  font-size: 28px;
  font-weight: bold;
  color: #1890ff;
}

.score-total {
  color: #999;
  font-size: 16px;
}

.accuracy {
  color: #666;
  font-size: 13px;
}

/* 重做按钮 */
.redo-btn {
  padding: 8px 16px;
  background: white;
  border: 1px solid #1890ff;
  border-radius: 4px;
  color: #1890ff;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s;
}

.redo-btn:hover {
  background: #1890ff;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.3);
}

/* 题目列表 */
.questions-list {
  padding: 20px;
}

.question-item {
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  margin-bottom: 20px;
  overflow: hidden;
  background: white;
  transition: all 0.3s;
}

/* 当前题目 - 深蓝色边框 */
.question-item.current {
  border-color: #096dd9;
  box-shadow: 0 0 0 2px rgba(9, 109, 217, 0.1);
}

/* 已做题 - 淡蓝色边框 */
.question-item.answered {
  border-left-color: #69c0ff;
}

/* 正确题目 - 浅蓝色边框 */
.question-item.correct {
  border-left-color: #69c0ff;
}

/* 错误题目 - 红色边框 */
.question-item.incorrect {
  border-left-color: #ff4d4f;
}

/* 题目头部 */
.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: #fafafa;
  border-bottom: 1px solid #e8e8e8;
}

.question-meta {
  display: flex;
  align-items: center;
  gap: 15px;
}

.question-number {
  font-weight: 600;
  color: #333;
}

.question-points {
  background: #1890ff;
  color: white;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}

.question-type {
  font-size: 12px;
  color: #666;
}

.question-status {
  font-size: 13px;
  font-weight: 500;
}

.status-answered {
  color: #1890ff;
}

.status-correct {
  color: #1890ff;
}

.status-incorrect {
  color: #ff4d4f;
}

.status-not-answered {
  color: #999;
}

/* 题目内容 */
.question-content {
  padding: 20px;
}

.question-text {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  margin-bottom: 20px;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 4px;
}

/* 选项 */
.options {
  margin-bottom: 20px;
}

.option {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
}

.option:hover {
  border-color: #e8e8e8;
  background: #fafafa;
}

/* 已选择的选项 - 保持正常样式，只改圆圈颜色 */
.option.selected {
  border-color: #e8e8e8;
  background: #fafafa;
}

/* 正确答案 - 保持正常样式，只改圆圈颜色 */
.option.correct {
  border-color: #e8e8e8;
  background: white;
}

/* 错误答案 - 保持正常样式，只改圆圈颜色 */
.option.wrong {
  border-color: #e8e8e8;
  background: white;
}

.option-letter {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #f0f0f0;
  font-weight: bold;
  color: #666;
  margin-right: 12px;
  flex-shrink: 0;
  transition: all 0.3s;
}

/* 未提交时，已选择的选项字母 - 蓝色圆圈 */
.option.selected .option-letter {
  background: #1890ff;
  color: white;
}

/* 提交后，正确答案 - 蓝色圆圈 */
.option.correct .option-letter {
  background: #1890ff;
  color: white;
}

/* 提交后，错误答案（用户选择了但答案是错的）- 红色圆圈 */
.option.wrong .option-letter {
  background: #ff4d4f;
  color: white;
}

.option-text {
  flex: 1;
  font-size: 15px;
  color: #333;
}

/* 答案解析 */
.answer-analysis {
  background: #f9f9f9;
  border-radius: 4px;
  padding: 15px;
  margin-top: 20px;
  border-left: 3px solid #1890ff;
}

.analysis-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
  font-size: 15px;
}

.analysis-header i {
  color: #1890ff;
}

.analysis-content {
  font-size: 14px;
}

.answer-info {
  display: flex;
  gap: 20px;
  margin-bottom: 10px;
  color: #666;
}

.correct-answer {
  color: #1890ff;
}

.explanation {
  color: #666;
  line-height: 1.6;
  margin: 10px 0;
  padding-top: 10px;
  border-top: 1px dashed #ddd;
}

.knowledge-points {
  margin-top: 10px;
  font-size: 13px;
}

.point-tag {
  display: inline-block;
  background: #f0f0f0;
  color: #666;
  padding: 2px 8px;
  border-radius: 10px;
  margin: 0 5px 5px 0;
}

/* 提示 */
.hint-section {
  margin-top: 15px;
}

.hint-toggle {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  color: #fa8c16;
  cursor: pointer;
  font-size: 13px;
  padding: 5px;
}

.hint-toggle i {
  font-size: 14px;
}

.hint-content {
  background: #fff7e6;
  border: 1px solid #ffd591;
  border-radius: 4px;
  padding: 12px;
  margin-top: 8px;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

/* 右侧功能区 - 跟随滚动 */
.sidebar {
  width: 280px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 20px;
  align-self: flex-start;
  max-height: calc(100vh - 40px);
  overflow-y: auto;
}

/* 题目导航卡片 */
.nav-card, .stats-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.nav-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.nav-header span {
  color: #666;
  font-size: 13px;
}

.nav-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}

.nav-btn {
  width: 36px;
  height: 36px;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  background: white;
  color: #666;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

/* 未答题 - 白色 */
.nav-btn.not-answered {
  background: white;
  border-color: #e8e8e8;
  color: #666;
}

/* 已答题 - 淡蓝色 */
.nav-btn.answered {
  background: #e6f7ff;
  border-color: #69c0ff;
  color: #1890ff;
}

/* 当前题目 - 深蓝色 */
.nav-btn.current {
  background: #096dd9;
  border-color: #096dd9;
  color: white;
}

/* 正确题目 - 浅蓝色 */
.nav-btn.correct {
  background: #69c0ff;
  border-color: #69c0ff;
  color: white;
}

/* 错误题目 - 红色 */
.nav-btn.incorrect {
  background: #ff4d4f;
  border-color: #ff4d4f;
  color: white;
}

.nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.nav-legends {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 15px;
  font-size: 12px;
  color: #666;
}

.legend {
  display: flex;
  align-items: center;
  gap: 6px;
}

.color-box {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.color-box.current {
  background: #096dd9;
}

.color-box.answered {
  background: #69c0ff;
}

.color-box.not-answered {
  background: #f0f0f0;
}

.color-box.correct {
  background: #69c0ff;
}

.color-box.incorrect {
  background: #ff4d4f;
}

/* 侧边栏操作按钮 */
.action-buttons-sidebar {
  display: flex;
  gap: 10px;
}

.back-btn {
  flex: 1;
  padding: 10px;
  border: 1px solid #e8e8e8;
  background: white;
  color: #666;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.back-btn:hover {
  border-color: #1890ff;
  color: #1890ff;
}

.redo-btn-sidebar {
  padding: 10px 15px;
  background: white;
  border: 1px solid #1890ff;
  border-radius: 4px;
  color: #1890ff;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s;
}

.redo-btn-sidebar:hover {
  background: #1890ff;
  color: white;
}

/* 统计卡片 */
.stats-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  color: #333;
  margin-bottom: 15px;
}

.stats-header i {
  color: #1890ff;
}

.stats-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-label {
  font-size: 13px;
  color: #666;
}

.stat-progress {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stat-progress .progress-bar {
  flex: 1;
  height: 6px;
  background: #f0f0f0;
  border-radius: 3px;
  overflow: hidden;
}

.stat-progress .progress-fill {
  height: 100%;
  background: #1890ff;
  border-radius: 3px;
}

.stat-value {
  font-size: 13px;
  color: #333;
  font-weight: 500;
  min-width: 40px;
}

/* 重做提示 */
.redo-hint {
  background: #f0f9ff;
  border: 1px solid #91d5ff;
  border-radius: 4px;
  padding: 10px;
  font-size: 12px;
  color: #1890ff;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 5px;
}

.redo-hint i {
  font-size: 14px;
}

/* 反馈弹窗 */
.feedback-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e8e8e8;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal-header i.fa-trophy {
  color: #ffd700;
}

.modal-header i.fa-check-circle {
  color: #1890ff;
}

.modal-header i.fa-exclamation-circle {
  color: #fa8c16;
}

.close-btn {
  background: none;
  border: none;
  font-size: 16px;
  color: #999;
  cursor: pointer;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f5f5f5;
}

/* 分数展示 */
.modal-body {
  padding: 20px;
}

.score-display-modal {
  display: flex;
  justify-content: center;
  margin-bottom: 25px;
}

.score-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
}

.score-circle.score-excellent {
  background: linear-gradient(135deg, #1890ff, #40a9ff);
}

.score-circle.score-good {
  background: linear-gradient(135deg, #69c0ff, #91d5ff);
}

.score-circle.score-poor {
  background: linear-gradient(135deg, #fa8c16, #ffc069);
}

.score-circle .score {
  font-size: 32px;
  font-weight: bold;
}

.score-circle .score-label {
  font-size: 14px;
}

/* 学习表现 */
.performance-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 25px;
}

.stat-item-modal {
  text-align: center;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 8px;
  font-size: 18px;
}

.stat-icon.correct {
  background: #e6f7ff;
  color: #1890ff;
}

.stat-icon.score {
  background: #f0f9ff;
  color: #1890ff;
}

.stat-icon.time {
  background: #fff7e6;
  color: #fa8c16;
}

.stat-name {
  font-size: 13px;
  color: #666;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

/* 反馈消息 */
.feedback-message {
  background: #f9f9f9;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 20px;
  text-align: center;
  color: #333;
  font-size: 14px;
  line-height: 1.5;
}

/* 学习建议 */
.suggestions {
  background: #f0f9ff;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 20px;
}

.suggestions h4 {
  margin: 0 0 12px 0;
  font-size: 15px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 6px;
}

.suggestions h4 i {
  color: #1890ff;
}

.suggestions ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.suggestions li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 13px;
  color: #666;
  line-height: 1.5;
}

.suggestions li:last-child {
  margin-bottom: 0;
}

.suggestions li i {
  color: #1890ff;
  font-size: 6px;
  margin-top: 6px;
  flex-shrink: 0;
}

/* 模态框底部 */
.modal-footer {
  display: flex;
  gap: 10px;
  padding: 0 20px 20px;
}

.confirm-btn {
  flex: 1;
  padding: 12px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s;
}

.confirm-btn:hover {
  background: #40a9ff;
}

.redo-modal-btn {
  flex: 1;
  padding: 12px;
  background: white;
  border: 1px solid #1890ff;
  color: #1890ff;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.redo-modal-btn:hover {
  background: #1890ff;
  color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    position: static;
  }
  
  .score-section {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .action-buttons-sidebar {
    flex-direction: column;
  }
  
  .performance-stats {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .modal-content {
    margin: 20px;
  }
  
  .nav-buttons {
    justify-content: center;
  }
  
  .modal-footer {
    flex-direction: column;
  }
}

@media (max-width: 576px) {
  .main-content {
    padding: 10px;
  }
  
  .exercise-header {
    padding: 15px;
  }
  
  .questions-list {
    padding: 15px;
  }
  
  .question-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .question-status {
    align-self: flex-end;
  }
  
  .answer-info {
    flex-direction: column;
    gap: 5px;
  }
  
  .action-buttons-sidebar {
    flex-direction: column;
  }
}
</style>