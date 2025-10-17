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
print("File Error")

unicode에러
print("Decoding Error")

타입에러
print('Invalid log format.')

그외 에러
print('processing error.')

if __name__ == "__main__":
    main()
메인에서 처리 
'''
