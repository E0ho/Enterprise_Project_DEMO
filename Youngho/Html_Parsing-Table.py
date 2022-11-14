import requests
from bs4 import BeautifulSoup
import openpyxl
from email import header

lists = [
    "http://slowacid.com/",        #4000   (성공)
    "https://escstudio.kr",        # 600   (성공) 
]

# 자동적으로 반복
for list in lists:

    # 현재 platform 확인
    print(list)

    # html 규칙 2 (주소/product/detail.html?product_no=(int)&cate_no=(int)&display_group=(int))
    for num1 in range(4000,99000):

        # 상품 판매 링크 가져오기
        header = {'User-Agent': 'Chrome/66.0.3359.181'}
        response = requests.get(f"{list}/product/detail.html?product_no={num1}", headers=header)

        # 해당 url 존재 유무 파악
        if response.status_code == 200:

            # 파싱
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            
            # 모든 페이지 공통 상품접근 Class 구조
            frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail')



            # 판매 중단한 상품 거르기
            if frame != None :

                # frame 안에서 infoarea접근하는 애들있고 , table 접근하는 애들이 있다.
                table = soup.find('table')
                data = []
                for tr in table.find_all('tr'):
                    data.append(tr)
                name = data[0].text
                price = data[1].text          

                # 사이트내 여러 선택사항
                select_list=[]
                for sel in frame.find_all('select'):
                    select_list.append(sel)

                # 사이트 선택사항 갯수
                max = len(select_list)
                
                # 선택사항마다의 옵션 추출
                for v in range(0, max):
                    option_list = []
                    for op in select_list[v].find_all('option'):
                        option_list.append([op.text])
                    print(str(option_list))
                    # worksheet[f'L{i}'] = option_list

                # print(option_list)
                
                print(name)
                print(price)
                print('------------------------------------------------')
