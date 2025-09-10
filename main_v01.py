import os
import json
from datetime import datetime

LOG_FILE = 'mission_computer_main.log'
OUTPUT_JSON_FILE = 'mission_computer_main.json'

def read_log_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        print(f"✅ '{filename}' 파일을 성공적으로 읽었습니다.")
        return lines
    except FileNotFoundError:
        print(f"❌ 오류: '{filename}' 파일이 존재하지 않습니다.")
    except UnicodeDecodeError:
        print(f"❌ 오류: 파일 디코딩 중 문제가 발생했습니다 (UTF-8 인코딩 문제).")
    except Exception as e:
        print(f"❌ 알 수 없는 오류 발생: {e}")
    return []

def parse_log_lines(lines):
    parsed_list = []
    for line in lines:
        if ',' in line:
            parts = line.strip().split(',', 1)
            timestamp = parts[0].strip()
            message = parts[1].strip()
            parsed_list.append([timestamp, message])
    return parsed_list

def sort_logs_by_time(log_list):
    try:
        # 날짜/시간 형식이 ISO8601이라고 가정: "YYYY-MM-DD HH:MM:SS"
        sorted_list = sorted(
            log_list,
            key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S"),
            reverse=True
        )
        return sorted_list
    except Exception as e:
        print(f"❌ 정렬 중 오류 발생: {e}")
        return log_list

def convert_list_to_dict(log_list):
    log_dict = {}
    for timestamp, message in log_list:
        log_dict[timestamp] = message
    return log_dict

def save_dict_to_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ '{filename}' 파일로 저장 완료.")
    except Exception as e:
        print(f"❌ JSON 저장 중 오류 발생: {e}")

def main():
    lines = read_log_file(LOG_FILE)
    if not lines:
        return

    log_list = parse_log_lines(lines)
    print("\n📄 원본 리스트 출력:")
    for item in log_list:
        print(item)

    sorted_list = sort_logs_by_time(log_list)
    print("\n📄 시간 역순 정렬된 리스트 출력:")
    for item in sorted_list:
        print(item)

    log_dict = convert_list_to_dict(sorted_list)
    save_dict_to_json(log_dict, OUTPUT_JSON_FILE)

if __name__ == '__main__':
    main()
