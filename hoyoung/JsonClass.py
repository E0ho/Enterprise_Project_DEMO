import HTMLClass as html

class ParsingJson:

    import pymysql
    import requests
    import json
    from bs4 import BeautifulSoup

    json_platform_list = []
    return_value = []
    wanted_value = {

        "product" : "price",
        "product" : "product_name"
        
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
        isAbleJson(count_json_list)


    def isAbleJson(self, count_json_list):

        for i in range(count_json_list) :
            platform = ParsingJson.json_platform_list[i][0]
            key = ParsingJson.json_platform_list[i][1]

            for k in range(129944, 129977):
                requestData = ParsingJson.requests.get(f"https://{platform}.cafe24api.com/api/v2/products/{k}?shop_no=1&cafe24_app_key={key}")
                
                if requestData.status_code == 200:
                    x = html.ParsingHTML()
                    ParsingJson.return_value.append(x.option(k))
                    ParsingJson.jsonParsing(requestData)
   
    def jsonParsing(requestData):         
        
        jsonData = requestData.json()

        for i in ParsingJson.wanted_value.values():
            ParsingJson.return_value.append(jsonData['product'][i])
                
                
if __name__ == "__main__":
    p = ParsingJson()
    p.connectDB()