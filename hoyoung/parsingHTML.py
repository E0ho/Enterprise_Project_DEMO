import requests
from bs4 import BeautifulSoup
import time
from email import header
from http.client import ImproperConnectionState
from urllib.error import URLError, HTTPError
import re

lists = [
    "http://rimrim.co.kr",
]

# Category_Num
cate_no = [24, 25]

# 엑셀 생성

# 자동적으로 반복
for list in lists:

    # 엑셀 스타일 시트 생성
    print(list)


    # html 규칙 2 (주소/product/detail.html?product_no=(int)&cate_no=(int)&display_group=(int))

    for num2 in cate_no:
        for num1 in range(180, 181):

            # 상품 판매 링크 가져오기
            header = {'User-Agent': 'Chrome/66.0.3359.181'}
            response = requests.get(
                f"{list}/product/detail.html?product_no={num1}&cate_no={num2}&display_group=1", headers=header)

            # 해당 url 존재 유무 파악
            if response.status_code == 200:

                # 파싱
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')

                # 원하는 정보 추출
                name_tag = soup.select_one('.infoArea')

                
                print((str(name_tag)))
                k = (re.findall('class=.+', str(name_tag)))
                
                print("*" * 100)
                
                class_name_list = []
                for i in k: 
                    class_name_list.append(i[0 : i.find('"', 7) + 1])
                    
                
                print(class_name_list)
                # print(name_tag)

                

            