'''
def read_log(path: str = "mission_computer_main.log")->str:
    try :
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    -- 에외 처리 --

첫번째 리스트 timestamp,event,message 이 메뉴 확인
데이터 처리 %Y-%m-%d %H:%M:%S 이걸 사용
리스트 듀플처리 spplit(',', 2) 사용

메뉴 갯수가 3개인지 확인

print로 리스트 4개 처리
일반 리스트
듀플 리스트
정렬 리스트
사전 리스트

파일에러 
File Error.

unicode에러
Decoding Error.

타입에러
Invalid log format.

그외 에러
processing error.

if __name__ == "__main__":
    main()
메인에서 처리 
'''
from datetime import datetime
def read_log(path: str = "mission_computer_main.log")->str:
    try :
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("File Error.")
    except UnicodeDecodeError:
        print("Decoding Error")
    except Exception:
        print('Error')

def main():
    result = read_log()
    print(result)
    log_list = []

    try:
        if not result.startswith('timestamp,event,message'):
            raise ValueError
        
        for i, logs in enumerate(result.splitlines()[1:], start=1):
            if not logs:
                continue

            parts = logs.strip().split(',', 2)

            try:
                if len(parts) == 3:
                    if datetime.strptime(parts[0].strip(), '%Y-%m-%d %H:%M:%S'):
                        try:
                            log_list.append((parts[0], parts[2]))
                        except RuntimeError:
                            raise RuntimeError
                else:
                    raise ValueError
            except RuntimeError:
                raise RuntimeError
        print(log_list)
        try:
            sorted_list = sorted(
                log_list,
                key=lambda x:x[0],
                reverse=True
            )
            print(sorted_list)
            dict_list = dict(sorted_list)
            print(dict_list)
        except RuntimeError:
            raise RuntimeError
    except ValueError:
        print("Invalid log format.")
    except RuntimeError:
        print("Processing error")
    except Exception:
        print("Error")
        
if __name__ == "__main__":
    main()