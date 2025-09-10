import os
import json
from datetime import datetime
import pandas as pd

OUTPUT_JSON_FILE = 'mission_computer_main.json'

def Hello()->str:
    a = "Hello Mars"

    return a

def file_read(e):
    MAX_MB = 10
    kk = []
    try:
        if not e.endswith(".log"): # endswith 확장자를 체크하는 함수
            text = "지원하지 않는 파일 확장자입니다."

        size_mb = os.path.getsize(e) / (1024 * 1024)

        if size_mb > MAX_MB:
            text = "파일 용량이 너무 큽니다."

        with open(e, "r", encoding="utf-8") as f:
            header = f.readline().strip().split(',')
            for line in f:
                tt = line.strip()
                if not tt:
                    continue

                values = tt.split(',')
                if len(values) == len(header):
                    kk.append(values)
                else:
                    text = "필드 수가 맞지 않음"

        text = pd.DataFrame(kk, columns=header)
        text["timestamp"] = pd.to_datetime(text["timestamp"], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        text = text.sort_values(by="timestamp").reset_index(drop=True)
        text = text.to_dict()
        # to_dict 사전으로 처리
        # to_dict(orient="-") 
        '''
        | 옵션 이름          | 설명                                                    | 예시 형태                                   |
        | --------------   | ----------------------------------------------------- | --------------------------------------- |
        | `'dict'` (기본값) | `{열 이름: {행 인덱스: 값}}`                               | `{ 'col1': {0: val1, 1: val2}, ... }`   |
        | `'list'`       | `{열 이름: [값, 값, ...]}`                                 | `{ 'col1': [val1, val2], ... }`         |
        | `'series'`     | `{열 이름: pandas.Series}`                                | `{ 'col1': pd.Series([...]), ... }`     |
        | `'records'`    | `[ {열: 값, 열: 값}, ... ]` (리스트 안에 행별 딕셔너리)        | `[ {'col1': val1, 'col2': val2}, ... ]` |
        | `'split'`      | `{ 'index': [...], 'columns': [...], 'data': [...] }`    | `딕셔너리 형태로 전체 구조 유지`                     |
        | `'tight'`      | `split`과 유사하나, 메타데이터까지 포함                        | 사용 잘 안 됨                                |
        '''
        # to_csv csv 파일 생성
        '''
        | 옵션                     | 설명                           |
        | ---------------------- | ---------------------------- |
        | `index=False`          | 행 번호(index)를 파일에 포함하지 않음     |
        | `encoding='utf-8-sig'` | 한글이 포함된 경우 윈도우에서도 깨지지 않도록 저장 |
        | `sep=','`              | 구분자 설정 (기본은 쉼표 `,`)          |
        | `columns=[...]`        | 저장할 열만 선택 가능                 |
        '''
        # to_csv()
        # to_json json 파일 생성
        '''
        | 옵션                  | 설명                                |
        | ------------------- | --------------------------------- |
        | `orient='records'`  | 리스트 안에 딕셔너리 형식 (`[{...}, {...}]`) |
        | `force_ascii=False` | 한글 깨짐 방지                          |
        | `indent=4`          | 보기 좋은 들여쓰기 적용                     |

        '''
        #text.to_csv("mission_computer_main.json", orient-"records", force_ascii=False, indent=4)

    except FileNotFoundError:
        text = "파일이 존재하지 않습니다."
    except UnicodeDecodeError:
        text = "디코딩 실패 인코딩을 확인하세요"
    except UnicodeEncodeError:
        text = "인코딩 실패 디코딩을 확인하세요"
    

    return text

if __name__ == "__main__":
    msg = Hello()
    print(msg)

    txt = file_read("mission_computer_main.log")

    print(txt)
