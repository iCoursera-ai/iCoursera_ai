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
              <i class="fas fa-chalkboard-teacher"></i>
              <h4>待审批课程</h4>
              <p id="statPendingCourses">{{ pendingCourses.length }}</p>
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
      pendingCourses: [],
      users: [],
      stats: {
        teachers: 12,
        totalUsers: 15420,
        totalCourses: 250
      }
    }
  },
  computed: {
    ...mapState(['user']),
    filteredUsers() {
      let filtered = this.users
      
      // 搜索过滤
      if (this.userSearch) {
        const query = this.userSearch.toLowerCase()
        filtered = filtered.filter(user => 
          user.id.toString().includes(query) ||
          user.name.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query)
        )
      }
      
      // 角色过滤
      if (this.roleFilter !== 'all') {
        filtered = filtered.filter(user => user.role === this.roleFilter)
      }
      
      return filtered
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
        },
        {
          id: 103,
          title: 'Vue 3 组合式 API',
          instructor: '王老师',
          submittedDate: '2023-10-13',
          status: 'pending'
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
        },
        {
          id: 3,
          name: '王五',
          email: 'wangwu@example.com',
          role: 'student'
        },
        {
          id: 4,
          name: '赵六',
          email: 'zhaoliu@example.com',
          role: 'teacher'
        }
      ]
    },
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
</style>