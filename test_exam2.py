# design_dome.py

# Step 1: 수학 계산을 위한 math 모듈 가져오기
import math

# --- 전역 변수 선언 ---
# 계산 결과를 저장할 전역 변수들을 미리 선언하고 None으로 초기화합니다.
dome_material = None
dome_diameter = None
dome_thickness = None
dome_area = None
dome_weight = None

# --- 상수 정의 ---
# 재질과 밀도 데이터를 딕셔너리로 관리하여 유지보수를 용이하게 합니다.
DENSITY_MAP = {
    "유리": 2.4,        # 단위: g/cm³
    "알루미늄": 2.7,
    "탄소강": 7.85
}
# 화성 중력 비율 상수를 정의하여 코드의 가독성을 높입니다.
MARS_GRAVITY_RATIO = 0.38

# --- 핵심 계산 함수 정의 ---
def sphere_area(diameter, material, thickness=1):
    """
    반구체 돔의 표면적(m²)과 화성에서의 무게(kg)를 계산합니다.

    Args:
        diameter (float): 돔의 지름 (m 단위)
        material (str): 돔의 재질 ('유리', '알루미늄', '탄소강')
        thickness (float, optional): 돔의 두께 (cm 단위). 기본값은 1cm.

    Returns:
        tuple: (표면적, 화성에서의 무게) 튜플을 반환합니다.

    Raises:
        ValueError: 유효하지 않은 인자값이 들어올 경우, 명시적인 오류 메시지와 함께 예외를 발생시킵니다.
    """
    
    # --- 보너스 과제: 함수 내에서 인자값 유효성 검사 ---
    # 잘못된 값이 들어오면 계산을 시도하지 않고 즉시 ValueError를 발생(raise)시킵니다.
    if material not in DENSITY_MAP:
        raise ValueError(f"지원하지 않는 재질입니다. {list(DENSITY_MAP.keys())} 중에서 선택해주세요.")
    
    if not isinstance(diameter, (int, float)) or diameter <= 0:
        raise ValueError("지름은 0보다 큰 숫자여야 합니다.")

    if not isinstance(thickness, (int, float)) or thickness <= 0:
        raise ValueError("두께는 0보다 큰 숫자여야 합니다.")
    
    # --- 계산 로직 ---
    # 1. 단위 통일: 계산의 일관성을 위해 모든 단위를 cm, g 기준으로 맞춥니다.
    radius_cm = (diameter * 100) / 2
    
    # 2. 돔의 표면적(m²) 계산 (출력용)
    area_m2 = 2 * math.pi * ((diameter / 2) ** 2)

    # 3. 돔의 부피(cm³) 계산 (무게 계산용)
    area_cm2 = 2 * math.pi * (radius_cm ** 2)
    volume_cm3 = area_cm2 * thickness
    
    # 4. 돔의 질량(kg) 계산
    density = DENSITY_MAP[material]
    mass_g = volume_cm3 * density
    mass_kg = mass_g / 1000

    # 5. 화성에서의 무게 계산
    weight_on_mars = mass_kg * MARS_GRAVITY_RATIO
    
    return area_m2, weight_on_mars

# --- 메인 프로그램 실행 부분 ---
def main():
    """메인 프로그램을 실행하는 함수입니다."""
    # global 키워드를 사용하여 함수 내에서 전역 변수의 값을 수정할 수 있도록 합니다.
    global dome_material, dome_diameter, dome_thickness, dome_area, dome_weight

    # 프로그램 반복 실행을 위한 while 루프
    while True:
        print("\n--- Mars 돔 구조물 설계 프로그램 ---")
        
        # 사용자로부터 재질과 지름을 입력받습니다.
        material_input = input("재질을 입력하세요 (유리, 알루미늄, 탄소강) / 종료하려면 '종료' 입력: ")
        if material_input == "종료":
            print("프로그램을 종료합니다.")
            break
        
        if material_input not in DENSITY_MAP:
            raise ValueError(f"지원하지 않는 재질입니다. {list(DENSITY_MAP.keys())} 중에서 선택해주세요.")
            
        
        diameter_input = input("돔의 지름(m)을 입력하세요: ")
        
        # [수정] 두께 입력을 받고, 기본값에 대한 안내를 추가합니다.
        thickness_input = input("돔의 두께(cm)를 입력하세요 (기본값: 1, Enter 입력 시): ")
        # --- try-except 문을 사용한 예외 처리 ---
        # 오류 발생 가능성이 있는 코드 블록 전체를 try로 묶습니다.
        try:
            # 1. 입력값(문자열)을 숫자(float)로 변환 시도
            #    만약 사용자가 "abc" 같은 문자를 입력하면 여기서 ValueError가 발생합니다.
            diameter_m = float(diameter_input)
            
            # 2. [수정] 두께 처리: 입력이 없으면 기본값 1, 있으면 숫자로 변환
            if thickness_input == "":
                thickness_cm = 1.0  # 사용자가 Enter만 입력 시 기본값 1.0 사용
            else:
                thickness_cm = float(thickness_input) # 입력값이 있으면 숫자로 변환 시도

            # 3. 핵심 계산 함수 호출 시도
            #    변환된 숫자가 유효하지 않거나(예: 0 이하), 재질이 잘못된 경우
            #    sphere_area 함수 내부에서 raise한 ValueError가 여기서 발생합니다.
            calculated_area, calculated_weight = sphere_area(diameter_m, material_input)

            # --- 이 아래 코드는 try 블록의 모든 코드가 성공적으로 실행된 경우에만 도달합니다 ---
            
            # 4. 계산 결과를 전역 변수에 저장
            dome_material = material_input
            dome_diameter = diameter_m
            dome_thickness = thickness_cm  # 기본값 1cm 사용
            dome_area = calculated_area
            dome_weight = calculated_weight
            
            # 4. 요구된 형식에 맞춰 결과 출력
            print("\n[계산 결과]")
            print(f"재질 ⇒ {dome_material}, 지름 ⇒ {dome_diameter}, 두께 ⇒ {dome_thickness}, "
                  f"면적 ⇒ {dome_area:.3f}, 무게 ⇒ {dome_weight:.3f} kg")

        # --- 예외 처리 블록 ---
        # try 블록 안에서 ValueError가 발생하면, 프로그램이 멈추지 않고 이 블록이 실행됩니다.
        except ValueError as e:
            # e 변수에는 발생한 오류의 상세 메시지가 담겨 있습니다.
            # (예: "could not convert string to float: 'abc'", "지름은 0보다 큰 숫자여야 합니다.")
            print(f"[오류] 입력값이 잘못되었습니다: {e}")
            # 루프의 다음 반복으로 넘어갑니다.

        # ValueError 외에 혹시 모를 다른 모든 종류의 예외를 처리하기 위한 블록입니다.
        except Exception as e:
            print(f"[알 수 없는 오류] 오류가 발생했습니다: {e}")
            # 루프의 다음 반복으로 넘어갑니다.

# 이 스크립트가 메인으로 실행될 때만 main() 함수를 호출합니다.
if __name__ == "__main__":
    main()