import axios from 'axios'

const api = axios.create({
  baseURL:'http://localhost:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  response => {
    // 返回完整的响应对象，而不是response.data
    return response
  },
  error => {
    const status = error.response?.status
    const message = error.response?.data?.msg || '请求失败'
    
    if (status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    
    // 不重新抛出错误，返回一个标准格式的错误响应
    return {
      data: error.response?.data || { code: status || 0, msg: message },
      status: status || 0,
      statusText: error.response?.statusText || 'ERROR',
      headers: error.response?.headers || {},
      config: error.config
    }
  }
)

export default api