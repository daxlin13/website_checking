# coding=utf-8
import os 
import re
import time
import requests
import datetime
import smtplib
from bs4 import BeautifulSoup
from urllib import parse


def send_email(ask_word=False):
    HOST = 'smtp.163.com'  # 网易邮箱smtp
    PORT = '465'
    sender = 'daxlin13@163.com'  # 发送人邮箱
    receiver = '906603565@qq.com'  # 收件人邮箱
    sender_pw = 'WAVYBXXCVQDDKVLT'
    if ask_word is True:
        unused_pattern, new_title, back_word, src = content_list(True)  # 提取网页内容列表
    else: 
        unused_pattern, new_title = content_list()

    title = new_title  # 邮件标题
    # context = new_pattern[0]  # 邮件内容
    # print('context', context)
    smtp = smtplib.SMTP_SSL(HOST, 465)  # 启用SSL发信, 端口一般是465
    res = smtp.login(user=sender, password=sender_pw)  # 登录验证，password是邮箱授权码而非密码，需要去网易邮箱手动开启
    print('发送结果：', res)
    msg = '\n'.join(
        ['From: {}'.format(sender), 'To: {}'.format(receiver), 'Subject: {}'.format(title), '', new_title])
    # smtp.sendmail(from_addr=sender, to_addrs=receiver, msg=msg.encode('utf-8'))  # 发送邮件
    # print(msg)


def content_list(re_back=False):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 \
                    (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}     # 设置headers信息，模拟成浏览器取访问网站
    web_raw = requests.get('http://wuli.snnu.edu.cn/xshd.htm', headers=headers)   # 向网站发起请求，并获取响应对象
    web_raw.encoding = 'utf-8'
    web_content = web_raw.text  # 获取网站源码
    soup = BeautifulSoup(web_content, features="html.parser")
    art_list = soup.find('div', class_='list-right')
    url_list = art_list.find('li')
    # print('url list is ', url_list)
    latest_title = url_list.find('a').text[1::]

    if re_back is True:
        latest_href = url_list.find('a')['href']
        latest_url = 'http://wuli.snnu.edu.cn/xshd.htm'.replace('xshd.htm', latest_href)
        # print(latest_url, type(latest_url))

        web_raw2 = requests.get(latest_url, headers=headers)
        web_raw2.encoding = 'utf-8'
        web_content2 = web_raw2.text  # 获取网站源码
        soup2 = BeautifulSoup(web_content2, features="html.parser")
        art_list2 = soup2.find('div', class_='v_news_content')
        imagesurl = set([img['src'] for img in art_list2.find_all('img') if hasattr(img, 'src')])
        for image in imagesurl:
            image_url = parse.urljoin(latest_url, image)
            dimg = requests.get(image_url, headers=headers).content
            # urlArr=parse.urlparse(image_url)
            # imagename=os.path.basename(urlArr.path)
            # with open(imagename, 'wb') as ima:
            #     ima.write(dimg)
            #     ima.close()

            print(type(dimg))
    
    if re_back is True:
        return art_list, latest_title, latest_url, src
    else:
        return art_list, latest_title

def update():
    print('通知系统启动中')
    old_list, old_title = content_list()  # 记录原始内容列表
    while True:
        new_list, new_title = content_list()  # 记录新内容列表
        if new_list != old_list:  # 判断内容列表是否更新
            old_list = new_list    # 原始内容列表改变
            if re.match('基金委理论物理', new_title):
                send_email(True)   # 发送邮件
            else:
                send_email()
        else:
            now = datetime.datetime.now()
            print(now, "尚无更新")
        time.sleep(3600)  # 一小时检测一次


if __name__ == "__main__":
    # sender = os.environ["SENDER"]
    # receiver = os.environ["RECERVER"]
    # sender_pw = os.environ["PASSWORD"]
    m = '基金委理论物理平台AMO系列活动：宏观介质中的超快动力学研究'
    # send_email(m)
    # update()
    content_list(True)
