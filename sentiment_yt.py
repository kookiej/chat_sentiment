'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# https://ppeum-archive.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-Selenium%EC%9C%BC%EB%A1%9C-%EC%9C%A0%ED%8A%9C%EB%B8%8C-%EB%8C%93%EA%B8%80-%EC%8A%A4%ED%81%AC%EB%A1%A4%EB%A7%81-%ED%95%98%EA%B8%B0

url='https://www.youtube.com/watch?v=301lKck_kr8'
options=webdriver.ChromeOptions()
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.maximize_window()
driver.get(url)
time.sleep(3)

body=driver.find_element(By.TAG_NAME,'body')
for _ in range(120):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

comments=driver.find_elements(By.CSS_SELECTOR,'#contents ytd-comment-thread-renderer')
comment_dict = {
    'author':[],
    'txt':[]
    }

for comment in comments:
    try:
        author=comment.find_element(By.CSS_SELECTOR,'#author-text').text
        txt=comment.find_element(By.CSS_SELECTOR,'#content-text').text
        comment_dict['author'].append(author[1:])
        comment_dict['txt'].append(txt)
    except:
        continue

driver.quit()

#------

import pandas as pd

data=pd.DataFrame(comment_dict)
# print(data)
data.insert(0,'url',url)
# print(data)

#------

from sqlalchemy import create_engine

user = 'yeon'
password = '102938'
host = 'ghdwo.com'
port = 3306
database = 'yeon'

# engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4')
# data.to_sql(name='comments', con=engine, if_exists='append', index=False)
'''
#------

import pymysql
import pandas as pd

conn=pymysql.connect(
    host='ghdwo.com',
    user='yeon',
    password='102938',
    database='yeon',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cur=conn.cursor()
cur.execute("SELECT txt FROM comments")
comments_txt=cur.fetchall()

txts=pd.DataFrame(comments_txt)

cur.close()
conn.close()

#------

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from sqlalchemy import create_engine
from collections import Counter

path='cardiffnlp/twitter-xlm-roberta-base-sentiment'
# 'sangrimlee/bert-base-multilingual-cased-nsmc'

model=AutoModelForSequenceClassification.from_pretrained(path)
tokenizer=AutoTokenizer.from_pretrained(path)
classifier=pipeline('sentiment-analysis',model=model,tokenizer=tokenizer)

score_dict={
    'label':[],
    'score':[]
    }

for txt in txts['txt']:   
    # if txt.strip()=='':
    #     continue

    tokens=tokenizer.encode(txt,add_special_tokens=False)
    chunks=[tokens[i:i+512] for i in range(0, len(tokens), 512)]
    dec=[tokenizer.decode(chunk) for chunk in chunks]
    # print(dec)
    try:
        result=classifier(dec)
        # print(result)
        label_count=Counter([re['label'] for re in result])
        label=label_count.most_common(1)[0][0]
        score=sum([re['score'] for re in result if re['label']==label])/label_count[label]

        score_dict['label'].append(label)
        score_dict['score'].append(score)
    except Exception as e:
        score_dict['label'].append(None)
        score_dict['score'].append(None)
        # print('에러발생', e)

data=pd.DataFrame(score_dict)
# print(data)
'''
user = 'yeon'
password = '102938'
host = 'ghdwo.com'
port = 3306
database = 'yeon'

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4')
data.to_sql(name='scores', con=engine, if_exists='append', index=False)
'''
#------

pd.set_option('display.max_rows',None)

conn=pymysql.connect(
    host='ghdwo.com',
    user='yeon',
    password='102938',
    database='yeon',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cur=conn.cursor()
cur.execute("SELECT idx,author,txt FROM comments")
comments=cur.fetchall()
cur.execute("SELECT * FROM scores")
scores=cur.fetchall()

data.insert(0,'idx',range(1,len(data)+1))
df=pd.merge(pd.DataFrame(comments),data,how='inner',on='idx')
df.dropna(subset=['score'],axis=0,inplace=True)

df.to_excel('유튜브_댓글_감성분석2.xlsx',index=False)
print(df)

cur.close()
conn.close()
