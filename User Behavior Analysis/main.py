# 核心依赖（包含所有必需模块）
import pymysql
import json
import base64
import numpy as np
import pandas as pd
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify, request

# ===================== 全局配置 =====================
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 解决JSON中文乱码

# Matplotlib跨系统中文配置（彻底解决字体警告）
plt.switch_backend('Agg')  # 非交互式后端，避免tkinter/GUI报错
matplotlib.rcParams.update({
    'font.family': 'sans-serif',  # 优先使用无衬线字体
    'font.sans-serif': [
        'SimHei',         # Windows系统默认黑体（优先）
        'Microsoft YaHei',# Windows雅黑
        'DejaVu Sans',    # Linux系统默认无衬线字体（兼容中文）
        'Arial Unicode MS',# Mac系统中文兼容字体
        'PingFang SC',    # Mac苹方
        'Heiti SC'        # Mac黑体
    ],
    'axes.unicode_minus': False,  # 解决负号显示为方块的问题
    'figure.figsize': (12, 10),   # 默认图表大小
    'figure.dpi': 100             # 默认分辨率
})

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "db": "bgarea"
}

# ===================== 数据库工具类（通用） =====================
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
                init_command='SET NAMES utf8mb4'  # 强制UTF8编码
            )
            self.cursor = self.conn.cursor()
        except pymysql.MySQLError as e:
            print(f"数据库连接失败：{e}")
            raise e

    def query(self, sql, params=None):
        """执行查询，返回字典列表"""
        try:
            self.cursor.execute(sql, params or ())
            return self.cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"查询失败：{e}")
            return []
    
    def execute(self, sql, params=None):
        """执行增/删/改操作，返回是否成功"""
        try:
            self.cursor.execute(sql, params or ())
            self.conn.commit()
            return True
        except pymysql.MySQLError as e:
            self.conn.rollback()
            print(f"执行失败：{e}")
            return False

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()

# ===================== 混合推荐核心类（完整保留原有逻辑） =====================
class HybridRecommender:
    def __init__(self, db_config):
        # 初始化数据库连接
        self.db = DBConnector(**db_config)
        # 加载基础数据
        self.user_list = self._load_all_users()
        self.user_domain = self._load_user_domain()
        self.course_dict = self._load_all_courses()
        self.course_domain = {cid: self.course_dict[cid]["domain"] for cid in self.course_dict}
        # 构建并填充评分矩阵
        self.rating_matrix = self._build_rating_matrix()
        self.rating_matrix_filled = self._fill_sparse_matrix()
        # SVD分解与相似度计算
        self.user_features, self.course_features = self._robust_svd_decomposition()
        self.course_similarity = self._compute_course_similarity()
        # 关闭初始连接
        self.db.close()

    def _load_all_users(self):
        """加载所有用户ID"""
        sql = "SELECT user_id FROM users"
        res = self.db.query(sql)
        return [item['user_id'] for item in res]

    def _load_user_domain(self):
        """加载用户-偏好领域映射"""
        sql = "SELECT user_id, favorite_domain FROM users"
        res = self.db.query(sql)
        return {item['user_id']: item['favorite_domain'] for item in res}

    def _load_all_courses(self):
        """加载课程信息（修复中文乱码）"""
        sql = "SELECT course_id, course_name, difficulty, domain FROM courses"
        res = self.db.query(sql)
        course_dict = {}
        for item in res:
            # 中文乱码修复
            course_name = item['course_name']
            if isinstance(course_name, bytes):
                course_name = course_name.decode('utf-8')
            domain = item['domain']
            if isinstance(domain, bytes):
                domain = domain.decode('utf-8')
            # 难度转数字
            difficulty = item['difficulty']
            if isinstance(difficulty, str):
                difficulty = int(difficulty)
            # 构建课程字典
            course_dict[item['course_id']] = {
                "name": course_name,
                "difficulty": difficulty,
                "domain": domain
            }
        return course_dict

    def _build_rating_matrix(self):
        """构建用户-课程评分矩阵（基于行为权重）"""
        # 查询行为数据
        sql = """
        SELECT user_id, course_id, behavior_type, COUNT(*) as behavior_count
        FROM user_behaviors
        GROUP BY user_id, course_id, behavior_type
        """
        behavior_data = self.db.query(sql)
        if not behavior_data:
            return pd.DataFrame(0.0, index=self.user_list, columns=list(self.course_dict.keys()))
        
        # 行为权重映射
        behavior_df = pd.DataFrame(behavior_data)
        behavior_weight = {"collect": 5, "video_finish": 4, "answer_submit": 3, "click": 1}
        behavior_df['weight'] = behavior_df['behavior_type'].map(behavior_weight).fillna(1)
        behavior_df['score'] = behavior_df['behavior_count'] * behavior_df['weight']
        user_course_total = behavior_df.groupby(['user_id', 'course_id'])['score'].sum().reset_index()
        
        # 初始化矩阵并填充
        course_ids = list(self.course_dict.keys())
        rating_matrix = pd.DataFrame(0.0, index=self.user_list, columns=course_ids)
        for _, row in user_course_total.iterrows():
            rating = min(row['score'], 5)  # 最大5分
            rating_matrix.loc[row['user_id'], row['course_id']] = max(rating, 1)  # 最小1分
        return rating_matrix

    def _fill_sparse_matrix(self):
        """填充稀疏矩阵（0值→用户/领域/全局均值）"""
        filled_matrix = self.rating_matrix.copy()
        global_mean = filled_matrix[filled_matrix > 0].mean().mean()
        
        for user_id in filled_matrix.index:
            user_ratings = filled_matrix.loc[user_id]
            user_mean = user_ratings[user_ratings > 0].mean() if user_ratings[user_ratings > 0].any() else np.nan
            
            for course_id in filled_matrix.columns:
                if filled_matrix.loc[user_id, course_id] == 0:
                    # 领域均值计算
                    course_domain = self.course_domain[course_id]
                    domain_courses = [cid for cid in self.course_domain if self.course_domain[cid] == course_domain]
                    domain_mean = filled_matrix.loc[user_id, domain_courses][filled_matrix.loc[user_id, domain_courses] > 0].mean()
                    # 填充值（优先级：用户均值→领域均值→全局均值）
                    fill_value = user_mean if not np.isnan(user_mean) else (domain_mean if not np.isnan(domain_mean) else global_mean)
                    filled_matrix.loc[user_id, course_id] = round(fill_value, 2)
        return filled_matrix

    def _robust_svd_decomposition(self):
        """鲁棒性SVD分解（低维度+正则化）"""
        matrix = self.rating_matrix_filled.fillna(0)
        svd = TruncatedSVD(
            n_components=1,
            random_state=42,
            n_iter=10
        )
        user_features = svd.fit_transform(matrix)
        course_features = svd.components_.T
        return user_features, course_features

    def _compute_course_similarity(self):
        """计算课程余弦相似度矩阵"""
        course_ratings = self.rating_matrix.T
        course_ratings = course_ratings[course_ratings.sum(axis=1) > 0]
        if course_ratings.empty:
            return pd.DataFrame(0, index=self.course_dict.keys(), columns=self.course_dict.keys())
        
        similarity = cosine_similarity(course_ratings)
        similarity_df = pd.DataFrame(
            similarity,
            index=course_ratings.index,
            columns=course_ratings.index
        )
        # 填充缺失课程
        all_courses = list(self.course_dict.keys())
        similarity_df = similarity_df.reindex(index=all_courses, columns=all_courses, fill_value=0)
        return similarity_df

    def _get_svd_rating(self, user_id, course_id):
        """计算SVD评分（加权相似度）"""
        if user_id not in self.rating_matrix.index or course_id not in self.rating_matrix.columns:
            return 0.0
        user_idx = self.rating_matrix.index.get_loc(user_id)
        course_idx = self.rating_matrix.columns.get_loc(course_id)
        
        svd_score = np.dot(self.user_features[user_idx], self.course_features[course_idx])
        learned_courses = self.rating_matrix.loc[user_id][self.rating_matrix.loc[user_id] > 0].index
        
        if learned_courses.empty:
            return float(svd_score)
        
        sim_sum = 0.0
        score_sum = 0.0
        for learned_cid in learned_courses:
            sim = self.course_similarity.loc[course_id, learned_cid]
            sim_sum += sim
            score_sum += sim * self.rating_matrix.loc[user_id, learned_cid]
        weighted_score = score_sum / sim_sum if sim_sum > 0 else svd_score
        return float(weighted_score)

    def _get_content_based_rating(self, user_id, course_id):
        """基于内容的评分（领域+难度）"""
        # 领域匹配分
        user_domain = self.user_domain.get(user_id, "")
        course_domain = self.course_domain.get(course_id, "")
        domain_score = 2 if user_domain == course_domain else 0
        
        # 难度匹配分
        learned_courses = self.rating_matrix.loc[user_id][self.rating_matrix.loc[user_id] > 0].index
        if learned_courses.empty:
            learned_avg_diff = 2.0
        else:
            learned_avg_diff = np.mean([self.course_dict[cid]["difficulty"] for cid in learned_courses])
        course_diff = float(self.course_dict[course_id]["difficulty"])
        diff_distance = abs(course_diff - learned_avg_diff)
        diff_score = max(3 - diff_distance, 0)
        
        return float(domain_score + diff_score)

    def recommend(self, user_id, top_n=None):
        """核心推荐逻辑"""
        if user_id not in self.rating_matrix.index or user_id not in self.user_domain:
            return []
        
        candidate_courses = list(self.course_domain.keys())
        if not candidate_courses:
            return []
        
        # 计算混合评分
        hybrid_ratings = {}
        for course_id in candidate_courses:
            svd_rating = self._get_svd_rating(user_id, course_id)
            content_rating = self._get_content_based_rating(user_id, course_id)
            hybrid_ratings[course_id] = round(svd_rating * 0.7 + content_rating * 0.3, 2)
        
        # 排序并限制数量
        sorted_courses = sorted(hybrid_ratings.items(), key=lambda x: x[1], reverse=True)
        if top_n is not None and isinstance(top_n, int):
            sorted_courses = sorted_courses[:top_n]
        
        # 构建结果
        result = []
        for course_id, rating in sorted_courses:
            is_viewed = bool(self.rating_matrix.loc[user_id, course_id] > 0)
            result.append({
                "course_id": course_id,
                "course_name": self.course_dict[course_id]["name"],
                "difficulty": int(self.course_dict[course_id]["difficulty"]),
                "predicted_rating": float(rating),
                "domain": self.course_dict[course_id]["domain"],
                "is_viewed": is_viewed
            })
        return result

# ===================== 自适应提示类（完整保留原有逻辑） =====================
class SimpleAdaptiveHint:
    def __init__(self, db_config):
        self.db = DBConnector(**db_config)
        self.course_knowledge_map = self._load_course_knowledge()
        self.db.close()

    def _load_course_knowledge(self):
        """加载课程-知识点映射"""
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
        """计算课程掌握度（知识点平均）"""
        knowledges = self.course_knowledge_map.get(course_id, [])
        if not knowledges:
            print(f"课程{course_id}无关联知识点")
            return None
        
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
            print(f"用户{user_id}对课程{course_id}无掌握度数据")
            return None
        
        scores = [item["mastery_score"] for item in mastery_res]
        return round(sum(scores) / len(scores), 2)

    def get_adaptive_hint(self, user_id, course_id, threshold=0.6):
        """获取自适应提示"""
        # 校验课程存在性
        db = DBConnector(**DB_CONFIG)
        course_check_sql = "SELECT 1 FROM courses WHERE course_id = %s"
        course_exist = db.query(course_check_sql, (course_id,))
        db.close()
        
        if not course_exist:
            return {"course_id": course_id, "course_mastery": None, "hint": "课程不存在"}
        
        # 计算掌握度并生成提示
        course_mastery = self.get_course_mastery(user_id, course_id)
        hint = ""
        if course_mastery is not None and course_mastery < threshold:
            hint = "如果您觉得本课程学习起来有点困难的话，可以尝试选择难度低一点的入门课程"
        
        return {
            "course_id": course_id,
            "course_mastery": course_mastery,
            "hint": hint
        }

# ===================== 教学优化引擎类（视频行为可视化） =====================
class TeachingOptimizationEngine:
    def __init__(self, db_config):
        self.db_config = db_config
        # 支持的视频行为类型
        self.video_behavior_types = [
            "video_play",    # 播放
            "video_pause",   # 暂停
            "video_forward", # 快进
            "video_slow",    # 慢放
            "video_finish"   # 完成
        ]

    def get_video_behavior_stats(self, course_id, chapter_id):
        """获取视频行为统计数据"""
        db = DBConnector(**self.db_config)
        # 构建查询SQL
        sql = f"""
        SELECT user_id, behavior_type, behavior_detail, behavior_time 
        FROM user_behaviors 
        WHERE course_id = %s 
          AND chapter_id = %s 
          AND behavior_type IN ({', '.join(['%s']*len(self.video_behavior_types))})
        """
        params = [course_id, chapter_id] + self.video_behavior_types
        behaviors = db.query(sql, params)
        db.close()

        if not behaviors:
            return {"behavior_type_count": {}, "timeline_data": [], "user_count": 0}

        # 解析行为数据
        behavior_records = []
        for item in behaviors:
            try:
                detail = json.loads(item["behavior_detail"])
            except json.JSONDecodeError:
                detail = {}
            behavior_records.append({
                "user_id": item["user_id"],
                "type": item["behavior_type"],
                "time": item["behavior_time"],
                "detail": detail
            })

        # 统计行为类型占比
        behavior_df = pd.DataFrame(behavior_records)
        type_count = behavior_df["type"].value_counts().to_dict()

        # 时间轴分布（30秒桶）
        time_buckets = {}
        for record in behavior_records:
            b_type = record["type"]
            detail = record["detail"]
            
            # 提取关键时间点
            if b_type == "video_pause":
                time_point = detail.get("pause_second", 0)
            elif b_type in ["video_forward", "video_slow"]:
                time_point = detail.get("start_second", 0)
            elif b_type == "video_play":
                time_point = detail.get("start_second", 0)
            elif b_type == "video_finish":
                time_point = detail.get("total_duration", 0)
            else:
                time_point = 0

            # 按30秒分组
            bucket = int(time_point // 30) * 30
            if bucket not in time_buckets:
                time_buckets[bucket] = {t: 0 for t in self.video_behavior_types}
            time_buckets[bucket][b_type] += 1

        # 格式化时间轴数据
        timeline_data = []
        for bucket in sorted(time_buckets.keys()):
            timeline_data.append({
                "time_bucket": f"{bucket}-{bucket+30}秒",
                "counts": time_buckets[bucket]
            })

        # 统计参与用户数
        user_count = len(behavior_df["user_id"].unique())

        return {
            "behavior_type_count": type_count,
            "timeline_data": timeline_data,
            "user_count": user_count
        }

    def generate_visualization(self, course_id, chapter_id):
        """生成视频行为可视化图表（Base64编码）"""
        stats = self.get_video_behavior_stats(course_id, chapter_id)
        if not stats["behavior_type_count"]:
            return ""

        # 创建图表
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle(f"课程{course_id} - 章节{chapter_id} 视频行为分析", fontsize=16)

        # 子图1：行为类型占比饼图
        types = list(stats["behavior_type_count"].keys())
        counts = list(stats["behavior_type_count"].values())
        ax1.pie(counts, labels=types, autopct='%1.1f%%', startangle=90)
        ax1.set_title(f"行为类型分布（参与用户数：{stats['user_count']}）")

        # 子图2：时间轴堆叠柱状图
        buckets = [item["time_bucket"] for item in stats["timeline_data"]]
        pause_counts = [item["counts"]["video_pause"] for item in stats["timeline_data"]]
        forward_counts = [item["counts"]["video_forward"] for item in stats["timeline_data"]]
        slow_counts = [item["counts"]["video_slow"] for item in stats["timeline_data"]]

        x = np.arange(len(buckets))
        width = 0.6
        ax2.bar(x, pause_counts, width, label="暂停", color="#FF6B6B")
        ax2.bar(x, forward_counts, width, bottom=pause_counts, label="快进", color="#4ECDC4")
        ax2.bar(x, slow_counts, width, bottom=np.array(pause_counts)+np.array(forward_counts), label="慢放", color="#45B7D1")

        ax2.set_xlabel("视频时间区间")
        ax2.set_ylabel("行为次数")
        ax2.set_title("各时间区间视频行为分布")
        ax2.set_xticks(x)
        ax2.set_xticklabels(buckets, rotation=45)
        ax2.legend()

        # 调整布局并转为Base64
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # 清理资源
        buffer.close()
        plt.close(fig)

        return img_base64

# ===================== Flask API接口（所有接口独立） =====================
# 初始化所有引擎实例
hybrid_recommender = HybridRecommender(DB_CONFIG)
adaptive_hint = SimpleAdaptiveHint(DB_CONFIG)
teaching_engine = TeachingOptimizationEngine(DB_CONFIG)

# 接口1：课程推荐接口
@app.route("/api/recommend", methods=["GET"])
def get_recommendation():
    user_id = request.args.get("user_id")
    top_n = request.args.get("top_n")

    if not user_id:
        return jsonify({"code": 400, "msg": "缺少必传参数user_id", "data": []}), 400
    
    # 处理top_n参数
    try:
        top_n = int(top_n) if top_n is not None else None
    except ValueError:
        return jsonify({"code": 400, "msg": "top_n必须为整数", "data": []}), 400
    
    # 获取推荐结果
    result = hybrid_recommender.recommend(user_id, top_n)
    return jsonify({
        "code": 200,
        "msg": "推荐成功",
        "data": result
    })

# 接口2：自适应提示接口
@app.route("/api/adaptive-hint", methods=["GET"])
def adaptive_hint_api():
    try:
        user_id = request.args.get("user_id")
        course_id = request.args.get("course_id")
        threshold = request.args.get("threshold", 0.6)

        # 参数校验
        if not user_id or not course_id:
            return jsonify({"code": 400, "msg": "缺少必填参数：user_id 或 course_id", "data": {}})
        
        threshold = float(threshold)
        if not (0 <= threshold <= 1):
            return jsonify({"code": 400, "msg": "threshold必须在0-1之间", "data": {}})

        # 获取提示结果
        result = adaptive_hint.get_adaptive_hint(user_id, course_id, threshold)
        return jsonify({"code": 200, "msg": "获取提示成功", "data": result})

    except ValueError:
        return jsonify({"code": 400, "msg": "threshold必须为数字", "data": {}})
    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务器错误：{str(e)}", "data": {}})

# 接口3：视频行为统计接口
@app.route("/api/teaching-optim/video-stats", methods=["GET"])
def get_video_stats():
    try:
        course_id = request.args.get("course_id")
        chapter_id = request.args.get("chapter_id")

        if not course_id or not chapter_id:
            return jsonify({
                "code": 400,
                "msg": "缺少必填参数：course_id 或 chapter_id",
                "data": {}
            })

        stats = teaching_engine.get_video_behavior_stats(course_id, chapter_id)
        return jsonify({
            "code": 200,
            "msg": "获取统计数据成功",
            "data": stats
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"服务器错误：{str(e)}",
            "data": {}
        })

# 接口4：视频行为可视化接口
@app.route("/api/teaching-optim/video-visual", methods=["GET"])
def get_video_visual():
    try:
        course_id = request.args.get("course_id")
        chapter_id = request.args.get("chapter_id")

        if not course_id or not chapter_id:
            return jsonify({
                "code": 400,
                "msg": "缺少必填参数：course_id 或 chapter_id",
                "data": {"img_base64": ""}
            })

        img_base64 = teaching_engine.generate_visualization(course_id, chapter_id)
        return jsonify({
            "code": 200,
            "msg": "生成可视化图表成功",
            "data": {"img_base64": img_base64}
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"服务器错误：{str(e)}",
            "data": {"img_base64": ""}
        })

# ===================== 运行入口 =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
