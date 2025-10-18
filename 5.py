'''
아래 변수 사용
CIPHER_TEXT = 'wkh txlfn eurzg ira nxpsv ryhu wkh odcb grj'

def caesar_cipher_decode(target_text: str) -> list[str]:
위 함수 사용

타입 에러
Invalid input.

그외 에러
Processing error.


if __name__ == "__main__":
    main()
메인에서 처리
'''

CIPHER_TEXT = 'wkh txlfn eurzg ira nxpsv ryhu wkh odcb grj'

def caesar_cipher_decode(target_text: str) -> list[str]:
    if not isinstance(target_text, str):
        raise ValueError
    if target_text == '':
        raise ValueError
    
    results:list[str] = []
    for i in range(26):
        decode = []
        for ch in target_text:
            if 'a' <= ch <= 'z':
                code = ord(ch) - i
                if code < ord('a'):
                    code += 26
                decode.append(chr(code))
            else:
                decode.append(ch)
        results.append(''.join(decode))
    return results

def main():
    try:
        decode_password = caesar_cipher_decode(CIPHER_TEXT)
        for m, password in enumerate(decode_password):
            print(f"{m}: {password}")

        t = input()
        if not isinstance(t, str):
            raise ValueError
        
        s = t.strip()
        if s == '':
            raise ValueError
        if not s.isdigit():
            raise ValueError
        
        idx = int(s)
        if not 0 <= idx <= 25:
            raise ValueError
        
        print(f"Result: {decode_password[idx]}")
    except ValueError:
        print("Invalid input.")
    except Exception:
        print("Processing error.")

if __name__ == "__main__":
    main()