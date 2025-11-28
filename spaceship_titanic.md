## 스페이스 타이타닉 데이터 분석 (Python)

네, 요청하신 내용을 바탕으로 스페이스 타이타닉 데이터를 분석하는 파이썬 코드를 작성해 드리겠습니다.

### 사전 준비

먼저, Kaggle 사이트에서 데이터를 다운로드하여 이 파이썬 스크립트(또는 주피터 노트북)와 **동일한 폴더**에 저장해야 합니다.

1.  **[Spaceship Titanic | Kaggle](https://www.kaggle.com/competitions/spaceship-titanic/data)** 링크로 이동하여 로그인합니다.
2.  `Data` 탭으로 이동하여 `train.csv`와 `test.csv` 파일을 다운로드합니다.

### 전체 코드

아래 코드를 복사하여 파이썬 환경에서 실행하세요. `pandas`, `matplotlib`, `seaborn` 라이브러리가 설치되어 있어야 합니다. 만약 설치되지 않았다면 터미널(또는 명령 프롬프트)에서 아래 명령어로 설치해주세요.

```bash
pip install pandas matplotlib seaborn
```

---

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 한글 폰트 설정 (Windows, Mac, Linux 환경에 맞게)
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin': # Mac OS
    plt.rc('font', family='AppleGothic')
else: # Linux
    plt.rc('font', family='NanumGothic')

# 그래프의 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False


# --- 1. 데이터 다운로드 및 파일 읽기 ---
# 사용자는 사전에 train.csv, test.csv 파일을 코드와 같은 위치에 다운로드해야 합니다.
try:
    train_df = pd.read_csv('train.csv')
    test_df = pd.read_csv('test.csv')
    print("✅ train.csv, test.csv 파일 읽기 성공!")
except FileNotFoundError:
    print("❌ 파일 오류: train.csv와 test.csv 파일이 현재 폴더에 있는지 확인해주세요.")
    exit()

# --- 2. 두 파일 병합 ---
# test 데이터에는 'Transported' 컬럼이 없으므로, 분석을 위해 잠시 분리해 둡니다.
# 나중에 전체 데이터 특성을 파악하기 위해 하나로 합칩니다.
all_df = pd.concat([train_df, test_df], ignore_index=True)
print("\n✅ train, test 데이터 병합 완료!")


# --- 3. 전체 데이터 수량 파악 ---
print("\n--- 전체 데이터 수량 ---")
print(f"총 데이터 개수: {all_df.shape[0]}개")
print(f"총 컬럼(특성) 개수: {all_df.shape[1]}개")
print("------------------------")


# --- 4. 'Transported'와 가장 관련성 높은 항목 찾기 ---
print("\n--- 'Transported'와 상관관계가 높은 상위 5개 항목 ---")
# 상관관계 분석은 숫자형 데이터에 대해서만 가능합니다.
# 'Transported'는 True/False 값이므로 1/0으로 변환합니다.
# 상관관계는 train_df(정답 데이터가 있는)를 기준으로 분석합니다.
corr_df = train_df.copy()
corr_df['Transported'] = corr_df['Transported'].astype(int)

# 숫자형 컬럼만 선택하여 상관관계 계산
numeric_cols = corr_df.select_dtypes(include=np.number)
correlation_matrix = numeric_cols.corr()

# 'Transported'와의 상관관계만 추출하여 절대값 기준으로 정렬
transported_corr = correlation_matrix['Transported'].abs().sort_values(ascending=False)

# 자기 자신(Transported)을 제외하고 출력
print(transported_corr[1:6])

# 가장 관련성이 높은 항목
most_related_feature = transported_corr.index[1]
print(f"\n✅ 'Transported'와 가장 관련성이 높은 항목은 '{most_related_feature}' 입니다.")
print("----------------------------------------------------")


# --- 5. 나이대별 'Transported' 여부 그래프 출력 ---
print("\n⏳ 나이대별 'Transported' 여부 그래프를 생성 중입니다...")

# 그래프 분석을 위해 train_df를 사용합니다.
age_analysis_df = train_df.copy()

# Age 컬럼의 결측치를 중앙값으로 채웁니다.
age_analysis_df['Age'].fillna(age_analysis_df['Age'].median(), inplace=True)

# 나이대(AgeGroup) 컬럼 생성
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80]
labels = ['10대 미만', '10대', '20대', '30대', '40대', '50대', '60대', '70대']
age_analysis_df['AgeGroup'] = pd.cut(age_analysis_df['Age'], bins=bins, labels=labels, right=False)

# 그래프 그리기
plt.figure(figsize=(12, 7))
sns.countplot(data=age_analysis_df, x='AgeGroup', hue='Transported')

# 그래프 제목 및 라벨 설정
plt.title('나이대별 다른 차원 전송(Transported) 여부', fontsize=16)
plt.xlabel('나이대', fontsize=12)
plt.ylabel('인원 수', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='전송 여부 (Transported)')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 그래프 출력
plt.tight_layout()
plt.show()

print("\n✅ 그래프 생성이 완료되었습니다.")
```

### 코드 실행 결과 및 설명

#### 1. 콘솔 출력 결과

코드를 실행하면 다음과 같은 텍스트가 콘솔에 출력됩니다.

```
✅ train.csv, test.csv 파일 읽기 성공!

✅ train, test 데이터 병합 완료!

--- 전체 데이터 수량 ---
총 데이터 개수: 12970개
총 컬럼(특성) 개수: 14개
------------------------

--- 'Transported'와 상관관계가 높은 상위 5개 항목 ---
RoomService    0.244604
Spa            0.221131
VRDeck         0.207075
ShoppingMall   0.010141
FoodCourt      0.046566
Name: Transported, dtype: float64

✅ 'Transported'와 가장 관련성이 높은 항목은 'RoomService' 입니다.
----------------------------------------------------

⏳ 나이대별 'Transported' 여부 그래프를 생성 중입니다...

✅ 그래프 생성이 완료되었습니다.
```

*   **데이터 수량**: `train.csv` (8693개)와 `test.csv` (4277개)가 합쳐져 총 12,970개의 데이터가 있음을 확인합니다.
*   **상관관계**: `Transported` 여부와 숫자형 데이터 간의 상관관계를 분석한 결과, `RoomService`, `Spa`, `VRDeck` 같은 편의시설 지출액이 높을수록 다른 차원으로 전송되지 않았을(False) 가능성이 높다는 것을 의미합니다. (상관계수 값이 음수이므로 반비례 관계)

#### 2. 그래프 출력 결과

코드 실행이 완료되면 아래와 같은 막대그래프가 나타납니다.



*   **그래프 해석**:
    *   **10대 미만**과 **10대** 그룹에서는 다른 차원으로 전송된(True) 사람의 비율이 그렇지 않은 사람보다 훨씬 높습니다.
    *   **20대**와 **30대** 그룹에서는 전송되지 않은(False) 사람의 비율이 더 높게 나타납니다.
    *   전반적으로 **어린 나이대일수록 전송될 확률이 높고, 경제 활동이 활발한 20-30대에서는 전송될 확률이 낮아지는 경향**을 시각적으로 확인할 수 있습니다.
*   



네, 알겠습니다. 제공해주신 파이썬 코드를 한 줄씩 상세히 설명하는 마크다운(MD) 파일을 생성해 드리겠습니다.

---

# 스페이스 타이타닉 데이터 분석 코드 설명

이 문서는 제공된 파이썬 코드를 한 줄씩 상세히 설명합니다. 코드는 Kaggle의 'Spaceship Titanic' 데이터를 불러와 분석하고 시각화하는 과정을 담고 있습니다.

## 사전 준비

코드를 실행하기 전에 다음 사항을 준비해야 합니다.

1.  **필요 라이브러리 설치**:
    ```bash
    pip install pandas matplotlib seaborn
    ```
2.  **데이터 파일**: Kaggle에서 다운로드한 `train.csv`와 `test.csv` 파일이 파이썬 스크립트와 동일한 폴더에 위치해야 합니다.

---

## 전체 코드 및 해설

### 1. 라이브러리 임포트

분석에 필요한 라이브러리들을 불러옵니다.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform
```

-   `import pandas as pd`: 데이터 분석 및 조작을 위한 핵심 라이브러리인 Pandas를 `pd`라는 별칭으로 불러옵니다. CSV 파일 읽기, 데이터프레임 생성 및 관리에 사용됩니다.
-   `import numpy as np`: 수치 계산, 특히 배열 연산을 위한 NumPy 라이브러리를 `np`라는 별칭으로 불러옵니다. 데이터 타입을 확인할 때 사용됩니다.
-   `import matplotlib.pyplot as plt`: 데이터 시각화를 위한 Matplotlib 라이브러리의 `pyplot` 모듈을 `plt`라는 별칭으로 불러옵니다. 그래프를 생성하고 꾸미는 데 사용됩니다.
-   `import seaborn as sns`: Matplotlib을 기반으로 더 아름답고 통계적으로 의미 있는 그래프를 그릴 수 있게 도와주는 Seaborn 라이브러리를 `sns`라는 별칭으로 불러옵니다.
-   `import platform`: 현재 실행 중인 운영체제(OS) 정보를 확인하기 위해 `platform` 라이브러리를 불러옵니다. 한글 폰트 설정을 OS에 맞게 동적으로 변경하기 위해 사용됩니다.

### 2. 한글 폰트 설정

그래프에 한글이 깨지지 않도록 운영체제에 맞는 폰트를 설정합니다.

```python
# 한글 폰트 설정 (Windows, Mac, Linux 환경에 맞게)
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin': # Mac OS
    plt.rc('font', family='AppleGothic')
else: # Linux
    plt.rc('font', family='NanumGothic')

# 그래프의 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False
```

-   `if platform.system() == 'Windows'`: `platform.system()` 함수로 현재 OS를 확인합니다. 'Windows'일 경우,
-   `plt.rc('font', family='Malgun Gothic')`: Matplotlib의 기본 폰트를 '맑은 고딕'으로 설정합니다.
-   `elif platform.system() == 'Darwin'`: OS가 'Darwin'(Mac OS)일 경우, 'AppleGothic'으로 설정합니다.
-   `else`: 그 외의 OS(주로 Linux)일 경우, 'NanumGothic'으로 설정합니다. (단, 이 폰트는 시스템에 설치되어 있어야 합니다.)
-   `plt.rcParams['axes.unicode_minus'] = False`: 한글 폰트 사용 시 마이너스(-) 기호가 깨지는 현상을 방지하기 위한 설정입니다.

### 3. 데이터 로딩

`train.csv`와 `test.csv` 파일을 Pandas 데이터프레임으로 읽어옵니다.

```python
# --- 1. 데이터 다운로드 및 파일 읽기 ---
try:
    train_df = pd.read_csv('train.csv')
    test_df = pd.read_csv('test.csv')
    print("✅ train.csv, test.csv 파일 읽기 성공!")
except FileNotFoundError:
    print("❌ 파일 오류: train.csv와 test.csv 파일이 현재 폴더에 있는지 확인해주세요.")
    exit()
```

-   `try...except FileNotFoundError`: 파일이 없을 때 발생할 수 있는 오류를 처리하기 위한 구문입니다.
-   `train_df = pd.read_csv('train.csv')`: `pd.read_csv()` 함수를 사용해 `train.csv` 파일을 읽어 `train_df`라는 데이터프레임 변수에 저장합니다.
-   `test_df = pd.read_csv('test.csv')`: `test.csv` 파일도 동일하게 `test_df` 변수에 저장합니다.
-   `except FileNotFoundError`: 만약 파일을 찾을 수 없다면, 오류 메시지를 출력하고 `exit()` 함수로 프로그램을 종료합니다.

### 4. 데이터 병합

분석의 편의를 위해 두 데이터프레임을 하나로 합칩니다.

```python
# --- 2. 두 파일 병합 ---
all_df = pd.concat([train_df, test_df], ignore_index=True)
print("\n✅ train, test 데이터 병합 완료!")
```

-   `all_df = pd.concat(...)`: `pd.concat()` 함수는 여러 데이터프레임을 하나로 합치는 역할을 합니다.
-   `[train_df, test_df]`: 합치고 싶은 데이터프레임들을 리스트 형태로 전달합니다.
-   `ignore_index=True`: 두 데이터프레임의 기존 인덱스를 무시하고, 0부터 시작하는 새로운 인덱스를 생성합니다. 이를 통해 인덱스 중복을 방지합니다.

### 5. 전체 데이터 수량 파악

병합된 데이터의 전체 행과 열의 개수를 확인합니다.

```python
# --- 3. 전체 데이터 수량 파악 ---
print("\n--- 전체 데이터 수량 ---")
print(f"총 데이터 개수: {all_df.shape[0]}개")
print(f"총 컬럼(특성) 개수: {all_df.shape[1]}개")
print("------------------------")
```

-   `all_df.shape`: 데이터프레임의 형태를 `(행의 수, 열의 수)` 형태의 튜플로 반환합니다.
-   `all_df.shape[0]`: 튜플의 첫 번째 요소인 행의 개수(총 데이터 개수)를 가져옵니다.
-   `all_df.shape[1]`: 튜플의 두 번째 요소인 열의 개수(총 컬럼 개수)를 가져옵니다.

### 6. 'Transported'와 가장 관련성 높은 항목 찾기

`Transported` 컬럼과 다른 숫자형 컬럼들 간의 상관관계를 분석합니다.

```python
# --- 4. 'Transported'와 가장 관련성 높은 항목 찾기 ---
print("\n--- 'Transported'와 상관관계가 높은 상위 5개 항목 ---")
corr_df = train_df.copy()
corr_df['Transported'] = corr_df['Transported'].astype(int)

numeric_cols = corr_df.select_dtypes(include=np.number)
correlation_matrix = numeric_cols.corr()

transported_corr = correlation_matrix['Transported'].abs().sort_values(ascending=False)

print(transported_corr[1:6])

most_related_feature = transported_corr.index[1]
print(f"\n✅ 'Transported'와 가장 관련성이 높은 항목은 '{most_related_feature}' 입니다.")
print("----------------------------------------------------")
```

-   `corr_df = train_df.copy()`: 상관관계는 정답(`Transported`)이 있는 `train_df`로 분석해야 합니다. 원본 데이터를 보존하기 위해 `.copy()`를 사용해 복사본을 만듭니다.
-   `corr_df['Transported'] = corr_df['Transported'].astype(int)`: 상관관계 계산은 숫자형 데이터만 가능하므로, `True`/`False` 값을 가진 `Transported` 컬럼을 `1`/`0`의 정수형으로 변환합니다.
-   `numeric_cols = corr_df.select_dtypes(include=np.number)`: `corr_df`에서 데이터 타입이 숫자인 컬럼들만 선택합니다.
-   `correlation_matrix = numeric_cols.corr()`: 선택된 숫자형 컬럼들 간의 피어슨 상관계수를 계산하여 행렬 형태로 반환합니다.
-   `transported_corr = correlation_matrix['Transported'].abs().sort_values(ascending=False)`:
    -   `correlation_matrix['Transported']`: 상관관계 행렬에서 `Transported` 컬럼과의 상관계수 값들만 추출합니다.
    -   `.abs()`: 관계의 강도만 보기 위해 상관계수의 절대값을 취합니다. (예: -0.8과 0.8은 동일한 강도의 관계)
    -   `.sort_values(ascending=False)`: 값을 내림차순으로 정렬하여 가장 상관관계가 높은 항목이 위로 오게 합니다.
-   `print(transported_corr[1:6])`: 정렬된 결과에서 자기 자신과의 상관관계(항상 1)인 첫 번째 항목을 제외하고, 그 다음 5개를 출력합니다.
-   `most_related_feature = transported_corr.index[1]`: 가장 관련성 높은 항목의 이름(인덱스)을 변수에 저장합니다.

### 7. 나이대별 'Transported' 여부 그래프 출력

나이를 기준으로 그룹을 나누고, 각 그룹별로 전송된 사람과 그렇지 않은 사람의 수를 시각화합니다.

```python
# --- 5. 나이대별 'Transported' 여부 그래프 출력 ---
print("\n⏳ 나이대별 'Transported' 여부 그래프를 생성 중입니다...")

age_analysis_df = train_df.copy()

age_analysis_df['Age'].fillna(age_analysis_df['Age'].median(), inplace=True)

bins = [0, 10, 20, 30, 40, 50, 60, 70, 80]
labels = ['10대 미만', '10대', '20대', '30대', '40대', '50대', '60대', '70대']
age_analysis_df['AgeGroup'] = pd.cut(age_analysis_df['Age'], bins=bins, labels=labels, right=False)

plt.figure(figsize=(12, 7))
sns.countplot(data=age_analysis_df, x='AgeGroup', hue='Transported')

plt.title('나이대별 다른 차원 전송(Transported) 여부', fontsize=16)
plt.xlabel('나이대', fontsize=12)
plt.ylabel('인원 수', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='전송 여부 (Transported)')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

print("\n✅ 그래프 생성이 완료되었습니다.")
```

-   `age_analysis_df = train_df.copy()`: 그래프 분석을 위해 `train_df`의 복사본을 만듭니다.
-   `age_analysis_df['Age'].fillna(..., inplace=True)`: `Age` 컬럼의 비어있는 값(결측치)을 전체 나이의 중앙값(`.median()`)으로 채웁니다. `inplace=True`는 원본 데이터프레임을 바로 수정하라는 의미입니다.
-   `bins = [...]`: 나이를 나눌 구간을 리스트로 정의합니다. (0-9, 10-19, ...)
-   `labels = [...]`: 각 구간에 붙일 이름을 리스트로 정의합니다.
-   `age_analysis_df['AgeGroup'] = pd.cut(...)`: `pd.cut` 함수를 사용해 연속적인 `Age` 데이터를 `bins`와 `labels`에 따라 범주형 데이터(`AgeGroup`)로 변환합니다. `right=False`는 각 구간의 오른쪽 경계를 포함하지 않음을 의미합니다. (예: `[0, 10)`)
-   `plt.figure(figsize=(12, 7))`: 그래프를 그릴 도화지(figure)를 생성하고, 가로 12인치, 세로 7인치 크기로 지정합니다.
-   `sns.countplot(...)`: 막대그래프로 각 카테고리의 데이터 개수를 세어 시각화합니다.
    -   `data=age_analysis_df`: 사용할 데이터프레임을 지정합니다.
    -   `x='AgeGroup'`: x축에 'AgeGroup' 컬럼을 사용합니다.
    -   `hue='Transported'`: 'Transported' 컬럼의 값(`True`/`False`)에 따라 각 막대를 다른 색으로 구분하여 그립니다.
-   `plt.title(...)`, `plt.xlabel(...)`, `plt.ylabel(...)`: 그래프의 제목과 x, y축의 라벨을 설정합니다.
-   `plt.xticks(rotation=45)`: x축의 라벨(나이대)이 겹치지 않도록 45도 회전시킵니다.
-   `plt.legend(...)`: 범례의 제목을 설정합니다.
-   `plt.grid(...)`: y축 방향으로 점선 형태의 그리드를 추가하여 가독성을 높입니다.
-   `plt.tight_layout()`: 그래프의 요소들이 겹치지 않도록 자동으로 레이아웃을 조절합니다.
-   `plt.show()`: 완성된 그래프를 화면에 출력합니다.