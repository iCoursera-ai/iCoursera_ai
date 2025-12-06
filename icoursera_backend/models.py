# models.py
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    avatar_url = Column(String(255))
    bio = Column(Text)
    role = Column(Enum('student', 'instructor', 'admin'), default='student')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime)
    ai_preferences = Column(JSON)

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)
    learning_level = Column(String(50))
    preferred_topics = Column(JSON)
    daily_study_time = Column(Integer, default=30)
    learning_style = Column(Enum('visual', 'auditory', 'reading', 'kinesthetic'))
    proficiency_score = Column(Float, default=0)

class Course(Base):
    __tablename__ = "courses"
    
    course_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(500))
    instructor_id = Column(Integer, ForeignKey("users.user_id"))
    category = Column(String(100))
    subcategory = Column(String(100))
    thumbnail_url = Column(String(255))
    description = Column(Text)
    difficulty = Column(Enum('beginner', 'intermediate', 'advanced'))
    rating = Column(Float, default=0)
    enrolled_count = Column(Integer, default=0)
    duration_hours = Column(Integer)
    price = Column(Float, default=0)
    is_free = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    status = Column(Enum('draft', 'published', 'archived'), default='draft')
    ai_tags = Column(JSON)
    created_at = Column(DateTime, default=func.now())

class CourseModule(Base):
    __tablename__ = "course_modules"
    
    module_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    module_order = Column(Integer)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer)
    video_url = Column(String(255))
    content_type = Column(Enum('video', 'text', 'quiz', 'assignment'))
    ai_difficulty_score = Column(Float)

class Quiz(Base):
    __tablename__ = "quizzes"
    
    quiz_id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("course_modules.module_id"))
    title = Column(String(200))
    total_questions = Column(Integer)
    passing_score = Column(Integer)
    time_limit_minutes = Column(Integer)
    ai_generated = Column(Boolean, default=False)

class Question(Base):
    __tablename__ = "questions"
    
    question_id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.quiz_id"))
    question_text = Column(Text, nullable=False)
    question_type = Column(Enum('multiple_choice', 'true_false', 'short_answer', 'code'))
    options = Column(JSON)
    correct_answer = Column(Text)
    ai_explanation = Column(Text)
    difficulty_level = Column(Integer)

class CourseStatistics(Base):
    __tablename__ = "course_statistics"
    
    stat_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    date = Column(DateTime)
    daily_views = Column(Integer, default=0)
    daily_enrollments = Column(Integer, default=0)
    avg_rating = Column(Float)
    completion_rate = Column(Float)

class UserBehaviorLog(Base):
    __tablename__ = "user_behavior_logs"
    
    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    action_type = Column(String(50))
    target_id = Column(Integer)
    target_type = Column(String(50))
    action_data = Column(JSON)
    created_at = Column(DateTime, default=func.now())