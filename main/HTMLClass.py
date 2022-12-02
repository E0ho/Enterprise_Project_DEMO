import DatabaseClass as db
class ParsingHTML :        
    
    import requests
    from bs4 import BeautifulSoup
    from email import header
    import pymysql
    import time

    # HTML 태그
    productName_List = ['h1.-font-ns', 'li.name', 'div.prdnames', 'h1.name', 'h2.info_name','h3.product-name','h2.product_title','h2']
    productPrice_List = ['#span_product_price_text' , 'li.price']
    productImg_List = ['.product_image ','.prdImgView', '.imgArea', '.prd-image-list']

    name_List = [productName_List, productPrice_List, productImg_List]
    index_info = []
    info_list = []
    op_list = []

    # platformLists = [
    #     # "http://rimrim.co.kr",              # 150     (성공)
    #     "https://www.unipopcorn.com",       # 1100    (성공)
    #     # "https://m.ycloset.com/",           # 5300    (성공)
    #     # "http://com-esta.co.kr/",           # 450     (성공)
    #     # "https://monicaroom.com",           # 14000   (성공)
    #     # "https://m.mainbooth.co.kr/",       # 3015    (성공)
    #     # "https://romand.co.kr",             # 500     (성공)
    #     # "https://www.awesomeneeds.com"      # 2300    (성공)   - 옵션이 없는 사이트 
    #     # "https://www.nothing-written.com",  # 1700    (가격 - Hidden되어 있다)
    # ]

    platformLists = []

    def connectDB(self):
        # STEP 2: MySQL Connection 연결
        con = ParsingHTML.pymysql.connect(host='127.0.0.1', user='capstone', password='1234',
                            db='shopping_crawler', charset='utf8') # 한글처리 (charset = 'utf8')

        # STEP 3: Connection 으로부터 Cursor 생성
        cur = con.cursor()
        # cur.execute("delete from platform_item")
        # con.commit()

        count_html_url = cur.execute("SELECT * FROM html_url")
        con.commit()
        ParsingHTML.platformLists = cur.fetchall()
        
        # 정확히는 여기서 리턴해줘서 전처리작업실시
        return ParsingHTML.parsingData()
        
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
    def html_option(frame):

        # 사이트내 여러 선택사항
        select_list=[]
        for sel in frame.find_all('select'):
            select_list.append(sel)

        # 선택사항마다의 옵션 추출
        
        final_list=[]
        for v in range(0, len(select_list)):
            option_list = []
            for op in select_list[v].find_all('option'):
                option_list.append([op.text])
            # del option_list[0:2]

            item_list=[]
            for i in range(2, len(option_list)):

                item_list.append(option_list[i][0])
            final_list.append(item_list)
        print("finallist", final_list)
        return final_list

    def json_option(self, frame):

        # 사이트내 여러 선택사항
        select_list=[]
        if frame == None:
            return

        for sel in frame.find_all('select'):
            select_list.append(sel)

        # 선택사항마다의 옵션 추출
        final_list=[]
        if select_list:
            for v in range(0, len(select_list)):
                option_list = []
                for op in select_list[v].find_all('option'):
                    option_list.append([op.text])
                # del option_list[0:2]

                item_list=[]
                for i in range(2, len(option_list)):

                    item_list.append(option_list[i][0])
                final_list.append(item_list)
            print("final list", final_list)
        else :
            final_list = None
        return final_list
        

    def parsingData():
        # Main문 자동적으로 반복
        for platformName in ParsingHTML.platformLists:

            # 사이트마다 num 초기화
            temp = 0
            index = 0
            
            # html 규칙 2 (주소/product/detail.html?product_no=(int)&cate_no=(int)&display_group=(int))
            for num1 in range(0,5000):

                # 상품 판매 링크 가져오기
                header = {'User-Agent': 'Chrome/66.0.3359.181'}
                response = ParsingHTML.requests.get(f"{platformName[0]}/product/detail.html?product_no={num1}", headers=header)
                ParsingHTML.time.sleep(1.0)
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
                            
                            img = None
                            if frame.select_one(ParsingHTML.name_List[0][ParsingHTML.index_info[0]]) != None and frame.select_one(ParsingHTML.name_List[1][ParsingHTML.index_info[1]]) != None and frame.select_one(ParsingHTML.name_List[2][ParsingHTML.index_info[2]]) != None:
                                ParsingHTML.select(ParsingHTML.index_info, frame)
                                img = ParsingHTML.info_list[2].select_one('img').get('src')
                                # 옵션 추출 함수
                            
                            try:
                                if ParsingHTML.info_list :
                                    print('상품번호: ', num1)
                                    print('플랫폼 : ' + platformName[1])
                                    print('상품명 : ' + ParsingHTML.info_list[0].text)
                                    print('가격 : ' + ParsingHTML.info_list[1].text)
                                    print('이미지 : ' + img)                                
                                return_value = [platformName[1], ParsingHTML.info_list[0].text, ParsingHTML.info_list[1].text, img]
                            except IndexError:
                                continue  

                            ParsingHTML.op_list.append(ParsingHTML.html_option(frame))
                            
                            option_num = 0
                            for option_num in range(1):
                                # print('옵션 : ' , ParsingHTML.op_list[option_num])
                                if not ParsingHTML.op_list[option_num]:
                                    return_value.append(None)
                                else :
                                    return_value.append(ParsingHTML.op_list[option_num])

                                
                               
                                option_num += 1
                                
                                # 받아서 전처리 작업
                            
                            # print(return_value)
                            # return_value = [platformName, ParsingHTML.info_list[0].text, ParsingHTML.info_list[1].text, img, ParsingHTML.op_list]
                            dbinput = db.DBClass()
                            # dbinput.option_parsing(return_value)
                            dbinput.optionlist_parsing(return_value)
                            

                        print('-' * 150)


if __name__ == "__main__":
    html_parsing = ParsingHTML()
    html_parsing.parsingData()