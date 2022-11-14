import makeClass as html

class Json:

    import requests
    import json
    from bs4 import BeautifulSoup

    def isAbleJson(self, shop_api_name, app_key): 
        for k in range(129944, 129977):
            requestData = Json.requests.get(f"https://{shop_api_name}.cafe24api.com/api/v2/products/{k}?shop_no=1&cafe24_app_key={app_key}")
            
            if requestData.status_code == 200:
                x = html.HTML()
                print(x.option_parsing(k))
                Json.jsonParsing(requestData)
   
    def jsonParsing(requestData):         
        
        jsonData = requestData.json()
        # print(jsonData)

        json_html_list = ['description']
        print('=' * 170)
        for i in jsonData['product'].keys():
            if i in json_html_list:
                k = jsonData['product'].get(i)
                #print(k)

                
                # 사이트내 여러 선택사항
                #print(frame)
                
                

p = Json()
p.isAbleJson("mall66", "f7kOrfNK8UAn2Z93owrB4C")