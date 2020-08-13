# matplotlib 한글 출력 가능하도록 만들기
from matplotlib import font_manager, rc

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/gulim.ttc").get_name()
rc('font', family=font_name)

# 데이터 크롤링 모듈
from selenium import webdriver
from bs4 import BeautifulSoup
import re
# 데이터 분석 모듈
import pandas as pd
import numpy as np

# first_crawler로 만든 데이터 로드
df = pd.read_csv('data/statiz_origin.csv')

# 해당 데이터셋 선수 이름순으로 정렬 및 인덱스 정리
df = df.sort_values(['선수'])
df = df.reset_index(drop=True)
del df['Unnamed: 0']

# 투수 포지션 선수들 삭제
pitcher_id = df[df['포지션'] == 'P'].index
df = df.drop(pitcher_id)
players = df['선수'].tolist()
births = df['생일'].tolist()

# 연봉 열 추가
df['연봉'] = 0

driver = webdriver.Chrome('webdrivers/chromedriver.exe')
play_list = []

for i in range(len(players)):
    play_list.append((players[i], births[i]))

# 선수리스트 순회하며 연봉 데이터 추출
for player, birth in play_list:
    if any(df[(df['선수'] == player) & (df['생일'] == birth)]['연봉'] == 0):
        url = 'http://www.statiz.co.kr/player.php?opt=11&name={}&birth={}'.format(player, birth)
        driver.get(url)
        driver.implicitly_wait(10)

        html = driver.find_element_by_xpath('//*[@class="table table-striped table-condensed"]/tbody').get_attribute(
            "innerHTML")  # 기록 table을 str형태로 저장
        soup = BeautifulSoup(html, 'html.parser')  # str 객체를 BeautifulSoup 객체로 변경

        # player 와 birth 일치하는 선수의 연봉 데이터 추출
        temp = [i.text.strip() for i in soup.findAll("tr")]  # tr 태그에서, text만 저장하기
        temp = pd.Series(temp)
        temp = temp[~temp.str.match("[연]")].reset_index(drop=True)
        tmp_list = []

        # 해당 선수 연봉데이터 연도, 연봉으로 분리
        for i in range(len(temp) - 1):
            if len(temp[i+1].replace('-', '')) < 10:
                tmp_list.append([temp[i][:4], '2200', temp[i][-5:]])
            else:
                tmp_list.append([temp[i][:4], temp[i + 1][4:-5], temp[i][-5:]])
        temp = pd.DataFrame(temp)

        # 연봉데이터 리스트 순회하며 df['연봉'] 에 채워넣기
        for info in tmp_list:
            info[1] = info[1].replace(',', '')
            info[1] = info[1].replace('-', '')
            year = int(info[0])
            salary = int(info[1])
            if salary == 900000:
                salary = 0
            df.loc[(df['선수'] == player) & (df['연도'] == year) & (df['생일'] == birth), '연봉'] = salary

driver.close()

# 해당 기록 당시 선수 연차 계산, 및 df['나이'] column 생성
year = df['연도'].tolist()
birth = df['생일'].tolist()
age = []
for i in range(len(year)):
    age.append(year[i] - int(birth[i][:4]) + 1)
df['나이'] = pd.DataFrame(age)

df.to_csv("data/statiz_fixed.csv",encoding='utf-8-sig')