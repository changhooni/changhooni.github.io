# design_dome.py

# Step 5: 수학 계산을 위한 math 모듈 가져오기
import math

# --- 전역 변수 선언 ---
# 문제의 요구사항에 따라 계산 결과를 저장할 전역 변수를 미리 선언합니다.
# 초기값은 None으로 설정하여 아직 계산된 값이 없음을 나타냅니다.
dome_material = None
dome_diameter = None
dome_thickness = None
dome_area = None
dome_weight = None

# --- 재질별 밀도 데이터 ---
# Step 5: 딕셔너리를 사용하여 재질과 밀도를 관리하면 if-elif-else 보다 코드가 깔끔해집니다.
# 사용자가 한글로 입력할 것이므로, 키(key)를 한글로 설정합니다.
DENSITY_MAP = {
    "유리": 2.4,        # 단위: g/cm³
    "알루미늄": 2.7,
    "탄소강": 7.85
}

# --- 핵심 계산 함수 정의 ---
# Step 3: 반구의 표면적과 무게를 계산하는 함수
def sphere_area(diameter, material, thickness=1):
    """
    반구체 돔의 표면적과 화성에서의 무게를 계산하는 함수입니다.

    Args:
        diameter (float): 돔의 지름 (m 단위)
        material (str): 돔의 재질 ('유리', '알루미늄', '탄소강')
        thickness (float, optional): 돔의 두께 (cm 단위). 기본값은 1cm.

    Returns:
        tuple: (표면적(m²), 화성에서의 무게(kg)) 튜플을 반환.
               계산에 실패하면 (None, None)을 반환.
    """
    
    # --- 보너스 과제: 유효성 검사 (함수 내부에서 예외 처리) ---
    if material not in DENSITY_MAP:
        # 지원하지 않는 재질이 입력되면 ValueError 발생
        raise ValueError(f"지원하지 않는 재질입니다. {list(DENSITY_MAP.keys())} 중에서 선택해주세요.")
    
    if not isinstance(diameter, (int, float)) or diameter <= 0:
        # 지름이 숫자가 아니거나 0 이하일 경우 ValueError 발생
        raise ValueError("지름은 0보다 큰 숫자여야 합니다.")

    if not isinstance(thickness, (int, float)) or thickness <= 0:
        # 두께가 숫자가 아니거나 0 이하일 경우 ValueError 발생
        raise ValueError("두께는 0보다 큰 숫자여야 합니다.")

    # --- 계산 로직 ---
    # Step 5: 단위 통일 및 계산 (매우 중요한 부분)
    # 1. 지름(m)을 반지름(cm)으로 변환
    radius_cm = (diameter * 100) / 2
    
    # 2. 돔의 표면적 계산 (단위: m²) - 출력용
    #    반구의 표면적 공식: 2 * pi * r^2
    area_m2 = 2 * math.pi * ((diameter / 2) ** 2)

    # 3. 돔의 부피 계산 (단위: cm³) - 무게 계산용
    #    표면적(cm²) * 두께(cm)
    area_cm2 = 2 * math.pi * (radius_cm ** 2)
    volume_cm3 = area_cm2 * thickness
    
    # 4. 돔의 질량 계산 (단위: kg)
    #    부피(cm³) * 밀도(g/cm³) = 질량(g)
    density = DENSITY_MAP[material]
    mass_g = volume_cm3 * density
    mass_kg = mass_g / 1000  # g을 kg으로 변환

    # 5. 화성에서의 무게 계산 (단위: kg)
    #    지구에서의 질량(kg) * 화성 중력 비율(0.38)
    #    (엄밀히는 무게 단위는 N이지만, 문제에서는 kg으로 출력하라고 했으므로 질량에 중력 상수를 곱한 값을 사용)
    weight_on_mars = mass_kg * 0.38
    
    return area_m2, weight_on_mars


# --- 메인 프로그램 실행 부분 ---
# Step 2: 프로그램이 계속 반복 실행되도록 while 무한 루프 사용
while True:
    print("\n--- Mars 돔 구조물 설계 프로그램 ---")
    
    # Step 1: 사용자로부터 재질 입력받기 (한글 입력 처리)
    # '종료'를 입력하면 프로그램이 중단되도록 종료 조건 구현
    material_input = input("재질을 입력하세요 (유리, 알루미늄, 탄소강) / 종료하려면 '종료' 입력: ")
    if material_input == "종료":
        print("프로그램을 종료합니다.")
        break # Step 2: break를 통해 while 루프 탈출

    # Step 1: 사용자로부터 지름 입력받기
    diameter_input = input("돔의 지름(m)을 입력하세요: ")

    # Step 4: 예외 처리 (잘못된 입력에 대한 방어)
    try:
        # Step 1: 입력받은 문자열을 실수(float)로 형 변환
        diameter_m = float(diameter_input)
        
        # 함수 호출하여 계산 실행
        # thickness는 기본값 1cm를 사용
        calculated_area, calculated_weight = sphere_area(diameter_m, material_input)

        # 계산 결과가 유효할 경우 (함수에서 None을 반환하지 않았을 경우)
        if calculated_area is not None:
            # --- 전역 변수에 결과 저장 ---
            # global 키워드를 사용하여 함수 바깥의 전역 변수 값을 수정
            dome_material = material_input
            dome_diameter = diameter_m
            dome_thickness = 1  # 이 문제에서는 기본값 1을 사용
            dome_area = calculated_area
            dome_weight = calculated_weight
            
            # --- 결과 출력 ---
            # Step 5: f-string과 소수점 포매팅을 사용하여 요구된 형식으로 출력
            print("\n[계산 결과]")
            print(f"재질 ⇒ {dome_material}, 지름 ⇒ {dome_diameter}, 두께 ⇒ {dome_thickness}, "
                  f"면적 ⇒ {dome_area:.3f}, 무게 ⇒ {dome_weight:.3f} kg")

    # 함수 내에서 발생시킨 ValueError나, float 변환 실패 시 발생하는 ValueError를 모두 처리
    except ValueError as e:
        print(f"[오류] 입력값이 잘못되었습니다: {e}")
    # 그 외 예측하지 못한 다른 모든 오류 처리
    except Exception as e:
        print(f"[알 수 없는 오류] 오류가 발생했습니다: {e}")
