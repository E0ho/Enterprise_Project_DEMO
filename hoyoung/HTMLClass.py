class ParsingHTML :        
    
    import requests
    from bs4 import BeautifulSoup
    from email import header

    productName_List = ['h1.-font-ns', 'li.name', 'div.prdnames', 'h1.name', 'h2.info_name','h3.product-name','h2.product_title','h2']
    productPrice_List = ['#span_product_price_text' , 'li.price']
    productImg_List = ['.product_image ','.prdImgView', '.imgArea', '.prd-image-list']

    name_List = [productName_List, productPrice_List, productImg_List]
    index_info = []
    info_list = []
    op_list = []

    platformLists = [
        # "http://rimrim.co.kr",              # 150     (성공)
        "https://www.unipopcorn.com",       # 1100    (성공)
        # "https://m.ycloset.com/",           # 5300    (성공)
        # "http://com-esta.co.kr/",           # 450     (성공)
        # "https://monicaroom.com",           # 14000   (성공)
        # "https://m.mainbooth.co.kr/",       # 3015    (성공)
        # "https://romand.co.kr",             # 500     (성공)
        # "https://www.awesomeneeds.com"      # 2300    (성공)   - 옵션이 없는 사이트 
        # "https://www.nothing-written.com",  # 1700    (가격 - Hidden되어 있다)
    ]

    # Class Name 조합 찾기 함수 (상품명, 가격, 이미지)
    def find_name_Combination(frame):
        temp = 0
        index = 0
        while (temp < len(ParsingHTML.name_List)):
            if frame.select_one(ParsingHTML.name_List[temp][index]) != None:
                ParsingHTML.index_info.append(index)
                temp += 1
                index = 0
            elif index < len(ParsingHTML.name_List[temp])-1:
                index += 1
            

    # 원하는 정보 추출 함수 (상품명, 가격, 이미지)
    def select(index_info, frame):
        temp = 0
        index = 0
        while (temp < len(index_info)):
            info = frame.select_one(ParsingHTML.name_List[temp][ParsingHTML.index_info[index]])
            ParsingHTML.info_list.append(info)
            temp += 1
            index += 1

    # 옵션 정보 추출 함수
    def option(frame):

        # 사이트내 여러 선택사항
        select_list=[]
        for sel in frame.find_all('select'):
            select_list.append(sel)

        # 선택사항마다의 옵션 추출
        for v in range(0, len(select_list)):
            option_list = []
            for op in select_list[v].find_all('option'):
                option_list.append(op.text)
            del option_list[0:2]
            ParsingHTML.op_list.append(str(option_list))

        

    def parsingData(self):
        # Main문 자동적으로 반복
        for platformName in ParsingHTML.platformLists:

            # 사이트마다 num 초기화
            temp = 0
            index = 0

            
            # html 규칙 2 (주소/product/detail.html?product_no=(int)&cate_no=(int)&display_group=(int))
            for num1 in range(1100,99000):

                # 상품 판매 링크 가져오기
                header = {'User-Agent': 'Chrome/66.0.3359.181'}
                response = ParsingHTML.requests.get(f"{platformName}/product/detail.html?product_no={num1}", headers=header)

                # 해당 url 존재 유무 파악
                if response.status_code == 200:

                    # 파싱
                    html = response.text
                    soup = ParsingHTML.BeautifulSoup(html, 'html.parser')
                    
                    # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)
                    frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail')

                    # 판매 중단한 상품 거르기
                    if frame != None :

                        # Select함수에 한번만 접근하기 위한 if 문
                        if not ParsingHTML.index_info:
                            ParsingHTML.find_name_Combination(frame)
                            print(ParsingHTML.index_info)

                        else:
                            ParsingHTML.info_list = []
                            ParsingHTML.op_list = []
                            # 예외 페이지 무시하기
                            if frame.select_one(ParsingHTML.name_List[0][ParsingHTML.index_info[0]]) != None and frame.select_one(ParsingHTML.name_List[1][ParsingHTML.index_info[1]]) != None and frame.select_one(ParsingHTML.name_List[2][ParsingHTML.index_info[2]]) != None:
                                ParsingHTML.select(ParsingHTML.index_info, frame)
                                img = ParsingHTML.info_list[2].select_one('img').get('src')
                                # 옵션 추출 함수
                            ParsingHTML.option(frame)
                            option_num = 0
                            while option_num < len(ParsingHTML.op_list):
                                print('옵션 : ' + ParsingHTML.op_list[option_num])
                                option_num += 1

                            if ParsingHTML.info_list:
                                print('플랫폼 : ' + platformName)
                                print('상품명 : ' + ParsingHTML.info_list[0].text)
                                print('가격 : ' + ParsingHTML.info_list[1].text)
                                print('이미지 : ' + img)
                            
                            

                        print('-------------------------------------------------------------------------------------------------------')


if __name__ == "__main__":
    html_parsing = ParsingHTML()
    html_parsing.parsingData()