# matplotlib 한글 출력 가능하도록 만들기
from matplotlib import font_manager, rc

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/gulim.ttc").get_name()
rc('font', family=font_name)

# 데이터 분석 모듈
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# second_crawler로 만든 데이터 로드
df = pd.read_csv('data/statiz_fixed.csv')

# 해당 데이터셋 선수명으로 정렬 및 인덱스 정리
df = df.sort_values(['선수'])
df = df.reset_index(drop=True)
del df['Unnamed: 0']

# 연봉 이상치(900000(만)원) 0 원으로 정리
tmp = df[df['연봉'] >= 900000].copy()
tmp['연봉'] = 0
df[df['연봉'] >= 900000] = tmp


# if 연봉 >0 -> train/ else -> test
train = df[df['연봉'] > 0].copy()
print(train.shape)
test = df[df['연봉'] == 0].copy()
print(test.shape)

# feature 에 쓰이지 않을 정보들 제외
feature_names = test.columns.tolist()
feature_names.remove("선수")
feature_names.remove("연도")
feature_names.remove("생일")
feature_names.remove("연봉")
feature_names.remove("포지션")


train = train.replace(pd.np.nan, 0)
test = test.replace(pd.np.nan, 0)

# 예측값 라벨링, label = 연봉
label_name = '연봉'

X_train = train[feature_names].astype(int)
y_train = train[label_name]

X_test = test[feature_names].astype(int)
y_test = test[label_name]

print(len(y_train))

#scikit-learn 모듈 로드
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import r2_score

model = DecisionTreeRegressor(random_state=42)

model.fit(X_train, y_train)
y_predict = cross_val_predict(model, X_train, y_train, cv=5, verbose=2)
score = r2_score(y_train, y_predict)
print(score)
error = abs(y_train - y_predict)
print(error.mean())
sns.distplot(error)
print(error.describe())


# 모델 결과 시각화 및 원본과 비교
# plt.figure(figsize=(15,15))
# sns.distplot(y_train, hist=False, label='train')
# sns.distplot(y_predict, hist=False, label='predict')
#
# plt.show()

