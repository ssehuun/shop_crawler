from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#-*- coding: utf-8 -*-
import re
import warnings
import pprint
import shutil
import subprocess
import time
import urllib
import json
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from openpyxl import Workbook
warnings.filterwarnings('ignore')


client_id = "RD1oPcv8ybcFOPSXm2xm"
client_secret = "asZCz3L4qr"

top500_dic = dict()
review_cnt_list = []
apiitem_list = []
filename = []


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("home.html", {"request": request, "id": id})

@app.get("/search", response_class=HTMLResponse)
async def selectItem(request: Request):
    # return templates.TemplateResponse("home.html")
    getRankKeyword()







def getRankKeyword():
    options = Options()
    options.add_argument("headless")
    # options.add_experimental_option("excludeSwitches", ["enable-logging"]) #크롬 종료되지 않는 상태 유지

    options.binary_location= 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

    driver = webdriver.Chrome(executable_path='C:\\Users\\user\\Downloads\\chromedriver_win32\\chromedriver.exe', chrome_options = options) ## 크롬 드라이버가 위치한 경로 대입 필요
    driver.get('https://datalab.naver.com/shoppingInsight/sCategory.naver')

    time.sleep(1)

    # driver.find_element(By.XPATH, '//*[@id="18_device_0"]').click() #기기별 전체 클릭
    # time.sleep(0.5)
    # driver.find_element(By.XPATH, '//*[@id="19_gender_0"]').click() #성별 전체 클릭
    # time.sleep(0.5)
    # driver.find_element(By.XPATH, '//*[@id="20_age_0"]').click() #연령별 전체 클릭
    # time.sleep(0.5)

    driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span').click() #분야 클릭
    time.sleep(0.5)

    filename.append(driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[5]/a').text)
    # driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[9]/a').click() #패션의류 클릭, 마지막 분야
    driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[5]/a').click() #가구/인테리어
    time.sleep(0.5)
    #//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[9]/a #생활건강

    
    driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span').click() # 2분류 클릭
    time.sleep(0.5)

    filename.append(driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[9]/a').text)
    # driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[8]/a').click() # 여성의류 클릭
    driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[9]/a').click() # 인테리어소품
    time.sleep(0.5)
    # //*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[8]/a #반려동물
    

    # driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/span').click() # 3분류 클릭
    # time.sleep(0.5)

    # driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/ul/li[1]/a').click() # 니트/스웨터 클릭
    # time.sleep(0.5)

    driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/a').click() #조회하기 클릭
    time.sleep(1)

    for i in range(0, 12) : # 25페이지까지
        for j in range(1, 21) : # 20개씩
            path = f'//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li[{j}]/a'
            result = driver.find_element(By.XPATH, path).text
            top500_dic[result.split('\n')[0]] = result.split('\n')[1]
            
            # time.sleep(0.1)
            # ws.append(result.split('\n'))
        
        driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]').click()
        time.sleep(0.1)
    driver.close()
    driver.quit()
    print(top500_dic, "네이버 데이터랩 Top 500 키워드 뽑기 완료")
