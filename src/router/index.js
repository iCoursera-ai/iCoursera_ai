import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Courses from '../views/Courses.vue'
import CourseDetail from '../views/CourseDetail.vue'
import VideoPlayer from '../views/VideoPlayer.vue'
import Quiz from '../views/Quiz.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'
import UserProfile from '../views/UserProfile.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/courses', name: 'Courses', component: Courses },
  { path: '/course/:id', name: 'CourseDetail', component: CourseDetail, props: true },
  { path: '/video/:courseId/:videoId', name: 'VideoPlayer', component: VideoPlayer, props: true },
  { path: '/quiz/:courseId/:quizId', name: 'Quiz', component: Quiz, props: true },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/user/:id', name: 'UserProfile', component: UserProfile, props: true },
  { path: '/admin', name: 'AdminDashboard', component: AdminDashboard }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router