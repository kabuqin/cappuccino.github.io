import subprocess

def scan_ports(ip):
    open_ports = []
    try:
        # 调用masscan命令进行端口扫描
        result = subprocess.run(["masscan", ip, "-p1-65535", "--rate=1000"], capture_output=True, text=True)
        output = result.stdout

        # 解析masscan输出，提取开放的端口
        lines = output.strip().split("\n")
        for line in lines:
            if "open" in line:
                port = line.split()[3].split("/")[0]
                open_ports.append(int(port))
    except subprocess.CalledProcessError as e:
        print("扫描发生错误：", e)
    return open_ports

# 从文件中读取IP地址
with open("../ip.txt", "r") as file:
    ip_addresses = file.readlines()

# 去除每个IP地址末尾的换行符
ip_addresses = [ip.strip() for ip in ip_addresses]

# 对每个IP地址进行端口扫描
for ip_address in ip_addresses:
    print("正在对IP地址", ip_address, "进行端口扫描...")
    open_ports = scan_ports(ip_address)
    if open_ports:
        print("IP地址", ip_address, "的开放端口：", open_ports)
    else:
        print("IP地址", ip_address, "没有开放的端口")