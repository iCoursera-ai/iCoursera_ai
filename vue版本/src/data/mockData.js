const TEST_ACCOUNT = {
  email: 'test@bgarea.com',
  password: 'test123456',
  username: '测试教师',
  id: 'test-teacher-001',
  realname: '张教授',
  realnameStatus: '已认证',
  userId: 'UID000001',
  phone: '13800138000',
  location: '北京市',
  school: '清华大学',
  followers: 15200,
  courses: 20,
  avatar: 'https://picsum.photos/200/200?random=teacher',
  bio: '计算机科学教授，专注于操作系统、计算机网络等领域的教学与研究，拥有20年教学经验。',
  signature: '教育改变未来，知识成就梦想',
  isNewUser: false,
  hasPreferences: true,
  registerTime: '2020-01-15T08:00:00.000Z',
  teacherCertStatus: '已认证',
  department: '计算机科学与技术学院'
}

const TEST_TEACHER_COURSES = [
  {
    id: 232,
    name: '操作系统原理与实践',
    tag: '操作系统',
    author: '张教授',
    playCount: 15600,
    createdAt: '2023-01-15 10:30',
    status: '已上线',
    avatar: 'https://picsum.photos/400/225?random=os1',
    viewCount: '156.0w',
    userCount: '12.5w',
    increase: '1245w',
    increaseIcon: 'fa fa-caret-up text-success',
    increaseDirection: 'text-success'
  },
  {
    id: 254,
    name: '计算机网络基础',
    tag: '计算机网络',
    author: '张教授',
    playCount: 12800,
    createdAt: '2023-02-20 09:15',
    status: '已上线',
    avatar: 'https://picsum.photos/400/225?random=network1',
    viewCount: '128.0w',
    userCount: '10.2w',
    increase: '980w',
    increaseIcon: 'fa fa-caret-up text-success',
    increaseDirection: 'text-success'
  },
  {
    id: 46,
    name: '数据结构与算法',
    tag: '编程基础',
    author: '张教授',
    playCount: 18900,
    createdAt: '2023-03-10 14:20',
    status: '已上线',
    avatar: 'https://picsum.photos/400/225?random=ds1',
    viewCount: '189.0w',
    userCount: '15.6w',
    increase: '1560w',
    increaseIcon: 'fa fa-caret-up text-success',
    increaseDirection: 'text-success'
  },
  {
    id: 577,
    name: '数据库系统原理',
    tag: '数据库',
    author: '张教授',
    playCount: 14200,
    createdAt: '2023-04-05 11:45',
    status: '已上线',
    avatar: 'https://picsum.photos/400/225?random=db1',
    viewCount: '142.0w',
    userCount: '11.8w',
    increase: '1120w',
    increaseIcon: 'fa fa-caret-up text-success',
    increaseDirection: 'text-success'
  },
  {
    id: 233,
    name: 'Linux系统管理',
    tag: '操作系统',
    author: '张教授',
    playCount: 11500,
    createdAt: '2023-05-12 16:30',
    status: '已上线',
    avatar: 'https://picsum.photos/400/225?random=linux1',
    viewCount: '115.0w',
    userCount: '9.5w',
    increase: '890w',
    increaseIcon: 'fa fa-caret-up text-success',
    increaseDirection: 'text-success'
  },
  {
    id: 255,
    name: '软件工程实践',
    tag: '软件工程',
    author: '张教授',
    playCount: 10800,
    createdAt: '2023-06-18 10:00',
    status: '已上线',
    avatar: 'https://picsum.photos/400/225?random=se1',
    viewCount: '108.0w',
    userCount: '8.9w',
    increase: '750w',
    increaseIcon: 'fa fa-caret-up text-success',
    increaseDirection: 'text-success'
  },
  {
    id: 47,
    name: '编译原理',
    tag: '编译器',
    author: '张教授',
    playCount: 9600,
    createdAt: '2023-07-22 13:15',
    status: '已上线',
    avatar: 'https://picsum.photos/400/225?random=compiler1',
    viewCount: '96.0w',
    userCount: '7.8w',
    increase: '680w',
    increaseIcon: 'fa fa-caret-up text-success',
    increaseDirection: 'text-success'
  },
  {
    id: 578,
    name: '计算机组成原理',
    tag: '计算机基础',
    author: '张教授',
    playCount: 13400,
    createdAt: '2023-08-30 09:45',
    status: '已上线',
    avatar: 'https://picsum.photos/400/225?random=arch1',
    viewCount: '134.0w',
    userCount: '11.2w',
    increase: '1050w',
    increaseIcon: 'fa fa-caret-up text-success',
    increaseDirection: 'text-success'
  },
  {
    id: 234,
    name: '网络安全基础',
    tag: '网络安全',
    author: '张教授',
    playCount: 16800,
    createdAt: '2023-09-15 15:20',
    status: '已上线',
    avatar: 'https://picsum.photos/400/225?random=security1',
    viewCount: '168.0w',
    userCount: '13.9w',
    increase: '1380w',
    increaseIcon: 'fa fa-caret-up text-success',
    increaseDirection: 'text-success'
  },
  {
    id: 256,
    name: '分布式系统',
    tag: '系统架构',
    author: '张教授',
    playCount: 8900,
    createdAt: '2023-10-20 11:30',
    status: '已上线',
    avatar: 'https://picsum.photos/400/225?random=distributed1',
    viewCount: '89.0w',
    userCount: '7.2w',
    increase: '620w',
    increaseIcon: 'fa fa-caret-up text-success',
    increaseDirection: 'text-success'
  }
]

const TEST_DASHBOARD_DATA = {
  videoStats: {
    totalPlayCount: '2456.8w',
    totalPlayCountChange: {
      value: '1856w',
      direction: 'up',
      icon: 'fa fa-caret-up'
    },
    fansCount: '152.0w',
    fansCountChange: {
      value: '12.5w',
      direction: 'up',
      icon: 'fa fa-caret-up'
    },
    totalVideos: '20',
    totalComments: '1856.3w',
    totalCommentsChange: {
      value: '956w',
      direction: 'up',
      icon: 'fa fa-caret-up'
    }
  },
  courses: [
    {
      id: 1,
      name: '操作系统原理与实践',
      avatar: 'https://picsum.photos/32/32?random=os1',
      playCount: '156.0w',
      increase: '12.5w',
      increaseIcon: 'fa fa-caret-up text-success',
      increaseDirection: 'text-success',
      viewCount: '156.0w',
      userCount: '12.5w'
    },
    {
      id: 2,
      name: '计算机网络基础',
      avatar: 'https://picsum.photos/32/32?random=network1',
      playCount: '128.0w',
      increase: '9.8w',
      increaseIcon: 'fa fa-caret-up text-success',
      increaseDirection: 'text-success',
      viewCount: '128.0w',
      userCount: '10.2w'
    },
    {
      id: 3,
      name: '数据结构与算法',
      avatar: 'https://picsum.photos/32/32?random=ds1',
      playCount: '189.0w',
      increase: '15.6w',
      increaseIcon: 'fa fa-caret-up text-success',
      increaseDirection: 'text-success',
      viewCount: '189.0w',
      userCount: '15.6w'
    },
    {
      id: 4,
      name: '数据库系统原理',
      avatar: 'https://picsum.photos/32/32?random=db1',
      playCount: '142.0w',
      increase: '11.2w',
      increaseIcon: 'fa fa-caret-up text-success',
      increaseDirection: 'text-success',
      viewCount: '142.0w',
      userCount: '11.8w'
    },
    {
      id: 5,
      name: 'Linux系统管理',
      avatar: 'https://picsum.photos/32/32?random=linux1',
      playCount: '115.0w',
      increase: '8.9w',
      increaseIcon: 'fa fa-caret-up text-success',
      increaseDirection: 'text-success',
      viewCount: '115.0w',
      userCount: '9.5w'
    },
    {
      id: 6,
      name: '软件工程实践',
      avatar: 'https://picsum.photos/32/32?random=se1',
      playCount: '108.0w',
      increase: '7.5w',
      increaseIcon: 'fa fa-caret-up text-success',
      increaseDirection: 'text-success',
      viewCount: '108.0w',
      userCount: '8.9w'
    },
    {
      id: 7,
      name: '编译原理',
      avatar: 'https://picsum.photos/32/32?random=compiler1',
      playCount: '96.0w',
      increase: '6.8w',
      increaseIcon: 'fa fa-caret-up text-success',
      increaseDirection: 'text-success',
      viewCount: '96.0w',
      userCount: '7.8w'
    },
    {
      id: 8,
      name: '计算机组成原理',
      avatar: 'https://picsum.photos/32/32?random=arch1',
      playCount: '134.0w',
      increase: '10.5w',
      increaseIcon: 'fa fa-caret-up text-success',
      increaseDirection: 'text-success',
      viewCount: '134.0w',
      userCount: '11.2w'
    },
    {
      id: 9,
      name: '网络安全基础',
      avatar: 'https://picsum.photos/32/32?random=security1',
      playCount: '168.0w',
      increase: '13.8w',
      increaseIcon: 'fa fa-caret-up text-success',
      increaseDirection: 'text-success',
      viewCount: '168.0w',
      userCount: '13.9w'
    },
    {
      id: 10,
      name: '分布式系统',
      avatar: 'https://picsum.photos/32/32?random=distributed1',
      playCount: '89.0w',
      increase: '6.2w',
      increaseIcon: 'fa fa-caret-up text-success',
      increaseDirection: 'text-success',
      viewCount: '89.0w',
      userCount: '7.2w'
    },
    {
      id: 11,
      name: '人工智能导论',
      avatar: 'https://picsum.photos/32/32?random=ai1',
      playCount: '176.0w',
      increase: '14.2w',
      increaseIcon: 'fa fa-caret-up text-success',
      increaseDirection: 'text-success',
      viewCount: '176.0w',
      userCount: '14.5w'
    },
    {
      id: 12,
      name: '云计算技术',
      avatar: 'https://picsum.photos/32/32?random=cloud1',
      playCount: '98.0w',
      increase: '7.8w',
      increaseIcon: 'fa fa-caret-up text-success',
      increaseDirection: 'text-success',
      viewCount: '98.0w',
      userCount: '8.1w'
    }
  ]
}

function initTestAccount() {
  const users = JSON.parse(localStorage.getItem('bgareaUsers') || '[]')
  const testUserExists = users.some(u => u.email === TEST_ACCOUNT.email)

  if (!testUserExists) {
    users.push(TEST_ACCOUNT)
    localStorage.setItem('bgareaUsers', JSON.stringify(users))
  } else {
    const userIndex = users.findIndex(u => u.email === TEST_ACCOUNT.email)
    users[userIndex] = TEST_ACCOUNT
    localStorage.setItem('bgareaUsers', JSON.stringify(users))
  }
}

function isTestAccount(email) {
  return email === TEST_ACCOUNT.email
}

function getTestAccountData() {
  return {
    account: TEST_ACCOUNT,
    courses: TEST_TEACHER_COURSES,
    dashboardData: TEST_DASHBOARD_DATA
  }
}

function getEmptyData() {
  return {
    courses: [],
    dashboardData: {
      videoStats: {
        totalPlayCount: '0',
        totalPlayCountChange: {
          value: '0',
          direction: 'up',
          icon: 'fa fa-caret-up'
        },
        fansCount: '0',
        fansCountChange: {
          value: '0',
          direction: 'up',
          icon: 'fa fa-caret-up'
        },
        totalVideos: '0',
        totalComments: '0',
        totalCommentsChange: {
          value: '0',
          direction: 'up',
          icon: 'fa fa-caret-up'
        }
      },
      courses: []
    }
  }
}

export {
  TEST_ACCOUNT,
  TEST_TEACHER_COURSES,
  TEST_DASHBOARD_DATA,
  initTestAccount,
  isTestAccount,
  getTestAccountData,
  getEmptyData
}
