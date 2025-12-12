import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { guestOnly: true } // 只有未登录用户可以访问
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { guestOnly: true } // 只有未登录用户可以访问
  },
  {
    path: '/personal-info',
    name: 'PersonalInfo',
    component: () => import('../views/PersonalInfo.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/article-management',
    name: 'ArticleManagement',
    component: () => import('../views/ArticleManagement.vue')
  },
  {
    path: '/personal-information',
    name: 'PersonalInformation',
    component: () => import('../views/PersonalInfo.vue')
  },
  {
    path: '/teacher-dashboard',
    name: 'TeacherDashboard',
    component: () => import('../views/TeacherDashboard.vue')
  },
  {
    path: '/video-analysis',
    name: 'VideoAnalysis',
    component: () => import('../views/VideoAnalysis.vue')
  },
  {
    path: '/exercise-analysis',
    name: 'ExerciseAnalysis',
    component: () => import('../views/ExerciseAnalysis.vue')
  },
  {
    path: '/course-management',
    name: 'CourseManagement',
    component: () => import('../views/CourseManagement.vue')
  },
  {
    path: '/user-management',
    name: 'UserManagement',
    component: () => import('../views/UserManagement.vue')
  },
  {
    path: '/favorites-management',
    name: 'FavoritesManagement',
    component: () => import('../views/FavoritesManagement.vue')
  },
  {
    path: '/work-engine',
    name: 'WorkEngine',
    component: () => import('../views/TeacherDashboard.vue')
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('../views/SearchPage.vue')
  },
  {
    path: '/course/:courseId/player',
    name: 'VideoPlayer',
    component: () => import('../views/VideoPlayer.vue'),
    props: route => ({
      courseId: parseInt(route.params.courseId)
    })
  },
  {
  path: '/course/:courseId/exercise/:seriesId',
  name: 'ExerciseSeries',
  component: () => import('../views/ExerciseSeries.vue'),
  props: route => ({
    courseId: parseInt(route.params.courseId),
    seriesId: route.params.seriesId
  })
  },
  {
    path: '/video-upload',
    name: 'VideoUpload',
    component: () => import('../views/VideoUpload.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/preferences-setup',
    name: 'PreferencesSetup',
    component: () => import('../views/PreferencesSetup.vue'),
    meta: { 
      requiresAuth: true,
      newUserOnly: true // 只有新用户需要访问
    }
  },
  {
  path: '/category/:categoryId?',
  name: 'Category',
  component: () => import('../views/Category.vue'),
  props: true
  },
  {
    path: '/teacher-space',
    name: 'TeacherSpace',
    component: () => import('../views/TeacherSpace.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 添加路由守卫
router.beforeEach((to, from, next) => {
  // 检查用户是否登录
  const currentUser = localStorage.getItem('bgareaCurrentUser') || sessionStorage.getItem('bgareaCurrentUser')
  const isAuthenticated = !!currentUser
  
  // 检查偏好设置状态
  const preferencesCompleted = localStorage.getItem('preferencesCompleted') === 'true'
  const preferencesSkipped = localStorage.getItem('preferencesSkipped') === 'true'
  
  // 如果路由需要认证但用户未登录
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }
  
  // 如果只有未登录用户可以访问的路由
  if (to.meta.guestOnly && isAuthenticated) {
    // 检查偏好设置状态
    if (!preferencesCompleted && !preferencesSkipped) {
      next('/preferences-setup')
    } else {
      next('/')
    }
    return
  }
  
  // 处理偏好设置页面
  if (to.path === '/preferences-setup') {
    if (!isAuthenticated) {
      next('/login')
      return
    }
    
    // 如果已经完成或跳过了偏好设置，跳转到首页
    if (preferencesCompleted || preferencesSkipped) {
      next('/')
      return
    }
  }
  
  // 如果用户已登录且访问首页
  if (to.path === '/' && isAuthenticated) {
    // 检查是否需要设置偏好
    if (!preferencesCompleted && !preferencesSkipped) {
      next('/preferences-setup')
      return
    }
  }
  
  // 继续导航
  next()
})

export default router