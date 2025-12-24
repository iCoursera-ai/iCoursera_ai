import api from './api.js'

export const recommendService = {
  /**
   * 获取用户推荐课程
   * @param {string} userId - 用户ID
   * @param {number} topN - 推荐数量（可选）
   * @returns {Promise} - 推荐课程列表
   */
  async getRecommendations(userId, topN = null) {
    try {
      const params = { user_id: userId }
      if (topN !== null && topN !== undefined) {
        params.top_n = topN
      }
      
      const response = await api.get('/recommend', { params })
      return response.data
    } catch (error) {
      console.error(`获取用户 ${userId} 的推荐课程失败:`, error)
      throw error
    }
  }
}

export default recommendService