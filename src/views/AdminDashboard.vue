<template>
  <main class="admin-main" v-if="user?.role === 'admin'">
    <div class="container">
      <h1 class="page-title">管理员控制台</h1>

      <div class="admin-tabs">
        <button 
          class="admin-tab" 
          :class="{ active: activeTab === 'dashboard' }"
          @click="activeTab = 'dashboard'"
        >
          <i class="fas fa-tachometer-alt"></i> 仪表盘
        </button>
        <button 
          class="admin-tab" 
          :class="{ active: activeTab === 'course-approval' }"
          @click="activeTab = 'course-approval'"
        >
          <i class="fas fa-clipboard-check"></i> 课程审批 (<span id="pendingCoursesCount">{{ pendingCourses.length }}</span>)
        </button>
        <button 
          class="admin-tab" 
          :class="{ active: activeTab === 'reported-courses' }"
          @click="activeTab = 'reported-courses'"
        >
          <i class="fas fa-flag"></i> 举报处理 (<span id="reportedCoursesCount">{{ reportedCourses.length }}</span>)
        </button>
        <button 
          class="admin-tab" 
          :class="{ active: activeTab === 'user-roles' }"
          @click="activeTab = 'user-roles'"
        >
          <i class="fas fa-users-cog"></i> 用户角色管理
        </button>
      </div>

      <div class="admin-content">
        <!-- 仪表盘内容 -->
        <div class="tab-content" :class="{ active: activeTab === 'dashboard' }">
          <h2>平台概览</h2>
          <div class="admin-stats-grid">
            <div class="stat-card">
              <i class="fas fa-clipboard-check"></i>
              <h4>待审批课程</h4>
              <p id="statPendingCourses">{{ pendingCourses.length }}</p>
            </div>
            <div class="stat-card">
              <i class="fas fa-flag"></i>
              <h4>待处理举报</h4>
              <p id="statReportedCourses">{{ reportedCourses.length }}</p>
            </div>
            <div class="stat-card">
              <i class="fas fa-user-tie"></i>
              <h4>教师总数</h4>
              <p id="statTeachers">{{ stats.teachers }}</p>
            </div>
            <div class="stat-card">
              <i class="fas fa-users"></i>
              <h4>注册用户总数</h4>
              <p id="statTotalUsers">{{ stats.totalUsers }}</p>
            </div>
            <div class="stat-card">
              <i class="fas fa-book-open"></i>
              <h4>总课程数</h4>
              <p id="statTotalCourses">{{ stats.totalCourses }}</p>
            </div>
            <div class="stat-card">
              <i class="fas fa-chart-line"></i>
              <h4>举报解决率</h4>
              <p id="statResolutionRate">{{ stats.resolutionRate }}%</p>
            </div>
          </div>
        </div>

        <!-- 课程审批内容 -->
        <div class="tab-content" :class="{ active: activeTab === 'course-approval' }">
          <h2>待审批课程列表</h2>
          <table class="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>课程名称</th>
                <th>讲师</th>
                <th>提交日期</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="course in pendingCourses" :key="course.id">
                <td>{{ course.id }}</td>
                <td>{{ course.title }}</td>
                <td>{{ course.instructor }}</td>
                <td>{{ course.submittedDate }}</td>
                <td>
                  <button class="btn btn-primary btn-sm" @click="approveCourse(course.id)">通过</button>
                  <button class="btn btn-danger btn-sm" @click="rejectCourse(course.id)">拒绝</button>
                  <button class="btn btn-outline btn-sm" @click="viewCourseDetails(course.id)">详情</button>
                </td>
              </tr>
              <tr v-if="pendingCourses.length === 0">
                <td colspan="5" class="text-center">暂无待审批课程</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 被举报课程处理 -->
        <div class="tab-content" :class="{ active: activeTab === 'reported-courses' }">
          <h2>被举报课程处理</h2>
          
          <!-- 筛选和搜索 -->
          <div class="admin-filter-bar">
            <input 
              type="text" 
              v-model="reportSearch"
              placeholder="搜索课程名称、举报人..." 
              class="form-control admin-search"
            >
            <select v-model="reportStatusFilter" class="form-control">
              <option value="all">所有状态</option>
              <option value="pending">待处理</option>
              <option value="processing">处理中</option>
              <option value="resolved">已解决</option>
              <option value="dismissed">已驳回</option>
            </select>
            <select v-model="reportSeverityFilter" class="form-control">
              <option value="all">所有严重程度</option>
              <option value="low">低</option>
              <option value="medium">中</option>
              <option value="high">高</option>
              <option value="critical">严重</option>
            </select>
          </div>

          <!-- 优化后的表格布局 -->
          <div class="table-responsive">
            <table class="admin-table reported-courses-table">
              <thead>
                <tr>
                  <th width="80">举报ID</th>
                  <th width="200">课程信息</th>
                  <th width="250">举报原因</th>
                  <th width="150">举报人</th>
                  <th width="100">严重程度</th>
                  <th width="120">举报时间</th>
                  <th width="120">状态</th>
                  <th width="180">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="report in filteredReports" :key="report.id">
                  <td data-label="举报ID">
                    <strong>#{{ report.id }}</strong>
                  </td>
                  <td data-label="课程信息">
                    <div class="course-info compact">
                      <div class="course-title" :title="report.course.title">
                        {{ report.course.title }}
                      </div>
                      <div class="course-instructor text-muted">
                        讲师: {{ report.course.instructor }}
                      </div>
                      <div class="course-id text-muted">
                        ID: {{ report.courseId }}
                      </div>
                    </div>
                  </td>
                  <td data-label="举报原因">
                    <div class="report-reason compact">
                      <div class="reason-title" :title="report.reason">
                        {{ report.reason }}
                      </div>
                      <div v-if="report.description" class="reason-description text-muted" :title="report.description">
                        {{ truncateText(report.description, 50) }}
                      </div>
                      <div v-if="report.evidence && report.evidence.length > 0" class="evidence-count">
                        <i class="fas fa-paperclip"></i>
                        {{ report.evidence.length }}个证据
                      </div>
                    </div>
                  </td>
                  <td data-label="举报人">
                    <div class="reporter-info compact">
                      <div class="reporter-name">{{ report.reporter.name }}</div>
                      <div class="reporter-email text-muted">{{ report.reporter.email }}</div>
                    </div>
                  </td>
                  <td data-label="严重程度">
                    <span class="severity-badge large" :class="report.severity">
                      <i :class="getSeverityIcon(report.severity)"></i>
                      {{ getSeverityText(report.severity) }}
                    </span>
                  </td>
                  <td data-label="举报时间">
                    <div class="report-time">
                      <div class="date">{{ formatDate(report.reportedAt) }}</div>
                      <div class="time text-muted">{{ formatTime(report.reportedAt) }}</div>
                    </div>
                  </td>
                  <td data-label="状态">
                    <span class="status-badge large" :class="report.status">
                      <i :class="getStatusIcon(report.status)"></i>
                      {{ getStatusText(report.status) }}
                    </span>
                  </td>
                  <td data-label="操作">
                    <div class="action-buttons expanded">
                      <button 
                        v-if="report.status === 'pending'"
                        class="btn btn-warning btn-sm action-btn" 
                        @click="startProcessingReport(report.id)"
                        title="开始处理"
                      >
                        <i class="fas fa-play"></i>
                        <span class="btn-text">处理</span>
                      </button>
                      <button 
                        v-if="report.status === 'processing'"
                        class="btn btn-success btn-sm action-btn" 
                        @click="resolveReport(report.id)"
                        title="标记为已解决"
                      >
                        <i class="fas fa-check"></i>
                        <span class="btn-text">解决</span>
                      </button>
                      <button 
                        class="btn btn-danger btn-sm action-btn" 
                        @click="dismissReport(report.id)"
                        :title="report.status === 'pending' ? '驳回举报' : '撤销处理'"
                      >
                        <i class="fas fa-times"></i>
                        <span class="btn-text">{{ report.status === 'pending' ? '驳回' : '撤销' }}</span>
                      </button>
                      <button 
                        v-if="report.severity === 'critical' || report.severity === 'high'"
                        class="btn btn-danger btn-sm action-btn" 
                        @click="suspendCourse(report.courseId)"
                        title="暂停课程"
                      >
                        <i class="fas fa-pause"></i>
                        <span class="btn-text">暂停</span>
                      </button>
                      <button 
                        class="btn btn-outline btn-sm action-btn" 
                        @click="viewReportDetails(report.id)"
                        title="查看详情"
                      >
                        <i class="fas fa-eye"></i>
                        <span class="btn-text">详情</span>
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="filteredReports.length === 0">
                  <td colspan="8" class="text-center no-data">
                    <i class="fas fa-inbox"></i>
                    <div>暂无被举报课程</div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 举报统计 -->
          <div class="report-stats" v-if="filteredReports.length > 0">
            <h3>举报统计</h3>
            <div class="stats-grid">
              <div class="stat-item">
                <span class="stat-number">{{ pendingReportsCount }}</span>
                <span class="stat-label">待处理</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ highSeverityCount }}</span>
                <span class="stat-label">高严重程度</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ resolvedThisWeek }}</span>
                <span class="stat-label">本周已解决</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ averageResolutionTime }}</span>
                <span class="stat-label">平均处理时间(小时)</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 用户角色管理内容 -->
        <div class="tab-content" :class="{ active: activeTab === 'user-roles' }">
          <h2>用户教师身份管理</h2>
          <div class="admin-filter-bar">
            <input 
              type="text" 
              v-model="userSearch"
              placeholder="搜索用户 (ID, 姓名, 邮箱)..." 
              class="form-control admin-search"
            >
            <select v-model="roleFilter" class="form-control">
              <option value="all">所有用户</option>
              <option value="teacher">仅教师</option>
              <option value="student">仅学生</option>
            </select>
          </div>
          
          <table class="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>姓名</th>
                <th>邮箱</th>
                <th>当前身份</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>
                  <span class="role-tag" :class="user.role">{{ getUserRoleText(user.role) }}</span>
                </td>
                <td>
                  <button 
                    v-if="user.role !== 'teacher'"
                    class="btn btn-primary btn-sm" 
                    @click="promoteToTeacher(user.id)"
                  >
                    设为教师
                  </button>
                  <button 
                    v-if="user.role === 'teacher'"
                    class="btn btn-danger btn-sm" 
                    @click="demoteFromTeacher(user.id)"
                  >
                    取消教师
                  </button>
                  <button class="btn btn-outline btn-sm" @click="viewUserDetails(user.id)">详情</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    
    <!-- 举报详情模态框 -->
    <div class="modal" :class="{ show: showReportModal }">
      <div class="modal-content large-modal">
        <div class="modal-header">
          <h3>举报详情 - #{{ selectedReport?.id }}</h3>
          <button class="modal-close" @click="closeReportModal">×</button>
        </div>
        <div class="modal-body" v-if="selectedReport">
          <div class="report-details">
            <div class="detail-section">
              <h4>课程信息</h4>
              <div class="detail-grid">
                <div class="detail-item">
                  <label>课程名称:</label>
                  <span>{{ selectedReport.course.title }}</span>
                </div>
                <div class="detail-item">
                  <label>讲师:</label>
                  <span>{{ selectedReport.course.instructor }}</span>
                </div>
                <div class="detail-item">
                  <label>课程ID:</label>
                  <span>{{ selectedReport.courseId }}</span>
                </div>
              </div>
            </div>
            
            <div class="detail-section">
              <h4>举报信息</h4>
              <div class="detail-grid">
                <div class="detail-item">
                  <label>举报原因:</label>
                  <span class="reason-text">{{ selectedReport.reason }}</span>
                </div>
                <div class="detail-item full-width">
                  <label>详细描述:</label>
                  <p class="description-text">{{ selectedReport.description || '无详细描述' }}</p>
                </div>
                <div class="detail-item">
                  <label>严重程度:</label>
                  <span class="severity-badge" :class="selectedReport.severity">
                    {{ getSeverityText(selectedReport.severity) }}
                  </span>
                </div>
              </div>
            </div>
            
            <div class="detail-section">
              <h4>举报人信息</h4>
              <div class="detail-grid">
                <div class="detail-item">
                  <label>姓名:</label>
                  <span>{{ selectedReport.reporter.name }}</span>
                </div>
                <div class="detail-item">
                  <label>邮箱:</label>
                  <span>{{ selectedReport.reporter.email }}</span>
                </div>
                <div class="detail-item">
                  <label>举报时间:</label>
                  <span>{{ selectedReport.reportedAt }}</span>
                </div>
              </div>
            </div>
            
            <div class="detail-section" v-if="selectedReport.evidence">
              <h4>证据材料</h4>
              <div class="evidence-list">
                <div v-for="(evidence, index) in selectedReport.evidence" :key="index" class="evidence-item">
                  <i class="fas fa-paperclip"></i>
                  <span>{{ evidence.name }}</span>
                  <button class="btn btn-outline btn-sm" @click="viewEvidence(evidence)">查看</button>
                </div>
              </div>
            </div>
            
            <div class="detail-section" v-if="selectedReport.history">
              <h4>处理历史</h4>
              <div class="history-timeline">
                <div v-for="(event, index) in selectedReport.history" :key="index" class="timeline-event">
                  <div class="event-time">{{ event.time }}</div>
                  <div class="event-action">{{ event.action }}</div>
                  <div class="event-operator">操作人: {{ event.operator }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="closeReportModal">关闭</button>
          <button 
            v-if="selectedReport?.status === 'pending'"
            class="btn btn-warning" 
            @click="startProcessingReport(selectedReport.id)"
          >
            开始处理
          </button>
          <button 
            v-if="selectedReport?.status === 'processing'"
            class="btn btn-success" 
            @click="resolveReport(selectedReport.id)"
          >
            标记为已解决
          </button>
          <button 
            class="btn btn-danger" 
            @click="dismissReport(selectedReport.id)"
          >
            {{ selectedReport?.status === 'pending' ? '驳回举报' : '撤销处理' }}
          </button>
        </div>
      </div>
    </div>
  </main>
  
  <div v-else class="access-denied">
    <div class="container">
      <div class="access-denied-content">
        <i class="fas fa-exclamation-triangle"></i>
        <h2>访问被拒绝</h2>
        <p>您没有权限访问管理员控制台。</p>
        <router-link to="/" class="btn btn-primary">返回首页</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      activeTab: 'dashboard',
      userSearch: '',
      roleFilter: 'all',
      reportSearch: '',
      reportStatusFilter: 'all',
      reportSeverityFilter: 'all',
      pendingCourses: [],
      reportedCourses: [],
      users: [],
      stats: {
        teachers: 12,
        totalUsers: 15420,
        totalCourses: 250,
        resolutionRate: 85
      },
      showReportModal: false,
      selectedReport: null
    }
  },
  computed: {
    ...mapState(['user']),
    filteredUsers() {
      let filtered = this.users
      
      if (this.userSearch) {
        const query = this.userSearch.toLowerCase()
        filtered = filtered.filter(user => 
          user.id.toString().includes(query) ||
          user.name.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query)
        )
      }
      
      if (this.roleFilter !== 'all') {
        filtered = filtered.filter(user => user.role === this.roleFilter)
      }
      
      return filtered
    },
    filteredReports() {
      let filtered = this.reportedCourses
      
      // 搜索过滤
      if (this.reportSearch) {
        const query = this.reportSearch.toLowerCase()
        filtered = filtered.filter(report => 
          report.course.title.toLowerCase().includes(query) ||
          report.reporter.name.toLowerCase().includes(query) ||
          report.reason.toLowerCase().includes(query)
        )
      }
      
      // 状态过滤
      if (this.reportStatusFilter !== 'all') {
        filtered = filtered.filter(report => report.status === this.reportStatusFilter)
      }
      
      // 严重程度过滤
      if (this.reportSeverityFilter !== 'all') {
        filtered = filtered.filter(report => report.severity === this.reportSeverityFilter)
      }
      
      return filtered
    },
    pendingReportsCount() {
      return this.reportedCourses.filter(report => report.status === 'pending').length
    },
    highSeverityCount() {
      return this.reportedCourses.filter(report => 
        report.severity === 'high' || report.severity === 'critical'
      ).length
    },
    resolvedThisWeek() {
      // 模拟本周解决的举报数量
      return 8
    },
    averageResolutionTime() {
      // 模拟平均处理时间
      return '24'
    }
  },
  created() {
    this.loadData()
  },
  methods: {
    loadData() {
      // 模拟待审批课程数据
      this.pendingCourses = [
        {
          id: 101,
          title: 'React 高级开发技巧',
          instructor: '张老师',
          submittedDate: '2023-10-15',
          status: 'pending'
        },
        {
          id: 102,
          title: 'Node.js 后端架构',
          instructor: '李老师',
          submittedDate: '2023-10-14',
          status: 'pending'
        }
      ]
      
      // 模拟被举报课程数据
      this.reportedCourses = [
        {
          id: 201,
          courseId: 105,
          course: {
            title: 'Python 数据分析实战',
            instructor: '王老师'
          },
          reason: '内容包含不当信息',
          description: '课程第三章包含不适宜的教学内容，涉及敏感话题。',
          reporter: {
            name: '学生A',
            email: 'studentA@example.com'
          },
          severity: 'high',
          status: 'pending',
          reportedAt: '2023-10-16 14:30',
          evidence: [
            { name: '截图1.png', url: '#' },
            { name: '课程内容片段.pdf', url: '#' }
          ],
          history: []
        },
        {
          id: 202,
          courseId: 108,
          course: {
            title: 'Web 开发入门',
            instructor: '赵老师'
          },
          reason: '版权问题',
          description: '课程中使用的图片和代码示例未经授权使用。',
          reporter: {
            name: '学生B',
            email: 'studentB@example.com'
          },
          severity: 'critical',
          status: 'processing',
          reportedAt: '2023-10-15 09:15',
          evidence: [
            { name: '版权证明.pdf', url: '#' }
          ],
          history: [
            {
              time: '2023-10-15 10:00',
              action: '开始处理',
              operator: '管理员'
            }
          ]
        },
        {
          id: 203,
          courseId: 112,
          course: {
            title: '机器学习基础',
            instructor: '刘老师'
          },
          reason: '内容质量低下',
          description: '课程内容过于简单，与描述不符，存在多处错误。',
          reporter: {
            name: '学生C',
            email: 'studentC@example.com'
          },
          severity: 'medium',
          status: 'resolved',
          reportedAt: '2023-10-14 16:45',
          evidence: [],
          history: [
            {
              time: '2023-10-14 17:00',
              action: '开始处理',
              operator: '管理员'
            },
            {
              time: '2023-10-15 09:30',
              action: '标记为已解决 - 已要求讲师更新内容',
              operator: '管理员'
            }
          ]
        }
      ]
      
      // 模拟用户数据
      this.users = [
        {
          id: 1,
          name: '张三',
          email: 'zhangsan@example.com',
          role: 'student'
        },
        {
          id: 2,
          name: '李四',
          email: 'lisi@example.com',
          role: 'teacher'
        }
      ]
    },
    
    // 新增的工具方法
    truncateText(text, length) {
      if (!text) return ''
      if (text.length <= length) return text
      return text.substring(0, length) + '...'
    },

    formatDate(dateTime) {
      if (!dateTime) return ''
      return dateTime.split(' ')[0]
    },

    formatTime(dateTime) {
      if (!dateTime) return ''
      return dateTime.split(' ')[1] || ''
    },

    getSeverityIcon(severity) {
      const icons = {
        'low': 'fas fa-info-circle',
        'medium': 'fas fa-exclamation-triangle',
        'high': 'fas fa-exclamation-circle',
        'critical': 'fas fa-skull-crossbones'
      }
      return icons[severity] || 'fas fa-circle'
    },

    getStatusIcon(status) {
      const icons = {
        'pending': 'fas fa-clock',
        'processing': 'fas fa-cog fa-spin',
        'resolved': 'fas fa-check-circle',
        'dismissed': 'fas fa-ban'
      }
      return icons[status] || 'fas fa-circle'
    },
    
    // 举报相关方法
    startProcessingReport(reportId) {
      const report = this.reportedCourses.find(r => r.id === reportId)
      if (report) {
        report.status = 'processing'
        report.history.push({
          time: new Date().toLocaleString(),
          action: '开始处理',
          operator: '当前管理员'
        })
        this.$notify({
          type: 'info',
          title: '开始处理',
          message: `举报 #${reportId} 已开始处理`
        })
        this.closeReportModal()
      }
    },
    
    resolveReport(reportId) {
      const report = this.reportedCourses.find(r => r.id === reportId)
      if (report) {
        report.status = 'resolved'
        report.history.push({
          time: new Date().toLocaleString(),
          action: '标记为已解决',
          operator: '当前管理员'
        })
        this.$notify({
          type: 'success',
          title: '处理完成',
          message: `举报 #${reportId} 已标记为已解决`
        })
        this.closeReportModal()
      }
    },
    
    dismissReport(reportId) {
      const report = this.reportedCourses.find(r => r.id === reportId)
      if (report) {
        const previousStatus = report.status
        report.status = 'dismissed'
        report.history.push({
          time: new Date().toLocaleString(),
          action: `举报已驳回`,
          operator: '当前管理员'
        })
        this.$notify({
          type: 'warning',
          title: '举报驳回',
          message: `举报 #${reportId} 已驳回`
        })
        this.closeReportModal()
      }
    },
    
    suspendCourse(courseId) {
      this.$notify({
        type: 'warning',
        title: '课程暂停',
        message: `课程 ID: ${courseId} 已被暂停`
      })
    },
    
    viewReportDetails(reportId) {
      this.selectedReport = this.reportedCourses.find(r => r.id === reportId)
      this.showReportModal = true
    },
    
    closeReportModal() {
      this.showReportModal = false
      this.selectedReport = null
    },
    
    viewEvidence(evidence) {
      this.$notify({
        type: 'info',
        title: '查看证据',
        message: `查看证据文件: ${evidence.name}`
      })
    },
    
    getSeverityText(severity) {
      const severityMap = {
        'low': '低',
        'medium': '中',
        'high': '高',
        'critical': '严重'
      }
      return severityMap[severity] || severity
    },
    
    getStatusText(status) {
      const statusMap = {
        'pending': '待处理',
        'processing': '处理中',
        'resolved': '已解决',
        'dismissed': '已驳回'
      }
      return statusMap[status] || status
    },
    
    // 原有方法保持不变
    approveCourse(courseId) {
      const course = this.pendingCourses.find(c => c.id === courseId)
      if (course) {
        this.pendingCourses = this.pendingCourses.filter(c => c.id !== courseId)
        this.$notify({
          type: 'success',
          title: '审批通过',
          message: `课程 "${course.title}" 已通过审批`
        })
      }
    },
    
    rejectCourse(courseId) {
      const course = this.pendingCourses.find(c => c.id === courseId)
      if (course) {
        this.pendingCourses = this.pendingCourses.filter(c => c.id !== courseId)
        this.$notify({
          type: 'warning',
          title: '审批拒绝',
          message: `课程 "${course.title}" 已被拒绝`
        })
      }
    },
    
    viewCourseDetails(courseId) {
      this.$notify({
        type: 'info',
        title: '查看详情',
        message: `查看课程 ID: ${courseId} 的详细信息`
      })
    },
    
    promoteToTeacher(userId) {
      const user = this.users.find(u => u.id === userId)
      if (user) {
        user.role = 'teacher'
        this.$notify({
          type: 'success',
          title: '权限提升',
          message: `用户 "${user.name}" 已被设为教师`
        })
      }
    },
    
    demoteFromTeacher(userId) {
      const user = this.users.find(u => u.id === userId)
      if (user) {
        user.role = 'student'
        this.$notify({
          type: 'warning',
          title: '权限变更',
          message: `用户 "${user.name}" 的教师权限已被取消`
        })
      }
    },
    
    viewUserDetails(userId) {
      this.$notify({
        type: 'info',
        title: '查看详情',
        message: `查看用户 ID: ${userId} 的详细信息`
      })
    },
    
    getUserRoleText(role) {
      const roles = {
        'teacher': '教师',
        'student': '学生',
        'admin': '管理员'
      }
      return roles[role] || role
    }
  }
}
</script>

<style scoped>
.access-denied {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
}

.access-denied-content i {
  font-size: 4rem;
  color: var(--warning);
  margin-bottom: 20px;
}

.access-denied-content h2 {
  margin-bottom: 10px;
  color: var(--text);
}

.access-denied-content p {
  color: var(--text-light);
  margin-bottom: 20px;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 0.8rem;
  margin-right: 5px;
}

.text-center {
  text-align: center;
}

/* 表格响应式容器 */
.table-responsive {
  overflow-x: auto;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: white;
  margin-bottom: 20px;
}

/* 优化举报课程表格 */
.reported-courses-table {
  min-width: 1200px;
  margin: 0;
}

.reported-courses-table th {
  background-color: var(--primary-dark);
  color: white;
  font-weight: 600;
  padding: 12px 15px;
  white-space: nowrap;
}

.reported-courses-table td {
  padding: 15px;
  vertical-align: top;
  border-bottom: 1px solid var(--border);
}

/* 紧凑信息布局 */
.course-info.compact .course-title {
  font-weight: 600;
  margin-bottom: 4px;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.course-info.compact .course-instructor,
.course-info.compact .course-id {
  font-size: 0.8rem;
  line-height: 1.2;
}

.report-reason.compact .reason-title {
  font-weight: 600;
  margin-bottom: 6px;
  color: var(--text);
  line-height: 1.3;
}

.report-reason.compact .reason-description {
  font-size: 0.85rem;
  line-height: 1.4;
  margin-bottom: 6px;
  color: var(--text-light);
}

.evidence-count {
  font-size: 0.8rem;
  color: var(--primary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.evidence-count i {
  font-size: 0.7rem;
}

.reporter-info.compact .reporter-name {
  font-weight: 500;
  margin-bottom: 2px;
}

.reporter-info.compact .reporter-email {
  font-size: 0.8rem;
}

.report-time .date {
  font-weight: 500;
  margin-bottom: 2px;
}

.report-time .time {
  font-size: 0.8rem;
}

/* 举报相关样式 */
.severity-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 500;
  color: white;
}

.severity-badge.low {
  background-color: var(--success);
}

.severity-badge.medium {
  background-color: var(--warning);
}

.severity-badge.high {
  background-color: var(--danger);
}

.severity-badge.critical {
  background-color: #8b0000;
}

/* 更大的状态和严重程度徽章 */
.status-badge.large,
.severity-badge.large {
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-width: 80px;
  justify-content: center;
  white-space: nowrap;
}

.status-badge.large i,
.severity-badge.large i {
  font-size: 0.8rem;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 500;
}

.status-badge.pending {
  background-color: var(--warning);
  color: white;
}

.status-badge.processing {
  background-color: var(--info);
  color: white;
}

.status-badge.resolved {
  background-color: var(--success);
  color: white;
}

.status-badge.dismissed {
  background-color: var(--text-light);
  color: white;
}

/* 扩展的操作按钮 */
.action-buttons.expanded {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 120px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  font-size: 0.8rem;
  width: 100%;
  justify-content: flex-start;
}

.action-btn .btn-text {
  flex: 1;
  text-align: left;
}

.action-buttons {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.action-buttons .btn-sm {
  padding: 4px 6px;
  min-width: 30px;
}

.course-info, .reporter-info, .report-reason {
  font-size: 0.9rem;
}

.text-muted {
  color: var(--text-light);
  font-size: 0.8rem;
}

/* 无数据状态 */
.no-data {
  padding: 40px 20px;
  color: var(--text-light);
  text-align: center;
}

.no-data i {
  font-size: 3rem;
  margin-bottom: 15px;
  opacity: 0.5;
}

.no-data div {
  font-size: 1rem;
}

/* 举报统计 */
.report-stats {
  margin-top: 30px;
  padding: 20px;
  background: var(--secondary);
  border-radius: 8px;
}

.report-stats h3 {
  margin-bottom: 15px;
  color: var(--text);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  background: white;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-number {
  display: block;
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--primary);
  margin-bottom: 5px;
}

.stat-label {
  color: var(--text-light);
  font-size: 0.9rem;
}

/* 模态框详情样式 */
.report-details {
  max-height: 60vh;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border);
}

.detail-section:last-child {
  border-bottom: none;
}

.detail-section h4 {
  margin-bottom: 15px;
  color: var(--primary);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-item label {
  font-weight: 600;
  color: var(--text-light);
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.reason-text {
  font-weight: 600;
  color: var(--text);
}

.description-text {
  background: var(--secondary);
  padding: 10px;
  border-radius: 4px;
  margin: 0;
  line-height: 1.5;
}

.evidence-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.evidence-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: var(--secondary);
  border-radius: 4px;
}

.evidence-item i {
  color: var(--primary);
}

.history-timeline {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.timeline-event {
  padding: 10px;
  background: var(--secondary);
  border-radius: 4px;
  border-left: 3px solid var(--primary);
}

.event-time {
  font-size: 0.8rem;
  color: var(--text-light);
  margin-bottom: 4px;
}

.event-action {
  font-weight: 500;
  margin-bottom: 2px;
}

.event-operator {
  font-size: 0.8rem;
  color: var(--text-light);
}

/* 角色标签 */
.role-tag {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.role-tag.teacher {
  background-color: var(--info);
  color: white;
}

.role-tag.student {
  background-color: var(--secondary);
  color: var(--text-light);
  border: 1px solid var(--border);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .reported-courses-table {
    min-width: 1000px;
  }
  
  .reported-courses-table th:nth-child(2),
  .reported-courses-table td:nth-child(2) {
    min-width: 180px;
  }
  
  .reported-courses-table th:nth-child(3),
  .reported-courses-table td:nth-child(3) {
    min-width: 200px;
  }
}

@media (max-width: 768px) {
  .table-responsive {
    border: none;
    border-radius: 0;
  }
  
  .reported-courses-table {
    min-width: auto;
  }
  
  .reported-courses-table thead {
    display: none;
  }
  
  .reported-courses-table tr {
    display: block;
    margin-bottom: 20px;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 15px;
  }
  
  .reported-courses-table td {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    text-align: left;
    border-bottom: 1px solid var(--border-light);
    padding: 12px 0;
  }
  
  .reported-courses-table td:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }
  
  .reported-courses-table td::before {
    content: attr(data-label);
    font-weight: 600;
    color: var(--text);
    min-width: 80px;
    margin-right: 15px;
    font-size: 0.9rem;
  }
  
  .action-buttons.expanded {
    flex-direction: row;
    flex-wrap: wrap;
    min-width: auto;
  }
  
  .action-btn {
    flex: 1;
    min-width: 80px;
    justify-content: center;
  }
  
  .action-btn .btn-text {
    display: none;
  }
  
  .status-badge.large,
  .severity-badge.large {
    min-width: 60px;
    padding: 6px 8px;
    font-size: 0.8rem;
  }

  .admin-table thead {
    display: none;
  }

  .admin-table tr {
    display: block;
    margin-bottom: 15px;
    border: 1px solid var(--border);
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }

  .admin-table td {
    display: flex;
    justify-content: space-between;
    align-items: center;
    text-align: right;
    border-bottom: none;
    padding: 8px 15px;
  }
  
  .admin-table td::before {
    content: attr(data-label);
    font-weight: 600;
    text-transform: uppercase;
    font-size: 12px;
    color: var(--text-light);
    margin-right: 10px;
  }

  .action-buttons {
    justify-content: flex-end;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons .btn-sm {
    min-width: 25px;
    padding: 3px 5px;
  }
  
  .action-buttons.expanded {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
}

/* 改善文本显示 */
.text-muted {
  color: var(--text-light) !important;
  opacity: 0.8;
}

/* 改善边框颜色 */
:root {
  --border-light: #f0f0f0;
}
</style>