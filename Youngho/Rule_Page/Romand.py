# Romand 사이트 상품 정보 Crawling
import requests
from bs4 import BeautifulSoup
import openpyxl

# # 엑셀 생성
# workbook = openpyxl.Workbook()
# worksheet = workbook.create_sheet('Romand 상품 정보')

# # 엑셀 행 지정
# i = 2

# for num3 in range(1, 5):
#     for num2 in range(1, 30):
#         for num1 in range(1, 100):
#             response = requests.get(f"https://romand.co.kr/Product/ /{num1}/category/{num2}/display/{num3}/")
#             html = response.text
#             soup = BeautifulSoup(html, 'html.parser')

#             name = soup.select_one('.-nopay.-titlebox > .-font-ns')
#             price =soup.select_one('span_product_price_text')

#             worksheet['A1'] = '상품명'
#             worksheet['B1'] = '가격'
#             worksheet[f'A{i}'] = name
#             worksheet[f'B{i}'] = price
#             i = i+1

# workbook.save('Romand.xlsx')

response = requests.get("https://romand.co.kr/product/%EB%A1%AC%EC%95%A4-%EC%A0%9C%EB%A1%9C-%EB%A7%A4%ED%8A%B8-%EB%A6%BD%EC%8A%A4%ED%8B%B1/516/category/1/display/2/")
html = response.text
soup = BeautifulSoup(html, 'html.parser')


name = soup.select_one('.-nopay.-titlebox > h1').text
price =soup.select_one('#span_product_price_text')

print(name)