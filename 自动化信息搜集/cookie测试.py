import requests
import time
from lxml import etree
start_time = time.time()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36','Cookie':'security=impossible; PHPSESSID=vh17kas59vufr1gm5ck1l5biqo'}
url1 = 'http://dvwa/vulnerabilities/csp/'
print(url1)
# url = 'https://chaziyu.com/ncpu.edu.cn/'
result = requests.get(url1, headers=headers).content.decode('utf-8')
print(result)

#
# soup = etree.HTML(result)
# #爬取功能列
# data = soup.xpath("//*[@class='menu-text']/text()")
# # print(ipdata)
# # data1=('\n'.join(data))
# # print(data1)
# url = soup.xpath("//a/@href")
# print=(url)
# ipdata = ('\n'.join(ipdata))
# with open('quanf.txt', 'w') as f:
#     f.write(ipdata)

