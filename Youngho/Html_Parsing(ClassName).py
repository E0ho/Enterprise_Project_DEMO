import requests
from bs4 import BeautifulSoup
import openpyxl
from email import header


productName_List = ['h1.-font-ns', 'li.name', 'div.prdnames', 'h1.name', 'h2.info_name','h3.product-name','h2.product_title','h2']
productPrice_List = ['#span_product_price_text' , 'li.price']
productImg_List = ['.product_image ','.prdImgView', '.imgArea', '.prd-image-list']

lists = [
    # "http://com-esta.co.kr/",           #450      (성공)
    # "https://monicaroom.com",           #14000    (성공)
    # "https://romand.co.kr",             # 500     (성공)
    # "http://rimrim.co.kr",              # 150     (성공)
    # "https://m.mainbooth.co.kr/",       # 3015    (성공)
    # "https://m.ycloset.com/",           # 5300    (성공)
    # "https://www.unipopcorn.com",       # 1100    (성공)
    # "https://www.nothing-written.com",  # 1700    (가격 - Hidden되어 있다)
    # "https://www.awesomeneeds.com"      # 2300    (성공)   
]

# 상품명 Parsing Class명 규칙 찾기
def select(name_num, price_num, img_num) :
    global frame
    productName = frame.select_one(productName_List[name_num])
    while productName == None:
        name_num += 1
        # 예외 처리 (오류 stop 방지 - None 사용)
        if len(productName_List) <= name_num :
            frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail')
            name_num = 0
        else: productName = frame.select_one(productName_List[name_num])

    productPrice = frame.select_one(productPrice_List[price_num])
    while productPrice == None:
        price_num += 1
        # 예외 처리 (오류 stop 방지 - None 사용)
        if len(productPrice_List) <= price_num :
            productPrice = 'sold out'
            price_num = 10000
        else: productPrice = frame.select_one(productPrice_List[price_num])

    productImg = frame.select_one(productImg_List[img_num])
    while productImg == None:
        img_num += 1
        # 예외 처리 (오류 stop 방지 - None 사용)
        if len(productImg_List) <= img_num :
            productImg = '이미지 없음'
            img_num = 10000
        else: productImg = frame.select_one(productImg_List[img_num])
        
    print(name_num, price_num, img_num)
    return name_num, price_num, img_num


# 엑셀 생성
workbook = openpyxl.Workbook()

# 자동적으로 반복
for list in lists:

    # 현재 platform 확인
    print(list)

    # 사이트마다 num 초기화
    name_num = 0
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
    for num1 in range(600,99000):

        # 상품 판매 링크 가져오기
        header = {'User-Agent': 'Chrome/66.0.3359.181'}
        response = requests.get(f"{list}/product/detail.html?product_no={num1}", headers=header)

        # 해당 url 존재 유무 파악
        if response.status_code == 200:

            # 파싱
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            
            # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)
            frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail .infoArea')

            # frame 안에서 infoarea접근하는 애들있고 , table, tbody, tr(1~2)
            table = frame.find('table')
            data = []
            for tr in table.find_all('tr'):
                data.append(tr)
            print(data[0].text)
            print(data[1].text)

            # 판매 중단한 상품 거르기
            if frame != None :
                
            # Select함수에 한번만 접근하기 위한 if 문
                if a == None:
                    print(num1)
                    a = select(name_num, price_num, img_num)
                    print(a)
                
                if len(productName_List) <= a[0] :
                    name = '등록되지 않은 Class'
                else :
                    name = frame.select_one(productName_List[a[0]]).text

                # soldout 예외 처리
                if len(productPrice_List) <= a[1] :
                    price = 'sold out'
                else :
                    price = frame.select_one(productPrice_List[a[1]]).text
                        
                # 예외 상황에도 not Error
                if len(productImg_List) <= a[2] :
                    img = None
                else:
                    imgDiv= frame.select_one(productImg_List[a[2]])
                    img = imgDiv.select_one('img').get('src')

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
                print(name , price , img)
                print('------------------------------------------------')
                
                
                worksheet[f'A{i}'] = list
                worksheet[f'D{i}'] = name
                worksheet[f'H{i}'] = price
                worksheet[f'J{i}'] = img
                # worksheet[f'L{i}'] = option_list
                i = i+1

workbook.save('Youngho/Rule2.xlsx')