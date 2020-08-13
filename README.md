# next_year_salary
--------------
## 프로젝트 설명
> KBO리그 타자들의 연봉 예측 모델 (statiz 크롤링으로 2010~2019년 '타자'들 기록만 수집)
> 데이터 분석 및 예측 입문 후 개인 Toy Project로 해당 기술들 체득을 위해 진행
> 평소 관심이 있었고 데이터가 풍부한 야구와 관련된 프로젝트 주제 선정

## 개발 히스토리
 1. 2020년 8월 10일(월)
 + https://dacon.io/competitions/official/235546/codeshare/592?page=1&dtype=recent&ptype=pub 를 바탕으로 제작 시작
 + statiz 기록실에서 KBO리그 선수들의 2010~2019년도 기록 수집
 + 연도, 포지션, 생일 column 추가
 + statiz-origin.csv 생성
 
 2. 2020년 8월 11일(화)
 + 포지션 == 투수 전부 삭제
 + statiz에서 수집한 선수들 연봉정보 수집 및 저장
 + 연봉, 나이 column추가
 + statiz-fixed.csv 생성
 
 3. 2020년 8월 13일(목)
 + 의사결정트리를 활용하여 회귀분석 진행
 + 결측치 및 이상치 단순작업(전부 0으로 만들었음)
 + r2score = 0.216
