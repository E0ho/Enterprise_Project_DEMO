import HTMLClass as html

class ParsingJson:

    import pymysql
    import requests
    import json
    import time
    from bs4 import BeautifulSoup

    json_platform_list = []
    return_value = []
    wanted_value = {

        "product" : "price",
        "product" : "product_name",
        "product" : "detail_image"
        # 원하는 정보
        
    }

    def connectDB():        
        con = ParsingJson.pymysql.connect(host='127.0.0.1', user='root', password='fouridiot1234',
                       db='Capstone', charset='utf8') # 한글처리 (charset = 'utf8')

        # STEP 3: Connection 으로부터 Cursor 생성
        cur = con.cursor()

        cur.execute("delete from platform_item")
        con.commit()

        count_json_list = cur.execute("SELECT * FROM platform_input")        
        con.commit()
        ParsingJson.json_platform_list = cur.fetchall()
        
        # 튜플을 리스트로 변환
        ParsingJson.json_platform_list = list(ParsingJson.json_platform_list)

        # 정확히는 여기서 리턴해줘서 전처리작업실시
        return ParsingJson.isAbleJson(count_json_list)


    def isAbleJson(self, count_json_list):        

        for i in range(count_json_list) :
            platform = ParsingJson.json_platform_list[i][0]
            key = ParsingJson.json_platform_list[i][1]
            url = ParsingJson.json_platform_list[i][2]

            for k in range(129944, 129977):
                ParsingJson.return_value = []   # 돌때마다 초기화
                ParsingJson.return_value.append(url)
                requestData = ParsingJson.requests.get(f"https://{platform}.cafe24api.com/api/v2/products/{k}?shop_no=1&cafe24_app_key={key}")
                ParsingJson.time.sleep(1)
                
                if requestData.status_code == 200:                       
                    ParsingJson.jsonParsing(requestData, k, url)
   
    def jsonParsing(requestData, product_no, url):  

        
        jsonData = requestData.json()
        for i, j in ParsingJson.wanted_value.items():
            ParsingJson.return_value.append(jsonData[i].get(j))
        
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

            html_ = html.ParsingHTML()
            ParsingJson.return_value.append(html_.option(frame))        
       


        # 받아서 전처리 작업
        return ParsingJson.return_value
                
                
if __name__ == "__main__":
    p = ParsingJson()
    p.connectDB()