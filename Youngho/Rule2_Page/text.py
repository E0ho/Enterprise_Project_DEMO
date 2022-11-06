import requests
from bs4 import BeautifulSoup
import openpyxl
import time
from email import header
from http.client import ImproperConnectionState
from urllib.error import URLError, HTTPError

productName_List = ['.prd_name_wrap', '.prdnames', '.name', ]
productPrice_List = ['.font_Gilroy', '#span_product_price_text', '.price']
productImg_List = ['.imgArea', '.prdImgView']

name_list = [productName_List, productPrice_List, productImg_List]

lists = [
    # "http://rimrim.co.kr",            # 150 ~ 200
    # "https://themedicube.co.kr/",     # 1 ~ 1200 # 상품명
    "https://m.mainbooth.co.kr/",       # 3000 ~ 3200 # 이미지
    # "https://m.ycloset.com/",         # 5300 ~ 5500
    # "https://www.andar.co.kr"         # 6000 ~ 8000 # 상품명
]

# 상품명 Parsing Class명 규칙 찾기
def select_ProductName(name_num) :
    productName = frame.select_one(productName_List[name_num])
    if productName == None :
        name_num = name_num+1
        productName = select_ProductName(name_num)
    return productName

# 가격 Parsing Class명 규칙 찾기
def select_ProductPrice(price_num) :
    productPrice = frame.select_one(productPrice_List[price_num])
    if productPrice == None :
        
        price_num = price_num+1
        productPrice = select_ProductPrice(price_num)
    return productPrice

# 이미지 Parsing Class명 규칙 찾기
def select_ProductImg(img_num) :
    ImgDiv = frame.select_one(productImg_List[img_num])
    print (ImgDiv)
    if ImgDiv != None :
        productImg = ImgDiv.select_one('img')
        return productImg
    img_num = img_num+1
    productImg = select_ProductImg(img_num)

# 엑셀 생성
workbook = openpyxl.Workbook()

# 자동적으로 반복
for list in lists:

    print(list)

    # 해당 사이트 Parsing Class명 규칙 찾기
    name_num=0
    price_num = 0
    img_num = 0

    # 엑셀 스타일 시트 생성
    worksheet = workbook.create_sheet('사이트')

    # 엑셀 행 지정
    i = 2
    worksheet['A1'] = '해당 상품 사이트'
    worksheet['D1'] = '상품명'
    worksheet['H1'] = '가격'
    worksheet['J1'] = '이미지'
    

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

            # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)
            frame = soup.select_one('.xans-product-detail')
            if frame != None:

                # 상품명, 가격, 이미지
                name = select_ProductName(name_num).text
                price = select_ProductPrice(price_num).text
                img = select_ProductImg(img_num)
                print(img)
                img = img.get('src')

                print(img, name, price)
                worksheet[f'A{i}'] = list
                worksheet[f'D{i}'] = name
                worksheet[f'H{i}'] = price
                worksheet[f'J{i}'] = img
                i = i+1

        # else:
        #     time.sleep(1)
workbook.save('Youngho/Rule2.xlsx')