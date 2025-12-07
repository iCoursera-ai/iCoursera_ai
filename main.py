# 核心依赖（保留必需）
import pymysql
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify, request

# ===================== 全局配置 =====================
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 解决中文乱码

# 数据库配置（替换为你的信息）
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "db": "bgarea"
}

# ===================== 数据库工具类 =====================
class DBConnector:
    def __init__(self, host, user, password, db):
        try:
            self.conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=db,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                init_command='SET NAMES utf8mb4'  # 强制编码
            )
            self.cursor = self.conn.cursor()
        except pymysql.MySQLError as e:
            print(f"数据库连接失败：{e}")
            raise e

    def query(self, sql, params=None):
        try:
            self.cursor.execute(sql, params or ())
            return self.cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"查询失败：{e}")
            return []

    def close(self):
        if self.conn:
            self.conn.close()

# ===================== 优化后的混合推荐核心类（保留原有完整逻辑） =====================
class HybridRecommender:
    def __init__(self, db_config):
        # 初始化数据库
        self.db = DBConnector(**db_config)
        # 加载基础数据
        self.user_list = self._load_all_users()
        self.user_domain = self._load_user_domain()  # 用户-领域映射
        self.course_dict = self._load_all_courses()  # 课程基础信息（修复中文乱码）
        self.course_domain = {cid: self.course_dict[cid]["domain"] for cid in self.course_dict}  # 课程-领域
        # 构建评分矩阵（预处理稀疏值）
        self.rating_matrix = self._build_rating_matrix()
        self.rating_matrix_filled = self._fill_sparse_matrix()  # 填充后的矩阵
        # 执行鲁棒性SVD分解
        self.user_features, self.course_features = self._robust_svd_decomposition()
        # 计算课程相似度矩阵
        self.course_similarity = self._compute_course_similarity()
        # 关闭数据库
        self.db.close()

    # ---------------------- 基础数据加载（修复中文乱码） ----------------------
    def _load_all_users(self):
        sql = "SELECT user_id FROM users"
        res = self.db.query(sql)
        return [item['user_id'] for item in res]

    def _load_user_domain(self):
        sql = "SELECT user_id, favorite_domain FROM users"
        res = self.db.query(sql)
        return {item['user_id']: item['favorite_domain'] for item in res}

    def _load_all_courses(self):
        """加载课程数据，强制转UTF-8修复中文乱码"""
        sql = "SELECT course_id, course_name, difficulty, domain FROM courses"
        res = self.db.query(sql)
        course_dict = {}
        for item in res:
            # 核心：修复中文乱码（bytes转str）
            course_name = item['course_name']
            if isinstance(course_name, bytes):
                course_name = course_name.decode('utf-8')
            # 课程难度转数字（避免字符串）
            difficulty = item['difficulty']
            if isinstance(difficulty, str):
                difficulty = int(difficulty)
            # 确保domain是原生字符串
            domain = item['domain']
            if isinstance(domain, bytes):
                domain = domain.decode('utf-8')
            course_dict[item['course_id']] = {
                "name": course_name,
                "difficulty": difficulty,
                "domain": domain
            }
        return course_dict

    # ---------------------- 稀疏矩阵预处理 ----------------------
    def _build_rating_matrix(self):
        """构建原始评分矩阵（1-5分）"""
        # 查询行为数据
        sql = """
        SELECT user_id, course_id, behavior_type, COUNT(*) as behavior_count
        FROM user_behaviors
        GROUP BY user_id, course_id, behavior_type
        """
        behavior_data = self.db.query(sql)
        if not behavior_data:
            return pd.DataFrame(0.0, index=self.user_list, columns=list(self.course_dict.keys()))
        # 计算行为评分（权重：收藏5>视频完成4>答题3>点击1）
        behavior_df = pd.DataFrame(behavior_data)
        behavior_weight = {"collect": 5, "video_finish": 4, "answer_submit": 3, "click": 1}
        behavior_df['weight'] = behavior_df['behavior_type'].map(behavior_weight).fillna(1)
        behavior_df['score'] = behavior_df['behavior_count'] * behavior_df['weight']
        user_course_total = behavior_df.groupby(['user_id', 'course_id'])['score'].sum().reset_index()
        # 构建矩阵
        course_ids = list(self.course_dict.keys())
        rating_matrix = pd.DataFrame(0.0, index=self.user_list, columns=course_ids)
        # 填充评分（限制1-5分）
        for _, row in user_course_total.iterrows():
            rating = min(row['score'], 5)  # 最大5分
            rating_matrix.loc[row['user_id'], row['course_id']] = max(rating, 1)  # 最小1分
        return rating_matrix

    def _fill_sparse_matrix(self):
        """填充稀疏矩阵：0值→用户均值（若无则领域均值，再无则全局均值）"""
        filled_matrix = self.rating_matrix.copy()
        # 计算全局均值
        global_mean = filled_matrix[filled_matrix > 0].mean().mean()
        # 按用户填充
        for user_id in filled_matrix.index:
            user_ratings = filled_matrix.loc[user_id]
            user_mean = user_ratings[user_ratings > 0].mean() if user_ratings[user_ratings > 0].any() else np.nan
            # 按课程填充
            for course_id in filled_matrix.columns:
                if filled_matrix.loc[user_id, course_id] == 0:
                    # 优先级：用户均值 → 课程领域均值 → 全局均值
                    course_domain = self.course_domain[course_id]
                    domain_courses = [cid for cid in self.course_domain if self.course_domain[cid] == course_domain]
                    domain_mean = filled_matrix.loc[user_id, domain_courses][filled_matrix.loc[user_id, domain_courses] > 0].mean()
                    # 填充值
                    fill_value = user_mean if not np.isnan(user_mean) else (domain_mean if not np.isnan(domain_mean) else global_mean)
                    filled_matrix.loc[user_id, course_id] = round(fill_value, 2)
        return filled_matrix

    # ---------------------- SVD分解优化 ----------------------
    def _robust_svd_decomposition(self):
        """鲁棒性SVD：低维度+正则化+限制迭代"""
        # 填充后的矩阵
        matrix = self.rating_matrix_filled.fillna(0)
        # 低维度（适配小数据）+ 正则化
        svd = TruncatedSVD(
            n_components=1,  # 维度从2→1，降低过拟合
            random_state=42,
            n_iter=10  # 限制迭代次数，提升稳定性
        )
        user_features = svd.fit_transform(matrix)
        course_features = svd.components_.T
        return user_features, course_features

    # ---------------------- 相似度计算 ----------------------
    def _compute_course_similarity(self):
        """计算课程余弦相似度矩阵（基于评分）"""
        # 只保留有行为的课程
        course_ratings = self.rating_matrix.T  # 课程×用户
        course_ratings = course_ratings[course_ratings.sum(axis=1) > 0]
        if course_ratings.empty:
            return pd.DataFrame(0, index=self.course_dict.keys(), columns=self.course_dict.keys())
        # 计算余弦相似度
        similarity = cosine_similarity(course_ratings)
        similarity_df = pd.DataFrame(
            similarity,
            index=course_ratings.index,
            columns=course_ratings.index
        )
        # 填充缺失课程（相似度0）
        all_courses = list(self.course_dict.keys())
        similarity_df = similarity_df.reindex(index=all_courses, columns=all_courses, fill_value=0)
        return similarity_df

    # ---------------------- 混合评分计算（不过滤0值） ----------------------
    def _get_svd_rating(self, user_id, course_id):
        """计算SVD评分（加权相似度），不过滤0值"""
        if user_id not in self.rating_matrix.index or course_id not in self.rating_matrix.columns:
            return 0.0  # 保留0值，不过滤
        # 用户/课程索引
        user_idx = self.rating_matrix.index.get_loc(user_id)
        course_idx = self.rating_matrix.columns.get_loc(course_id)
        # 基础SVD评分
        svd_score = np.dot(self.user_features[user_idx], self.course_features[course_idx])
        # 相似度加权（和用户已学课程的相似度）
        learned_courses = self.rating_matrix.loc[user_id][self.rating_matrix.loc[user_id] > 0].index
        if learned_courses.empty:
            return float(svd_score)  # 转原生float
        # 计算课程相似度加权
        sim_sum = 0.0
        score_sum = 0.0
        for learned_cid in learned_courses:
            sim = self.course_similarity.loc[course_id, learned_cid]
            sim_sum += sim
            score_sum += sim * self.rating_matrix.loc[user_id, learned_cid]
        weighted_score = score_sum / sim_sum if sim_sum > 0 else svd_score
        return float(weighted_score)  # 转原生float

    def _get_content_based_rating(self, user_id, course_id):
        """基于内容的评分（领域+难度），不过滤0值"""
        # 1. 领域匹配分（0-2分）
        user_domain = self.user_domain.get(user_id, "")
        course_domain = self.course_domain.get(course_id, "")
        domain_score = 2 if user_domain == course_domain else 0
        # 2. 难度匹配分（0-3分）
        learned_courses = self.rating_matrix.loc[user_id][self.rating_matrix.loc[user_id] > 0].index
        if learned_courses.empty:
            learned_avg_diff = 2.0  # 转原生float
        else:
            learned_avg_diff = np.mean([self.course_dict[cid]["difficulty"] for cid in learned_courses])
            learned_avg_diff = float(learned_avg_diff)  # 转原生float
        course_diff = float(self.course_dict[course_id]["difficulty"])  # 转原生float
        diff_distance = abs(course_diff - learned_avg_diff)
        diff_score = max(3 - diff_distance, 0)  # 距离越近分越高
        # 总分（保留0值，转原生float）
        total_score = float(domain_score + diff_score)
        return total_score

    # ---------------------- 核心推荐逻辑（保留原有完整功能） ----------------------
    def recommend(self, user_id, top_n=None):
        """
        核心逻辑：返回所有课程+按评分降序，保留原有功能
        """
        # 基础校验
        if user_id not in self.rating_matrix.index or user_id not in self.user_domain:
            return []
        
        # 候选课程：系统内所有课程
        candidate_courses = list(self.course_domain.keys())
        if not candidate_courses:
            return []
        
        # 计算所有课程的混合评分（SVD×0.7 + 内容×0.3）
        hybrid_ratings = {}
        for course_id in candidate_courses:
            svd_rating = self._get_svd_rating(user_id, course_id)
            content_rating = self._get_content_based_rating(user_id, course_id)
            hybrid_rating = svd_rating * 0.7 + content_rating * 0.3
            hybrid_ratings[course_id] = round(hybrid_rating, 2)
        
        # 按评分降序排序
        sorted_courses = sorted(
            hybrid_ratings.items(),
            key=lambda x: x[1],
            reverse=True
        )
        # 控制返回条数
        if top_n is not None and isinstance(top_n, int):
            sorted_courses = sorted_courses[:top_n]
        
        # 构建结果
        result = []
        for course_id, rating in sorted_courses:
            is_viewed_np = self.rating_matrix.loc[user_id, course_id] > 0
            is_viewed = bool(is_viewed_np)
            
            result.append({
                "course_id": course_id,
                "course_name": self.course_dict[course_id]["name"],
                "difficulty": int(self.course_dict[course_id]["difficulty"]),
                "predicted_rating": float(rating),
                "domain": self.course_dict[course_id]["domain"],
                "is_viewed": is_viewed
            })
        return result

# ===================== 独立自适应提示类（复用你提供的逻辑） =====================
class SimpleAdaptiveHint:
    def __init__(self, db_config):
        self.db = DBConnector(**db_config)
        self.course_knowledge_map = self._load_course_knowledge()  # 课程-知识点映射
        self.db.close()  # 初始化后关闭连接，避免资源占用

    def _load_course_knowledge(self):
        """加载课程与知识点的关联关系"""
        sql = "SELECT course_id, knowledge_id FROM course_knowledge"
        res = self.db.query(sql)
        course_knowledge = {}
        for item in res:
            cid = item["course_id"]
            kid = item["knowledge_id"]
            if cid not in course_knowledge:
                course_knowledge[cid] = []
            course_knowledge[cid].append(kid)
        return course_knowledge

    def get_course_mastery(self, user_id, course_id):
        """计算用户对指定课程的掌握度（知识点平均掌握度）"""
        # 1. 获取课程关联的知识点
        knowledges = self.course_knowledge_map.get(course_id, [])
        if not knowledges:
            print(f"课程{course_id}无关联知识点")
            return None

        # 2. 重新连接数据库查询掌握度（按需连接）
        db = DBConnector(**DB_CONFIG)
        placeholders = ', '.join(['%s'] * len(knowledges))
        mastery_sql = f"""
        SELECT knowledge_id, mastery_score 
        FROM user_knowledge_mastery 
        WHERE user_id = %s AND knowledge_id IN ({placeholders})
        """
        mastery_res = db.query(mastery_sql, [user_id] + knowledges)
        db.close()

        if not mastery_res:
            print(f"用户{user_id}对课程{course_id}无知识点掌握度数据")
            return None

        # 3. 计算平均掌握度
        scores = [item["mastery_score"] for item in mastery_res]
        avg_mastery = sum(scores) / len(scores)
        return round(avg_mastery, 2)

    def get_adaptive_hint(self, user_id, course_id, threshold=0.6):
        """获取自适应提示文字"""
        # 1. 校验课程是否存在
        db = DBConnector(**DB_CONFIG)
        course_check_sql = "SELECT 1 FROM courses WHERE course_id = %s"
        course_exist = db.query(course_check_sql, (course_id,))
        db.close()
        if not course_exist:
            return {"course_id": course_id, "course_mastery": None, "hint": "课程不存在"}

        # 2. 计算课程掌握度
        course_mastery = self.get_course_mastery(user_id, course_id)

        # 3. 判断是否触发提示
        hint = ""
        if course_mastery is not None and course_mastery < threshold:
            hint = "如果您觉得本课程学习起来有点困难的话，可以尝试选择难度低一点的入门课程"

        return {
            "course_id": course_id,
            "course_mastery": course_mastery,
            "hint": hint
        }

# ===================== Flask API接口（独立接口，无冲突） =====================
# 初始化推荐器和自适应提示实例（独立无耦合）
hybrid_recommender = HybridRecommender(DB_CONFIG)
adaptive_hint = SimpleAdaptiveHint(DB_CONFIG)

# 接口1：原有推荐接口（保留完整功能）
@app.route("/api/recommend", methods=["GET"])
def get_recommendation():
    user_id = request.args.get("user_id")
    top_n = request.args.get("top_n")
    # 参数校验
    if not user_id:
        return jsonify({"code": 400, "msg": "缺少必传参数user_id", "data": []}), 400
    
    # 处理top_n
    if top_n is None:
        top_n = None
    else:
        try:
            top_n = int(top_n)
        except ValueError:
            return jsonify({"code": 400, "msg": "top_n必须为整数", "data": []}), 400
    
    # 获取推荐结果
    result = hybrid_recommender.recommend(user_id, top_n)
    return jsonify({
        "code": 200,
        "msg": "推荐成功",
        "data": result
    })

# 接口2：独立自适应提示接口（复用你的逻辑）
@app.route("/api/adaptive-hint", methods=["GET"])
def adaptive_hint_api():
    try:
        # 获取参数
        user_id = request.args.get("user_id")
        course_id = request.args.get("course_id")
        threshold = request.args.get("threshold", 0.6)

        # 参数校验
        if not user_id or not course_id:
            return jsonify({"code": 400, "msg": "缺少必填参数：user_id 或 course_id", "data": {}})
        try:
            threshold = float(threshold)
            if not (0 <= threshold <= 1):
                return jsonify({"code": 400, "msg": "threshold必须在0-1之间", "data": {}})
        except ValueError:
            return jsonify({"code": 400, "msg": "threshold必须为数字", "data": {}})

        # 获取自适应提示
        result = adaptive_hint.get_adaptive_hint(user_id, course_id, threshold)
        return jsonify({"code": 200, "msg": "获取提示成功", "data": result})

    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务器错误：{str(e)}", "data": {}})

# ===================== 运行入口 =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
