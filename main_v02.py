import os
import json
from datetime import datetime

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

        # 파일 용량 체크
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > MAX_MB:
            return "❌ 파일 용량이 너무 큽니다."

        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        print("\n📄 [전체 로그 파일 내용 출력]")
        for line in lines:
            print(line.strip())

        # 날짜와 메시지 분리
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if ',' not in line:
                continue
            parts = line.split(',', 1)
            timestamp = parts[0].strip()
            message = parts[1].strip()
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
        except ValueError as ve:
            return f"❌ 시간 파싱 오류: {ve}"

        print("\n📄 [시간 역순 정렬된 리스트 출력]")
        for item in sorted_list:
            print(item)

        # 리스트 → 딕셔너리 변환
        log_dict = {timestamp: message for timestamp, message in sorted_list}

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
