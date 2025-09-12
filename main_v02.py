import os                           # os 모듈은 운영체제와 상호 작용할 수 있는 기능 제공
import json                         # python 객체(딕셔너리, 리스트등)를 JSON 파일로 저장, 파일읽기에 사용
from datetime import datetime       # datetime 클래스는 날짜와 시간 관련 작업처리 여기서는 문자열을 날짜형식으로 변경하는데 사용
'''
- 이 코드는 mission_computer_main.log 파일을 읽고:
- 각 줄에서 타임스탬프와 메시지를 분리한 후,
- 유효한 날짜 형식만 골라내고,
- 시간 기준으로 역순 정렬한 뒤,
- 그 결과를 JSON 파일(mission_computer_main.json)로 저장하는 프로그램입니다.

1. 파일 확장자 검사
2. 파일 용량 제한(10MB 이하)
3. 예외처리 
    - 파일 존재여부
    - 파일 인코딩, 디코딩 확인
    - 그외 예외처리

json 모듈 사용
json.dump(data, file, ensure_ascii=False, indent=4)  # 데이터를 JSON으로 파일에 저장
 - ensure_ascii=False: 한글 깨짐 방지
 - indent=4: 예쁘게 들여쓰기
'''

LOG_FILE = 'mission_computer_main.log'
OUTPUT_JSON_FILE = 'mission_computer_main.json'
MAX_MB = 10

def Hello() -> str:
    return "Hello Mars"

def read_and_process_log(file_path):
    log_list = []

    try:
        # 확장자 체크
        if not file_path.endswith('.log'): 
            return "❌ 지원하지 않는 파일 확장자입니다."
        #endswith()은 끝나는 문자열을 검사
        #startswith()는 시작하는 문자열을 검사

        # 파일 용량 체크
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > MAX_MB:
            return "❌ 파일 용량이 너무 큽니다."
        # 파일 크기를 바이트 → MB로 변환하여 MAX_MB보다 크면 에러 반환

        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines() 
        # readlines 모든 줄을 리스트로 가져옵니다
        # read() 전체 내용을 문자열 하나로 변환
        # 아래 내용을 기반으로 간단한 파일이기 때문에 readlines를 사용
        '''
        # readlines() 예
        with open("log.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                print(line.strip())
        모든 줄을 메모리에 올린 후 처리
        간단하지만 메모리를 많이 차리할 수 있어, 작은 파일에 적함

        # for line in f 예
        with open("log.txt", "r") as f:
            for line in f:
                print(line.strip())
        한 줄씩 읽으며 처리
        대용량 파일에는 for line in file 방식이 가장 효율적
        '''

        print("\n📄 [전체 로그 파일 내용 출력]") # 디버깅 용도 출력
        for line in lines:
            print(line.strip()) 
        # strip() 불필요한 공백이나 특정 문자를 제거할 때 사용
        # lstrip() 문자열에 왼쪽에 있는 불필요한 공백이나 특정 문자 제거
        # rstrip() 문자열에 오른쪽에 있는 불필요한 공백이나 특정 문자 제거
        '''
        기본 공백 제거에 매우 유용
        파일 줄 처리할 때 필수
        특정 문자 제거 시는 괄호 안에 제거할 문자 입력
        중간 문자 제거는 안됨
        중간 문자 제거하기 위해서는 "replace()" 변환함수를 사용하여 처리
        '''

        # 날짜와 메시지 분리
        for i, line in enumerate(lines, start=1):
            '''
            enumerate()는 반복 가능한 객체(iterable)를 받아서,
            각 요소에 대해 (인덱스, 요소) 쌍을 반환하는 
            **열거 객체(iterator)**를 생성합니다.
            start 인덱스 시작 값

            enumerate()를 사용하지 않고 사용하는 방법은 아래와 같은 형식으로 처리 
            for i in range(len(lines)):
                print(i, lines[i])

            그러나 enumarate()를 사용하면 휠씬 직관적이고 안전함.
            '''
            line = line.strip()
            if not line:
                print(f"[line {i}] 빈 줄 건너뜀")
                continue
            if ',' not in line:
                print(f"[line {i}] 쉼표 없음 → 무시됨: {line}")
                continue
            parts = line.split(',', 1)
            '''
            line.split(',', 1)는 ,를 기준으로 
            2조각(1로 지정된 부분에 숫자에 따라 나누는 수가 정해짐)으로 
            나누는 형식이다
            
            예시로 line.split(',', 2) 지정을 하면 ,를 기준으로 3조각으로 나누며
            관련 변수 지정는 
            변수1 = 변수[0]
            변수2 = 변수[1]
            변수3 = 변수[2]
            으로 처리
            만약 변수2와 변수3을 하나에 변수로 처리를 할려면 
            ','.join(변수[1:]).strip() 으로 join를 사용해야 함
            아래와 위에 내용를 기준으로 처리 방법
            parts = line.split(',', 2)
            timestamp = parts[0].strip()
            message = ','.join(parts[1:]).strip()
            으로 처리

            기본 로그 처리라면 split(',', 1)이 더 안전하고 직관적합니다.
            메시지 내용까지 세분화할 경우에만 split(',', 2)처럼 더 나눠서 쓰되, 
            나머지를 합치는 로직이 반드시 필요합니다.
            실전 로그 분석에서는 
            단순성 + 안전성 때문에 대부분 split(',', 1)을 사용합니다.
            '''
            timestamp = parts[0].strip()
            message = parts[1].strip()

            try:
                datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                '''
                strptime() = string parse time
                문자열을 datetime 형식으로 변환
                형식이 맞아야만 변환됨. 틀리면 ValueError 예외 발생
                '''
            except ValueError:
                continue  # 날짜 형식이 맞지 않으면 건너뜀
            
            log_list.append([timestamp, message])

        print("\n📄 [리스트 객체 출력]")
        for item in log_list:
            print(item)

        # 시간 역순 정렬
        try:
            sorted_list = sorted(
                log_list,
                key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S"),
                reverse=True
            )
            '''
            reverse=True
            기본 정렬은 오름차순 (과거 → 미래)
            reverse=True를 주면 내림차순 (미래 → 과거)
            즉, 가장 최근 로그가 가장 먼저 나옴

            lambda 정의
            익명 함수(함수 이름 없이 정의)
            단순하고 한 번만 쓰일 함수라면 lambda로 인라인(한 줄로) 간단하게
            작성하는 것이 휠씬 깔끔합니다
            lambda 매개변수: 리턴값 형태

            lambda를 사용하지 않고 처리 방법
            def get_datetime(log_entry):
                return datetime.strptime(log_entry[0], "%Y-%m-%d %H:%M:%S")
            sorted_list = sorted(log_list, key=get_datetime, reverse=True)
            위 형식으로 처리도 가능 

            lambda는 작고 일회성인 함수를 짧게 작성할 때 매우 유용
            정렬할 때 key=lambda ...는 거의 표준처럼 쓰이는 패턴
            datetime.strptime(...)은 문자열 → 날짜로 바꿔서 정확한 
            시간 비교를 가능하게 함
            reverse=True로 최신 로그가 먼저 오도록 정렬
            '''
        except ValueError as ve:
            return f"❌ 시간 파싱 오류: {ve}"

        print("\n📄 [시간 역순 정렬된 리스트 출력]")
        for item in sorted_list:
            print(item)

        # 리스트 → 딕셔너리 변환
        log_dict = {timestamp: message for timestamp, message in sorted_list}
        # log_dict = {timestamp: message for timestamp, message in sorted_list if "에러" in message}
        # 메세지에 "에러"가 포함된 딕셔너리에 추가

        print(f"\n✅ [딕셔너리 데이터 출력]")
        return log_dict
    
        '''
        딕셔너리 변환에 다른 방법
        
        단순한 딕셔너리(dict함수 사용)
        log_dict = dict(sorted_list)
        sorted_list는 이미 [key, value] 구조의 리스트이므로,
        dict() 생성자에 바로 넘겨서 딕셔너리로 변환할 수 있음
        단, 내부 리스트가 정확히 2개의 요소를 갖고 있어야 함 ([key, value])

        for문을 활용
        log_dict = {}
        for item in sorted_list:
            timestamp = item[0]
            message = item[1]
            log_dict[timestamp] = message

        for문을 활용한 더 간결한 방법(위와 같음)
        log_dict = {}
        for timestamp, message in sorted_list:
            log_dict[timestamp] = message

        map() + dict() 사용
        log_dict = dict(map(lambda x: (x[0], x[1]), sorted_list))
        map()으로 (key, value) 튜플을 만들고
        dict()로 변환
        복잡도만 늘어나므로, 실무에서는 비추천(컴프리헨션이나 dict()가 더 좋음)

        zip() 방식 (별도의 리스트 두 개가 있을 때)
        timestamps = [x[0] for x in sorted_list]
        messages = [x[1] for x in sorted_list]
        위와 같은 방식으로 처리가 되어 있으면 
        log_dict = dict(zip(timestamps, messages))로 사용
        데이터가 각각 리스트로 분리되어 있을 경우
        예: csv열을 리스트로 따로 나눠서 다룰 때

        dict.fromkeys() 사용
        모든 키에 동일한 값을 줄 때 사용
        그러나 데이터에는 key마다 value값이 다르면 사용하지 않는다

        '''
        # 딕셔너리 → JSON 파일 저장
        with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as json_file:
            json.dump(log_dict, json_file, ensure_ascii=False, indent=4)

        print(f"\n✅ JSON 파일 저장 완료: {OUTPUT_JSON_FILE}")
        return log_dict

    except FileNotFoundError:
        return "❌ 오류: 파일이 존재하지 않습니다."
    except UnicodeDecodeError:
        return "❌ 오류: 디코딩 실패 (UTF-8 인코딩 확인)"
    except UnicodeEncodeError:
        return "❌ 오류: 인코딩 실패 (UTF-8 저장 중 오류 발생)"
    except Exception as e:
        return f"❌ 알 수 없는 오류 발생: {e}"

if __name__ == "__main__":
    print(Hello())
    result = read_and_process_log(LOG_FILE)

    print("\n📦 [최종 결과]")
    print(result)
