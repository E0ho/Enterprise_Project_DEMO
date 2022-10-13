import requests
from bs4 import BeautifulSoup
import openpyxl
import time

lists = [
    "http://rimrim.co.kr/index.html",
    "https://unipopcorn.com/",
    # "http://www.arcencielofficial.com/",
    # "https://vastcharm.kr/?country=KR",
    # "https://romand.co.kr/",
    # "https://www.equmal.com/index.html",
    "https://www.carrieandshop.co.kr/",
    # "https://kravebeauty.co.kr/",
]


# 엑셀 생성
workbook = openpyxl.Workbook()
worksheet = workbook.create_sheet('Romand 상품 정보')

# 엑셀 행 지정
i = 2

# 여러 사이트 등록
for list in lists:

    # html 규칙 2 (주소/product/detail.html?product_no=(int)&cate_no=(int)&display_group=(int))
    try:
        for num3 in range(1, 5):
            for num2 in range(1, 50):
                for num1 in range(1, 5000):
                    response = requests.get(f"{list}/product/detail.html?product_no={num1}&cate_no={num2}&display_group={num3}")
                    html = response.text
                    soup = BeautifulSoup(html, 'html.parser')

                    name = soup.select_one('.-nopay.-titlebox > .-font-ns')
                    price =soup.select_one('span_product_price_text')

                    worksheet['A1'] = '상품명'
                    worksheet['B1'] = '가격'
                    worksheet[f'A{i}'] = name
                    worksheet[f'B{i}'] = price
                    i = i+1

    # Html 규칙 3 (주소/goods/goods_view.php?goodsNo=1934)
    except:
        for num4 in range(1900,2000):
            response = requests.get(f"https://www.carrieandshop.co.kr/goods/goods_view.php?goodsNo={num4}")
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            name = soup.select_one('.-nopay.-titlebox > .-font-ns')
            price =soup.select_one('span_product_price_text')

            worksheet['A1'] = '상품명'
            worksheet['B1'] = '가격'
            worksheet[f'A{i}'] = name
            worksheet[f'B{i}'] = price
            i = i+1

    workbook.save('Romand.xlsx')