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
        if not result.startswith("timestamp,event,message"):
            raise RuntimeError
        
        for i, logs in enumerate(result.splitlines()[1:] , start=1):
            if not logs:
                continue

            parts = logs.strip().split(',', 2)
            try: 
                if len(parts) == 3:
                    if datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S'):
                        try:
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
            sorted_list = sorted(
                log_list,
                key=lambda x: x[0],
                reverse=True
            )

            print(sorted_list)
            dict_list = dict(sorted_list)
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