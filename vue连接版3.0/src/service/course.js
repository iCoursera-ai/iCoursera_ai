import api from './api.js'

export const courseService = {
  /**
   * 获取课程第一个视频
   * @param {string} courseId - 课程ID
   * @returns {Promise} - 视频信息
   */
  async getFirstVideo(courseId) {
    try {
      const response = await api.get(`/course/first-video/${courseId}`)
      return response.data
    } catch (error) {
      console.error(`获取课程 ${courseId} 的第一个视频失败:`, error)
      throw error
    }
  },

  /**
   * 获取课程结构（模块和视频）
   * @param {string} courseId - 课程ID
   * @returns {Promise} - 课程结构数据
   */
  async getCourseFullStructure(courseId) {
    try {
      const response = await api.get(`/course/${courseId}/structure`)
      return response.data
    } catch (error) {
      console.error(`获取课程 ${courseId} 结构失败:`, error)
      throw error
    }
  },

  /**
   * 获取视频播放地址
   * @param {string} videoId - 视频ID
   * @returns {Promise} - 视频播放信息
   */
  async getVideoUrl(videoId) {
    try {
      const response = await api.get(`/video/${videoId}`)
      return response.data
    } catch (error) {
      console.error(`获取视频 ${videoId} 播放地址失败:`, error)
      throw error
    }
  },
  async getCoursesByDomain(domain, page = 1, pageSize = 20) {
    try {
      const response = await api.get('/course/by-domain', {
        params: {
          domain: domain,
          page: page,
          page_size: pageSize
        }
      })
      return response.data
    } catch (error) {
      console.error(`获取 ${domain} 领域的课程失败:`, error)
      throw error
    }
  },
  async searchCourses(keyword, page = 1, pageSize = 20) {
    try {
      const response = await api.get('/api/course/search', {
        params: {
          keyword: keyword,
          page: page,
          page_size: pageSize
        }
      })
      return response.data
    } catch (error) {
      console.error(`搜索课程 "${keyword}" 失败:`, error)
      throw error
    }
  },
  async getCoursesByTeacher(userId, page = 1, pageSize = 20) {
    try {
      const response = await api.get('/course/by-teacher', {
        params: {
          user_id: userId,  // 使用user_id参数，与后端保持一致
          page: page,
          page_size: pageSize
        }
      })
      return response.data
    } catch (error) {
      console.error(`获取教师 ${userId} 的课程失败:`, error)
      throw error
    }
  },

  async searchCoursesByName(searchTerm, page = 1, pageSize = 12, sortBy = 'enrolled_count', domain = null) {
    try {
      const params = {
        q: searchTerm,
        page: page,
        page_size: pageSize,
        sort_by: sortBy,
        order: 'desc'  // 默认降序
      }
      
      // 领域筛选
      if (domain && domain !== 'all') {
        params.domain = domain
      }
      
      // 调试信息
      console.log('搜索API调用:', {
        searchTerm,
        sortBy,
        params
      })
      
      const response = await api.get('/course/search', { params })
      
      // 检查排序结果
      if (sortBy === 'duration_hours' && response.data.data?.courses) {
        console.log('按时长排序检查:')
        response.data.data.courses.slice(0, 5).forEach((course, i) => {
          console.log(`${i+1}. ${course.course_name}: ${course.duration_hours}小时`)
        })
      }
      
      return response.data
    } catch (error) {
      console.error(`搜索失败:`, error)
      throw error
    }
  }
}

export default courseService