import pymysql
import csv
import re

con = pymysql.connect(host='127.0.0.1', user='root', password='fouridiot1234',
                       db='Capstone', charset='utf8')

try :
    cor = con.cursor()
    data = []
    sql = 'select item_name from platform_item'
    cor.execute(sql)

    rows = cor.fetchall()
    for row in rows:
        data.append(row)

finally:
    cor.close()
    con.close()


# print(data[0][0])
headers = ['item_name']
rows = data

with open('Capstone.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)

