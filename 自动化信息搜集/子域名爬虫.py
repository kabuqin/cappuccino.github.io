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
print(result)


soup = etree.HTML(result)
ipdata = soup.xpath("//*[contains(@href,'https://ipchaxun.com')]/text()")
ipdata = ('\n'.join(ipdata))
with open('../ip.txt', 'w') as f:
    f.write(ipdata)

