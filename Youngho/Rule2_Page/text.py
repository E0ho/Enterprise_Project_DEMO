import requests
from bs4 import BeautifulSoup
import openpyxl
import time
from email import header
from http.client import ImproperConnectionState
from urllib.error import URLError, HTTPError


frameName_List = ['.infoArea', '.xans-product-detail']
productName_List = ['.prd_name_wrap', '.name', '.prdnames']
productPrice_List = ['.font_Gilroy', '.price', '#span_product_price_text']

lists = [
    "http://rimrim.co.kr",            # 150 ~ 200
    "https://themedicube.co.kr/",     # 1 ~ 1200
    "https://m.mainbooth.co.kr/",     # 3000 ~ 3200
    "https://m.ycloset.com/",         # 5300 ~ 5500
    "https://www.andar.co.kr"         # 6000 ~ 8000
]


def select_FrameName(i) :
    frameName = soup.select_one(frameName_List[i])
    if frameName == None :
        i=i+1
        frameName = select_FrameName(i)
    return frameName

def select_ProductName(j) :
    productName = soup.select_one(productName_List[j])
    if productName == None :
        j = j+1
        productName = select_ProductName(j)
    return productName

def select_ProductPrice(k) :
    productPrice = soup.select_one(productPrice_List[k])
    if productPrice == None :
        k = k+1
        productPrice = select_ProductPrice(k)
    return productPrice

# 자동적으로 반복
for list in lists:
    print(list)
    i=0
    j=0
    k=0
    # html 규칙 2 (주소/product/detail.html?product_no=(int)&cate_no=(int)&display_group=(int))
    for num1 in range(1,5500):
        # 상품 판매 링크 가져오기
        header = {'User-Agent': 'Chrome/66.0.3359.181'}
        response = requests.get(
            f"{list}/product/detail.html?product_no={num1}", headers=header)

        # 해당 url 존재 유무 파악
        if response.status_code == 200:

            # 파싱
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            frame = soup.select_one('.xans-product-detail')
            # 원하는 정보 추출 (재귀 함수)
            img = soup.select_one('img').get('src')

            print(list+img)
            
            name = select_ProductName(j).text
            price = select_ProductPrice(k).text
            print(name, price)



            # # 원하는 정보 추출
            # name_tag = soup.select_one('.infoArea .prd_name_wrap')
            # if name_tag == None :
            #     name_tag = soup.select_one('.infoArea .name')

            # if name_tag == None :
            #     name_tag = soup.select_one('.xans-product-detail .prdnames')

            # if name_tag == None :
            #     name_tag = soup.select_one('.xans-product-detail .name')


            # price_tag = soup.select_one('.infoArea .font_Gilroy')
            # if price_tag == None :
            #     price_tag = soup.select_one('.infoArea .price')
            # if price_tag == None :
            #     price_tag = soup.select_one('#span_product_price_text')

            # if price_tag != None and name_tag != None:
            #     name = name_tag.text
            #     price = price_tag.text

            #     print('상품명 :' + name, price)



