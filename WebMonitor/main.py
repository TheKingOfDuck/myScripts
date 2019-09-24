# -*- coding: utf-8 -*-

__author__ = 'CoolCat'

import requests
import time
import sys
import hashlib
import nltk
import requests
import time
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
import asyncio
from pyppeteer import launch
import configparser



class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

sys.stdout = Logger(str(time.strftime('%Y%m%d--%H-%M-%S')) + ".log")


async def screenshot(url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setViewport({'width': 640, 'height': 480})
    await page.goto(url)
    imageName = url.replace("https://", "").replace("http://", "").replace("/", "") + ".png"
    await page.screenshot({'path': imageName})
    await browser.close()


def sendMail(sender,receiver,password,mailserver,port,url,sub,contents):

    try:
        msg = MIMEMultipart('related')
        msg['From'] = formataddr(["sender", sender])  # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["receiver", receiver])  # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = sub

        # 文本信息
        # txt = MIMEText('this is a test mail', 'plain', 'utf-8')
        # msg.attach(txt)

        # 附件信息
        # attach = MIMEApplication(open("1.zip").read())
        # attach.add_header('Content-Disposition', 'attachment', filename='1.zip')
        # msg.attach(attach)

        # 正文显示图片

        body = contents + """
        <br><img src="cid:image"><br>
        """

        #asyncio.get_event_loop().run_until_complete(screenshot(url))

        imageName = url.replace("https://", "").replace("http://", "").replace("/", "") + ".png"
        text = MIMEText(body, 'html', 'utf-8')

        try:
            f = open(imageName, 'rb')
            pic = MIMEImage(f.read())
            f.close()
            pic.add_header('Content-ID', '<image>')
            msg.attach(text)
            msg.attach(pic)
        except:
            f = open('404.jpg', 'rb')
            pic = MIMEImage(f.read())
            f.close()
            pic.add_header('Content-ID', '<image>')
            msg.attach(text)
            msg.attach(pic)
            pass
        server = smtplib.SMTP(mailserver, port)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(sender, password)  # 发件人邮箱账号、邮箱密码
        server.sendmail(sender, receiver, msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()
        print(time.strftime('[%H:%M:%S]') + ' Notification has been sent successfully')
    except Exception as e:
        print(e)
        pass


def bigram(text1, text2):

    # bigram考虑匹配开头和结束，所以使用pad_right和pad_left
    text1_bigrams = nltk.bigrams(text1.split(), pad_right=True, pad_left=True)

    text2_bigrams = nltk.bigrams(text2.split(), pad_right=True, pad_left=True)

    # 交集的长度
    distance = len(set(text1_bigrams).intersection(set(text2_bigrams)))

    return distance

def sendHttp(url):

    try:
        # session = requests.Session()

        headers = {"Cache-Control": "max-age=0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                   "Upgrade-Insecure-Requests": "1",
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
                   "Connection": "close",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "zh-CN,zh;q=0.9"
                   }
        cookies = {"__jsluid_h": "d78b520921595ab02a00dd2cbc4484ad",
                   "JSESSIONID": "3823B8751C6732F651649703DEE19F50"
                   }

        data = requests.get(url,
                            headers=headers,
                            cookies=cookies,
                            timeout=10
                            )
        return data
    except Exception as e:
        print(e)
        return 'error'
        pass

def getHash(data):
    lastHash = hashlib.md5()
    lastHash.update(data.text.encode(encoding='UTF-8'))
    return lastHash.hexdigest()

if __name__ == '__main__':

    badSite = []
    errorSite = []
    goodSite = []
    hashDict = {}
    txt = {}

    conf = configparser.ConfigParser()

    try:
        conf.read("config.ini")
        sender = conf.get("mailconf", "sender")
        receiver = conf.get("mailconf", "receiver")
        password = conf.get("mailconf", "password")
        mailserver = conf.get("mailconf", "mailserver")
        port = int(conf.get("mailconf", "port"))

        print(time.strftime('[%H:%M:%S]') + " Config file load success...")
    except:
        print(time.strftime('[%H:%M:%S]') + " Config file load error...")


    n = 0
    for url in open('urls.txt'):
        n += 1
        url = url.replace('\n','').replace('\r','')

        try:
            data = sendHttp(url)
            print(time.strftime('[%H:%M:%S]') + '\t{}\t{}\t{}\t{}'.format(n, data.status_code, len(data.text), url))
            txt[url] = data.text
            goodSite.append(url)
            if data.status_code != 200:
                errorSite.append(url)
        except Exception as e:
            badSite.append(url)
            print(e)
            pass

        # if url in coolcat:
        #     try:
        #         data = sendHttp(url)
        #         print(time.strftime('[%H:%M:%S]') + '\t{}\t{}\t{}\t{}'.format(n, data.status_code, len(data.text), url))
        #         txt[url] = data.text
        #         goodSite.append(url)
        #     except Exception as e:
        #         print(e)
        #         pass
        # else:
        #     try:
        #         data = sendHttp(url)
        #         initHash = getHash(data)
        #         hashDict[url] = initHash
        #         print(time.strftime('[%H:%M:%S]') + '\t{}\t{}\t{}\t{}'.format(n, data.status_code, initHash, url))
        #         if data.status_code != 200:
        #             errorSite.append(url)
        #         goodSite.append(url)
        #     except Exception as e:
        #         print(time.strftime('[%H:%M:%S]') + '\t{} \terror\t{}\n{}'.format(n, url, e))
        #         badSite.append(url)
        #         pass
        # time.sleep(2)

    print(time.strftime('[%H:%M:%S]') + ' Test notification will be sent')

    contents = time.strftime('[%H:%M:%S]') + '共{}个站点连接失败:<br>'.format(len(badSite))

    for bad in badSite:
        contents += bad + '<br>'
        # print(bad)


    contents = contents + time.strftime('[%H:%M:%S]') + '共{}个站点返回的内容错误:<br>'.format(len(errorSite))

    for error in errorSite:
        contents += error + '<br>'

        # print(error)

    sub = '测试邮件-已开始监控 %s 等站点的内容' % url
    sendMail(sender, receiver, password, mailserver, port, url, sub,contents)


    # print(txt)

    print('=' * 150)

    while True:
        cat = []
        m = 0
        for url in goodSite:
            # print(url)
            try:
                data = sendHttp(url)
                # print('=' * 20)
                # print(url)
                fuck = bigram(txt[url], data.text) / bigram(txt[url], txt[url])
                print('[{}]{}'.format(fuck, url))
                if fuck < 0.95:
                    sub = '【警告】{}内容发生变化...'.format(url)
                    print(sub)
                    contents = '监测到站点<a href="{}">{}</a>有内容变化，请人工核查是否为合法修改。<br>页面相似度: {}'.format(url, url, fuck)
                    sendMail(sender, receiver, password, mailserver, port, url, sub, contents)
                # print('=' * 20)
            except Exception as e:
                print(e)
                pass

            time.sleep(2)

        time.sleep(1800)

        # if url in coolcat:
        #     try:
        #         data = sendHttp(url)
        #         # print('=' * 20)
        #         # print(url)
        #         fuck = bigram(txt[url], data.text) / bigram(txt[url], txt[url])
        #         print('[{}]{}'.format(fuck,url))
        #         if fuck < 0.95:
        #             sub = '【警告】{}内容发生变化...'.format(url)
        #             print(sub)
        #             contents = '监测到站点<a href="{}">{}</a>有内容变化，请人工核查是否为合法修改。<br>页面相似度: {}'.format(url, url, fuck)
        #             sendMail(sender, receiver, password, mailserver, port, url, sub, contents)
        #         # print('=' * 20)
        #     except Exception as e:
        #         print(e)
        #         pass
        # else:
        #     m += 1
        #     # print(url)
        #     try:
        #         lastData = sendHttp(url)
        #         lastHash = getHash(lastData)
        #         if lastHash != hashDict[url]:
        #             print(time.strftime('[%H:%M:%S]') + '\t{}\t{}\t{}'.format(m, lastData.status_code, url))
        #             print('{}!={}\n站点已被修改'.format(lastHash, hashDict[url]))
        #
        #             sub = '【警告】{}内容发生变化...'.format(url)
        #             contents = '监测到站点<a href="{}">{}</a>有内容变化，请人工核查是否为合法修改。'.format(url, url)
        #             sendMail(sender, receiver, password, mailserver, port, url, sub, contents)
        #
        #             cat.append(url)
        #     except Exception as e:
        #         print(e)
        #         pass




