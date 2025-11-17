import { createStore } from 'vuex'

export default createStore({
  state: {
    user: null,
    isLoggedIn: false,
    courses: [],
    currentCourse: null,
    currentVideo: null,
    quizProgress: {}
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
      state.isLoggedIn = !!user
    },
    SET_COURSES(state, courses) {
      state.courses = courses
    },
    SET_CURRENT_COURSE(state, course) {
      state.currentCourse = course
    },
    SET_CURRENT_VIDEO(state, video) {
      state.currentVideo = video
    },
    UPDATE_QUIZ_PROGRESS(state, { quizId, progress }) {
      state.quizProgress[quizId] = progress
    }
  },
  actions: {
    login({ commit }, userData) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          if (userData.email === 'admin@edulearn.com' && userData.password === 'adminpass') {
            const user = { ...userData, role: 'admin' }
            commit('SET_USER', user)
            localStorage.setItem('user', JSON.stringify(user))
            resolve(user)
          } else if (userData.email && userData.password) {
            const user = { ...userData, role: 'student' }
            commit('SET_USER', user)
            localStorage.setItem('user', JSON.stringify(user))
            resolve(user)
          } else {
            reject(new Error('登录失败，请检查邮箱和密码。'))
          }
        }, 500)
      })
    },
    logout({ commit }) {
      commit('SET_USER', null)
      localStorage.removeItem('user')
    },
    register({ commit }, userData) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          if (userData.password !== userData.confirmPassword) {
            reject(new Error('密码不匹配'))
            return
          }
          
          if (userData.password.length < 8) {
            reject(new Error('密码长度至少8个字符'))
            return
          }
          
          const user = {
            id: Date.now(),
            ...userData,
            role: 'student'
          }
          commit('SET_USER', user)
          localStorage.setItem('user', JSON.stringify(user))
          resolve(user)
        }, 1500)
      })
    },
    initializeApp({ commit }) {
      const user = localStorage.getItem('user')
      if (user) {
        commit('SET_USER', JSON.parse(user))
      }
    }
  }
})