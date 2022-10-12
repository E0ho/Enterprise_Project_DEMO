import requests
from bs4 import BeautifulSoup
import time

lists = [
    "https://romand.co.kr/",
    "https://www.equmal.com/index.html",
    "https://www.carrieandshop.co.kr/",
    "https://kravebeauty.co.kr/",
    "http://rimrim.co.kr/index.html",
    "http://www.arcencielofficial.com/",
    "https://unipopcorn.com/",
    "https://vastcharm.kr/?country=KR",
]



# 여러 사이트 등록
for list in lists:

    # html 규칙 1 (주소/Product/ /(int)/category/(int)/display/(int)/)
    try:
        for num3 in range(1, 5):
            for num2 in range(1, 50):
                for num1 in range(1, 5000):
                    response = requests.get(f"{list}/Product/ /{num1}/category/{num2}/display/{num3}/")
                    html = response.text
    except:
        print("오류")