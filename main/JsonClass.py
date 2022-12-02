import HTMLClass as ht
import DatabaseClass as db

class ParsingJson:

    import re
    import pymysql
    import requests
    import json
    import time
    from bs4 import BeautifulSoup

    json_platform_list = []
    return_value = []
    # wanted_value = {

    #     "product" : "product_name",
    #     "product" : "price",
    #     "product" : "detail_image"
    #     # 원하는 정보
        
    # }
    wanted_value = ["product_name", "price", "detail_image"]

    def connectDB(self):        
        con = ParsingJson.pymysql.connect(host='127.0.0.1', user='capstone', password='1234',
                       db='shopping_crawler', charset='utf8') # 한글처리 (charset = 'utf8')

        # STEP 3: Connection 으로부터 Cursor 생성
        cur = con.cursor()

        # cur.execute("delete from platform_item")
        # con.commit()

        count_json_list = cur.execute("SELECT * FROM platform_input")        
        con.commit()
        ParsingJson.json_platform_list = cur.fetchall()
        
        # 튜플을 리스트로 변환
        ParsingJson.json_platform_list = list(ParsingJson.json_platform_list)

        # 정확히는 여기서 리턴해줘서 전처리작업실시
        return ParsingJson.isAbleJson(count_json_list)


    def isAbleJson(count_json_list):        

        for i in range(count_json_list) :
            platform = ParsingJson.json_platform_list[i][0]
            key = ParsingJson.json_platform_list[i][1]
            url = ParsingJson.json_platform_list[i][2]
            platform_name = ParsingJson.json_platform_list[i][3]

            for k in range(0, 5000):
                ParsingJson.return_value = []   # 돌때마다 초기화                

                ParsingJson.return_value.append(platform_name)
                requestData = ParsingJson.requests.get(f"https://{platform}.cafe24api.com/api/v2/products/{k}?shop_no=1&cafe24_app_key={key}")
                ParsingJson.time.sleep(1)
                
                if requestData.status_code == 200:                       
                    ParsingJson.jsonParsing(requestData, k, url)
   
    def jsonParsing(requestData, product_no, url):  

        
        jsonData = requestData.json()
        for i in ParsingJson.wanted_value:
            if jsonData["product"].get(i) == None:
                return
            if i == 1:
                 ParsingJson.return_value.append(int(jsonData["product"].get(i)))
            else:                
                ParsingJson.return_value.append(jsonData["product"].get(i))
            print("테스트", jsonData["product"].get(i))
        
        header = {'User-Agent': 'Chrome/66.0.3359.181'}
        ## HTML옵션을 가져오려면 input 받을때 url 이름도 가져오는것은 어떨까.
        response = ParsingJson.requests.get(f"{url}/product/detail.html?product_no={product_no}", headers=header)
        ParsingJson.time.sleep(1) 

        # 해당 url 존재 유무 파악
        if response.status_code == 200:
            # 파싱
            html = response.text
            soup = ParsingJson.BeautifulSoup(html, 'html.parser')
            
            # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)
            frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail')

            html_ = ht.ParsingHTML()
            print(html_.json_option(frame))
            ParsingJson.return_value.append(html_.json_option(frame))        
       

            dbinp = db.DBClass()
            dbinp.optionlist_parsing(ParsingJson.return_value)
       
                
if __name__ == "__main__":
    p = ParsingJson()
    p.connectDB()