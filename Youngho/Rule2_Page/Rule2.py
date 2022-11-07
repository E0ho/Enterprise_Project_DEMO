import requests
from bs4 import BeautifulSoup
import openpyxl
import time
from email import header
from http.client import ImproperConnectionState
from urllib.error import URLError, HTTPError

lists = [
    # "https://m.ycloset.com/" ,        # 5300 ~ 5500
    "https://m.mainbooth.co.kr/",     # 3000 ~ 3200
    # "http://rimrim.co.kr",           # 150 ~ 200
    # "https://themedicube.co.kr/",    # 1 ~ 1200
    "https://www.andar.co.kr"        # 6000 ~ 8000
]


# 엑셀 생성
workbook = openpyxl.Workbook()


# 자동적으로 반복
for list in lists:

    # 엑셀 스타일 시트 생성
    worksheet = workbook.create_sheet('사이트')
    print(list)

    # 엑셀 행 지정
    i = 2
    worksheet['A1'] = '해당 상품 사이트'
    worksheet['D1'] = '상품명'
    worksheet['H1'] = '가격'

    # html 규칙 2 (주소/product/detail.html?product_no=(int)&cate_no=(int)&display_group=(int))


    for num1 in range(3000,8000):
        # 상품 판매 링크 가져오기
        header = {'User-Agent': 'Chrome/66.0.3359.181'}
        response = requests.get(
            f"{list}/product/detail.html?product_no={num1}", headers=header)

        # 해당 url 존재 유무 파악
        if response.status_code == 200:

            # 파싱
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            # 원하는 정보 추출
            name_tag = soup.select_one('.infoArea .prd_name_wrap')
            # if name_tag == None :
            #     name_tag = soup.select_one('.infoArea .name')
            #     print('ssssss')

            if name_tag == None :
                name_tag = soup.select_one('.xans-product-detail .prdnames')
                print('sssssaaaaaaaaaaas')

            # if name_tag == None :
            #     name_tag = soup.select_one('.xans-product-detail .name')
                


            price_tag = soup.select_one('.infoArea .font_Gilroy')
            if price_tag == None :
                price_tag = soup.select_one('.infoArea .price')
            if price_tag == None :
                price_tag = soup.select_one('#span_product_price_text')

            if price_tag != None and name_tag != None:
                name = name_tag.text
                price = price_tag.text

                print('상품명 :' + name, price)
                
                worksheet[f'A{i}'] = list
                worksheet[f'D{i}'] = name
                worksheet[f'H{i}'] = price
                i = i+1

workbook.save('Youngho/Rule2_Page/Rule2.xlsx')