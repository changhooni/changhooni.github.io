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