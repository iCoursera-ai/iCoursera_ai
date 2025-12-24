// src/services/teacher.js
import api from './api.js'

export const teacherService = {
  /**
   * 根据用户ID获取用户信息（使用您已有的API）
   * @param {string} userId - 用户ID（如：U001, U002等）
   * @returns {Promise} - 用户信息
   */
  async getTeacherInfo(userId) {
    try {
      const response = await api.get(`/auth/user-info`, {
        params: {
          user_id: userId
        }
      })
      
      if (response.data.code === 200) {
        // 将API返回的用户信息转换为老师信息格式
        return this.transformUserToTeacher(response.data.data, userId)
      } else {
        console.error(`获取用户 ${userId} 信息失败:`, response.data.msg)
        // 返回模拟数据作为降级
        return this.getMockTeacherInfo(userId)
      }
    } catch (error) {
      console.error(`获取老师 ${userId} 信息失败:`, error)
    }
  },

  /**
   * 将用户信息转换为老师信息格式
   * @param {object} userData - API返回的用户信息
   * @param {string} userId - 用户ID
   * @returns {object} - 老师信息
   */
  transformUserToTeacher(userData, userId) {
    return {
      code: 200,
      msg: '获取成功',
      data: {
        user_id: userId,
        name: userData.username || userData.name || `用户${userId}`,
        username: userData.username || `user_${userId.toLowerCase()}`,
        title: this.getUserTitle(userData),
        avatar: userData.avatar_url || userData.profile_picture || '',
        bio: userData.bio || userData.description || '暂无个人简介',
        email: userData.email || '',
        location: userData.location || '未知',
        school: userData.school || userData.organization || '未知机构',
        phone: userData.phone || userData.contact_number || '',
        expertise: this.parseExpertise(userData),
        follower_count: userData.follower_count || userData.followers || 0,
        course_count: userData.course_count || 0,
        average_rating: userData.average_rating || 4.5,
        teaching_years: userData.teaching_years || this.calculateTeachingYears(userData.created_at),
        created_at: userData.created_at,
        updated_at: userData.updated_at
      }
    }
  },

  /**
   * 根据用户信息推断用户头衔
   * @param {object} userData - 用户信息
   * @returns {string} - 用户头衔
   */
  getUserTitle(userData) {
    if (userData.is_professor) return '教授'
    if (userData.is_expert) return '专家'
    if (userData.title) return userData.title
    if (userData.experience_years && userData.experience_years >= 5) return '资深讲师'
    return '讲师'
  },

  /**
   * 解析用户专长
   * @param {object} userData - 用户信息
   * @returns {array} - 专长列表
   */
  parseExpertise(userData) {
    if (userData.expertise && Array.isArray(userData.expertise)) {
      return userData.expertise
    }
    
    if (userData.skills) {
      if (typeof userData.skills === 'string') {
        return userData.skills.split(',').map(skill => skill.trim())
      }
      if (Array.isArray(userData.skills)) {
        return userData.skills
      }
    }
    
    return ['教学', '技术分享']
  },

  /**
   * 解析用户标签
   * @param {object} userData - 用户信息
   * @returns {array} - 标签列表
   */
  parseTags(userData) {
    const tags = []
    
    if (userData.tags && Array.isArray(userData.tags)) {
      tags.push(...userData.tags)
    }
    
    // 根据用户角色添加标签
    if (userData.is_professor) tags.push('教授')
    if (userData.is_expert) tags.push('专家')
    if (userData.is_certified) tags.push('认证讲师')
    
    // 根据教学年限添加标签
    if (userData.experience_years && userData.experience_years >= 5) {
      tags.push('资深')
    }
    
    return tags.length > 0 ? tags : ['讲师', '技术分享']
  },

  /**
   * 计算教学年限
   * @param {string} createdAt - 创建时间
   * @returns {number} - 教学年限
   */
  calculateTeachingYears(createdAt) {
    if (!createdAt) return Math.floor(Math.random() * 10) + 1
    
    try {
      const createdDate = new Date(createdAt)
      const currentDate = new Date()
      const diffYears = currentDate.getFullYear() - createdDate.getFullYear()
      return Math.max(1, diffYears)
    } catch (error) {
      return Math.floor(Math.random() * 10) + 1
    }
  }
}

export default teacherService