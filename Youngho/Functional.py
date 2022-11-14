import requests
from bs4 import BeautifulSoup
from email import header
import re

productName_List = ['h1.-font-ns', 'li.name', 'div.prdnames', 'h1.name', 'h2.info_name','h3.product-name','h2.product_title','h2']
productPrice_List = ['#span_product_price_text' , 'li.price']
productImg_List = ['.product_image ','.prdImgView', '.imgArea', '.prd-image-list']

name_List = [productName_List, productPrice_List, productImg_List]

lists = [
    "http://rimrim.co.kr",              # 150     (성공)
    # "https://www.unipopcorn.com",       # 1100    (성공)
    # "https://m.ycloset.com/",           # 5300    (성공)
    # "http://com-esta.co.kr/",           # 450     (성공)
    # "https://monicaroom.com",           # 14000   (성공)
    # "https://m.mainbooth.co.kr/",       # 3015    (성공)
    # "https://romand.co.kr",             # 500     (성공)
    # "https://www.awesomeneeds.com"      # 2300    (성공)   - 옵션이 없는 사이트 
    # "https://www.nothing-written.com",  # 1700    (가격 - Hidden되어 있다)
]

# Class Name 조합 찾기 함수
def find_className():
    temp = 0
    index = 0
    while (temp < len(name_List)):
        if frame.select_one(name_List[temp][index]) != None:
            col.append(index)
            temp += 1
            index = 0
        else :
            index += 1
    
    return col

# 원하는 정보 추출 함수
def select(col):
    temp = 0
    index = 0
    while (temp < len(col)):
        if frame.select_one(name_List[temp][col[index]]) == None:
            print('예외처리')
            temp += 1
            index += 1
        else:
            vv = frame.select_one(name_List[temp][col[index]])
            info.append(vv)
            temp += 1
            index += 1
    return info


# 자동적으로 반복
for platformName in lists:

    # 사이트마다 num 초기화
    # temp = 0
    # index = 0
    col = []
    a= None
    
    # html 규칙 2 (주소/product/detail.html?product_no=(int)&cate_no=(int)&display_group=(int))
    for num1 in range(150,99000):

        # 상품 판매 링크 가져오기
        header = {'User-Agent': 'Chrome/66.0.3359.181'}
        response = requests.get(f"{platformName}/product/detail.html?product_no={num1}", headers=header)

        # 해당 url 존재 유무 파악
        if response.status_code == 200:

            # 파싱
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            
            # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)
            frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail')

            # 판매 중단한 상품 거르기
            if frame != None :

            # Select함수에 한번만 접근하기 위한 if 문
                if a == None:
                    print(num1)
                    a = find_className()
                    print(a)

                # select 함수
                info = []
                b = select(col)

                img = b[2].select_one('img').get('src')

                print(b[0].text)
                print(b[1].text)
                print (img)

                # 사이트내 여러 선택사항
                select_list=[]
                for sel in frame.find_all('select'):
                    select_list.append(sel)

                # 선택사항마다의 옵션 추출
                for v in range(0, len(select_list)):
                    option_list = []
                    print('옵션')
                    for op in select_list[v].find_all('option'):
                        option_list.append([op.text])
                    del option_list[0]
                    del option_list[0]
                    print(option_list)


                print('-------------------------------------------------------------------------------------------------------')