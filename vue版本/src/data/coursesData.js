const categories = ['人工智能', '机器学习', '深度学习', '数据科学', '编程开发', '金融投资', '医学健康', '商业管理', '设计创意', 'Web开发']

const teachers = [
  '李明教授', '王静教授', '陈明教授', '张伟教授', '刘芳教授',
  '赵明教授', '李华教授', '王芳教授', '孙教授', '周老师',
  '吴工程师', '郑博士', '钱老师', '黄教授', '林老师'
]

const courseTitles = {
  '人工智能': [
    'AI基础入门与实践',
    '人工智能算法精讲',
    'AI项目实战训练营',
    '智能系统设计',
    'AI伦理与应用',
    '人工智能前沿技术',
    '智能机器人开发',
    'AI数据处理'
  ],
  '机器学习': [
    '机器学习基础：理论与Python实践',
    '机器学习算法精讲与实战',
    '机器学习工程师养成',
    '统计学习方法',
    '机器学习项目实战',
    'sklearn实战教程',
    '机器学习数学基础',
    '特征工程实践'
  ],
  '深度学习': [
    '深度学习实战：从零搭建AI模型',
    '深度学习进阶：神经网络优化与应用',
    'TensorFlow实战教程',
    'PyTorch深度学习',
    '卷积神经网络详解',
    'RNN与LSTM实战',
    'GAN生成对抗网络',
    'Transformer架构详解'
  ],
  '数据科学': [
    'Python数据分析实战：从数据处理到可视化',
    '数据科学入门',
    '大数据分析技术',
    '数据挖掘算法',
    '数据可视化实战',
    'Pandas数据处理',
    '数据清洗技巧',
    '统计分析方法'
  ],
  '编程开发': [
    'Python编程零基础入门',
    'Java全栈开发',
    'Web全栈开发：React + Node.js实战',
    'JavaScript高级编程',
    'Vue3实战开发',
    'Spring Boot企业级开发',
    'Go语言开发实战',
    'Rust编程入门'
  ],
  '金融投资': [
    '金融投资分析与量化交易',
    '股票投资实战',
    '金融衍生品分析',
    '量化交易策略',
    '金融风险管理',
    '证券投资分析',
    '期货交易实战',
    '区块链金融应用'
  ],
  '医学健康': [
    '医学基础：人体解剖与生理',
    '人工智能在医疗健康领域的应用',
    '医学影像分析',
    '临床医学基础',
    '中医养生保健',
    '药物研发流程',
    '医疗数据分析',
    '健康管理实务'
  ],
  '商业管理': [
    'MBA核心课程精讲',
    '项目管理实战',
    '战略管理',
    '市场营销学',
    '人力资源管理',
    '财务管理基础',
    '运营管理',
    '创业管理'
  ],
  '设计创意': [
    'UI/UX设计实战',
    '平面设计基础',
    '色彩理论与应用',
    '品牌视觉设计',
    'Figma设计实战',
    '网页设计规范',
    '交互设计原理',
    '创意思维训练'
  ],
  'Web开发': [
    '前端开发完全指南',
    'React开发实战',
    'Vue全家桶实战',
    'Node.js后端开发',
    'RESTful API设计',
    '微服务架构',
    'Docker容器化',
    'Kubernetes实战'
  ]
}

const descriptions = {
  '人工智能': '全面讲解人工智能基础理论与实践应用，掌握核心算法与技术',
  '机器学习': '系统学习机器学习核心算法，结合实战案例掌握模型训练与评估',
  '深度学习': '深入学习深度神经网络，掌握主流框架与实际应用',
  '数据科学': '掌握数据分析核心技能，从数据处理到可视化全流程',
  '编程开发': '从基础语法到项目实战，系统学习编程开发技能',
  '金融投资': '学习金融市场分析方法，掌握投资策略与风险管理',
  '医学健康': '系统学习医学基础知识与健康管理实践',
  '商业管理': '掌握现代企业管理核心理念与实战技能',
  '设计创意': '学习设计原理与创意表达，提升审美与实践能力',
  'Web开发': '全栈Web开发技能培养，从前端到后端完整掌握'
}

const difficulties = ['beginner', 'intermediate', 'advanced']
const badges = [
  { class: 'badge-blue', text: '新品' },
  { class: 'badge-green', text: '精讲' },
  { class: 'badge-orange', text: '热门' },
  { class: 'badge-blue', text: '精品' },
  { class: 'badge-green', text: '推荐' }
]

function generateCourses() {
  const courses = []
  let id = 1

  Object.keys(courseTitles).forEach(category => {
    courseTitles[category].forEach(title => {
      for (let i = 0; i < 3; i++) {
        const teacher = teachers[Math.floor(Math.random() * teachers.length)]
        const views = (Math.random() * 50 + 5).toFixed(1) + '万播放'
        const rating = (95 + Math.floor(Math.random() * 5)) + '%好评'
        const duration = 3600 + Math.floor(Math.random() * 50000)
        const difficulty = difficulties[Math.floor(Math.random() * difficulties.length)]
        const price = Math.random() > 0.5 ? 'free' : 'paid'
        const badge = badges[Math.floor(Math.random() * badges.length)]

        courses.push({
          id: id++,
          title: title + (i > 0 ? ` (${i + 1})` : ''),
          description: descriptions[category] || '精品课程，值得学习',
          teacher: teacher,
          views: views,
          rating: rating,
          category: category,
          duration: duration,
          image: `https://picsum.photos/300/200?random=${id}`,
          badgeClass: badge.class,
          badgeText: badge.text,
          difficulty: difficulty,
          price: price
        })
      }
    })
  })

  return courses
}

export const allCourses = generateCourses()

export function searchCourses(query) {
  if (!query || !query.trim()) {
    return allCourses
  }

  const searchTerm = query.toLowerCase().trim()
  return allCourses.filter(course =>
    course.title.toLowerCase().includes(searchTerm) ||
    course.description.toLowerCase().includes(searchTerm) ||
    course.teacher.toLowerCase().includes(searchTerm) ||
    course.category.toLowerCase().includes(searchTerm)
  )
}
