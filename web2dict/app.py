#
import re
import sys
import requests
from loguru import logger

import urllib3
urllib3.disable_warnings()

proxies = {
    "http":  "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

all_words = []

def get_text_from_url(url):

    print("Getting text from url: %s" % url)

    session = requests.Session()

    headers = {
        "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"", 
        "Accept": "application/json, text/plain, */*", 
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
        "Sec-Fetch-Site": "same-origin", 
        "Sec-Fetch-Dest": "empty", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8", 
        "Sec-Ch-Ua-Mobile": "?0", 
        "X-Origin-Product": "1", 
        "Sec-Fetch-Mode": "cors"
    }
    response = session.get(url=url, headers=headers, proxies=proxies, verify=False)

    # print("Status code:   %i" % response.status_code)
    # print("Response body: %s" % response.content)
    return str(response.text)


def get_word_from_text(text):
    words = re.findall("[a-zA-Z0-9]+", text)
    # print("Got word size: %s" %len(words))
    for word in words:
        all_words.append(word)

def save_word_to_file(words, filename):
    for word in words:
        if len(word) < 45:
            f = open(filename, 'a')
            f.write(word + "\n")
            f.flush()
            f.close()


if __name__ == '__main__':
    url = sys.argv[1]
    filename = sys.argv[2]
    print("Starting to connect to Web Server...")
    text = get_text_from_url(url)
    # print(text)
    get_word_from_text(text)

    urls  = re.findall('(href=\"|src=\")(.*?)(\?|\")', text)
    for url2 in urls:
        url2 = url2[1]
        # print(url2)
        text = ""
        if url2.startswith("http") and url2.endswith(".js"):
            text = get_text_from_url(url2)
        elif url2.startswith("//") and url2.endswith(".js"):
            text = get_text_from_url("http:" + url2)
        elif url2.endswith(".js"):
            text = get_text_from_url(url + "/" + url2)
        get_word_from_text(text)
    print(len(all_words))
    all_words = set(all_words)
    print(len(all_words))
    save_word_to_file(all_words,filename)
    