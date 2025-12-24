import api from './api.js'

export const authService = {
  // 用户登录
  login(email, password) {
    return api.post('/auth/login', {
      email,
      password
    })
  },

  // 用户注册
  register(username, email, password) {
    return api.post('/auth/register', {
      username,
      email,
      password
    }).catch(error => {
      if (error.response && error.response.data) {
        return {
          data: error.response.data,
          status: error.response.status,
          statusText: error.response.statusText,
          headers: error.response.headers,
          config: error.response.config
        }
      }
      return {
        data: {
          code: 0,
          msg: '网络连接失败，请检查网络设置'
        },
        status: 0,
        statusText: 'NETWORK_ERROR'
      }
    })
  },

  // 获取用户信息
  getUserInfo(userId) {
    return api.get('/auth/user-info', {
      params: { user_id: userId }
    })
  },

  
  updateUserPreferences(userId, favoriteDomain) {
    return api.post('/auth/update-preferences', {
      user_id: userId,
      favorite_domain: favoriteDomain
    })
  },

  // 更新用户信息
  updateUserInfo(userId, userData) {
    return api.post('/auth/update-info', {
      user_id: userId,
      ...userData
    })
  },

  // 用户退出
  logout() {
    return api.post('/auth/logout')
  }
}