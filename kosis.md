## 인구 통계 데이터 분석 및 시각화 (Python)

요청하신 내용에 따라, 다운로드 받은 CSV 파일을 Pandas DataFrame으로 읽어와서 특정 데이터를 분석하고 시각화하는 Python 프로그램을 작성하고, 이를 한 줄 한 줄 설명하는 마크다운(MD) 파일을 생성했습니다.

---

### 개요

이 프로그램은 통계청 등에서 받은 인구 통계 CSV 파일을 처리하는 과정을 담고 있습니다. 주요 작업은 다음과 같습니다.

1.  **데이터 로드**: `cp949` 인코딩으로 된 CSV 파일을 다중 헤더(Multi-header) 구조를 유지하며 불러옵니다.
2.  **데이터 정제**: 필요한 '일반가구원' 컬럼만 선택하고, 2015년 이후 데이터만 필터링합니다.
3.  **데이터 분석**:
    *   연도별 성별(남자/여자) 일반가구원 통계를 집계합니다.
    *   연도별 연령별 일반가구원 통계를 집계합니다.
4.  **데이터 시각화**: 최신 연도의 연령별 성별 일반가구원 데이터를 꺾은선 그래프로 시각화합니다.

### 전체 Python 프로그램 코드

```python
# 1. 필요 라이브러리 임포트
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings

# 2. 경고 메시지 무시 설정
warnings.filterwarnings('ignore')

# 3. 한글 폰트 설정 (Windows, macOS, Linux 환경에 맞게 수정)
# Windows의 경우
font_path = 'c:/Windows/Fonts/malgun.ttf'
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)
# macOS의 경우
# plt.rc('font', family='AppleGothic')

# 마이너스 부호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# 4. 파일명 정의 및 데이터 로드
file_path = '성__연령_및_가구주와의_관계별_인구__시군구_20251128184004.csv'

try:
    # 통계청 CSV는 보통 다중 헤더를 가지므로 header=[0, 1, 2]로 지정
    # 한글 파일이므로 encoding='cp949' 사용
    df = pd.read_csv(file_path, encoding='cp949', header=[0, 1, 2])
except FileNotFoundError:
    print(f"오류: '{file_path}' 파일을 찾을 수 없습니다. 파일명과 경로를 확인해주세요.")
    exit()

# 5. '일반가구원' 데이터만 필터링
# 첫 번째와 두 번째 컬럼(행정구역, 시점)은 유지
# 세 번째 레벨의 헤더가 '일반가구원'인 컬럼들만 선택
cols_to_keep = [df.columns[1]] + [col for col in df.columns if col[2] == '일반가구원']
df_filtered = df[cols_to_keep]

# 6. 컬럼 이름 재구성 및 정리
# 첫 번째 컬럼('시점') 이름 변경
df_filtered.rename(columns={df_filtered.columns[0]: '시점'}, inplace=True)

# 다중 헤더를 '성별_연령' 형태로 조합하여 단일 컬럼명으로 변경
new_columns = ['시점'] + [f"{c[0]}_{c[1]}" for c in df_filtered.columns[1:]]
df_filtered.columns = new_columns

# 7. 데이터 타입 변환 및 필터링
# '시점' 컬럼을 숫자형으로 변환
df_filtered['시점'] = pd.to_numeric(df_filtered['시점'])

# 데이터 컬럼들의 쉼표(,)를 제거하고 숫자형으로 변환
for col in df_filtered.columns[1:]:
    df_filtered[col] = pd.to_numeric(df_filtered[col].str.replace(',', ''), errors='coerce')

# NaN 값이 있을 경우 0으로 채움
df_filtered.fillna(0, inplace=True)

# 2015년 이후 데이터만 선택
df_final = df_filtered[df_filtered['시점'] >= 2015].copy()

print("=" * 50)
print("데이터 정제 및 필터링 완료 (2015년 이후)")
print(df_final.head())
print("=" * 50)


# 8. 남자 및 여자의 연도별 일반가구원 데이터 통계 출력
# '남자_'로 시작하는 컬럼과 '여자_'로 시작하는 컬럼을 각각 찾음
male_cols = [col for col in df_final.columns if '남자' in col]
female_cols = [col for col in df_final.columns if '여자' in col]

# 각 행(지역별 데이터)에 대해 남자 합계와 여자 합계를 계산하여 새로운 컬럼 추가
df_final['남자_총계'] = df_final[male_cols].sum(axis=1)
df_final['여자_총계'] = df_final[female_cols].sum(axis=1)

# '시점'(연도)을 기준으로 그룹화하여 남자와 여자의 총계를 합산
gender_stats_by_year = df_final.groupby('시점')[['남자_총계', '여자_총계']].sum()

print("\n[2015년 이후 연도별 남/여 일반가구원 통계]")
print(gender_stats_by_year)
print("=" * 50)


# 9. 연령별 일반가구원 데이터 통계 출력
# 연령대 컬럼 이름 추출 (예: '0~4세', '5~9세' 등)
age_groups = sorted(list(set([c.split('_')[1] for c in df_final.columns if '_' in c and '총계' not in c])))

# 연도별 연령대 총계를 저장할 빈 DataFrame 생성
age_stats_by_year = pd.DataFrame(index=gender_stats_by_year.index)

# 각 연령대에 대해 남자와 여자 데이터를 합산하여 연도별 통계 계산
for age in age_groups:
    male_age_col = f'남자_{age}'
    female_age_col = f'여자_{age}'
    # 해당 연령대의 남녀 데이터를 합산하여 새로운 컬럼으로 추가
    age_stats_by_year[age] = df_final.groupby('시점')[[male_age_col, female_age_col]].sum().sum(axis=1)

print("\n[2015년 이후 연도별 연령별 일반가구원 통계]")
print(age_stats_by_year)
print("=" * 50)


# 10. 남자 및 여자의 연령별 일반가구원 데이터 꺾은선 그래프
# 분석 기간 중 가장 최신 연도 선택
latest_year = df_final['시점'].max()

# 최신 연도 데이터만 필터링
df_latest_year = df_final[df_final['시점'] == latest_year]

# 최신 연도의 전국 합계 데이터 계산
latest_year_total = df_latest_year.sum()

# 남자와 여자 연령대별 데이터 추출
male_age_data = latest_year_total[male_cols]
female_age_data = latest_year_total[female_cols]

# 그래프의 x축 레이블로 사용할 연령대 이름 정리 (예: '남자_0~4세' -> '0~4세')
male_age_data.index = [idx.replace('남자_', '') for idx in male_age_data.index]
female_age_data.index = [idx.replace('여자_', '') for idx in female_age_data.index]

# 그래프 그리기
plt.figure(figsize=(16, 8))
plt.plot(male_age_data.index, male_age_data.values, marker='o', linestyle='-', label='남자')
plt.plot(female_age_data.index, female_age_data.values, marker='s', linestyle='--', label='여자')

# 그래프 제목 및 레이블 설정
plt.title(f'{int(latest_year)}년 연령별 남/여 일반가구원 수', fontsize=16)
plt.xlabel('연령대', fontsize=12)
plt.ylabel('가구원 수 (명)', fontsize=12)
plt.xticks(rotation=45) # x축 레이블 45도 회전
plt.grid(True, linestyle=':') # 그리드 추가
plt.legend() # 범례 표시

# 그래프 출력
print(f"\n[{int(latest_year)}년 기준] 연령별 남/여 일반가구원 데이터 시각화 그래프를 출력합니다.")
plt.tight_layout() # 그래프 레이아웃 최적화
plt.show()

```

---

### 코드 한 줄 한 줄 설명

#### 1. 필요 라이브러리 임포트
```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings
```
- `import pandas as pd`: 데이터 분석 및 조작을 위한 핵심 라이브러리인 Pandas를 `pd`라는 별칭으로 불러옵니다.
- `import matplotlib.pyplot as plt`: 데이터 시각화를 위한 Matplotlib의 pyplot 모듈을 `plt`라는 별칭으로 불러옵니다.
- `import matplotlib.font_manager as fm`: 그래프에서 한글 폰트를 설정하기 위해 폰트 관리자 모듈을 불러옵니다.
- `import warnings`: 불필요한 경고 메시지를 제어하기 위해 `warnings` 모듈을 불러옵니다.

#### 2. 경고 메시지 무시 설정
```python
warnings.filterwarnings('ignore')
```
- 프로그램 실행 중 발생할 수 있는 사소한 경고(예: 특정 함수가 추후 버전에서 변경될 예정이라는 경고)를 무시하여 출력을 깔끔하게 만듭니다.

#### 3. 한글 폰트 설정
```python
# Windows의 경우
font_path = 'c:/Windows/Fonts/malgun.ttf'
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)
# macOS의 경우
# plt.rc('font', family='AppleGothic')

# 마이너스 부호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False
```
- Matplotlib은 기본적으로 한글을 지원하지 않으므로, 시스템에 설치된 한글 폰트를 지정해야 합니다.
- `font_path`: Windows의 '맑은 고딕' 폰트 경로를 지정합니다. (macOS 사용자는 `AppleGothic` 등을 사용)
- `fm.FontProperties(...)`: 폰트 경로를 이용해 폰트 속성을 가져오고, `.get_name()`으로 폰트의 공식 이름을 얻습니다.
- `plt.rc('font', ...)`: Matplotlib의 전역 폰트 설정을 위에서 찾은 한글 폰트로 변경합니다.
- `plt.rcParams['axes.unicode_minus'] = False`: 한글 폰트 사용 시 간혹 발생하는 마이너스(-) 부호 깨짐 현상을 방지합니다.

#### 4. 파일명 정의 및 데이터 로드
```python
file_path = '성__연령_및_가구주와의_관계별_인구__시군구_20251128184004.csv'
try:
    df = pd.read_csv(file_path, encoding='cp949', header=[0, 1, 2])
except FileNotFoundError:
    print(f"오류: '{file_path}' 파일을 찾을 수 없습니다. 파일명과 경로를 확인해주세요.")
    exit()
```
- `file_path`: 읽어올 CSV 파일의 이름을 변수에 저장합니다.
- `try-except`: 파일이 없을 경우 발생하는 `FileNotFoundError`를 처리하여 사용자에게 친절한 메시지를 보여주고 프로그램을 종료합니다.
- `pd.read_csv(...)`: CSV 파일을 Pandas DataFrame 객체로 읽어옵니다.
  - `encoding='cp949'`: 한글이 포함된 파일이 깨지지 않도록 MS Windows에서 사용하는 한글 인코딩 방식인 `cp949`를 지정합니다.
  - `header=[0, 1, 2]`: 통계청 CSV 파일은 보통 3줄에 걸쳐 컬럼 이름(헤더)이 정의되어 있으므로, 첫 3줄을 헤더로 인식하도록 설정합니다.

#### 5. '일반가구원' 데이터만 필터링
```python
cols_to_keep = [df.columns[1]] + [col for col in df.columns if col[2] == '일반가구원']
df_filtered = df[cols_to_keep]
```
- `df.columns[1]`: 두 번째 컬럼인 '시점' 컬럼은 분석에 반드시 필요하므로 먼저 선택합니다.
- `[col for col in df.columns if col[2] == '일반가구원']`: 다중 헤더의 세 번째 레벨(`col[2]`) 값이 '일반가구원'인 컬럼들만 리스트로 만듭니다.
- `df_filtered = df[cols_to_keep]`: 위에서 선택한 컬럼들('시점' + '일반가구원' 컬럼들)만으로 새로운 DataFrame을 생성합니다.

#### 6. 컬럼 이름 재구성 및 정리
```python
df_filtered.rename(columns={df_filtered.columns[0]: '시점'}, inplace=True)
new_columns = ['시점'] + [f"{c[0]}_{c[1]}" for c in df_filtered.columns[1:]]
df_filtered.columns = new_columns
```
- `df_filtered.rename(...)`: 다중 헤더로 되어 있는 첫 번째 컬럼의 이름을 '시점'으로 간단하게 변경합니다.
- `new_columns = ...`: 새로운 컬럼 이름 리스트를 만듭니다. 첫 번째는 '시점'이고, 나머지는 다중 헤더의 첫 번째와 두 번째 레벨을 밑줄(`_`)로 연결하여 (예: '남자_0~4세') 만듭니다.
- `df_filtered.columns = new_columns`: DataFrame의 컬럼 이름을 새로 만든 리스트로 교체하여 다루기 쉽게 만듭니다.

#### 7. 데이터 타입 변환 및 필터링
```python
df_filtered['시점'] = pd.to_numeric(df_filtered['시점'])
for col in df_filtered.columns[1:]:
    df_filtered[col] = pd.to_numeric(df_filtered[col].str.replace(',', ''), errors='coerce')
df_filtered.fillna(0, inplace=True)
df_final = df_filtered[df_filtered['시점'] >= 2015].copy()
```
- `pd.to_numeric(...)`: '시점' 컬럼의 데이터 타입을 문자열에서 숫자(정수 또는 실수)로 변환합니다.
- `for col in ...`: '시점'을 제외한 모든 데이터 컬럼에 대해 반복 작업을 수행합니다.
  - `.str.replace(',', '')`: 인구 데이터에 포함된 쉼표(,)를 제거합니다. (예: "1,234" -> "1234")
  - `pd.to_numeric(..., errors='coerce')`: 쉼표를 제거한 문자열을 숫자로 변환합니다. 변환이 불가능한 값은 `NaN`(결측치)으로 처리합니다.
- `df_filtered.fillna(0, inplace=True)`: 혹시 모를 결측치(`NaN`)를 0으로 채웁니다.
- `df_final = ...`: '시점'이 2015 이상인 행들만 선택하여 최종 분석용 DataFrame인 `df_final`을 생성합니다. `.copy()`를 사용하여 불필요한 경고를 방지합니다.

#### 8. 남자 및 여자의 연도별 일반가구원 데이터 통계 출력
```python
male_cols = [col for col in df_final.columns if '남자' in col]
female_cols = [col for col in df_final.columns if '여자' in col]
df_final['남자_총계'] = df_final[male_cols].sum(axis=1)
df_final['여자_총계'] = df_final[female_cols].sum(axis=1)
gender_stats_by_year = df_final.groupby('시점')[['남자_총계', '여자_총계']].sum()
print(gender_stats_by_year)
```
- `male_cols = ...`, `female_cols = ...`: 컬럼 이름에 '남자' 또는 '여자'가 포함된 컬럼들을 각각 리스트로 만듭니다.
- `df_final['남자_총계'] = ...`: 남자 관련 컬럼들의 값을 행(가로 방향, `axis=1`) 기준으로 모두 더해 '남자_총계'라는 새 컬럼을 만듭니다.
- `df_final['여자_총계'] = ...`: 여자 관련 컬럼들도 동일하게 합산하여 '여자_총계' 컬럼을 만듭니다.
- `df_final.groupby('시점')`: 데이터를 '시점'(연도)별로 그룹화합니다.
- `[['남자_총계', '여자_총계']].sum()`: 그룹화된 각 연도에 대해 '남자_총계'와 '여자_총계'의 합계를 계산합니다.
- `print(...)`: 최종 계산된 연도별 성별 통계를 출력합니다.

#### 9. 연령별 일반가구원 데이터 통계 출력
```python
age_groups = sorted(list(set([c.split('_')[1] for c in df_final.columns if '_' in c and '총계' not in c])))
age_stats_by_year = pd.DataFrame(index=gender_stats_by_year.index)
for age in age_groups:
    male_age_col = f'남자_{age}'
    female_age_col = f'여자_{age}'
    age_stats_by_year[age] = df_final.groupby('시점')[[male_age_col, female_age_col]].sum().sum(axis=1)
print(age_stats_by_year)
```
- `age_groups = ...`: 컬럼 이름(예: '남자_0~4세')을 `_`로 분리하여 두 번째 부분('0~4세')만 추출하고, 중복을 제거한 뒤 정렬하여 순수한 연령대 리스트를 만듭니다.
- `age_stats_by_year = ...`: 연도를 인덱스로 하는 빈 DataFrame을 생성하여 결과를 저장할 공간을 마련합니다.
- `for age in age_groups:`: 각 연령대 그룹에 대해 반복합니다.
  - `male_age_col`, `female_age_col`: 해당 연령대의 남자, 여자 컬럼 이름을 만듭니다.
  - `df_final.groupby('시점')...`: 연도별로 그룹화한 뒤, 해당 연령대의 남녀 컬럼 값을 합산하고, 다시 그 결과를 합산하여(`sum(axis=1)`) 연도별/연령대별 총 인구를 계산합니다.
- `print(...)`: 최종 계산된 연도별 연령대 통계를 출력합니다.

#### 10. 남자 및 여자의 연령별 일반가구원 데이터 꺾은선 그래프
```python
latest_year = df_final['시점'].max()
df_latest_year = df_final[df_final['시점'] == latest_year]
latest_year_total = df_latest_year.sum()
male_age_data = latest_year_total[male_cols]
female_age_data = latest_year_total[female_cols]
male_age_data.index = [idx.replace('남자_', '') for idx in male_age_data.index]
female_age_data.index = [idx.replace('여자_', '') for idx in female_age_data.index]

plt.figure(figsize=(16, 8))
plt.plot(male_age_data.index, male_age_data.values, marker='o', linestyle='-', label='남자')
plt.plot(female_age_data.index, female_age_data.values, marker='s', linestyle='--', label='여자')

plt.title(f'{int(latest_year)}년 연령별 남/여 일반가구원 수', fontsize=16)
plt.xlabel('연령대', fontsize=12)
plt.ylabel('가구원 수 (명)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, linestyle=':')
plt.legend()

plt.tight_layout()
plt.show()
```
- `latest_year = ...`: 데이터에서 가장 최신 연도를 찾습니다.
- `df_latest_year = ...`: 최신 연도에 해당하는 데이터만 필터링합니다.
- `latest_year_total = ...`: 최신 연도 데이터의 모든 행(지역)을 합산하여 전국 총계를 구합니다.
- `male_age_data = ...`, `female_age_data = ...`: 전국 총계에서 남자 연령별, 여자 연령별 데이터를 각각 추출합니다.
- `male_age_data.index = ...`: 그래프의 x축 레이블을 깔끔하게 만들기 위해 인덱스 이름에서 '남자_'와 '여자_' 접두사를 제거합니다.
- `plt.figure(figsize=(16, 8))`: 그래프를 그릴 도화지(figure)의 크기를 가로 16인치, 세로 8인치로 설정합니다.
- `plt.plot(...)`: 꺾은선 그래프를 그립니다. x축은 연령대, y축은 가구원 수이며, 남자와 여자를 각각 다른 마커와 선 스타일로 그립니다. `label`은 범례에 표시될 이름입니다.
- `plt.title(...)`, `plt.xlabel(...)`, `plt.ylabel(...)`: 그래프의 제목, x축, y축의 이름을 설정합니다.
- `plt.xticks(rotation=45)`: x축의 연령대 레이블이 겹치지 않도록 45도 회전시킵니다.
- `plt.grid(True, ...)`: 그래프에 점선 형태의 격자를 추가하여 가독성을 높입니다.
- `plt.legend()`: `plot` 함수에서 설정한 `label`을 기반으로 범례를 표시합니다.
- `plt.tight_layout()`: 그래프의 제목, 레이블 등이 서로 겹치지 않도록 레이아웃을 자동으로 조절합니다.
- `plt.show()`: 완성된 그래프를 화면에 출력합니다.