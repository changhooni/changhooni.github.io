네, 알겠습니다. 국가통계포털(KOSIS)에서 데이터를 자동화하여 다운로드하고, Pandas와 Matplotlib를 사용하여 분석 및 시각화하는 전체 과정을 담은 파이썬 코드와 상세한 설명을 Markdown 파일 형식으로 작성해 드리겠습니다.

---

### 결과물 미리보기
1.  **`kosis_automation.py`**: 전체 작업을 수행하는 파이썬 스크립트 파일입니다.
2.  **`README.md`**: 파이썬 스크립트의 각 라인을 상세하게 설명하는 마크다운 파일입니다.

---

### 1. 파이썬 스크립트 (`kosis_automation.py`)

```python
# kosis_automation.py

import os
import time
import glob
import pandas as pd
import matplotlib.pyplot as plt
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- 1. 초기 설정 및 다운로드 경로 지정 ---
# KOSIS 목표 URL
URL = "https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1IN1507&vw_cd=MT_ZTITLE&list_id=A11_2015_1_10_10&scrId=&seqNo=&lang_mode=ko&obj_var_id=&itm_id=&conn_path=MT_ZTITLE&path=%252FstatisticsList%252FstatisticsListIndex.do"

# CSV 파일을 다운로드할 폴더 지정
DOWNLOAD_DIR = os.path.join(os.getcwd(), "kosis_download")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- 2. 웹 드라이버 설정 ---
# Chrome 옵션 설정
chrome_options = Options()
# 다운로드 경로 설정 및 다운로드 시 확인창 비활성화
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
}
chrome_options.add_experimental_option("prefs", prefs)
# 브라우저를 백그라운드에서 실행 (주석 해제 시)
# chrome_options.add_argument("--headless")

# 웹 드라이버 서비스 설정 및 드라이버 객체 생성
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# --- 3. 웹 자동화 (Selenium) ---
try:
    # 3.1. KOSIS 페이지 접속
    driver.get(URL)
    print("KOSIS 페이지에 접속했습니다.")

    # WebDriverWait 객체 생성 (최대 10초 대기)
    wait = WebDriverWait(driver, 10)

    # 3.2. 시점 조정 (2015년 ~ 최신)
    # '시점' 메뉴 클릭
    time_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='시점']")))
    time_menu.click()
    print("'시점' 메뉴를 클릭했습니다.")

    # 시작 년도 '2015'로 설정
    start_year_select = Select(wait.until(EC.presence_of_element_located((By.ID, "strt_period"))))
    start_year_select.select_by_value("2015")
    print("시작 년도를 2015년으로 설정했습니다.")

    # 종료 년도를 선택 가능한 가장 마지막 값으로 설정
    end_year_select = Select(driver.find_element(By.ID, "end_period"))
    latest_year = end_year_select.options[-1].get_attribute("value")
    end_year_select.select_by_value(latest_year)
    print(f"종료 년도를 최신({latest_year}년)으로 설정했습니다.")

    # '조회' 버튼 클릭
    search_button = driver.find_element(By.CSS_SELECTOR, "a[onclick*='getStatisticData()']")
    search_button.click()
    print("데이터를 조회했습니다.")

    # 3.3. 행렬 전환
    # 행렬 전환 버튼이 나타날 때까지 대기 후 클릭
    transpose_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_transpose")))
    transpose_button.click()
    print("행렬을 전환했습니다.")

    # 3.4. CSV 파일 다운로드
    # 다운로드 메뉴 클릭
    download_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.a-down#ico_download")))
    download_menu.click()
    print("다운로드 메뉴를 클릭했습니다.")

    # CSV 형식 선택
    csv_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='csv']")))
    csv_option.click()
    print("CSV 형식을 선택했습니다.")

    # 다운로드 확인 버튼 클릭
    confirm_download_button = wait.until(EC.element_to_be_clickable((By.ID, "btnConfirm")))
    confirm_download_button.click()
    print("CSV 파일 다운로드를 시작합니다.")

    # 다운로드가 완료될 때까지 대기 (최대 30초)
    time.sleep(5) # 파일 생성을 위한 최소 대기 시간
    seconds = 0
    while seconds < 30:
        # .crdownload 파일이 없으면 다운로드 완료로 간주
        if not glob.glob(os.path.join(DOWNLOAD_DIR, "*.crdownload")):
            print("다운로드가 완료되었습니다.")
            break
        time.sleep(1)
        seconds += 1
    else:
        raise TimeoutError("CSV 파일 다운로드 시간 초과")

finally:
    # --- 4. 자원 정리 ---
    driver.quit()
    print("웹 드라이버를 종료했습니다.")


# --- 5. 다운로드 파일 처리 및 데이터프레임 생성 ---
# 다운로드 폴더에서 가장 최근에 수정된 CSV 파일 경로 찾기
list_of_files = glob.glob(os.path.join(DOWNLOAD_DIR, '*.csv'))
latest_file = max(list_of_files, key=os.path.getctime)
print(f"처리할 파일: {latest_file}")

# CSV 파일을 DataFrame으로 읽기 (KOSIS는 보통 cp949 인코딩 사용)
df = pd.read_csv(latest_file, encoding='cp949', header=1) # KOSIS CSV는 2번째 행이 헤더
print("\nCSV 파일을 DataFrame으로 변환했습니다.")
print("초기 DataFrame 정보:")
df.info()

# --- 6. 데이터 전처리 ---
# 6.1. 필요한 컬럼만 선택 ('시점', '성별', '연령별', '일반가구원')
# '시점' 컬럼 이름이 다를 수 있으므로 첫 번째 컬럼을 '시점'으로 간주
df.rename(columns={df.columns[0]: '시점'}, inplace=True)
df = df[['시점', '성별', '연령별', '일반가구원']]
print("\n'일반가구원' 관련 컬럼만 선택했습니다.")

# 6.2. 데이터 타입 변환 (숫자형으로)
df['일반가구원'] = pd.to_numeric(df['일반가구원'])
print("'일반가구원' 컬럼을 숫자형으로 변환했습니다.")

# 6.3. 불필요한 '계' 데이터 제거
df_filtered = df[(df['성별'] != '계') & (df['연령별'] != '계')].copy()
print("'성별' 및 '연령별'의 '계' 데이터를 제거했습니다.")

# --- 7. 통계 데이터 출력 ---
# 7.1. 연도별, 성별 일반가구원 통계
gender_stats = df_filtered.groupby(['시점', '성별'])['일반가구원'].sum().unstack()
print("\n[최종 통계 1: 연도별/성별 일반가구원 (단위: 명)]")
print(gender_stats)

# 7.2. 연도별, 연령별 일반가구원 통계
age_stats = df_filtered.groupby(['시점', '연령별'])['일반가구원'].sum().unstack()
print("\n[최종 통계 2: 연도별/연령별 일반가구원 (단위: 명)]")
print(age_stats)

# --- 8. 데이터 시각화 (Matplotlib) ---
# 8.1. 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin': # MacOS
    plt.rc('font', family='AppleGothic')
else: # Linux
    plt.rc('font', family='NanumGothic')
plt.rc('axes', unicode_minus=False) # 마이너스 기호 깨짐 방지

# 8.2. 시각화를 위한 데이터 준비 (가장 최신 연도 데이터 사용)
latest_year_data = df_filtered[df_filtered['시점'] == df_filtered['시점'].max()]
pivot_data = latest_year_data.pivot(index='연령별', columns='성별', values='일반가구원')

# 8.3. 꺾은선 그래프 그리기
plt.figure(figsize=(14, 8))
plt.plot(pivot_data.index, pivot_data['남자'], marker='o', linestyle='-', label='남자')
plt.plot(pivot_data.index, pivot_data['여자'], marker='s', linestyle='--', label='여자')

# 8.4. 그래프 서식 설정
plt.title(f'{int(latest_year_data["시점"].max())}년 성별 및 연령별 일반가구원', fontsize=16)
plt.xlabel('연령', fontsize=12)
plt.ylabel('일반가구원 (명)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()

# 8.5. 그래프 출력
print("\n데이터 시각화 그래프를 출력합니다.")
plt.show()
```

---

### 2. 마크다운 설명 파일 (`README.md`)

````markdown
# KOSIS 데이터 자동화 및 분석 파이썬 스크립트 설명

이 문서는 `kosis_automation.py` 스크립트의 작동 방식을 한 줄 한 줄 상세하게 설명합니다. 이 스크립트는 국가통계포털(KOSIS)에 접속하여 특정 통계 데이터를 자동으로 다운로드하고, 이를 Pandas로 분석하여 최종 결과를 출력 및 시각화하는 과정을 담고 있습니다.

## 사전 준비

스크립트를 실행하기 전에 다음 라이브러리들이 설치되어 있어야 합니다.

```bash
pip install pandas matplotlib selenium webdriver-manager
```

## `kosis_automation.py` 코드 설명

### 1. 라이브러리 임포트

```python
import os
import time
import glob
import pandas as pd
import matplotlib.pyplot as plt
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
```
- **os**: 파일 시스템 경로를 다루거나 디렉터리를 생성하기 위해 사용합니다.
- **time**: 프로그램 실행을 잠시 멈추기 위해 사용합니다. (예: 파일 다운로드 대기)
- **glob**: 특정 패턴의 파일 목록을 가져오기 위해 사용합니다. (예: 다운로드된 CSV 파일 찾기)
- **pandas as pd**: 데이터 분석 및 조작을 위한 핵심 라이브러리입니다. CSV 파일을 DataFrame으로 읽고 처리합니다.
- **matplotlib.pyplot as plt**: 데이터 시각화를 위해 사용됩니다. 꺾은선 그래프를 생성합니다.
- **platform**: 실행 중인 운영체제(Windows, macOS 등)를 확인하여 그에 맞는 한글 폰트를 설정하기 위해 사용합니다.
- **selenium**: 웹 브라우저를 자동으로 제어하는 라이브러리입니다. 웹 페이지 접속, 클릭, 데이터 선택 등을 수행합니다.
- **webdriver_manager.chrome**: 로컬 환경에 맞는 Chrome 웹 드라이버를 자동으로 설치 및 관리해줍니다.

### 2. 초기 설정 및 다운로드 경로 지정

```python
# KOSIS 목표 URL
URL = "https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1IN1507&vw_cd=MT_ZTITLE&list_id=A11_2015_1_10_10&scrId=&seqNo=&lang_mode=ko&obj_var_id=&itm_id=&conn_path=MT_ZTITLE&path=%252FstatisticsList%252FstatisticsListIndex.do"

# CSV 파일을 다운로드할 폴더 지정
DOWNLOAD_DIR = os.path.join(os.getcwd(), "kosis_download")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)
```
- **URL**: 자동화할 KOSIS 통계표의 주소를 변수에 저장합니다.
- **DOWNLOAD_DIR**: 다운로드된 CSV 파일을 저장할 폴더 경로를 지정합니다. `os.getcwd()`는 현재 스크립트가 실행되는 경로를 의미하며, 그 안에 `kosis_download`라는 폴더를 생성합니다.
- **os.makedirs()**: 지정된 폴더가 존재하지 않으면 새로 생성합니다.

### 3. 웹 드라이버 설정

```python
# Chrome 옵션 설정
chrome_options = Options()
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
}
chrome_options.add_experimental_option("prefs", prefs)

# 웹 드라이버 서비스 설정 및 드라이버 객체 생성
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
```
- **Options()**: Chrome 브라우저의 여러 설정을 제어하기 위한 객체를 생성합니다.
- **prefs**: 다운로드 관련 설정을 담는 딕셔너리입니다.
  - `download.default_directory`: 파일이 저장될 기본 경로를 위에서 지정한 `DOWNLOAD_DIR`로 설정합니다.
  - `download.prompt_for_download`: `False`로 설정하여 파일 다운로드 시 확인 창이 뜨지 않고 바로 다운로드되도록 합니다.
- **add_experimental_option()**: 위에서 정의한 `prefs` 설정을 Chrome 옵션에 추가합니다.
- **Service(ChromeDriverManager().install())**: `webdriver-manager`를 통해 현재 Chrome 버전에 맞는 드라이버를 자동으로 다운로드하고, 서비스 객체를 생성합니다.
- **webdriver.Chrome()**: 설정된 서비스와 옵션을 바탕으로 제어할 Chrome 브라우저 객체(`driver`)를 생성합니다.

### 4. 웹 자동화 (Selenium)

이 부분은 `try...finally` 구문으로 감싸서, 중간에 오류가 발생하더라도 `finally` 블록의 `driver.quit()`가 항상 실행되어 브라우저가 정상적으로 종료되도록 합니다.

```python
try:
    # 3.1. KOSIS 페이지 접속
    driver.get(URL)
    wait = WebDriverWait(driver, 10)

    # 3.2. 시점 조정 (2015년 ~ 최신)
    time_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='시점']")))
    time_menu.click()
    start_year_select = Select(wait.until(EC.presence_of_element_located((By.ID, "strt_period"))))
    start_year_select.select_by_value("2015")
    end_year_select = Select(driver.find_element(By.ID, "end_period"))
    latest_year = end_year_select.options[-1].get_attribute("value")
    end_year_select.select_by_value(latest_year)
    search_button = driver.find_element(By.CSS_SELECTOR, "a[onclick*='getStatisticData()']")
    search_button.click()

    # 3.3. 행렬 전환
    transpose_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_transpose")))
    transpose_button.click()

    # 3.4. CSV 파일 다운로드
    download_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.a-down#ico_download")))
    download_menu.click()
    csv_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='csv']")))
    csv_option.click()
    confirm_download_button = wait.until(EC.element_to_be_clickable((By.ID, "btnConfirm")))
    confirm_download_button.click()
    
    # 다운로드 완료 대기 로직...
finally:
    driver.quit()
```
- **driver.get(URL)**: 지정된 KOSIS URL로 접속합니다.
- **WebDriverWait(driver, 10)**: 웹 페이지의 특정 요소가 로드될 때까지 최대 10초간 기다리는 `wait` 객체를 생성합니다. 이는 페이지 로딩 속도에 따른 오류를 방지합니다.
- **wait.until(...)**: 특정 조건이 만족될 때까지 기다립니다. `EC.element_to_be_clickable`은 해당 요소가 화면에 보이고 클릭 가능할 때까지 기다리는 조건입니다.
- **'시점' 메뉴 클릭**: CSS 선택자를 이용해 '시점' 설정 메뉴를 찾아 클릭합니다.
- **Select(...)**: 드롭다운 메뉴(`<select>`)를 제어하기 위한 객체를 생성합니다.
- **select_by_value("2015")**: 시작 년도 드롭다운에서 값이 "2015"인 항목을 선택합니다.
- **end_year_select.options[-1]**: 종료 년도 드롭다운의 모든 옵션 중 마지막 옵션(가장 최신 연도)을 가져옵니다.
- **'조회' 버튼 클릭**: 설정된 기간으로 데이터를 조회하기 위해 '조회' 버튼을 클릭합니다.
- **행렬 전환**: '행렬전환' 버튼을 찾아 클릭하여 년도가 행으로 오도록 테이블 구조를 변경합니다.
- **CSV 다운로드**: '다운로드' 아이콘 클릭 → 'CSV' 형식 선택 → '확인' 버튼 클릭의 순서로 파일 다운로드를 진행합니다.
- **다운로드 대기**: `glob`을 이용해 다운로드 폴더에 임시 파일(`.crdownload`)이 사라질 때까지 대기하여 파일 다운로드가 완전히 끝났는지 확인합니다.
- **driver.quit()**: 모든 자동화 작업이 끝나면 웹 드라이버와 브라우저 창을 종료하여 시스템 자원을 해제합니다.

### 5. 다운로드 파일 처리 및 데이터프레임 생성

```python
list_of_files = glob.glob(os.path.join(DOWNLOAD_DIR, '*.csv'))
latest_file = max(list_of_files, key=os.path.getctime)
df = pd.read_csv(latest_file, encoding='cp949', header=1)
```
- **glob.glob(...)**: 다운로드 폴더 내의 모든 `.csv` 파일 목록을 가져옵니다.
- **max(..., key=os.path.getctime)**: 파일 목록 중에서 생성 시간(`ctime`)이 가장 최신인 파일(방금 다운로드한 파일)의 경로를 찾습니다.
- **pd.read_csv(...)**: 찾은 CSV 파일을 Pandas DataFrame으로 읽어옵니다.
  - `encoding='cp949'`: KOSIS에서 제공하는 한글 CSV 파일은 주로 'cp949' 인코딩을 사용하므로, 한글이 깨지지 않도록 지정합니다.
  - `header=1`: KOSIS CSV 파일은 보통 첫 번째 행이 통계표 제목이고 두 번째 행(인덱스 1)이 실제 컬럼명이므로, `header=1`로 지정하여 두 번째 행을 헤더로 사용합니다.

### 6. 데이터 전처리

```python
df.rename(columns={df.columns[0]: '시점'}, inplace=True)
df = df[['시점', '성별', '연령별', '일반가구원']]
df['일반가구원'] = pd.to_numeric(df['일반가구원'])
df_filtered = df[(df['성별'] != '계') & (df['연령별'] != '계')].copy()
```
- **df.rename(...)**: 행렬 전환 시 첫 번째 컬럼 이름이 '성별, 연령별' 등으로 되어 있을 수 있어, 명확하게 '시점'으로 변경합니다.
- **df[[...]]**: 전체 컬럼 중 분석에 필요한 '시점', '성별', '연령별', '일반가구원' 컬럼만 선택하여 새로운 DataFrame을 만듭니다.
- **pd.to_numeric(...)**: '일반가구원' 컬럼의 값들이 문자열(예: "1,234")이 아닌 실제 숫자로 계산될 수 있도록 숫자형으로 변환합니다.
- **df[...]**: '성별'과 '연령별' 컬럼에서 합계에 해당하는 '계' 행들을 제외하여 순수한 데이터만 남깁니다.

### 7. 통계 데이터 출력

```python
# 연도별, 성별 일반가구원 통계
gender_stats = df_filtered.groupby(['시점', '성별'])['일반가구원'].sum().unstack()
print(gender_stats)

# 연도별, 연령별 일반가구원 통계
age_stats = df_filtered.groupby(['시점', '연령별'])['일반가구원'].sum().unstack()
print(age_stats)
```
- **groupby()**: 데이터를 특정 기준으로 그룹화합니다.
- **unstack()**: 그룹화된 결과를 피벗(pivot)하여 보기 좋은 테이블 형태로 만듭니다. 예를 들어, `gender_stats`는 행이 '시점', 열이 '성별'인 테이블이 됩니다.
- **print()**: 최종적으로 정리된 두 종류의 통계표를 콘솔에 출력합니다.

### 8. 데이터 시각화 (Matplotlib)

```python
# 8.1. 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
# ... (macOS, Linux 설정)

# 8.2. 시각화를 위한 데이터 준비
latest_year_data = df_filtered[df_filtered['시점'] == df_filtered['시점'].max()]
pivot_data = latest_year_data.pivot(index='연령별', columns='성별', values='일반가구원')

# 8.3. 꺾은선 그래프 그리기
plt.figure(figsize=(14, 8))
plt.plot(pivot_data.index, pivot_data['남자'], marker='o', label='남자')
plt.plot(pivot_data.index, pivot_data['여자'], marker='s', label='여자')

# 8.4. 그래프 서식 설정
plt.title(...)
plt.xlabel(...)
plt.ylabel(...)
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()

# 8.5. 그래프 출력
plt.show()
```
- **한글 폰트 설정**: `platform.system()`으로 운영체제를 확인하고, 각 운영체제에 맞는 한글 폰트를 설정하여 그래프의 한글이 깨지는 현상을 방지합니다.
- **데이터 준비**: 시각화를 위해 가장 최신 연도의 데이터만 필터링합니다. 그 후 `pivot()` 함수를 사용해 그래프를 그리기 쉬운 형태(index: 연령별, columns: 성별, values: 일반가구원)로 데이터를 재구성합니다.
- **plt.figure()**: 그래프가 그려질 도화지(figure)의 크기를 설정합니다.
- **plt.plot()**: 꺾은선 그래프를 그립니다. x축은 `pivot_data`의 인덱스('연령별'), y축은 '남자'와 '여자'의 '일반가구원' 수입니다.
- **그래프 서식 설정**: `title`, `xlabel`, `ylabel`로 제목과 축 라벨을 추가하고, `legend`로 범례를 표시하는 등 그래프를 더 이해하기 쉽게 꾸밉니다.
- **plt.show()**: 완성된 그래프를 화면에 보여줍니다.
````