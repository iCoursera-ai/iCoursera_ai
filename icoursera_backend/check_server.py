# check_server.py
import socket
import requests

def check_server():
    print("🔍 检查服务器状态...")
    
    # 1. 检查端口是否被占用
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8000))
    
    if result == 0:
        print("✅ 端口 8000 正在被占用（可能有服务运行）")
    else:
        print("❌ 端口 8000 没有被占用")
    
    sock.close()
    
    # 2. 尝试连接
    try:
        response = requests.get('http://localhost:8000/', timeout=2)
        print(f"✅ 服务器响应: {response.status_code}")
        print(f"   响应内容: {response.text[:100]}...")
    except requests.ConnectionError:
        print("❌ 无法连接到服务器")
    except Exception as e:
        print(f"❌ 连接错误: {e}")
    
    # 3. 检查可能的错误
    print("\n📋 常见问题:")
    print("1. 防火墙阻止了8000端口")
    print("2. 服务启动失败但没显示错误")
    print("3. 使用了不同的IP或端口")

check_server()