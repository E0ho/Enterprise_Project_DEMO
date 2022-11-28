import pymysql
import re
import csv
from krwordrank.word import summarize_with_keywords
from krwordrank.word import KRWordRank
from krwordrank.hangle import normalize
# import pandas as pd

#csv 파일 불러오기
with open('C:/Users/H/OneDrive/바탕 화면/Capstone/fouridiots/Industry-project_Cafe24-Crawling-/Capstone.csv', 'r', encoding='cp949') as f:
    data = []

    row_data = csv.reader(f)
    for line in row_data:
        data.append(line)
    #csv파일내의 것을 모두 불러와서 2칸씩 띄어서 가져오기
    print(data[2::2])
#전처리 함수 생성(영어와 한국어만 받아오기(숫자 및 기호는 받지 않는다.))
file = re.compile('[A-Za-z가-힣]+').findall(str(data[2::2]))

# print(type(file))

##블로그에서 따옴 https://mojjisoft.tistory.com/25

min_count = 1   # 단어의 최소 출현 빈도수 (그래프 생성 시)
max_length = 15 # 단어의 최대 길이
verbose =True
wordrank_extractor = KRWordRank(min_count, max_length , verbose)
 
beta = 0.85    # PageRank의 decaying factor beta
max_iter = 10
 
with open('C:/Users/H/OneDrive/바탕 화면/Capstone/fouridiots/Industry-project_Cafe24-Crawling-/Capstone.csv', 'r') as f:
    texts = []
    for line in f:
        texts.append(line)
 
texts = [normalize(text,english=False , number=True) for text in texts ]
keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter)
 
for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:20]:
        print('%8s:\t%.4f' % (word, r))
 
 
# stopwords ={'세트'}
# keywords = summarize_with_keywords(texts, min_count=1, max_length=15,
#     beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)
# keywords = summarize_with_keywords(texts) # with default arguments
# print(keywords)
