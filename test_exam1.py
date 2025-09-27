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
 - git reset --soft HEAD^
 체크아웃된 로컬 브랜치의 upstream을 origin/new-feature으로 설정
 - git branch -u origin/new-feature
변경사항을 로컬로 가져오되 현재 브랜치에는 병합하기 않음
 - git fetch

 ㄴ3번 시험
 오류 print에 문제에서 오류 처리 문구 넣어서 처리
'''

from datetime import datetime

def read_log(path: str = "mission_computer_main.log")->str:
    try :
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("파일이 존재하지 않습니다.")
    except UnicodeDecodeError:
        print("인코딩 에러")
    except Exception as e:
        print(f"{e}")
    return ""

def main():
    result = read_log()
    log_list = []
    try:
        # log파일에 첫번재 줄에 대한 확인 부분
        if not result.startswith("timestamp,event,message"):
            raise RuntimeError
        # log파일에 첫번재 줄에 대한 확인 부분

        # return 값으로 넘어온 데이터 가공을 위한 for문 시작
        # result.splitlines()[1:] 헤드가 아닌 부분부터 데이터 확인
        for i, logs in enumerate(result.splitlines()[1:] , start=1):
            # 데이터값이 빈값이면 무시
            if not logs:
                continue
            # parts 변수에 3조각(.split(',', 2) ',' 표시를 
            # 기준으로 지정된 부분에 숫자에 따라 나누는 수가 정해짐)
            parts = logs.strip().split(',', 2)

            try: 
                # parts 데이터가 3조각여부 확인
                if len(parts) == 3:
                    # parts[0] 첫번째 값에 데이터 타입 확인 조건문
                    if datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S'):
                        try:
                            # 오류가 존재하지 않으면 log_list 배열에 조건에 맞는 값을 넣음
                            log_list.append((parts[0], parts[2]))
                        except RuntimeError:
                            raise RuntimeError
                    else:
                        raise ValueError
                else:
                    raise RuntimeError
            except Exception as e:
                print(f"error: {e}")

        print(log_list)
        try:
            # log_list 값을 데이터 역순으로 재정렬
            sorted_list = sorted(
                log_list,
                key=lambda x: x[0],
                reverse=True # True 역순으로 처리 , False 처리된 데이터로 정렬
            )

            print(sorted_list)
            dict_list = dict(sorted_list) # 사전 작업 위한 dict 내장 함수 사용
            print(dict_list)
        except RuntimeError:
            raise RuntimeError
    except (TypeError, ValueError):
        print('ddd')
    except RuntimeError:
        print('ddd')
    except Exception:
        print("ddd")

if __name__ == "__main__":
    main()