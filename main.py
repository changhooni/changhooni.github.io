import os
import pandas as pd

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

    except FileNotFoundError:
        text = "파일이 존재하지 않습니다."
    except UnicodeDecodeError:
        text = "디코딩 실패 인코딩을 확인하세요"
    except UnicodeEncodeError:
        text = "인코딩 실패 디코딩을 확인하세요"
    

    return text

if __name__ == "__main__":
    #msg = Hello()
    #print(msg)

    txt = file_read("mission_computer_main.log")

    print(txt)
