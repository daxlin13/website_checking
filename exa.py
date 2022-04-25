import requests
from bs4 import BeautifulSoup
import os
from urllib import parse
import validators

#下载图片的方法
def downloadImage(href,cnt):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/63.0.3239.132 Safari/537.36'}
    try:
        #获取图片
        dimg = requests.get(href, headers=headers).content
        #url解析，对url按照一定格式进行拆分,回一个包含6个字符串项目的元组：协议，位置，路径(path)，参数，查询，判断
        urlArr=parse.urlparse(href)
        #返回path最后的文件名
        filename=os.path.basename(urlArr.path)
        #在指定路径创建图片
        with open("E:\\python\\downfiles\\"+filename, 'wb') as f:
            f.write(dimg)
            f.close()
            print("图片"+str(cnt)+"已下载")
    except Exception as e:
        print('url:'+href+',图片无法下载')

#需要抓取图片的网址
url='https://zhuanlan.zhihu.com/p/266269353'
# 服务器反爬虫机制会判断客户端请求头中的User-Agent是否来源于真实浏览器，所以，我们使用Requests经常会指定UA伪装成浏览器发起请求
headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/63.0.3239.132 Safari/537.36'}
#请求详细页面
r = requests.get(url, headers=headers)
#改编码
r.encoding = "utf-8"
soup = BeautifulSoup(r.text, "html.parser")
 #查找出所有img标签的src属性
imagesurl = set([img['src'] for img in soup.find_all('img') if hasattr(img, 'src')])
cnt = 1
#遍历图片地址，调用下载图片的方法
for tag in imagesurl:
    fullurl=tag
    #判断是否有效的url,防止图片地址的相对路径
    if not validators.url(tag):
        #加上主域名，拼接成绝对路径
        fullurl = parse.urljoin(url, tag)
    #下载图片
    downloadImage(fullurl,cnt)
    cnt+=1