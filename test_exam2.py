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
def sphere_area(diameter: float, material: str, thickness: float=1)->tuple[float, float]:
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
        raise ValueError
    
    if not isinstance(diameter, (int, float)) or diameter <= 0:
        raise ValueError

    if not isinstance(thickness, (int, float)) or thickness <= 0:
        raise ValueError
    
    # --- 계산 로직 ---
    # 1. 단위 통일: 계산의 일관성을 위해 모든 단위를 cm, g 기준으로 맞춥니다.
    # radius_cm = (diameter * 100) / 2
    
    # 2. 돔의 표면적(m²) 계산 (출력용)
    #area_m2 = 2 * math.pi * ((diameter / 2) ** 2)
    try: 
        area_m2 = math.pi * (diameter)

        # 3. 돔의 부피(cm³) 계산 (무게 계산용)
        area_cm2 = area_m2 * 10000
        volume_cm3 = area_cm2 * thickness
        #area_cm2 = 2 * math.pi * (radius_cm ** 2)
        #volume_cm3 = area_cm2 * thickness
        
        # 4. 돔의 질량(kg) 계산
        density = DENSITY_MAP[material]
        mass_kg = density * volume_cm3 / 1000
        #mass_g = volume_cm3 * density
        #mass_kg = mass_g / 1000

        # 5. 화성에서의 무게 계산
        #weight_on_mars = mass_kg * MARS_GRAVITY_RATIO
        mass_weight_kg = mass_kg * 0.38
    except Exception:
        Exception

    return area_m2, mass_weight_kg
# --- 메인 프로그램 실행 부분 ---
def main():
    """메인 프로그램을 실행하는 함수입니다. 프로그램은 한 번만 실행됩니다."""
    global dome_material, dome_diameter, dome_thickness, dome_area, dome_weight

    print("--- Mars 돔 구조물 설계 프로그램 ---")
    
    # 사용자로부터 재질, 지름, 두께를 순서대로 입력받습니다.
    material_input = input("재질을 입력하세요 (유리, 알루미늄, 탄소강): ")
    diameter_input = input("돔의 지름(m)을 입력하세요: ")
    thickness_input = input("돔의 두께(cm)를 입력하세요 (기본값: 1, Enter 입력 시): ")
    
    # --- try-except 문을 사용한 예외 처리 ---
    try:
        # 1. 입력값들을 숫자로 변환
        diameter_m = float(diameter_input)
        
        if thickness_input == "":
            thickness_cm = 1.0  # 입력이 없으면 기본값 1.0 사용
        else:
            thickness_cm = float(thickness_input)

        # 2. 핵심 계산 함수 호출
        #    잘못된 재질, 지름, 두께가 입력되면 이 함수가 ValueError를 발생시키고,
        #    아래 except 블록에서 처리됩니다.
        area, w = sphere_area(diameter_m, material_input, thickness_cm)

        # 3. 계산 결과를 전역 변수에 저장
        dome_material = material_input
        dome_diameter = diameter_m
        dome_thickness = thickness_cm
        dome_area = area
        dome_weight = w
        
        # 4. 결과 출력
        print("\n[계산 결과]")
        print(f"재질 : {dome_material}, 지름 : {dome_diameter}, 두께 : {dome_thickness}, "
              f"면적 : {dome_area:.3f}, 무게 : {dome_weight:.3f} kg")

    except ValueError as e:
        # 잘못된 입력에 대한 모든 오류를 여기서 처리합니다.
        print("Invalid input")

    except Exception as e:
        print("Processing error")

# 이 스크립트가 메인으로 실행될 때만 main() 함수를 호출합니다.
if __name__ == "__main__":
    main()