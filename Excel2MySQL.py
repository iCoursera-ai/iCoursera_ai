import pandas as pd
import pymysql
from pymysql import Error

# -------------------------- 1. 配置数据库连接（已验证正确，无需改） --------------------------
DB_CONFIG = {
    "host": "localhost",    
    "user": "root",         
    "password": "root",     
    "database": "bgarea",   
    "charset": "utf8mb4"
}

# -------------------------- 2. 读取Excel数据（无错误，保留） --------------------------
def read_excel_data(excel_path):
    try:
        course_df = pd.read_excel(excel_path, sheet_name="course")
        profile_df = pd.read_excel(excel_path, sheet_name="user_profile")
        behavior_df = pd.read_excel(excel_path, sheet_name="user_behavior")
        
        empty_sheets = []
        if course_df.empty:
            empty_sheets.append("course")
        if profile_df.empty:
            empty_sheets.append("user_profile")
        if behavior_df.empty:
            empty_sheets.append("user_behavior")
        if empty_sheets:
            print(f"⚠️  以下Sheet数据为空：{', '.join(empty_sheets)}，请检查Excel内容！")
        
        return course_df, profile_df, behavior_df
    
    except FileNotFoundError:
        print(f"❌ 致命错误：未找到Excel文件！路径：{excel_path}")
        exit()
    
    except ValueError as e:
        if "No sheet named" in str(e):
            missing_sheet = str(e).split("'")[1]
            print(f"❌ 致命错误：Excel中缺少Sheet：{missing_sheet}")
        else:
            print(f"❌ 读取Excel失败：{str(e)}")
        exit()

# -------------------------- 3. 辅助函数：检查表是否存在（无错误，保留） --------------------------
def check_table_exists(table_name, connection):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT COUNT(*) FROM information_schema.tables "
        f"WHERE table_schema = '{DB_CONFIG['database']}' AND table_name = '{table_name}'"
    )
    exists = cursor.fetchone()[0] == 1
    cursor.close()  # 这里直接close，无需判断
    return exists

# -------------------------- 4. 数据导入MySQL（核心修正：finally块的关闭逻辑） --------------------------
def insert_data_to_mysql(df, table_name, db_config):
    connection = None  
    cursor = None      
    try:
        # 1. 建立连接
        connection = pymysql.connect(**db_config)
        if not connection.open:
            raise Error("数据库连接已建立，但未处于打开状态")
        
        print(f"✅ 成功连接数据库（{db_config['database']}），开始处理 {table_name} 表...")
        
        # 2. 检查表是否存在
        if not check_table_exists(table_name, connection):
            print(f"❌ 插入失败：{table_name} 表不存在！")
            return
        
        # 3. 匹配列名
        cursor = connection.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        mysql_columns = [col[0] for col in cursor.fetchall()]
        valid_columns = [col for col in df.columns if col in mysql_columns]
        if not valid_columns:
            print(f"❌ 插入失败：Excel列名与 {table_name} 表不匹配！")
            return
        
        # 4. 生成SQL并插入
        columns = ",".join(valid_columns)
        values_placeholder = ",".join(["%s"] * len(valid_columns))
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})"
        
        data = []
        for _, row in df.iterrows():
            row_data = tuple(row[col] if pd.notna(row[col]) else None for col in valid_columns)
            data.append(row_data)
        
        if not data:
            print(f"⚠️  {table_name} 无有效数据可插入，跳过...")
            return
        
        cursor.executemany(insert_sql, data)
        connection.commit()
        print(f"✅ {table_name} 插入成功！共插入 {len(data)} 条数据\n")

    except Error as e:
        print(f"❌ {table_name} 处理失败：{str(e)}")
        if connection and connection.open:
            connection.rollback()
            print(f"   已回滚 {table_name} 的插入操作\n")

    # -------------------------- 核心修正：删除 cursor.closed 判断 --------------------------
    finally:
        # 1. 关闭游标：直接调用close()，无需判断是否关闭
        if cursor:  # 仅当cursor被创建时才关闭
            cursor.close()
            print(f"🔌 已关闭 {table_name} 的游标")
        
        # 2. 关闭连接：用 connection.open 判断是否打开（connection有open属性，Cursor没有）
        if connection and connection.open:
            connection.close()
            print(f"🔌 已关闭 {table_name} 的数据库连接\n")

# -------------------------- 5. 执行导入（注意：先处理course表主键冲突！） --------------------------
if __name__ == "__main__":
    excel_path = r"D:\user_behavior\data.xlsx"
    
    print("="*50)
    print(f"开始读取Excel文件：{excel_path}")
    course_df, profile_df, behavior_df = read_excel_data(excel_path)
    
    print("="*50)
    # 注意：之前已插入1条course数据，再次运行会报“主键冲突”（course_id自增）
    # 解决方案：先删除bgarea.course表的现有数据，再运行
    insert_data_to_mysql(course_df, "course", DB_CONFIG)       
    insert_data_to_mysql(profile_df, "user_profile", DB_CONFIG)
    insert_data_to_mysql(behavior_df, "user_behavior", DB_CONFIG)
    
    print("="*50)
    print("所有表处理完毕！")