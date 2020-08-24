# 데이터 크롤링 모듈
from selenium import webdriver
from bs4 import BeautifulSoup
import re
# 데이터 분석 모듈
import pandas as pd
import numpy as np

# second_crawler로 만든 데이터 로드
df = pd.read_csv('data/statiz_origin.csv')

# 투수 포지션 선수들 삭제
pitcher_id = df[df['포지션'] == 'P'].index
df = df.drop(pitcher_id)
# 30G 이하 출전 선수 삭제
df = df[df.G >= 30]

# 선수 정보 조회 위한 선수, 생일 list 생성
players = df['선수'].tolist()
births = df['생일'].tolist()

driver = webdriver.Chrome('webdrivers/chromedriver.exe')

foreigner = []

# 선수리스트 순회하며 외인타자들 index 확보
for i in range(len(players)):
    url = 'http://www.statiz.co.kr/player.php?name={}&birth={}'.format(players[i], births[i])
    driver.get(url)
    driver.implicitly_wait(10)

    html = driver.find_element_by_xpath('//*[@class="dropdown-menu dropdown-menu-left"]').get_attribute(
        "innerHTML")
    soup = BeautifulSoup(html, 'html.parser')  # str 객체를 BeautifulSoup 객체로 변경
    temp = [i.text.strip() for i in soup.findAll("li")]
    if '용병' in temp[2]:
        foreigner.append(i)
driver.close()

# 기존 리스트에서 외인타자 전부 삭제
for i in foreigner:
    df = df.drop(i+1)

# csv파일로 저장
df.to_csv("data/statiz_fixed.csv",encoding='utf-8-sig')