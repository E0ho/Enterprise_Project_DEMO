# api_list = [
# # 패션
# {'ozkiz' : 'ozkiz1'}, {'nerdy':'multinex'}, {'66girls':'mall66'},
# {"spao":"spao"}, {"discovery": "discoveryglobal"}, {'stylenanado' : 'nandaglobal'},

# # 뷰티
# {"kundal" : "thesf1"},

# # 푸드
# {"mihsgnon": "nsmall2022"}, {"food-ology":"manfidence"}, {"healthhelper": "nextgoods"},

# # 가구
# {"curble":"abluestore"}, {"marketb":"marketb"}
# ]


api_dict = {
# 패션
'ozkiz' : 'ozkiz1', 'nerdy':'multinex', '66girls':'mall66', "spao":"spao",
"discovery": "discoveryglobal", 'stylenanda' : 'nandaglobal', 'ggsing': "hkm0977", "leesle" : "leesle1",
"byther" : "harlem09", "pak-namae" : "piachess", "bluepops" : "ju021026", "habi-unni" : "mmmmj22", 
"giftxgift" : "kang24100", "monodaily" : "monodaily", "crump":"skw620", "athletekorea": "athlete", "monicaroom":"monica2012",
"mannergram":"s092814", "fibreno":"newfibreno", "jrium":"jrium917", "loar":"iroainc",
# 뷰티
"kundal":"thesf1", 
# 푸드
"mihsgnon": "nsmall2022", "food-ology":"manfidence", "healthhelper": "nextgoods","atemshop":"labnosh",
"labnosh":"labnosh", 
# 가구
"curble":"abluestore", "marketb":"marketb",

# 그 외
"chuu" : "chuukr", "ohscent" : "ohscent", "perfumegraphy": "pggraphy"
}

# print(len(api_dict))
# for i in api_list:
#     print(i)



import requests
import json

# 해당 페이지의 Json 데이터를 파싱하는 함수
# url과 app_key를 함수의 파라미터로 사용하여 사용자로부터 전달 받는다.
def isAbleJson(url, app_key):

    # url 은 https:// 와 www 두가지로 시작할 것.
    # url 가공

    # https:// 로 시작한다면 :// 을 .으로 바꾼다.
    url = url.replace('://', '.')
    shop_name = url.split('.')
    shop_name = ''.join([item for item in shop_name if item != "www" and item != "com" and item != "https" 
                            and item != 'co' and item != 'kr'])

    shop_api_name = api_dict.get(shop_name)

    print(shop_api_name)

    # shop_api_name 이 none 이면 json 파일이 존재하지 않기 때문에 html 파싱으로 이동.
    if shop_api_name != None:
        # 파싱하는 코드
        for k in range(4124, 4125):
            requestData = requests.get(f"https://{shop_api_name}.cafe24api.com/api/v2/products/{k}?shop_no=1&cafe24_app_key={app_key}")
            if requestData.status_code == 200:
                jsonParsing(requestData)
            else:
                continue

    else:
        print("html을 파싱하는 함수로 이동.")




def jsonParsing(requestData) : 
    # print(requestData.text)
    # print(type(requestData.text))
    
    jsonData = requestData.json()
    # print('==================================')
    # print(jsonData)
    # print(type(jsonData))
    # print(jsonData.get('price'))

    # print(jsonData['product'])
    # print("00000000")
    # print(jsonData['product']['product_name'])
    # print(jsonData['product']['price'])
    # print(jsonData['product']['detail_image'])

    html_list = ['description', 'mobile_description']
    # print(jsonData)
    for i in jsonData['product'].keys():
        if(i in html_list):
            continue
        print(i)
        # print(jsonData['product'][i])
        # print("==================================")           

    
    




     
# isAbleJson("https://www.ozkiz.com", "KU5HdZg4BVXlfoLDEPu6EC")
# # isAbleJson("www.spao.com", "iJf0852OYiGZTznb7gXaEG")
# isAbleJson("www.stylenanda.com","KU5HdZg4BVXlfoLDEPu6EC")
# isAbleJson("ggsing.com", "f7kOrfNK8UAn2Z93owrB4C")
# isAbleJson("leesle.com", 'iJf0852OYiGZTznb7gXaEG')
# isAbleJson("giftxgift.com", "f7kOrfNK8UAn2Z93owrB4C")
# isAbleJson("curble.co.kr", 'iJf0852OYiGZTznb7gXaEG')
isAbleJson("mannergram.com", "KU5HdZg4BVXlfoLDEPu6EC")