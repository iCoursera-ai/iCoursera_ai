<template>
  <div class="settings-section">
    <div class="section-header">
      <h2>账户设置</h2>
      <p>管理您的账户信息和偏好设置</p>
    </div>

    <div class="settings-tabs">
      <div 
        class="settings-tab" 
        :class="{ active: activeSettingsTab === 'profile' }"
        @click="activeSettingsTab = 'profile'"
      >
        <i class="fas fa-user"></i>
        个人资料
      </div>
      <div 
        class="settings-tab" 
        :class="{ active: activeSettingsTab === 'security' }"
        @click="activeSettingsTab = 'security'"
      >
        <i class="fas fa-shield-alt"></i>
        安全设置
      </div>
      <div 
        class="settings-tab" 
        :class="{ active: activeSettingsTab === 'notifications' }"
        @click="activeSettingsTab = 'notifications'"
      >
        <i class="fas fa-bell"></i>
        通知偏好
      </div>
      <div 
        class="settings-tab" 
        :class="{ active: activeSettingsTab === 'billing' }"
        @click="activeSettingsTab = 'billing'"
      >
        <i class="fas fa-credit-card"></i>
        订阅与账单
      </div>
    </div>

    <div class="settings-content">
      <!-- 个人资料设置 -->
      <div class="settings-panel" :class="{ active: activeSettingsTab === 'profile' }">
        <form class="settings-form" @submit.prevent="updateProfile">
          <div class="form-row">
            <div class="form-group">
              <label for="settings-firstName">名字 *</label>
              <input 
                type="text" 
                id="settings-firstName"
                v-model="profileForm.firstName"
                class="form-control" 
                placeholder="请输入您的名字"
                required
              >
            </div>
            <div class="form-group">
              <label for="settings-lastName">姓氏 *</label>
              <input 
                type="text" 
                id="settings-lastName"
                v-model="profileForm.lastName"
                class="form-control" 
                placeholder="请输入您的姓氏"
                required
              >
            </div>
          </div>

          <div class="form-group">
            <label for="settings-email">电子邮件 *</label>
            <input 
              type="email" 
              id="settings-email"
              v-model="profileForm.email"
              class="form-control" 
              placeholder="请输入您的电子邮箱"
              required
            >
          </div>

          <div class="form-group">
            <label for="settings-bio">个人简介</label>
            <textarea 
              id="settings-bio"
              v-model="profileForm.bio"
              class="form-control" 
              rows="4"
              placeholder="向其他用户介绍您自己，分享您的专业背景和兴趣..."
              maxlength="500"
            ></textarea>
            <div class="form-hint">{{ profileForm.bio.length }}/500 字符</div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="settings-location">位置</label>
              <input 
                type="text" 
                id="settings-location"
                v-model="profileForm.location"
                class="form-control" 
                placeholder="例如：北京, 中国"
              >
            </div>
            <div class="form-group">
              <label for="settings-profession">职业</label>
              <input 
                type="text" 
                id="settings-profession"
                v-model="profileForm.profession"
                class="form-control" 
                placeholder="例如：软件工程师、数据分析师"
              >
            </div>
          </div>

          <div class="form-group">
            <label for="settings-website">个人网站</label>
            <input 
              type="url" 
              id="settings-website"
              v-model="profileForm.website"
              class="form-control" 
              placeholder="https://example.com"
            >
          </div>

          <div class="form-actions">
            <button type="button" class="btn btn-outline" @click="resetProfileForm">
              <i class="fas fa-undo"></i>重置
            </button>
            <button type="submit" class="btn btn-primary" :disabled="savingProfile">
              <i class="fas fa-save"></i> {{ savingProfile ? '保存中...' : '保存更改' }}
            </button>
          </div>
        </form>
      </div>

      <!-- 安全设置 -->
      <div class="settings-panel" :class="{ active: activeSettingsTab === 'security' }">
        <form class="settings-form" @submit.prevent="updatePassword">
          <div class="form-group">
            <label for="current-password">当前密码 *</label>
            <input 
              type="password" 
              id="current-password"
              v-model="securityForm.currentPassword"
              class="form-control" 
              placeholder="请输入当前密码"
              required
            >
          </div>

          <div class="form-group">
            <label for="new-password">新密码</label>
            <input 
              type="password" 
              id="new-password"
              v-model="securityForm.newPassword"
              class="form-control" 
              placeholder="留空则不修改密码"
              @input="checkPasswordStrength"
            >
            <div class="password-strength">
              <div class="strength-bar" :style="{ width: passwordStrength + '%', background: passwordStrengthColor }"></div>
              <span class="strength-text">{{ passwordStrengthText }}</span>
            </div>
          </div>

          <div class="form-group">
            <label for="confirm-password">确认新密码</label>
            <input 
              type="password" 
              id="confirm-password"
              v-model="securityForm.confirmPassword"
              class="form-control"
              placeholder="请再次输入新密码"
            >
          </div>

          <div class="security-options">
            <h4><i class="fas fa-cog"></i> 安全选项</h4>
            <label class="checkbox">
              <input type="checkbox" v-model="securityForm.twoFactorEnabled">
              <span class="checkmark"></span>
              启用双重认证
              <span class="option-description">为您的账户添加额外的安全层</span>
            </label>
            <label class="checkbox">
              <input type="checkbox" v-model="securityForm.loginAlerts">
              <span class="checkmark"></span>
              登录提醒
              <span class="option-description">在新设备登录时接收通知</span>
            </label>
            <label class="checkbox">
              <input type="checkbox" v-model="securityForm.sessionTimeout">
              <span class="checkmark"></span>
              会话超时自动退出
              <span class="option-description">30分钟无操作自动退出登录</span>
            </label>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="savingSecurity">
              <i class="fas fa-shield-alt"></i> {{ savingSecurity ? '更新中...' : '更新安全设置' }}
            </button>
          </div>
        </form>

        <div class="security-sessions">
          <h4><i class="fas fa-laptop"></i> 登录会话</h4>
          <div class="session-list">
            <div class="session-item" v-for="session in activeSessions" :key="session.id">
              <div class="session-info">
                <div class="session-device">
                  <i :class="session.deviceIcon"></i>
                  <div>
                    <strong>{{ session.deviceName }}</strong>
                    <span>{{ session.location }} · {{ session.isCurrent ? '当前会话' : session.lastActive }}</span>
                  </div>
                </div>
                <span class="session-time">{{ session.lastActive }}</span>
              </div>
              <button 
                v-if="!session.isCurrent"
                class="btn btn-text" 
                @click="revokeSession(session.id)"
              >
                <i class="fas fa-sign-out-alt"></i>退出
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 通知偏好 -->
      <div class="settings-panel" :class="{ active: activeSettingsTab === 'notifications' }">
        <form class="settings-form" @submit.prevent="updateNotifications">
          <div class="notification-category">
            <h4><i class="fas fa-graduation-cap"></i> 课程相关</h4>
            <label class="checkbox">
              <input type="checkbox" v-model="notificationSettings.courseUpdates">
              <span class="checkmark"></span>
              新课程发布通知
            </label>
            <label class="checkbox">
              <input type="checkbox" v-model="notificationSettings.courseAnnouncements">
              <span class="checkmark"></span>
              课程更新通知
            </label>
            <label class="checkbox">
              <input type="checkbox" v-model="notificationSettings.deadlineReminders">
              <span class="checkmark"></span>
              学习截止日期提醒
            </label>
          </div>

          <div class="notification-category">
            <h4><i class="fas fa-users"></i> 社区互动</h4>
            <label class="checkbox">
              <input type="checkbox" v-model="notificationSettings.comments">
              <span class="checkmark"></span>
              评论和回复通知
            </label>
            <label class="checkbox">
              <input type="checkbox" v-model="notificationSettings.newFollowers">
              <span class="checkmark"></span>
              新关注者通知
            </label>
            <label class="checkbox">
              <input type="checkbox" v-model="notificationSettings.mentions">
              <span class="checkmark"></span>
              被提及通知
            </label>
          </div>

          <div class="notification-category">
            <h4><i class="fas fa-bullhorn"></i> 营销信息</h4>
            <label class="checkbox">
              <input type="checkbox" v-model="notificationSettings.promotions">
              <span class="checkmark"></span>
              特别优惠和促销
            </label>
            <label class="checkbox">
              <input type="checkbox" v-model="notificationSettings.newsletter">
              <span class="checkmark"></span>
              学习资源和技巧
            </label>
            <label class="checkbox">
              <input type="checkbox" v-model="notificationSettings.productUpdates">
              <span class="checkmark"></span>
              产品更新通知
            </label>
          </div>

          <div class="notification-delivery">
            <h4><i class="fas fa-paper-plane"></i> 通知方式</h4>
            <div class="delivery-options">
              <label class="checkbox">
                <input type="checkbox" v-model="notificationSettings.emailNotifications">
                <span class="checkmark"></span>
                电子邮件
              </label>
              <label class="checkbox">
                <input type="checkbox" v-model="notificationSettings.pushNotifications">
                <span class="checkmark"></span>
                推送通知
              </label>
              <label class="checkbox">
                <input type="checkbox" v-model="notificationSettings.smsNotifications">
                <span class="checkmark"></span>
                短信通知
              </label>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="savingNotifications">
              <i class="fas fa-save"></i> {{ savingNotifications ? '保存中...' : '保存偏好' }}
            </button>
          </div>
        </form>
      </div>

      <!-- 订阅与账单 -->
      <div class="settings-panel" :class="{ active: activeSettingsTab === 'billing' }">
        <div class="billing-info">
          <div class="plan-card">
            <div class="plan-header">
              <div>
                <h3>{{ currentPlan.name }}</h3>
                <p class="plan-description">享受完整的学习体验和专属功能</p>
              </div>
              <span class="plan-badge active">当前计划</span>
            </div>
            <div class="plan-features">
              <div class="feature" v-for="feature in currentPlan.features" :key="feature">
                <i class="fas fa-check"></i>
                <span>{{ feature }}</span>
              </div>
            </div>
            <div class="plan-price">
              <span class="price">{{ currentPlan.price }}</span>
              <span class="period">{{ currentPlan.period }}</span>
            </div>
            <button class="btn btn-outline" @click="changePlan">
              <i class="fas fa-sync"></i>更改计划
            </button>
          </div>

          <div class="payment-methods">
            <h4><i class="fas fa-credit-card"></i> 支付方式</h4>
            <div class="payment-card" v-for="card in paymentMethods" :key="card.id">
              <div class="card-info">
                <i :class="card.icon"></i>
                <div>
                  <strong>{{ card.type }} 尾号 {{ card.last4 }}</strong>
                  <span>有效期 {{ card.expiry }}</span>
                </div>
              </div>
              <div class="card-actions">
                <button class="btn btn-text" @click="editPaymentMethod(card.id)">
                  <i class="fas fa-edit"></i>编辑
                </button>
                <button class="btn btn-text" @click="removePaymentMethod(card.id)">
                  <i class="fas fa-trash"></i>删除
                </button>
              </div>
            </div>
            <button class="btn btn-outline" @click="addPaymentMethod">
              <i class="fas fa-plus"></i> 添加支付方式
            </button>
          </div>

          <div class="billing-history">
            <h4><i class="fas fa-receipt"></i> 账单历史</h4>
            <div class="billing-table">
              <div class="billing-header">
                <span>日期</span>
                <span>描述</span>
                <span>金额</span>
                <span>状态</span>
                <span>操作</span>
              </div>
              <div class="billing-row" v-for="invoice in billingHistory" :key="invoice.id">
                <div class="billing-date">{{ invoice.date }}</div>
                <div class="billing-description">{{ invoice.description }}</div>
                <div class="billing-amount">{{ invoice.amount }}</div>
                <div class="billing-status" :class="invoice.status">
                  <i class="fas fa-circle"></i>{{ invoice.statusText }}
                </div>
                <button class="btn btn-text" @click="downloadInvoice(invoice.id)">
                  <i class="fas fa-download"></i>下载
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AccountSettingsSection',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      activeSettingsTab: 'profile',
      savingProfile: false,
      savingSecurity: false,
      savingNotifications: false,
      profileForm: {
        firstName: '',
        lastName: '',
        email: '',
        bio: '',
        location: '',
        website: '',
        profession: ''
      },
      securityForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
        twoFactorEnabled: true,
        loginAlerts: true,
        sessionTimeout: true
      },
      notificationSettings: {
        // 课程相关
        courseUpdates: true,
        courseAnnouncements: true,
        deadlineReminders: false,
        // 社区互动
        comments: true,
        newFollowers: true,
        mentions: true,
        // 营销信息
        promotions: false,
        newsletter: true,
        productUpdates: true,
        // 通知方式
        emailNotifications: true,
        pushNotifications: true,
        smsNotifications: false
      },
      passwordStrength: 0,
      passwordStrengthColor: '#dc3545',
      passwordStrengthText: '密码强度：弱',
      activeSessions: [
        {
          id: 1,
          deviceName: 'Windows Chrome',
          deviceIcon: 'fas fa-desktop',
          location: '北京',
          isCurrent: true,
          lastActive: '刚刚'
        },
        {
          id: 2,
          deviceName: 'iPhone Safari',
          deviceIcon: 'fas fa-mobile-alt',
          location: '北京市',
          isCurrent: false,
          lastActive: '2天前'
        },
        {
          id: 3,
          deviceName: 'Mac Safari',
          deviceIcon: 'fas fa-laptop',
          location: '上海',
          isCurrent: false,
          lastActive: '1周前'
        }
      ],
      currentPlan: {
        name: '高级会员',
        price: '¥99',
        period: '/月',
        features: [
          '无限制课程访问',
          '专业课程证书',
          '专属学习资源',
          '优先技术支持',
          '离线下载功能',
          '无广告体验'
        ]
      },
      paymentMethods: [
        {
          id: 1,
          type: 'Visa',
          last4: '4242',
          expiry: '12/2025',
          icon: 'fab fa-cc-visa'
        }
      ],
      billingHistory: [
        {
          id: 1,
          date: '2023年11月1日',
          description: '高级会员订阅',
          amount: '¥99.00',
          status: 'paid',
          statusText: '已支付'
        },
        {
          id: 2,
          date: '2023年10月1日',
          description: '高级会员订阅',
          amount: '¥99.00',
          status: 'paid',
          statusText: '已支付'
        },
        {
          id: 3,
          date: '2023年9月1日',
          description: '高级会员订阅',
          amount: '¥99.00',
          status: 'paid',
          statusText: '已支付'
        }
      ]
    }
  },
  created() {
    this.initializeProfileForm()
  },
  methods: {
    initializeProfileForm() {
      this.profileForm = {
        firstName: this.user.firstName || '',
        lastName: this.user.lastName || '',
        email: this.user.email || '',
        bio: this.user.bio || '我是一名热衷于分享知识的在线教育者，专注于编程和数据分析领域。拥有5年教学经验，致力于让复杂的技术概念变得简单易懂。',
        location: this.user.location || '北京, 中国',
        website: this.user.website || '',
        profession: this.user.profession || '软件工程师'
      }
    },
    resetProfileForm() {
      this.initializeProfileForm()
    },
    async updateProfile() {
      this.savingProfile = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1500))
        this.$emit('update-profile', this.profileForm)
        alert('个人资料更新成功！')
      } catch (error) {
        alert('更新失败，请重试')
      } finally {
        this.savingProfile = false
      }
    },
    async updatePassword() {
      if (this.securityForm.newPassword && this.securityForm.newPassword !== this.securityForm.confirmPassword) {
        alert('新密码和确认密码不匹配')
        return
      }
      
      this.savingSecurity = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1500))
        this.$emit('update-password', this.securityForm)
        alert('安全设置更新成功！')
        this.securityForm.currentPassword = ''
        this.securityForm.newPassword = ''
        this.securityForm.confirmPassword = ''
      } catch (error) {
        alert('更新失败，请重试')
      } finally {
        this.savingSecurity = false
      }
    },
    async updateNotifications() {
      this.savingNotifications = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        this.$emit('update-notifications', this.notificationSettings)
        alert('通知偏好已保存！')
      } catch (error) {
        alert('保存失败，请重试')
      } finally {
        this.savingNotifications = false
      }
    },
    checkPasswordStrength() {
      const password = this.securityForm.newPassword
      let strength = 0
      
      if (password.length >= 8) strength += 25
      if (/[A-Z]/.test(password)) strength += 25
      if (/[0-9]/.test(password)) strength += 25
      if (/[^A-Za-z0-9]/.test(password)) strength += 25
      
      this.passwordStrength = strength
      
      if (strength < 50) {
        this.passwordStrengthColor = '#dc3545'
        this.passwordStrengthText = '密码强度：弱'
      } else if (strength < 75) {
        this.passwordStrengthColor = '#ffc107'
        this.passwordStrengthText = '密码强度：中'
      } else {
        this.passwordStrengthColor = '#28a745'
        this.passwordStrengthText = '密码强度：强'
      }
    },
    revokeSession(sessionId) {
      this.activeSessions = this.activeSessions.filter(session => session.id !== sessionId)
      alert('会话已撤销')
    },
    changePlan() {
      alert('更改计划功能将在完整版本中实现')
    },
    editPaymentMethod(cardId) {
      alert(`编辑支付方式: ${cardId}`)
    },
    removePaymentMethod(cardId) {
      if (confirm('确定要删除此支付方式吗？')) {
        this.paymentMethods = this.paymentMethods.filter(card => card.id !== cardId)
        alert('支付方式已删除')
      }
    },
    addPaymentMethod() {
      alert('添加支付方式功能将在完整版本中实现')
    },
    downloadInvoice(invoiceId) {
      alert(`下载发票: ${invoiceId}`)
    }
  }
}
</script>

<style scoped>
.settings-section {
  padding: 20px 0;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  margin-bottom: 40px;
  text-align: center;
}

.section-header h2 {
  font-size: 2.2rem;
  color: var(--text);
  margin-bottom: 12px;
  font-weight: 700;
}

.section-header p {
  color: var(--text-light);
  font-size: 1.1rem;
}

.settings-tabs {
  display: flex;
  border-bottom: 1px solid var(--border);
  background: var(--secondary);
  margin-bottom: 0;
  border-radius: 12px 12px 0 0;
  overflow-x: auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.settings-tab {
  padding: 18px 30px;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: nowrap;
  color: var(--text-light);
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.95rem;
}

.settings-tab.active {
  border-bottom-color: var(--primary);
  color: var(--primary);
  background: white;
  font-weight: 600;
}

.settings-tab:hover {
  color: var(--primary);
  background: rgba(0, 86, 210, 0.05);
}

.settings-tab i {
  font-size: 1rem;
  width: 16px;
  text-align: center;
}

.settings-content {
  background: white;
  border-radius: 0 0 12px 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  border: 1px solid var(--border);
  border-top: none;
}

.settings-panel {
  display: none;
  padding: 40px;
  animation: fadeInUp 0.4s ease;
}

.settings-panel.active {
  display: block;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.settings-form {
  max-width: 700px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
}

.form-group {
  margin-bottom: 25px;
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: var(--text);
  font-size: 0.95rem;
}

.form-control {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid var(--border);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  color: var(--text);
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(0, 86, 210, 0.1);
  transform: translateY(-1px);
}

.form-control:invalid {
  border-color: var(--danger);
}

.form-control::placeholder {
  color: var(--text-light);
  opacity: 0.7;
}

.form-hint {
  font-size: 0.85rem;
  color: var(--text-light);
  margin-top: 8px;
  text-align: right;
}

.password-strength {
  margin-top: 12px;
}

.strength-bar {
  height: 6px;
  border-radius: 3px;
  transition: all 0.3s ease;
  margin-bottom: 6px;
  background: #e9ecef;
}

.strength-text {
  font-size: 0.85rem;
  color: var(--text-light);
  font-weight: 500;
}

.security-options {
  margin: 30px 0;
  padding: 25px;
  background: var(--secondary);
  border-radius: 12px;
  border: 1px solid var(--border);
}

.security-options h4 {
  margin-bottom: 20px;
  color: var(--text);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.checkbox {
  display: flex;
  align-items: flex-start;
  margin-bottom: 18px;
  cursor: pointer;
  font-size: 0.95rem;
  padding: 8px 0;
}

.checkbox input {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border);
  border-radius: 5px;
  margin-right: 12px;
  position: relative;
  transition: all 0.3s ease;
  flex-shrink: 0;
  margin-top: 2px;
}

.checkbox input:checked + .checkmark {
  background: var(--primary);
  border-color: var(--primary);
}

.checkbox input:checked + .checkmark::after {
  content: '';
  position: absolute;
  left: 5px;
  top: 2px;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.option-description {
  display: block;
  font-size: 0.85rem;
  color: var(--text-light);
  margin-top: 4px;
  font-weight: normal;
}

.security-sessions {
  margin-top: 40px;
  padding-top: 30px;
  border-top: 2px solid var(--border);
}

.security-sessions h4 {
  margin-bottom: 20px;
  color: var(--text);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.session-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px;
  background: var(--secondary);
  border-radius: 10px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.session-item:hover {
  background: white;
  border-color: var(--border);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.session-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: 1;
  margin-right: 20px;
}

.session-device {
  display: flex;
  align-items: center;
  gap: 15px;
}

.session-device i {
  color: var(--primary);
  font-size: 1.3rem;
  width: 24px;
  text-align: center;
}

.session-device div {
  display: flex;
  flex-direction: column;
}

.session-device strong {
  color: var(--text);
  font-size: 0.95rem;
  margin-bottom: 4px;
}

.session-device span {
  color: var(--text-light);
  font-size: 0.85rem;
}

.session-time {
  color: var(--text-light);
  font-size: 0.85rem;
  font-weight: 500;
}

.notification-category {
  margin-bottom: 30px;
  padding-bottom: 25px;
  border-bottom: 1px solid var(--border);
}

.notification-category:last-of-type {
  border-bottom: none;
}

.notification-category h4 {
  margin-bottom: 20px;
  color: var(--text);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.notification-delivery {
  margin-top: 35px;
  padding: 25px;
  background: var(--secondary);
  border-radius: 12px;
  border: 1px solid var(--border);
}

.notification-delivery h4 {
  margin-bottom: 20px;
  color: var(--text);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.delivery-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
}

.billing-info {
  display: flex;
  flex-direction: column;
  gap: 35px;
}

.plan-card {
  background: linear-gradient(135deg, var(--secondary) 0%, #f8fafc 100%);
  border-radius: 16px;
  padding: 30px;
  border: 2px solid var(--border);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.plan-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), #0056d6);
}

.plan-card:hover {
  border-color: var(--primary);
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 86, 210, 0.15);
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 25px;
}

.plan-header h3 {
  color: var(--text);
  font-size: 1.5rem;
  margin: 0 0 8px 0;
  font-weight: 700;
}

.plan-description {
  color: var(--text-light);
  font-size: 0.95rem;
  margin: 0;
}

.plan-badge {
  padding: 6px 16px;
  background: var(--success);
  color: white;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.plan-badge.active {
  background: var(--primary);
}

.plan-features {
  margin-bottom: 25px;
}

.feature {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  color: var(--text);
  font-size: 0.95rem;
}

.feature i {
  color: var(--success);
  font-size: 1rem;
}

.plan-price {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 25px;
}

.price {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text);
  line-height: 1;
}

.period {
  color: var(--text-light);
  font-size: 1.1rem;
}

.payment-methods {
  padding: 30px;
  background: var(--secondary);
  border-radius: 12px;
  border: 1px solid var(--border);
}

.payment-methods h4 {
  margin-bottom: 20px;
  color: var(--text);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.payment-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: white;
  border-radius: 10px;
  margin-bottom: 15px;
  border: 1px solid var(--border);
  transition: all 0.3s ease;
}

.payment-card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.card-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.card-info i {
  color: var(--primary);
  font-size: 2rem;
}

.card-info div {
  display: flex;
  flex-direction: column;
}

.card-info strong {
  color: var(--text);
  font-size: 1rem;
  margin-bottom: 4px;
}

.card-info span {
  color: var(--text-light);
  font-size: 0.85rem;
}

.card-actions {
  display: flex;
  gap: 10px;
}

.billing-history {
  padding: 30px;
  background: var(--secondary);
  border-radius: 12px;
  border: 1px solid var(--border);
}

.billing-history h4 {
  margin-bottom: 20px;
  color: var(--text);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.billing-table {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.billing-header {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr auto;
  gap: 20px;
  padding: 15px 20px;
  background: white;
  border-radius: 8px;
  font-weight: 600;
  color: var(--text);
  font-size: 0.9rem;
  border: 1px solid var(--border);
}

.billing-row {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr auto;
  gap: 20px;
  align-items: center;
  padding: 18px 20px;
  background: white;
  border-radius: 8px;
  border: 1px solid var(--border);
  transition: all 0.3s ease;
}

.billing-row:hover {
  border-color: var(--primary);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.billing-date,
.billing-description,
.billing-amount,
.billing-status {
  color: var(--text);
  font-size: 0.9rem;
}

.billing-amount {
  font-weight: 700;
  color: var(--text);
}

.billing-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
}

.billing-status.paid {
  color: var(--success);
}

.billing-status i {
  font-size: 0.6rem;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 35px;
  padding-top: 25px;
  border-top: 2px solid var(--border);
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.btn:hover::before {
  left: 100%;
}

.btn-primary {
  background: var(--primary);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 86, 210, 0.3);
}

.btn-primary:hover {
  background: #0046b8;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 86, 210, 0.4);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-primary:disabled {
  background: var(--border);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-outline {
  background: transparent;
  color: var(--primary);
  border: 2px solid var(--primary);
}

.btn-outline:hover {
  background: var(--primary);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 86, 210, 0.2);
}

.btn-text {
  background: transparent;
  color: var(--primary);
  padding: 8px 12px;
  font-size: 0.85rem;
  border: 1px solid transparent;
}

.btn-text:hover {
  background: rgba(0, 86, 210, 0.1);
  border-color: var(--border);
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .settings-section {
    padding: 15px;
  }
  
  .settings-tabs {
    flex-direction: column;
    border-radius: 8px 8px 0 0;
  }
  
  .settings-tab {
    border-bottom: none;
    border-left: 4px solid transparent;
    padding: 15px 20px;
  }
  
  .settings-tab.active {
    border-left-color: var(--primary);
    border-bottom: none;
  }
  
  .settings-panel {
    padding: 25px 20px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .session-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    margin-right: 0;
  }
  
  .billing-header,
  .billing-row {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .billing-header {
    display: none;
  }
  
  .billing-row {
    position: relative;
    padding: 15px;
  }
  
  .billing-row::before {
    content: attr(data-label);
    font-weight: 600;
    color: var(--text-light);
    font-size: 0.8rem;
    margin-bottom: 4px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
  
  .delivery-options {
    grid-template-columns: 1fr;
  }
  
  .card-actions {
    flex-direction: column;
    gap: 5px;
  }
  
  .plan-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
}
</style>