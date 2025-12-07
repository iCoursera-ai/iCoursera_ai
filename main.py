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

# ===================== 优化后的混合推荐核心类（返回所有课程 + 降序排序） =====================
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
        behavior_weight = {"collect":5, "video_finish":4, "answer_submit":3, "click":1}
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
                    # 填充值（保留0值的话注释这行？不，填充是为了SVD有效，评分最终会保留原始逻辑）
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

    # ---------------------- 核心推荐逻辑（返回所有课程 + 按评分降序） ----------------------
    def recommend(self, user_id, top_n=None):
        """
        核心修改点：
        1. 候选课程改为【所有课程】（不再限制用户偏好领域）
        2. 保留所有predicted_rating（包括0值）
        3. 严格按predicted_rating降序排序所有课程
        4. top_n=None时返回全部课程，否则返回前top_n条
        """
        # 基础校验
        if user_id not in self.rating_matrix.index or user_id not in self.user_domain:
            return []
        
        # 候选课程：系统内所有课程（关键修改！）
        candidate_courses = list(self.course_domain.keys())
        if not candidate_courses:
            return []

        # 计算所有课程的混合评分（SVD×0.7 + 内容×0.3），保留0值
        hybrid_ratings = {}
        for course_id in candidate_courses:
            svd_rating = self._get_svd_rating(user_id, course_id)
            content_rating = self._get_content_based_rating(user_id, course_id)
            hybrid_rating = svd_rating * 0.7 + content_rating * 0.3
            hybrid_ratings[course_id] = round(hybrid_rating, 2)  # 保留2位小数

        # 按predicted_rating严格降序排序所有课程
        sorted_courses = sorted(
            hybrid_ratings.items(), 
            key=lambda x: x[1], 
            reverse=True  # 降序
        )

        # 控制返回条数：top_n=None返回全部，否则返回前top_n条
        if top_n is not None and isinstance(top_n, int):
            sorted_courses = sorted_courses[:top_n]

        # 构建最终结果（修复序列化问题）
        result = []
        for course_id, rating in sorted_courses:
            # 转原生bool，避免序列化错误
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

# ===================== Flask接口 =====================
# 全局初始化推荐器
hybrid_recommender = HybridRecommender(DB_CONFIG)

@app.route("/api/recommend", methods=["GET"])
def get_recommendation():
    # 获取参数：user_id必传，top_n可选（不传返回全部课程）
    user_id = request.args.get("user_id")
    top_n = request.args.get("top_n")

    # 参数校验
    if not user_id:
        return jsonify({"code": 400, "msg": "缺少必传参数user_id", "data": []}), 400
    
    # 处理top_n：不传则返回全部，传则转为整数
    if top_n is None:
        top_n = None
    else:
        try:
            top_n = int(top_n)
        except ValueError:
            return jsonify({"code": 400, "msg": "top_n必须为整数", "data": []}), 400

    # 获取推荐结果（所有课程按评分降序）
    result = hybrid_recommender.recommend(user_id, top_n)

    # 返回响应
    return jsonify({
        "code": 200,
        "msg": "推荐成功",
        "data": result
    })

# ===================== 运行入口 =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)