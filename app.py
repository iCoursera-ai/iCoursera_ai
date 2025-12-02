from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域问题
import pymysql
from pymysql import Error
import joblib
from datetime import datetime

# -------------------------- 1. 初始化Flask应用 --------------------------
app = Flask(__name__)
CORS(app)  # 允许所有跨域请求（开发环境用，生产环境可限制域名）

# -------------------------- 2. 配置数据库和模型 --------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "edu_recommend",
    "charset": "utf8mb4"
}
# 加载训练好的推荐模型
MODEL = joblib.load("svd_recommend_model.pkl")

# -------------------------- 3. 工具函数：数据库查询/插入 --------------------------
def execute_sql(sql, params=None, is_select=True):
    """执行SQL语句，支持查询（is_select=True）和插入/更新（is_select=False）"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)  # 返回字典格式
        cursor.execute(sql, params) if params else cursor.execute(sql)
        
        if is_select:
            result = cursor.fetchall()  # 查询：返回所有结果
        else:
            connection.commit()  # 插入/更新：提交事务
            result = cursor.rowcount  # 返回影响行数
        
        connection.close()
        return {"success": True, "data": result}
    except Error as e:
        connection.rollback() if not is_select else None
        connection.close() if 'connection' in locals() else None
        return {"success": False, "error": str(e)}

# -------------------------- 4. 接口1：获取推荐列表 --------------------------
@app.route("/api/recommend/getList", methods=["GET"])
def get_recommend_list():
    """
    获取推荐列表：
    参数：user_id（必填）
    逻辑：判断用户是否有行为数据 → 老用户用协同过滤，新用户用冷启动
    """
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"code": 400, "msg": "用户ID不能为空"})
    
    # 步骤1：判断用户是否有行为数据（是否老用户）
    behavior_sql = f"SELECT COUNT(*) AS count FROM user_behavior WHERE user_id='{user_id}'"
    behavior_result = execute_sql(behavior_sql)
    if not behavior_result["success"]:
        return jsonify({"code": 500, "msg": f"查询行为数据失败：{behavior_result['error']}"})
    
    is_old_user = behavior_result["data"][0]["count"] > 0  # 有行为→老用户
    
    # 步骤2：获取用户画像（新/老用户都需要）
    profile_sql = f"SELECT * FROM user_profile WHERE user_id='{user_id}'"
    profile_result = execute_sql(profile_sql)
    if not profile_result["success"]:
        return jsonify({"code": 500, "msg": f"查询用户画像失败：{profile_result['error']}"})
    if not profile_result["data"]:
        return jsonify({"code": 404, "msg": "用户画像不存在，请先完善画像"})
    user_profile = profile_result["data"][0]
    
    # 步骤3：生成推荐列表
    if is_old_user:
        # 老用户：调用协同过滤模型
        from recommend_model import get_recommend_for_old_user  # 导入之前的推荐函数
        recommend_list = get_recommend_for_old_user(user_id, MODEL, DB_CONFIG)
    else:
        # 新用户：冷启动推荐
        from recommend_model import get_recommend_for_new_user
        recommend_list = get_recommend_for_new_user(user_profile, DB_CONFIG)
    
    # 步骤4：返回推荐结果（添加推荐理由）
    for course in recommend_list:
        if is_old_user:
            course["reason"] = "根据你的学习行为推荐"
        else:
            course["reason"] = f"根据你的需求「{user_profile['learning_goal']}」推荐"
    
    return jsonify({
        "code": 200,
        "msg": "获取推荐成功",
        "data": {
            "is_old_user": is_old_user,
            "recommend_list": recommend_list
        }
    })

# -------------------------- 5. 接口2：上报用户行为 --------------------------
@app.route("/api/behavior/report", methods=["POST"])
def report_behavior():
    """
    上报用户行为：
    请求体（JSON）：user_id, course_id, behavior_type, search_keyword（可选）, duration（可选）
    """
    data = request.get_json()
    required_fields = ["user_id", "behavior_type"]
    # 检查必填字段
    for field in required_fields:
        if field not in data:
            return jsonify({"code": 400, "msg": f"{field}不能为空"})
    
    # 补充默认值
    course_id = data.get("course_id")
    search_keyword = data.get("search_keyword", "")
    duration = data.get("duration", 0)
    behavior_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 当前时间
    
    # 构造插入SQL
    insert_sql = """
        INSERT INTO user_behavior 
        (user_id, course_id, behavior_type, behavior_time, search_keyword, duration)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (data["user_id"], course_id, data["behavior_type"], behavior_time, search_keyword, duration)
    insert_result = execute_sql(insert_sql, params, is_select=False)
    
    if insert_result["success"]:
        return jsonify({"code": 200, "msg": "行为上报成功", "data": {"affected_rows": insert_result["data"]}})
    else:
        return jsonify({"code": 500, "msg": f"行为上报失败：{insert_result['error']}"})

# -------------------------- 6. 接口3：更新用户画像 --------------------------
@app.route("/api/user/profile/update", methods=["POST"])
def update_user_profile():
    """
    更新用户画像：
    请求体（JSON）：user_id, learning_goal（可选）, base_level（可选）, prefer_style（可选）
    """
    data = request.get_json()
    if "user_id" not in data:
        return jsonify({"code": 400, "msg": "用户ID不能为空"})
    
    # 构造更新字段（只更新传入的字段）
    update_fields = []
    params = []
    if "learning_goal" in data:
        update_fields.append("learning_goal = %s")
        params.append(data["learning_goal"])
    if "base_level" in data:
        update_fields.append("base_level = %s")
        params.append(data["base_level"])
    if "prefer_style" in data:
        update_fields.append("prefer_style = %s")
        params.append(data["prefer_style"])
    
    if not update_fields:
        return jsonify({"code": 400, "msg": "至少需要更新一个字段"})
    
    # 构造更新SQL
    update_sql = f"""
        UPDATE user_profile 
        SET {",".join(update_fields)}, update_time = NOW()
        WHERE user_id = %s
    """
    params.append(data["user_id"])  # 最后一个参数是user_id
    
    update_result = execute_sql(update_sql, params, is_select=False)
    if update_result["success"]:
        if update_result["data"] == 0:
            return jsonify({"code": 404, "msg": "用户画像不存在，无法更新"})
        return jsonify({"code": 200, "msg": "画像更新成功", "data": {"affected_rows": update_result["data"]}})
    else:
        return jsonify({"code": 500, "msg": f"画像更新失败：{update_result['error']}"})

# -------------------------- 7. 启动服务 --------------------------
if __name__ == "__main__":
    # 开发环境：debug=True，端口5000
    app.run(host="0.0.0.0", port=5000, debug=True)