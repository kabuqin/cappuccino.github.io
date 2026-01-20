import socket

def scan_ports(ip):
    open_ports = []
    for port in range(1, 65536):  # 扫描端口范围从1到65535
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # 设置超时时间为1秒
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
        except socket.error as e:
            print("连接发生异常：", e)
        finally:
            sock.close()
    return open_ports

# 从文件中读取IP地址
with open("../ip.txt", "r") as file:
    ip_addresses = file.readlines()

# 去除每个IP地址末尾的换行符
ip_addresses = [ip.strip() for ip in ip_addresses]

# 对每个IP地址进行全端口扫描
for ip_address in ip_addresses:
    print("正在对IP地址", ip_address, "进行全端口扫描...")
    open_ports = scan_ports(ip_address)
    if open_ports:
        print("IP地址", ip_address, "的开放端口：", open_ports)
    else:
        print("IP地址", ip_address, "没有开放的端口")