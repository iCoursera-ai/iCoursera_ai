<template>
  <section class="quiz-page" v-if="quiz">
    <div class="container">
      <div class="quiz-container">
        <!-- 测验头部 -->
        <div class="quiz-header">
          <div class="breadcrumb">
            <router-link to="/">首页</router-link> > 
            <router-link :to="`/course/${courseId}`">{{ course.title }}</router-link> > 
            <span>{{ quiz.title }}</span>
          </div>
          <h1>{{ quiz.title }}</h1>
          <div class="quiz-meta">
            <div class="meta-item">
              <i class="fas fa-clock"></i>
              <span>预计用时：{{ quiz.estimatedTime }}</span>
            </div>
            <div class="meta-item">
              <i class="fas fa-question-circle"></i>
              <span>{{ quiz.questions.length }}道题目</span>
            </div>
            <div class="meta-item">
              <i class="fas fa-trophy"></i>
              <span>通过分数：{{ quiz.passingScore }}%</span>
            </div>
          </div>
        </div>

        <!-- 进度和得分显示 -->
        <div class="quiz-progress-section">
          <div class="progress-card">
            <div class="progress-info">
              <div class="progress-text">
                <span class="progress-label">当前进度</span>
                <span class="progress-value">{{ currentQuestionIndex + 1 }}/{{ quiz.questions.length }}</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: progress + '%' }"></div>
              </div>
            </div>
            <div class="score-info">
              <div class="score-text">
                <span class="score-label">当前得分</span>
                <span class="score-value">{{ currentScore }}%</span>
              </div>
              <div class="score-circle">
                <div class="circle-background"></div>
                <div class="circle-progress" :style="{ transform: `rotate(${currentScore * 3.6}deg)` }"></div>
                <div class="circle-text">{{ currentScore }}%</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 测验内容 -->
        <div class="quiz-content" v-if="!quizCompleted">
          <form @submit.prevent="submitQuiz">
            <!-- 题目 -->
            <div 
              v-for="(question, index) in quiz.questions" 
              :key="index"
              class="question-card"
              :class="{ active: currentQuestionIndex === index }"
            >
              <div class="question-header">
                <h3>题目 {{ index + 1 }}/{{ quiz.questions.length }}</h3>
                <span class="question-points">{{ question.points }}分</span>
              </div>
              <div class="question-content">
                <p>{{ question.text }}</p>
                <div class="options" v-if="question.type === 'single'">
                  <label 
                    v-for="(option, optionIndex) in question.options" 
                    :key="optionIndex"
                    class="option"
                  >
                    <input 
                      type="radio" 
                      :name="`q${index}`" 
                      :value="option.value"
                      v-model="userAnswers[index]"
                    >
                    <span class="option-text">{{ option.label }}</span>
                  </label>
                </div>
                <div class="options" v-else-if="question.type === 'multiple'">
                  <label 
                    v-for="(option, optionIndex) in question.options" 
                    :key="optionIndex"
                    class="option"
                  >
                    <input 
                      type="checkbox" 
                      :name="`q${index}`" 
                      :value="option.value"
                      v-model="userAnswers[index]"
                    >
                    <span class="option-text">{{ option.label }}</span>
                  </label>
                </div>
                <div class="text-answer" v-else>
                  <textarea 
                    v-model="userAnswers[index]"
                    placeholder="请输入您的答案..." 
                    rows="4"
                  ></textarea>
                </div>
              </div>
            </div>

            <!-- 导航按钮 -->
            <div class="quiz-navigation">
              <button 
                type="button" 
                class="btn btn-outline" 
                @click="previousQuestion"
                :disabled="currentQuestionIndex === 0"
              >
                上一题
              </button>
              <button 
                v-if="currentQuestionIndex < quiz.questions.length - 1"
                type="button" 
                class="btn btn-primary" 
                @click="nextQuestion"
              >
                下一题
              </button>
              <button 
                v-else
                type="submit" 
                class="btn btn-success"
              >
                提交测验
              </button>
            </div>
          </form>
        </div>

        <!-- 测验结果 -->
        <div class="quiz-result" v-else>
          <div class="result-header" :class="{ passed: finalScore >= quiz.passingScore, failed: finalScore < quiz.passingScore }">
            <i :class="finalScore >= quiz.passingScore ? 'fas fa-trophy' : 'fas fa-times-circle'"></i>
            <h2>{{ finalScore >= quiz.passingScore ? '恭喜！测验通过' : '测验未通过' }}</h2>
          </div>

          <div class="score-display">
            <div class="final-score">{{ finalScore }}%</div>
            <div class="score-percentage">得分</div>
          </div>

          <div class="result-details">
            <div class="detail-item">
              <span class="detail-label">正确题目</span>
              <span class="detail-value">{{ correctAnswers }}/{{ quiz.questions.length }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">用时</span>
              <span class="detail-value">{{ timeSpent }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">通过分数</span>
              <span class="detail-value">{{ quiz.passingScore }}%</span>
            </div>
          </div>

          <div class="result-actions">
            <button class="btn btn-primary" @click="reviewAnswers">查看答案</button>
            <button class="btn btn-outline" @click="retakeQuiz">重新测验</button>
            <button class="btn btn-outline" @click="backToCourse">返回课程</button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'Quiz',
  props: ['courseId', 'quizId'],
  data() {
    return {
      quiz: null,
      course: null,
      currentQuestionIndex: 0,
      userAnswers: [],
      quizCompleted: false,
      finalScore: 0,
      correctAnswers: 0,
      startTime: null,
      timeSpent: '0:00',
      showReview: false
    }
  },
  computed: {
    progress() {
      return ((this.currentQuestionIndex + 1) / this.quiz.questions.length) * 100
    },
    currentScore() {
      if (this.quizCompleted) return this.finalScore
      
      // 计算当前已答题目的得分
      let score = 0
      for (let i = 0; i <= this.currentQuestionIndex; i++) {
        if (this.isAnswerCorrect(i)) {
          score += this.quiz.questions[i].points
        }
      }
      return Math.round((score / this.getTotalPossibleScore()) * 100)
    }
  },
  created() {
    this.loadQuizData()
    this.startTime = new Date()
  },
  methods: {
    ...mapMutations(['UPDATE_QUIZ_PROGRESS']),
    loadQuizData() {
      // 模拟测验数据
      const quizzes = {
        'quiz-1': {
          id: 'quiz-1',
          title: '测验1：机器学习基础概念',
          estimatedTime: '20分钟',
          passingScore: 60,
          questions: [
            {
              type: 'single',
              text: '机器学习的主要目标是什么？',
              points: 2,
              options: [
                { label: 'A. 编写复杂的算法', value: 'a' },
                { label: 'B. 让计算机从数据中学习模式', value: 'b', correct: true },
                { label: 'C. 创建人工智能机器人', value: 'c' },
                { label: 'D. 处理大数据', value: 'd' }
              ]
            },
            {
              type: 'single',
              text: '以下哪项是监督学习的典型应用？',
              points: 2,
              options: [
                { label: 'A. 客户细分', value: 'a' },
                { label: 'B. 垃圾邮件分类', value: 'b', correct: true },
                { label: 'C. 异常检测', value: 'c' },
                { label: 'D. 推荐系统', value: 'd' }
              ]
            },
            {
              type: 'multiple',
              text: '关于过拟合，以下说法正确的是？',
              points: 3,
              options: [
                { label: 'A. 模型在训练集上表现很好，但在测试集上表现差', value: 'a', correct: true },
                { label: 'B. 模型过于复杂，学习了训练数据中的噪声', value: 'b', correct: true },
                { label: 'C. 可以通过增加训练数据来缓解', value: 'c', correct: true },
                { label: 'D. 是机器学习中期望出现的情况', value: 'd' }
              ]
            },
            {
              type: 'single',
              text: '梯度下降算法的目的是：',
              points: 2,
              options: [
                { label: 'A. 找到函数的最大值', value: 'a' },
                { label: 'B. 最小化损失函数', value: 'b', correct: true },
                { label: 'C. 计算数据梯度', value: 'c' },
                { label: 'D. 优化计算速度', value: 'd' }
              ]
            },
            {
              type: 'text',
              text: '请简要描述监督学习和无监督学习的主要区别。',
              points: 3
            }
          ]
        }
      }
      
      this.quiz = quizzes[this.quizId] || quizzes['quiz-1']
      this.userAnswers = new Array(this.quiz.questions.length).fill(null)
      
      // 模拟课程数据
      this.course = {
        id: this.courseId,
        title: '机器学习入门'
      }
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.quiz.questions.length - 1) {
        this.currentQuestionIndex++
      }
    },
    previousQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--
      }
    },
    submitQuiz() {
      this.calculateScore()
      this.quizCompleted = true
      
      // 更新测验进度
      this.UPDATE_QUIZ_PROGRESS({
        quizId: this.quizId,
        progress: this.finalScore >= this.quiz.passingScore ? 100 : Math.round((this.correctAnswers / this.quiz.questions.length) * 100)
      })
    },
    calculateScore() {
      let totalScore = 0
      let maxScore = 0
      let correctCount = 0
      
      this.quiz.questions.forEach((question, index) => {
        maxScore += question.points
        
        if (this.isAnswerCorrect(index)) {
          totalScore += question.points
          correctCount++
        }
      })
      
      this.correctAnswers = correctCount
      this.finalScore = Math.round((totalScore / maxScore) * 100)
      
      // 计算用时
      const endTime = new Date()
      const timeDiff = (endTime - this.startTime) / 1000 // 秒
      const minutes = Math.floor(timeDiff / 60)
      const seconds = Math.floor(timeDiff % 60)
      this.timeSpent = `${minutes}:${seconds.toString().padStart(2, '0')}`
    },
    isAnswerCorrect(questionIndex) {
      const question = this.quiz.questions[questionIndex]
      const userAnswer = this.userAnswers[questionIndex]
      
      if (question.type === 'single') {
        const correctOption = question.options.find(opt => opt.correct)
        return userAnswer === correctOption?.value
      } else if (question.type === 'multiple') {
        const correctValues = question.options.filter(opt => opt.correct).map(opt => opt.value)
        if (!Array.isArray(userAnswer)) return false
        return userAnswer.length === correctValues.length && 
               userAnswer.every(val => correctValues.includes(val)) &&
               correctValues.every(val => userAnswer.includes(val))
      }
      
      // 文本题默认给分（在实际应用中需要教师批改）
      return userAnswer && userAnswer.trim().length > 0
    },
    getTotalPossibleScore() {
      return this.quiz.questions.reduce((total, question) => total + question.points, 0)
    },
    reviewAnswers() {
      this.showReview = true
      // 在实际应用中，这里可以显示详细的答案回顾
      alert('答案回顾功能将在完整版本中实现')
    },
    retakeQuiz() {
      this.currentQuestionIndex = 0
      this.userAnswers = new Array(this.quiz.questions.length).fill(null)
      this.quizCompleted = false
      this.finalScore = 0
      this.correctAnswers = 0
      this.startTime = new Date()
    },
    backToCourse() {
      this.$router.push(`/course/${this.courseId}`)
    }
  }
}
</script>