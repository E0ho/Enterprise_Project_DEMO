import requests
from bs4 import BeautifulSoup
import openpyxl
import time
from email import header
from http.client import ImproperConnectionState
from urllib.error import URLError, HTTPError

productName_List = ['product-name','.prd_name_wrap', '.prdnames','.name','h3','h1','h2']
productPrice_List = ['.font_Gilroy', '#span_product_price_text', '.price']
productImg_List = ['.product_image ','.prdImgView', '.imgArea', '.prd-image-list']

name_list = [productName_List, productPrice_List, productImg_List]

lists = [
    # "https://romand.co.kr"              # 500
    "http://rimrim.co.kr",              # 150 ~ 200
    # "https://m.mainbooth.co.kr/",       # 3000 ~ 3200 
    # "https://m.ycloset.com/",           # 5300 ~ 5500
    # "https://www.andar.co.kr"           # 6000 ~ 8000
    # "https://www.unipopcorn.com"        # 1100
    # "https://www.nothing-written.com"   # 1700
    # "https://www.awesomeneeds.com"      # 2300     
]

# 상품명 Parsing Class명 규칙 찾기
def select(name_num, price_num, img_num) :
    global frame
    productName = frame.select_one(productName_List[name_num])
    while productName == None:
        name_num += 1
        # 예외 처리
        if len(productName_List) <= name_num :
            frame = soup.select_one('.detailArea')
            name_num = 0
        productName = frame.select_one(productName_List[name_num])

    productPrice = frame.select_one(productPrice_List[price_num])
    while productPrice == None:
        price_num += 1
        # 예외 처리 (SoldOut)
        if len(productPrice_List) <= price_num :
            break
        productPrice = frame.select_one(productPrice_List[price_num])

    productImg = frame.select_one(productImg_List[img_num])
    while productImg == None:
        img_num += 1
        # 예외 처리 (None)
        if len(productImg_List) <= img_num :
            break
        productImg = frame.select_one(productImg_List[img_num])
    print(name_num, price_num, img_num)
    return name_num, price_num, img_num, frame


# 엑셀 생성
workbook = openpyxl.Workbook()

# 자동적으로 반복
for list in lists:

    print(list)

    # 해당 사이트 Parsing Class명 규칙 찾기
    name_num=0
    price_num = 0
    img_num = 0
    a= None
    global frame
    # 엑셀 스타일 시트 생성
    worksheet = workbook.create_sheet('사이트')

    # 엑셀 행 지정
    i = 2
    worksheet['A1'] = '해당 상품 사이트'
    worksheet['D1'] = '상품명'
    worksheet['H1'] = '가격'
    worksheet['J1'] = '이미지'
    
    # html 규칙 2 (주소/product/detail.html?product_no=(int)&cate_no=(int)&display_group=(int))
    for num1 in range(150,8000):
        # 상품 판매 링크 가져오기
        header = {'User-Agent': 'Chrome/66.0.3359.181'}
        response = requests.get(f"{list}/product/detail.html?product_no={num1}", headers=header)

        # 해당 url 존재 유무 파악
        if response.status_code == 200:

            # 파싱
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)

            frame = soup.select_one('.xans-product-detail')
            
            if frame != None :
                print(num1)
                # 상품명, 가격, 이미지 조합 찾기 (1번만 실행하기 위한 if문)
                if a == None:
                    a = select(name_num, price_num, img_num)

                if len(productName_List) <= a[0] :
                    name = None
                else :
                    name = frame.select_one(productName_List[a[0]]).text
                # soldout 예외 처리
                if len(productPrice_List) <= a[1] :
                    price = None
                else :
                    price = frame.select_one(productPrice_List[a[1]]).text
                # 예외 상황에도 not Error
                if len(productImg_List) <= a[2] :
                    img = None
                else:
                    imgDiv= frame.select_one(productImg_List[a[2]])
                    img = imgDiv.select_one('img').get('src')

                sel = frame.select_one('select')
                option_list = []
                k = 0
                for op in sel.find_all('option'):
                    if k > 1 :
                        option_list.append([op.text])
                    k+=1
                print(option_list)
                print(name, price, img)
                
                worksheet[f'A{i}'] = list
                worksheet[f'D{i}'] = name
                worksheet[f'H{i}'] = price
                worksheet[f'J{i}'] = img
                worksheet[f'L{i}'] = option_list
                i = i+1

workbook.save('Youngho/Rule2.xlsx')