# next_year_salary
--------------
## 프로젝트 설명
> KBO리그 타자들의 연봉 예측 모델 (statiz 크롤링으로 2010~2019년 '타자'들 기록만 수집)
> 데이터 분석 및 예측 입문 후 개인 Toy Project로 해당 기술들 체득을 위해 진행
> 평소 관심이 있었고 데이터가 풍부한 야구와 관련된 프로젝트 주제 선정

## 개발 히스토리
 1. 2020년 8월 10일(월)
 > + https://dacon.io/competitions/official/235546/codeshare/592?page=1&dtype=recent&ptype=pub 를 바탕으로 제작 시작
 > + statiz 기록실에서 KBO리그 선수들의 2010~2019년도 기록 수집
 > + 연도, 포지션, 생일 column 추가
 > + statiz-origin.csv 생성
 
 2. 2020년 8월 11일(화)
 > + 포지션 == 투수 전부 삭제
 > + statiz에서 수집한 선수들 연봉정보 수집 및 저장
 > + 연봉, 나이 column추가
 > + statiz-fixed.csv 생성
 
 3. 2020년 8월 13일(목)
 > + 의사결정트리를 활용하여 회귀분석 진행
 > + 결측치 및 이상치 단순작업(전부 0으로 만들었음)
 > + r2score = 0.216

 4. 2020년 8월 21일(금)
 > + r2score를 줄이기 위한 가설 설정
 > + 외국인타자들의 비정상적 연봉 및 FA선수들의 FA여부 변수 요망
 > + 기존 2nd Crawling -> 3rd Crawilng
 > + 새 2nd Crawling.py 생성하여 외국인타자들 기록 삭제
 
 5. 2020년 8월 24일(월)
 > + 사용 툴을 Pycharm 에서 Jupyter Notebook 으로 변경.
 > + 크롤링 코드 수정을 통하여 크롤링 단계에서 부터 깨끗한 데이터 수집
 > + 연봉 이상치, 뛴 게임 수 30G 미만 선수들 등등 이상치 최대한 제거하였음
 
 6. 2020년 8월 25일(화)
 > + 의사결정트리를 활용하여 회귀분석 진행
 > + r2score = 0.066
 > + 기존 dirty data 사용하여 진행했을 때(r2=0.2) 보다 정확도가 매우 낮아졌음
 
 7. 2020년 9월 8일(화)
 > + 의사결정트리, 랜덤포레스트, 등의 모델들 중 베스트 데이터 측정
 > + 랜덤포레스트 결과가 가장 좋았음.
 > + r2score = 0.53으로 대폭 상승하였음
