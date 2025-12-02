import pandas as pd
import pymysql
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
import joblib

# -------------------------- 1. 自定义 Precision@k/Recall@k 函数（无改动） --------------------------
def precision_recall_at_k(predictions, k=5, threshold=3.5):
    user_ratings = {}
    for uid, iid, true_r, est, _ in predictions:
        if uid not in user_ratings:
            user_ratings[uid] = []
        user_ratings[uid].append((est, true_r))
    
    precision_list = []
    recall_list = []
    
    for uid, ratings in user_ratings.items():
        ratings.sort(key=lambda x: x[0], reverse=True)
        true_positives = sum(1 for (_, true_r) in ratings if true_r >= threshold)
        if true_positives == 0:
            continue
        
        recommended_positives = sum(1 for (_, true_r) in ratings[:k] if true_r >= threshold)
        precision = recommended_positives / min(k, len(ratings))
        recall = recommended_positives / true_positives
        
        precision_list.append(precision)
        recall_list.append(recall)
    
    avg_precision = sum(precision_list) / len(precision_list) if precision_list else 0.0
    avg_recall = sum(recall_list) / len(recall_list) if recall_list else 0.0
    
    return avg_precision, avg_recall

# -------------------------- 2. 从MySQL加载用户-课程评分数据（无改动） --------------------------
def load_rating_data(db_config):
    connection = pymysql.connect(**db_config)
    sql = """
        SELECT user_id, course_id, rating
        FROM (
            SELECT 
                user_id, 
                course_id,
                CASE 
                    WHEN behavior_type = 'collect' THEN 5
                    WHEN behavior_type = 'search' THEN 4
                    WHEN behavior_type = 'click' THEN 3
                    WHEN behavior_type = 'view' AND duration > 30 THEN 2
                    ELSE 0
                END AS rating
            FROM user_behavior
        ) AS sub_query
        WHERE sub_query.rating > 0;
    """
    try:
        rating_df = pd.read_sql(sql, connection)
    finally:
        connection.close()
    
    return rating_df

# -------------------------- 3. 训练SVD模型（无改动） --------------------------
def train_svd_model(rating_df, model_save_path="svd_recommend_model.pkl"):
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(rating_df[["user_id", "course_id", "rating"]], reader)
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
    
    model = SVD(
        n_factors=100,
        n_epochs=20,
        lr_all=0.005,
        reg_all=0.02
    )
    model.fit(trainset)
    print("📌 模型训练完成！")
    
    predictions = model.test(testset)
    precision, recall = precision_recall_at_k(predictions, k=5, threshold=3.5)
    print(f"📊 模型评估结果：")
    print(f"   - Precision@5: {precision:.3f}")
    print(f"   - Recall@5:    {recall:.3f}")
    
    joblib.dump(model, model_save_path)
    print(f"✅ 模型已保存到：{model_save_path}")
    
    return model

# -------------------------- 4. 修复：生成老用户推荐列表（核心改游标模式） --------------------------
def get_recommend_for_old_user(user_id, model, db_config, top_k=10):
    connection = pymysql.connect(**db_config)
    # 核心修复：创建字典游标（cursorclass=pymysql.cursors.DictCursor）
    cursor = connection.cursor(cursorclass=pymysql.cursors.DictCursor)
    
    # 步骤1：获取用户已互动的课程（此时row是字典，支持row["course_id"]）
    cursor.execute(f"SELECT DISTINCT course_id FROM user_behavior WHERE user_id='{user_id}'")
    interacted_courses = [row["course_id"] for row in cursor.fetchall()]  # 这里也需要字典索引
    
    # 步骤2：获取所有候选课程（排除已互动）
    cursor.execute("SELECT course_id FROM course")
    all_courses = [row["course_id"] for row in cursor.fetchall()]  # 字典索引
    candidate_courses = [cid for cid in all_courses if cid not in interacted_courses]
    
    # 步骤3：预测候选课程评分（无改动）
    course_predictions = []
    for cid in candidate_courses:
        pred = model.predict(user_id, cid)
        course_predictions.append({"course_id": cid, "pred_rating": pred.est})
    
    # 步骤4：补充课程详情（无改动，此时row是字典）
    top_courses = sorted(course_predictions, key=lambda x: x["pred_rating"], reverse=True)[:top_k]
    if not top_courses:
        cursor.close()
        connection.close()
        return []
    
    course_ids = ",".join(map(str, [course["course_id"] for course in top_courses]))
    cursor.execute(f"""
        SELECT course_id, course_name, difficulty, tags, teacher_style, avg_score
        FROM course
        WHERE course_id IN ({course_ids})
    """)
    # 此时row是字典，可通过row["course_id"]索引
    course_details = {row["course_id"]: row for row in cursor.fetchall()}
    
    # 步骤5：整理推荐结果（无改动）
    recommend_list = []
    for course in top_courses:
        cid = course["course_id"]
        recommend_list.append({
            "course_id": cid,
            "course_name": course_details[cid]["course_name"],
            "difficulty": course_details[cid]["difficulty"],
            "tags": course_details[cid]["tags"],
            "teacher_style": course_details[cid]["teacher_style"],
            "avg_score": float(course_details[cid]["avg_score"]),  # Decimal转float
            "pred_rating": round(course["pred_rating"], 2),
            "reason": "根据你的学习行为推荐"
        })
    
    # 关闭资源（游标+连接）
    cursor.close()
    connection.close()
    return recommend_list

# -------------------------- 5. 测试入口（无改动） --------------------------
if __name__ == "__main__":
    DB_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "bgarea",
        "charset": "utf8mb4"
    }
    
    print("="*50)
    print("1. 从数据库加载用户行为评分数据...")
    rating_df = load_rating_data(DB_CONFIG)
    print(f"   ✅ 成功加载 {len(rating_df)} 条有效评分数据")
    
    print("\n2. 开始训练SVD推荐模型...")
    model = train_svd_model(rating_df)
    
    # # 后续运行可注释训练，直接加载模型
    # print("\n2. 加载已训练的推荐模型...")
    # model = joblib.load("svd_recommend_model.pkl")
    # print("   ✅ 模型加载成功")
    
    print("\n3. 测试老用户推荐...")
    test_user_id = "U2023001"  # 模拟数据中的考研用户
    recommend_list = get_recommend_for_old_user(test_user_id, model, DB_CONFIG, top_k=5)
    
    # 打印推荐结果（无改动）
    print(f"\n🎯 为用户 {test_user_id} 推荐的Top5课程：")
    for idx, course in enumerate(recommend_list, 1):
        print(f"{idx}. {course['course_name']}")
        print(f"   - 难度：{course['difficulty']} | 评分：{course['avg_score']} | 预测评分：{course['pred_rating']}")
        print(f"   - 标签：{course['tags']} | 风格：{course['teacher_style']}\n")
    
    print("="*50)
    print("🎉 所有流程执行完毕！")