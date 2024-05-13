import socket

def check_port(ip, port):
    try:
        # 创建 socket 对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置超时时间为2秒
        s.settimeout(2)
        # 尝试连接到目标 IP 地址和端口
        result = s.connect_ex((ip, port))
        if result == 0:
            print(f"端口 {port} 开启")
        else:
            print(f"端口 {port} 未开启")
        # 关闭 socket 连接
        s.close()
    except Exception as e:
        print(f"发生异常：{e}")

if __name__ == "__main__":
    target_ip = input("请输入目标 IP 地址: ")
    target_port = int(input("请输入要检查的端口号: "))
    check_port(target_ip, target_port)
