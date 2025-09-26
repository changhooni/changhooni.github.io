import os
import json
from datetime import datetime
'''
시험 1번 문제 정답 
새로운 브랜치 생성하고 해당 브랜치로 전환
 - git checkout -b new
새로운 커밋을 생성하지 않고 기존 커밋을 완전히 대체, 커밋 메세지나 파일 내용 변경
 - git commit --amend
병합 시 충동지점 작업 취소하고 병합 시작 전 상태로 처리
git merge --abort

시험 2번 문제 정답
커밋을 되돌리고 변경사항을 스태이징 상태로 유지 
 - git reset --sort HEAD^
변경사항을 로컬로 가져오되 현재 브랜치에는 병합하기 않음
 - git fetch
체크아웃된 로컬 브랜치의 upstream을 origin/new-feature으로 설정
 - git branch -u origin/new-feature
'''
#LOG_FILE = 'mission_computer_main.log'
MAX_MB= 10

def main():
    result = read_log()
    print(result)

def read_log(path: str = "mission_computer_main.log")->str:
#def read_log(path_file):
    log_list = []
    try :
        if not path.endswith(".log"):
            return "파일 확장가 다릅니다."
        
        size_mb = os.path.getsize(path) / (1024 *1024)

        if size_mb > MAX_MB:
            return "10메가를 넘어씁니다"
        
        with open(path, 'r', encoding='utf8') as f:
            lines = f.readlines()
        print('로그 리스트')
        for line in lines:
            print(line.strip())
        
        for i, line in enumerate(lines, start=1):
            line = line.strip()

            if not line:
                continue
            if ',' not in line:
                continue
            parts =line.split(',', 2)
            timestamp = parts[0].strip()
            message = parts[2].strip()

            try:
                datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print('타입 오류')
                continue
            log_list.append((timestamp, message))
        print('로그 리스트 timestamp, message')
        print(log_list)

        try:
            sorted_list = sorted(
                log_list,
                key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'),
                reverse=True
            )
        except ValueError as ve:
            print(f"{ve}")
        print('역순 정렬 리스트')
        print(sorted_list)
        dict_result = dict(sorted_list)
        return dict_result

    except FileNotFoundError:
        print("파일이 존재하지 않습니다.")
    except UnicodeDecodeError:
        print("인코딩 에러")
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    main()
    
    #result = read_log(LOG_FILE)
    #print(result)