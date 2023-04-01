#-*- coding: utf-8 -*-
import re
import warnings
import pprint
import shutil
import subprocess
import time
import urllib
import json
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
item_list = []

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
            res_body = response.read()
            json_obj = json.loads(res_body.decode('utf-8'))
            apiitem_list = json_obj["items"]
            print(apiitem_list)
        else:
            print("Error Code:" + rescode)
        return


def getData():
    wb = Workbook()
    for k, v in top500_dic.items():
        encText = urllib.parse.quote(v)
        driver.get('https://search.shopping.naver.com/search/all?query='+ encText)
        time.sleep(1)
        body = driver.find_element(By.TAG_NAME, 'body')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

        mall_list = driver.find_elements(By.CSS_SELECTOR, ".basicList_item__0T9JD")
        #mall_list = driver.find_elements(By.CSS_SELECTOR, ".basicList_item__0T9JD:not(.ad)")
        ws = wb.create_sheet(v)
        if 'Sheet' in wb.sheetnames:
            wb.remove_sheet(wb['Sheet'])
        ws.append((['상품명', '가격', '등록일', '리뷰', '구매건수', '스토어링크']))

        for i in range(1, len(mall_list)+1): 
            itemName_path = f'//*[@id="content"]/div[1]/div[2]/div/div[{i}]/div/div/div[2]/div[1]/a' # 상품명
            #itemPrice_path = f'//*[@id="content"]/div[1]/div[2]/div/div[5]/div/div/div[2]/div[2]/strong/span/span'
            # itemPrice_path = f'//*[@id="content"]/div[1]/div[2]/div/div[{i}]/div/div/div[2]/div[2]/strong/span/span/span[2]'
            itemDate_path = f'//*[@id="content"]/div[1]/div[2]/div/div[{i}]/div/div/div[2]/div[5]/span[1]' # 상품등록일
            rev_path = f'//*[@id="content"]/div[1]/div[2]/div/div[{i}]/div/div/div[2]/div[5]/a[1]/em' # 리뷰수
            buy_path = f'//*[@id="content"]/div[1]/div[2]/div/div[{i}]/div/div/div[2]/div[5]/a[2]/em' # 구매건수
            itemLink_path = f'//*[@id="content"]/div[1]/div[2]/div/div[{i}]/div/div/div[2]/div[1]/a' # 상품link
            li = []
            try:
                itemName = driver.find_element(By.XPATH, itemName_path).text
                li.append(itemName)
            except NoSuchElementException:
                pass
            try:#<span class="price_num__S2p_v" data-testid="SEARCH_PRODUCT_PRICE">27,900원</span>
                itemPrice = mall_list[i-1].find_element(By.CSS_SELECTOR, ".price_num__S2p_v").text
                li.append(itemPrice)
            except NoSuchElementException:
                pass
            try:
                itemDate = driver.find_element(By.XPATH, itemDate_path).text
                li.append(itemDate.split()[1])
            except NoSuchElementException:
                pass
            try:
                rev_cnt = driver.find_element(By.XPATH, rev_path).text
                li.append(re.sub("\D", "", rev_cnt))
            except NoSuchElementException:
                li.append(0)
                pass
            try:
                buy_cnt = driver.find_element(By.XPATH, buy_path).text
                li.append(re.sub("\D", "", buy_cnt))
            except NoSuchElementException:
                li.append(0)
                pass
            try:
                itemLink = driver.find_element(By.XPATH, itemLink_path).get_attribute('href')
                li.append(itemLink)
            except NoSuchElementException:
                pass
            # item_list.append(li)
            ws.append(li)
        print(k, v, "완료")
    wb.save('C:\\Users\\LG\\.virtualenvs\\naverdatalabtop500.xlsx')
    wb.close()
        # pprint.pprint(item_list)
    return
    """
        items = driver.find_elements(By.CSS_SELECTOR, ".basicList_item__0T9JD")
        for item in items:
            li = []
            try:
                itemName = item.find_element(By.CSS_SELECTOR, ".basicList_link__JLQJf").text
                li.append(itemName)
            except NoSuchElementException:
                print("No itemName")
                pass
            try:
                itemPrice = item.find_element(By.CSS_SELECTOR, ".price_num__S2p_v").text
                li.append(itemPrice)
            except NoSuchElementException:
                print("No price")
                pass
            try:
                itemDate = item.find_element(By.CSS_SELECTOR, ".basicList_etc__LSkN_").text
                li.append(itemDate.split(' ')[-1])
            except NoSuchElementException:
                print("No date")
                pass
            try:
                revbuys = item.find_elements(By.CSS_SELECTOR, ".basicList_num__sfz3h")
                for i in revbuys:
                    li.append(i.find_element(By.CSS_SELECTOR, ".basicList_num__sfz3h").text)
            except NoSuchElementException:
                print("No review")
                pass
            # try:
            #     buy_cnt = item.find_element(By.CSS_SELECTOR, ".basicList_num__sfz3h").text
            #     li.append(buy_cnt)
            # except NoSuchElementException:
            #     print("No link")
            #     pass
            item_list.append(li)
            """
        # while True:
        #     pass
        # review_cnt_list.append(rev_cnt)
        # print(review_cnt_list)
        
def writeExcel():
    wb = Workbook()
    for i in top500_dic:
        ws = wb.create_sheet(top500_dic[i])
        if 'Sheet' in wb.sheetnames:
            wb.remove_sheet(wb['Sheet'])
        ws.append((['상품명', '가격', '등록일', '리뷰', '구매건수', '스토어링크']))
        for i in item_list:
            ws.append(i)
    wb.save('C:\\Users\\user\\.virtualenvs\\naverdatalabtop500.xlsx')
    wb.close()

start = time.time()
# def getRankKeyword():
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"]) #크롬 종료되지 않는 상태 유지

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

driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[9]/a').click() #패션의류 클릭, 마지막 분야
time.sleep(0.5)#//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[9]/a
#//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[9]/a #생활건강

driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span').click() # 2분류 클릭
time.sleep(0.5)

driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[8]/a').click() # 여성의류 클릭
time.sleep(0.5)#//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[25]/a
# //*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[8]/a #반려동물

# driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/span').click() # 3분류 클릭
# time.sleep(0.5)

# driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/ul/li[1]/a').click() # 니트/스웨터 클릭
# time.sleep(0.5)

driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/a').click() #조회하기 클릭
time.sleep(1)

for i in range(0, 1) : # 25페이지까지
    for j in range(1, 5) : # 20개씩
        path = f'//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li[{j}]/a'
        result = driver.find_element(By.XPATH, path).text
        top500_dic[result.split('\n')[0]] = result.split('\n')[1]
        
        # time.sleep(0.1)
        # ws.append(result.split('\n'))
    
    driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]').click()
    time.sleep(0.1)
print(top500_dic)
# driver.close()
# driver.quit()
print("네이버 데이터랩 Top 500 키워드 뽑기 완료")

# searchKeyword()
getData()
# writeExcel()
# if __name__ == '__main__':
    # getRankKeyword()
    
end = time.time()
print("총시간: ", end-start)