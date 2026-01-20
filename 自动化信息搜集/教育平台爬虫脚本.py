import requests
from lxml import etree
import time

from requests import post

# 获取源代码
start_time = time.time()
url = 'https://src.sjtu.edu.cn/list/?page='
for i in range(0, 3): #左闭右开
    url_end = url + str(i)
    print(url_end)
    result = requests.get(url_end).content.decode('utf-8')
    print(result)
# 创建一个result.txt

# 定位元素
soup = etree.HTML(result)
# content_data = soup.xpath('//*[contains(@href,'/post/226')]/text()')
content_data = soup.xpath("//*[contains(@href,'/post/2')]/text()")
print(content_data)
# soup = etree.HTML(result)
# end_time = time.time()
with open('../content_data.txt', 'w') as f:
    f.write(str(content_data))
