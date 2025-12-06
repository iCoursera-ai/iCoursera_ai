# insert_data.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()  


from datetime import datetime, timedelta
import json
from database import SessionLocal, engine
from models import Base, User, UserProfile, Course, CourseModule, Quiz, Question, CourseStatistics, UserBehaviorLog


def insert_sample_data():
    """插入示例数据"""
    db = SessionLocal()
    
    try:
        # 1. 插入用户数据
        print("📝 插入用户数据...")
        users = [
            {
                "username": "student_zhang",
                "email": "zhang@example.com",
                "password_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # password: 123456
                "full_name": "张明",
                "role": "student",
                "created_at": datetime.now()
            },
            {
                "username": "professor_wang",
                "email": "wangjing@tsinghua.edu.cn",
                "password_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "full_name": "王静",
                "role": "instructor",
                "created_at": datetime.now()
            },
            {
                "username": "professor_liu",
                "email": "liufang@zju.edu.cn",
                "password_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "full_name": "刘芳",
                "role": "instructor",
                "created_at": datetime.now()
            },
            {
                "username": "professor_zhang",
                "email": "zhangwei@pku.edu.cn",
                "password_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "full_name": "张伟",
                "role": "instructor",
                "created_at": datetime.now()
            }
        ]
        
        for user_data in users:
            user = User(**user_data)
            db.add(user)
        db.commit()
        print(f"✅ 已插入 {len(users)} 个用户")
        
        # 2. 插入用户档案
        print("📊 插入用户档案...")
        profiles = [
            {
                "user_id": 1,
                "learning_level": "中级",
                "preferred_topics": json.dumps(["编程", "数据科学"]),
                "daily_study_time": 60,
                "learning_style": "visual",
                "proficiency_score": 65.5
            },
            {
                "user_id": 2,
                "learning_level": "专家",
                "preferred_topics": json.dumps(["经济学", "金融"]),
                "daily_study_time": 120,
                "learning_style": "reading",
                "proficiency_score": 95.0
            }
        ]
        
        for profile_data in profiles:
            profile = UserProfile(**profile_data)
            db.add(profile)
        db.commit()
        
        # 3. 插入课程数据（对应你界面中的8个课程）
        print("🎓 插入课程数据...")
        courses = [
            {
                "title": "Python编程从入门到精通",
                "subtitle": "全面掌握Python编程技能，从基础到高级应用",
                "instructor_id": 2,  # 王静教授
                "category": "编程开发",
                "subcategory": "Python",
                "thumbnail_url": "/images/courses/python.jpg",
                "description": "本课程将带领你从零开始学习Python编程，涵盖基础语法、面向对象编程、Web开发、数据分析等多个方面。",
                "difficulty": "beginner",
                "rating": 4.99,
                "enrolled_count": 123000,
                "duration_hours": 40,
                "price": 0.00,
                "is_free": True,
                "is_featured": True,
                "status": "published",
                "ai_tags": json.dumps(["Python", "编程", "入门", "实战"]),
                "created_at": datetime.now() - timedelta(days=30)
            },
            {
                "title": "机器学习实战：核心算法与应用",
                "subtitle": "深入理解机器学习算法原理与实践应用",
                "instructor_id": 2,
                "category": "人工智能",
                "subcategory": "机器学习",
                "thumbnail_url": "/images/courses/ml.jpg",
                "description": "掌握机器学习核心算法，包括监督学习、无监督学习、深度学习等，并通过实际项目进行应用。",
                "difficulty": "intermediate",
                "rating": 4.59,
                "enrolled_count": 89000,
                "duration_hours": 50,
                "price": 299.00,
                "is_free": False,
                "is_featured": True,
                "status": "published",
                "ai_tags": json.dumps(["机器学习", "AI", "算法", "实战"]),
                "created_at": datetime.now() - timedelta(days=45)
            },
            {
                "title": "金融学基础：投资与理财",
                "subtitle": "王静教授讲授金融基础知识与投资理财技巧",
                "instructor_id": 2,
                "category": "商业管理",
                "subcategory": "金融",
                "thumbnail_url": "/images/courses/finance.jpg",
                "description": "系统学习金融学基础知识，掌握投资理财的核心概念和方法，实现财富增值。",
                "difficulty": "beginner",
                "rating": 4.79,
                "enrolled_count": 166000,
                "duration_hours": 35,
                "price": 199.00,
                "is_free": False,
                "is_featured": True,
                "status": "published",
                "ai_tags": json.dumps(["金融", "投资", "理财", "经济学"]),
                "created_at": datetime.now() - timedelta(days=60)
            },
            {
                "title": "医学基础知识精讲",
                "subtitle": "张伟教授系统讲解医学基础理论",
                "instructor_id": 4,  # 张伟教授
                "category": "职业技能",
                "subcategory": "医学",
                "thumbnail_url": "/images/courses/medical.jpg",
                "description": "全面系统讲解医学基础理论知识，为医学学习打下坚实基础。",
                "difficulty": "intermediate",
                "rating": 4.99,
                "enrolled_count": 213000,
                "duration_hours": 60,
                "price": 399.00,
                "is_free": False,
                "is_featured": True,
                "status": "published",
                "ai_tags": json.dumps(["医学", "健康", "基础", "精讲"]),
                "created_at": datetime.now() - timedelta(days=75)
            },
            {
                "title": "机械设计原理与应用",
                "subtitle": "郭明教授讲授机械设计核心原理",
                "instructor_id": 2,  # 假设郭明教授用户ID=2
                "category": "设计创新",
                "subcategory": "机械设计",
                "thumbnail_url": "/images/courses/mechanical.jpg",
                "description": "学习机械设计的基本原理和实际应用，培养工程实践能力。",
                "difficulty": "intermediate",
                "rating": 4.89,
                "enrolled_count": 95000,
                "duration_hours": 45,
                "price": 249.00,
                "is_free": False,
                "is_featured": True,
                "status": "published",
                "ai_tags": json.dumps(["机械", "设计", "工程", "原理"]),
                "created_at": datetime.now() - timedelta(days=90)
            },
            {
                "title": "现代建筑设计与理论",
                "subtitle": "刘芳教授讲授现代建筑设计理念",
                "instructor_id": 3,  # 刘芳教授
                "category": "设计创新",
                "subcategory": "建筑设计",
                "thumbnail_url": "/images/courses/architecture.jpg",
                "description": "探索现代建筑设计理念，学习建筑理论与实践的结合。",
                "difficulty": "intermediate",
                "rating": 4.79,
                "enrolled_count": 192000,
                "duration_hours": 40,
                "price": 299.00,
                "is_free": False,
                "is_featured": True,
                "status": "published",
                "ai_tags": json.dumps(["建筑", "设计", "现代", "理论"]),
                "created_at": datetime.now() - timedelta(days=100)
            },
            {
                "title": "数据分析与可视化实战",
                "subtitle": "李刚教授讲授数据分析核心技能",
                "instructor_id": 2,  # 假设李刚教授用户ID=2
                "category": "数据科学",
                "subcategory": "数据分析",
                "thumbnail_url": "/images/courses/data-analysis.jpg",
                "description": "掌握数据分析和可视化技能，从数据中提取有价值的信息。",
                "difficulty": "intermediate",
                "rating": 4.89,
                "enrolled_count": 187000,
                "duration_hours": 50,
                "price": 349.00,
                "is_free": False,
                "is_featured": True,
                "status": "published",
                "ai_tags": json.dumps(["数据分析", "可视化", "Python", "实战"]),
                "created_at": datetime.now() - timedelta(days=110)
            },
            {
                "title": "数字营销与品牌案例",
                "subtitle": "王静教授解析数字营销策略与品牌建设",
                "instructor_id": 2,
                "category": "市场营销",
                "subcategory": "数字营销",
                "thumbnail_url": "/images/courses/marketing.jpg",
                "description": "学习数字营销的最新策略和品牌建设方法，通过实际案例加深理解。",
                "difficulty": "beginner",
                "rating": 4.89,
                "enrolled_count": 134000,
                "duration_hours": 30,
                "price": 199.00,
                "is_free": False,
                "is_featured": True,
                "status": "published",
                "ai_tags": json.dumps(["营销", "品牌", "数字", "案例"]),
                "created_at": datetime.now() - timedelta(days=120)
            }
        ]
        
        for course_data in courses:
            course = Course(**course_data)
            db.add(course)
        db.commit()
        print(f"✅ 已插入 {len(courses)} 门课程")
        
        # 4. 插入课程章节（为每门课程添加3-5个章节）
        print("📚 插入课程章节...")
        modules = []
        module_counter = 1
        
        for course_id in range(1, 9):  # 8门课程
            for i in range(1, 5):  # 每门课程4个章节
                modules.append({
                    "course_id": course_id,
                    "module_order": i,
                    "title": f"第{i}章：课程{course_id}的第{i}个模块",
                    "description": f"这是课程{course_id}的第{i}个模块的详细描述",
                    "duration_minutes": 45 + i * 15,
                    "video_url": f"/videos/course_{course_id}_module_{i}.mp4",
                    "content_type": "video" if i % 2 == 0 else "text",
                    "ai_difficulty_score": 0.3 + i * 0.1
                })
                module_counter += 1
        
        for module_data in modules:
            module = CourseModule(**module_data)
            db.add(module)
        db.commit()
        print(f"✅ 已插入 {len(modules)} 个课程章节")
        
        # 5. 插入测验数据（每个章节一个测验）
        print("📝 插入测验数据...")
        quizzes = []
        
        for module_id in range(1, len(modules) + 1):
            quizzes.append({
                "module_id": module_id,
                "title": f"模块{module_id}的测验",
                "total_questions": 10,
                "passing_score": 6,
                "time_limit_minutes": 30,
                "ai_generated": True
            })
        
        for quiz_data in quizzes:
            quiz = Quiz(**quiz_data)
            db.add(quiz)
        db.commit()
        print(f"✅ 已插入 {len(quizzes)} 个测验")
        
        # 6. 插入题目数据（每个测验5个题目）
        print("❓ 插入题目数据...")
        questions = []
        
        for quiz_id in range(1, len(quizzes) + 1):
            for q_num in range(1, 6):
                questions.append({
                    "quiz_id": quiz_id,
                    "question_text": f"这是测验{quiz_id}的第{q_num}个问题？",
                    "question_type": "multiple_choice",
                    "options": json.dumps([
                        f"选项A - 测验{quiz_id}问题{q_num}",
                        f"选项B - 测验{quiz_id}问题{q_num}",
                        f"选项C - 测验{quiz_id}问题{q_num}",
                        f"选项D - 测验{quiz_id}问题{q_num}"
                    ]),
                    "correct_answer": f"选项A - 测验{quiz_id}问题{q_num}",
                    "ai_explanation": f"这是AI生成的问题{quiz_id}-{q_num}的详细解释",
                    "difficulty_level": (q_num % 3) + 1
                })
        
        for question_data in questions:
            question = Question(**question_data)
            db.add(question)
        db.commit()
        print(f"✅ 已插入 {len(questions)} 个题目")
        
        # 7. 插入课程统计数据
        print("📈 插入课程统计数据...")
        stats = []
        
        for course_id in range(1, 9):
            for day_offset in range(30, 0, -1):  # 最近30天的数据
                stats.append({
                    "course_id": course_id,
                    "date": datetime.now().date() - timedelta(days=day_offset),
                    "daily_views": 1000 + course_id * 100 + day_offset * 10,
                    "daily_enrollments": 50 + course_id * 5 + day_offset,
                    "avg_rating": 4.5 + (course_id * 0.05),
                    "completion_rate": 0.3 + (course_id * 0.02)
                })
        
        for stat_data in stats:
            stat = CourseStatistics(**stat_data)
            db.add(stat)
        db.commit()
        print(f"✅ 已插入 {len(stats)} 条课程统计数据")
        
        # 8. 插入用户行为日志
        print("📋 插入用户行为日志...")
        actions = ["view_course", "start_module", "complete_quiz", "pause_video", "rate_course"]
        logs = []
        
        for user_id in range(1, 3):  # 前2个用户
            for i in range(20):  # 每个用户20条日志
                logs.append({
                    "user_id": user_id,
                    "action_type": actions[i % len(actions)],
                    "target_id": (i % 8) + 1,  # 课程ID 1-8
                    "target_type": "course",
                    "action_data": json.dumps({
                        "timestamp": datetime.now().isoformat(),
                        "duration": i * 10,
                        "score": i * 5 if i % 2 == 0 else None
                    }),
                    "created_at": datetime.now() - timedelta(hours=i*2)
                })
        
        for log_data in logs:
            log = UserBehaviorLog(**log_data)
            db.add(log)
        db.commit()
        print(f"✅ 已插入 {len(logs)} 条用户行为日志")
        
        print("\n🎉 所有数据插入完成！")
        print("=" * 50)
        print("📊 数据统计:")
        print(f"   用户: {db.query(User).count()} 个")
        print(f"   课程: {db.query(Course).count()} 门")
        print(f"   章节: {db.query(CourseModule).count()} 个")
        print(f"   测验: {db.query(Quiz).count()} 个")
        print(f"   题目: {db.query(Question).count()} 个")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 插入数据时出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 开始数据库初始化...")
    insert_sample_data()
    print("✅ 数据库初始化完成！")