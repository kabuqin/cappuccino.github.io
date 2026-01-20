import requests
import time
from lxml import etree
start_time = time.time()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
url1 = 'https://chaziyu.com/'
print(url1)
domain = input('输入域名')
print(url1 + domain)
url = url1 + domain
# url = 'https://chaziyu.com/ncpu.edu.cn/'
result = requests.get(url, headers=headers).content.decode('utf-8')
# print(result)

soup = etree.HTML(result)
# //*[contains(@href,'https://icplishi.com')]/text()
ipdata = soup.xpath("//*[contains(text(),'沪ICP')]/text()")

# //*[contains(text(),'沪ICP')]
# ipdata = soup.xpath("//*[contains(@href,'https://ipchaxun.com')]/text()")
ipdata = ('\n'.join(ipdata))
with open('../beian.txt', 'w') as f:
    f.write(ipdata)

# python爬虫笔记：https://www.bilibili.com/h5/note-app/view?cvid=18557521&pagefrom=comment