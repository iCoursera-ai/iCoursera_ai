# api/courses.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Course, CourseModule

# 🔧 关键：创建路由对象
router = APIRouter(prefix="/api", tags=["courses"])

@router.get("/courses")
def get_courses(
    category: Optional[str] = Query(None, description="课程分类"),
    difficulty: Optional[str] = Query(None, description="难度级别"),
    limit: int = Query(10, description="返回数量"),
    page: int = Query(1, description="页码"),
    db: Session = Depends(get_db)
):
    """获取课程列表"""
    query = db.query(Course).filter(Course.status == "published")
    
    if category:
        query = query.filter(Course.category == category)
    if difficulty:
        query = query.filter(Course.difficulty == difficulty)
    
    offset = (page - 1) * limit
    total = query.count()
    courses = query.order_by(Course.rating.desc()).offset(offset).limit(limit).all()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
        "data": [
            {
                "id": course.course_id,
                "title": course.title,
                "subtitle": course.subtitle,
                "category": course.category,
                "difficulty": course.difficulty,
                "rating": course.rating,
                "enrolled_count": course.enrolled_count,
                "duration_hours": course.duration_hours,
                "price": course.price,
                "is_free": course.is_free,
                "is_featured": course.is_featured,
                "thumbnail_url": course.thumbnail_url,
                "instructor_id": course.instructor_id
            }
            for course in courses
        ]
    }

@router.get("/courses/hot")
def get_hot_courses(
    limit: int = Query(8, description="热门课程数量"),
    db: Session = Depends(get_db)
):
    """获取热门课程"""
    courses = db.query(Course).filter(
        Course.status == "published",
        Course.is_featured == True
    ).order_by(
        Course.rating.desc(),
        Course.enrolled_count.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": course.course_id,
            "title": course.title,
            "subtitle": course.subtitle,
            "rating": course.rating,
            "enrolled_count": course.enrolled_count,
            "difficulty": course.difficulty,
            "duration_hours": course.duration_hours,
            "price": course.price,
            "is_free": course.is_free,
            "thumbnail_url": course.thumbnail_url
        }
        for course in courses
    ]

@router.get("/courses/{course_id}")
def get_course_detail(course_id: int, db: Session = Depends(get_db)):
    """获取课程详情"""
    course = db.query(Course).filter(Course.course_id == course_id).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    modules = db.query(CourseModule).filter(
        CourseModule.course_id == course_id
    ).order_by(CourseModule.module_order).all()
    
    return {
        "id": course.course_id,
        "title": course.title,
        "subtitle": course.subtitle,
        "description": course.description,
        "category": course.category,
        "difficulty": course.difficulty,
        "rating": course.rating,
        "enrolled_count": course.enrolled_count,
        "duration_hours": course.duration_hours,
        "price": course.price,
        "is_free": course.is_free,
        "thumbnail_url": course.thumbnail_url,
        "created_at": course.created_at,
        "ai_tags": course.ai_tags,
        "modules": [
            {
                "id": module.module_id,
                "title": module.title,
                "order": module.module_order,
                "duration_minutes": module.duration_minutes,
                "content_type": module.content_type
            }
            for module in modules
        ]
    }

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """获取所有课程分类"""
    categories = db.query(Course.category).distinct().all()
    return {"categories": [cat[0] for cat in categories if cat[0]]}