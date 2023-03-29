#-*- coding: utf-8 -*-
import warnings
import shutil
import subprocess
import time
import urllib
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
warnings.filterwarnings('ignore')

client_id = ""
client_secret = ""
top500_dic = dict()
review_cnt_list = []


def writeExcel():
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.create_sheet('keyword')
    wb.remove_sheet(wb['Sheet'])
    ws.append((['No', '인기검색어']))
    wb.save('C:\\Users\\user\\.virtualenvs\\naverdatalabtop500.xlsx')
    wb.close()


def searchKeyword():    
    for k, v in top500_dic.items():
        print(k, v)
        encText = urllib.parse.quote(v)
        url = "https://openapi.naver.com/v1/search/shop?query=" + encText + "&display=40"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            print(response_body.decode('utf-8'))
        else:
            print("Error Code:" + rescode)
        return



def getReviewCnt():
    options = Options()
    options.binary_location= 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    driver = webdriver.Chrome(executable_path='C:\\Users\\user\\Downloads\\chromedriver_win32\\chromedriver.exe', chrome_options = options) ## 크롬 드라이버가 위치한 경로 대입 필요

    for k, v in top500_dic.items():
        encText = urllib.parse.quote(v)
        driver.get('https://https://search.shopping.naver.com/search/all?query='+ encText)
        time.sleep(1)

        for i in range(1, 41) :
            path = f'//*[@id="content"]/div[1]/div[2]/div/div[{i}]/div/div/div[2]/div[5]/a[1]/em'        
            rev_cnt = driver.find_element(By.XPATH, path).text
            review_cnt_list.append(rev_cnt)        
        print(review_cnt_list)
        return


def getRankKeyword():
    options = Options()
    options.binary_location= 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

    driver = webdriver.Chrome(executable_path='C:\\Users\\user\\Downloads\\chromedriver_win32\\chromedriver.exe', chrome_options = options) ## 크롬 드라이버가 위치한 경로 대입 필요
    driver.get('https://datalab.naver.com/shoppingInsight/sCategory.naver')

    time.sleep(1)

    driver.find_element(By.XPATH, '//*[@id="18_device_0"]').click() #기기별 전체 클릭
    #time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="19_gender_0"]').click() #성별 전체 클릭
    #time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="20_age_0"]').click() #연령별 전체 클릭
    #time.sleep(0.5)

    driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span').click() #분야 클릭
    #time.sleep(0.5)

    driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[4]/a').click() #디지털/가전 클릭
    #time.sleep(0.5)

    driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/a').click() #조회하기 클릭
    #time.sleep(1)
    
    for i in range(0, 2) :
        for j in range(1, 21) :
            path = f'//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li[{j}]/a'
            result = driver.find_element(By.XPATH, path).text
            top500_dic[result.split('\n')[0]] = result.split('\n')[1]
            # print(result.split('\n'))
            # time.sleep(0.1)
            # ws.append(result.split('\n'))
        driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]').click()
        time.sleep(0.1)
    # print(top500_dic)

    driver.close()
    driver.quit()





if __name__ == '__main__':
    getRankKeyword()
    print("네이버 데이터랩 Top 500 키워드 뽑기 완료")
    searchKeyword()
    getReviewCnt()
