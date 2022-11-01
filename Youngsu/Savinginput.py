import pymysql
import pyautogui
import requests

con = pymysql.connect(host='127.0.0.1', user='root', password='fouridiot1234',
                       db='Capstone', charset='utf8') # 한글처리 (charset = 'utf8')

# STEP 3: Connection 으로부터 Cursor 생성
cur = con.cursor()

key = pyautogui.prompt("key 값을 입력해주세요..")
platform = pyautogui.prompt("json header를 입력해주세요..")

str2= f"INSERT INTO platform_input VALUES('{platform}', '{key}')"
cur.execute(str2)
con.commit()


#만약 하나씩 저장할 때는 아래와 같이 코드 작성
#해당 값을 db에 한번만 저장하기 위해 사용
        # if not flag:
        #     str2= f"INSERT INTO platform_input VALUES('{platform}', '{key}')"
        #     cur.execute(str2)
        #     con.commit()
        #     flag = True

