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

driver = webdriver.Chrome('webdrivers/chromedriver.exe')

# 크롤링
for i in range(31):

    # 2010년 부터 2018년 까지 statiz에 기록된 선수들 필터링
    url = 'http://www.statiz.co.kr/stat.php?mid=stat&re=0&ys=2010&ye=2019&sn=100&pa={}'.format(i * 100)

    driver.get(url)
    driver.implicitly_wait(20)

    html = driver.find_element_by_xpath('//*[@id="mytable"]/tbody').get_attribute("innerHTML")  # 기록 table을 str형태로 저장
    soup = BeautifulSoup(html, 'html.parser')  # str 객체를 BeautifulSoup 객체로 변경

    temp = [i.text.strip() for i in soup.findAll("tr")]  # tr 태그에서, text만 저장하기
    temp = pd.Series(temp)  # list 객체에서 series 객체로 변경

    # '순'이나 'W'로 시작하는 row 제거
    # 즉, 선수별 기록만 남기고, index를 reset 해주기
    temp = temp[~temp.str.match("[순W]")].reset_index(drop=True)
    temp = temp.apply(lambda x: pd.Series(x.split(' ')))  # 띄어쓰기 기준으로 나눠서 dataframe으로 변경

    # 선수 팀 정보 이후 첫번째 기록과는 space 하나로 구분, 그 이후로는 space 두개로 구분이 되어 있음
    # 그래서 space 하나로 구분을 시키면, 빈 column들이 존재 하는데, 해당 column들 제거
    temp = temp.replace('', np.nan).dropna(axis=1)

    # 선수 이름 앞의 숫자 제거
    temp[0] = temp[0].str.replace("^\d+", '')
    tmp = temp[0]

    # 선수 이름 뒤의 팀 제거 및 포지션, 년도 추출
    year, position = [], []
    for k in range(len(temp[0])):
        if temp[0][k][len(temp[0][k]) - 1] == 'P':
            position.append('P')
        elif temp[0][k][len(temp[0][k]) - 2:] in ('1B', '2B', '3B', 'SS', 'LF', 'RF', 'CF'):
            position.append(temp[0][k][len(temp[0][k]) - 2:])
        elif temp[0][k][len(temp[0][k]) - 1] == 'C':
            position.append('C')
        else:
            position.append('DH')
        year.extend(re.compile('\d\d').findall(temp[0][k]))
        temp[0][k] = re.compile('[가-힣]+').findall(temp[0][k])[0]

    # 연도 형식 20dd로 통일
    for k in range(len(year)):
        year[k] = '20' + year[k]

    # 추출한 값들로 새 column 제작
    temp['연도'] = year
    temp['포지션'] = position

    # 선수들의 생일 정보가 담긴 tag들 가지고 오기
    birth = [i.find("a") for i in soup.findAll('tr') if 'birth' in i.find('a').attrs['href']]

    # tag내에서, 생일 날짜만 추출하기
    p = re.compile("\d{4}\-\d{2}\-\d{2}")
    birth = [p.findall(i.attrs['href'])[0] for i in birth]

    # 생일 column 추가
    temp['생일'] = birth

    # page별 완성된 dataframe을 계속해서 result에 추가 시켜주기
    if i == 0:
        result = temp
    else:
        result = result.append(temp)
        result = result.reset_index(drop=True)

    print(i, "완료")

# column 명 정보 저장
columns = ['선수', 'WAR'] + [i.text for i in soup.findAll("tr")[0].findAll("th")][4:-3] + ['타율', '출루', '장타', 'OPS',
                                                                                         'wOBA',
                                                                                         'wRC+', 'WAR+', '연도', '포지션',
                                                                                         '생일']
print(columns)
# column 명 추가
result.columns = columns

# webdriver 종료
driver.close()

print("최종 완료")
# 결과값 저장해두기
result.to_csv("data/statiz_origin.csv", encoding='utf-8-sig')
