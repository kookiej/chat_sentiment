# https://castr.com/blog/vp9-codec/#:~:text=Pros:%20It%20is%20an%20open-source%20and%20royalty-free,container%20formats%20such%20as%20WebM%20and%20MKV.
# https://opensource.googleblog.com/2024/02/youtube-releases-scripts-to-help-partners-and-creators-optimize-work.html

# https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import subprocess
import time
import threading
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

end = threading.Event()

def page_down(body):
    for _ in range(10):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

def analyze(body):
    slots = body.find_elements(By.CLASS_NAME,'live-chat-list-item-slot-_-container')
    for slot in slots:
        msg=slot.find_element(By.CLASS_NAME, 'live-chat-list-item-message-_-message_body').text
        result=classifier(msg)

        if result[0]['label'] == 'positive' and result[0]['score'] > 0.7:
            name=slot.find_element(By.CLASS_NAME, 'live-chat-list-item-profile-_-profile_name').text
            print(f'{name} : {msg} | {result}')
            driver.execute_script("arguments[0].remove();", slot)


path='cardiffnlp/twitter-xlm-roberta-base-sentiment'
model=AutoModelForSequenceClassification.from_pretrained(path)
tokenizer=AutoTokenizer.from_pretrained(path)
classifier=pipeline('sentiment-analysis',model=model,tokenizer=tokenizer)

subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe' \
' --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')

option=Options()
option.add_experimental_option("debuggerAddress","127.0.0.1:9222")
driver=webdriver.Chrome(options=option)

url='https://account.weverse.io/ko/login/credential?client_id=weverse&redirect_uri=https%3A%2F%2Fweverse.io%2Fbts%2Flive%2F3-207801548&redirect_method=COOKIE&v=4'
id='5557802@naver.com'
pw='KCkc246808@'
driver.get(url)
driver.implicitly_wait(5)

fields = driver.find_elements(By.CLASS_NAME,'text-field_input__gyQwG')
input_id = fields[0]
input_pw = fields[1]

input_id.send_keys(id)
input_pw.send_keys(pw)
input_pw.send_keys(Keys.RETURN)
time.sleep(2)

url='https://weverse.io/bts/live/3-207801548?hl=ko'
driver.get(url)
driver.implicitly_wait(3)

body=driver.find_element(By.CLASS_NAME,'live-chat-list-slot-_-chat_list')

#------

t1 = threading.Thread(target=page_down, args=(body,)).start()
t2 = threading.Thread(target=analyze, args=(body,)).start()


input()


'''
from playwright.sync_api import sync_playwright
import time
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

path = 'cardiffnlp/twitter-xlm-roberta-base-sentiment'
model = AutoModelForSequenceClassification.from_pretrained(path)
tokenizer = AutoTokenizer.from_pretrained(path)
classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

id = '5557802@naver.com'
pw = 'KCkc246808@'
user_data_dir = 'C:/chromeCookie'

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        # 자동화 표시 관련 기본 인자 제거/옵션 추가 (선택)
        ignore_default_args=["--enable-automation"],
        args=["--disable-blink-features=AutomationControlled"],
        # channel='chrome',  # 설치된 Chrome을 사용하려면 주석 해제
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    # 자동 제어 탐지 기본 우회 스크립트 (선택)
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)


    page = context.new_page()
    page.goto('https://account.weverse.io/ko/login/credential?client_id=weverse&redirect_uri=https%3A%2F%2Fweverse.io%2Fbts%2Flive%2F3-207801548&redirect_method=COOKIE&v=4')
    page.fill('input[type="text"]', id)
    page.fill('input[type="password"]', pw)
    page.press('input[type="password"]', 'Enter')
    #page.goto('https://weverse.io/bts/live/3-207801548?hl=ko')
    
    page.goto('https://weverse.io/bts/live/3-207801548?hl=ko')
    time.sleep(3)

    body = page.query_selector('.live-chat-list-slot-_-chat_list')
    for _ in range(10):
        body.scroll_into_view_if_needed()
        page.keyboard.press('PageDown')
        time.sleep(1)
    
    slots = page.query_selector_all('.live-chat-list-item-slot-_-container')
    for slot in slots:
        msg = slot.query_selector('.live-chat-list-item-message-_-message_body').inner_text()
        result = classifier(msg)

        if result[0]['label'] == 'positive' and result[0]['score'] > 0.7:
            slot.evaluate("element => element.remove()")

    context.close()
'''

# 두개나오는데, 0번째는 일반사용자채팅, 1번째는 가수채팅
# s = driver.find_elements(By.CLASS_NAME,'live-chat-container-slot-_-body_wrap')
# msg = t[0].find_element(By.CLASS_NAME, 'live-chat-list-item-message-_-message_body').text
# driver.execute_script("arguments[0].removeAttribute('readonly');", t[0])

# 컨테이너는 live-chat-list-item-slot-_-container
# 작성자는   live-chat-list-item-profile-_-profile_name
# 내용은     live-chat-list-item-message-_-message_bodys
