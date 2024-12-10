# 可以对1.txt中的ip进行ping操作
import os
import subprocess


# 读取 IP 地址列表
def read_ips(filename):
    with open(filename, 'r') as file:
        ips = [line.strip() for line in file.readlines()]
    return ips


# 执行 ping 命令
def ping_ip(ip):
    # 在 Windows 上使用 "ping -n 1"；Linux/Mac 上使用 "ping -c 1"
    command = ['ping', '-n', '1', ip]  # Windows 系统
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    ip_file = '1.txt'

    # 读取 IP 地址
    if not os.path.exists(ip_file):
        print(f"{ip_file} 文件不存在！")
        return

    ips = read_ips(ip_file)

    # 对每个 IP 地址执行 ping 操作
    for ip in ips:
        print(f"正在 ping {ip} ...")
        if ping_ip(ip):
            print(f"{ip} 可达")
        else:
            print(f"{ip} 不可达")


if __name__ == "__main__":
    main()
