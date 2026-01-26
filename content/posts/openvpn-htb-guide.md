**Kali Linux 作为渗透测试专用系统，默认软件源里就包含 OpenVPN，我们直接通过命令行安装即可。**

## 一、安装openvpn

1、打开 Kali 终端，先更新软件包索引，确保能获取到最新的安装包

```bash
sudo apt-get update
```

2、执行安装命令，等待程序自动完成安装：

```bash
sudo apt-get install openvpn
```

![在这里插入图片描述](/images/image-20260126210915286.png)

安装过程中如果出现确认提示，输入 y 并回车即可。

## 二、获取 OpenVPN 配置文件

1、点击viewconnection
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/fa47b06edac44d679874dfdd5ed2925b.png)
2、我一般选择tcp443,点击download
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/4e0450ec2166453d886da4e5db5d70fe.png)

## 三、连接OPENVPN

1、输入openvpn --config + vpn文件路径
如：

```bash
openvpn --config starting_points_eu-starting-point-1-dhcp\(1\).ovpn 
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a2d1bc487c3f49558ee89164508b70f3.png)
2、输入ip addr show tun0 验证连接是否生效

```bash
ip addr show tun0
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3e7ac5e5470044fab27a2562d0d4e599.png)
