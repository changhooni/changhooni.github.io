# design_dome.py

# Step 1: 수학 계산을 위한 math 모듈 가져오기
import math

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
def sphere_area(diameter: float, material: str, thickness: float=1) -> tuple[float, float]:
    '''
    반구체 돔의 표면적(m²)과 화성에서의 무게(kg)를 계산합니다.

    Args:
        diameter (float): 돔의 지름 (m 단위)
        material (str): 돔의 재질 ('유리', '알루미늄', '탄소강')
        thickness (float, optional): 돔의 두께 (cm 단위). 기본값은 1cm.

    Returns:
        tuple: (표면적, 화성에서의 무게) 튜플을 반환합니다.

    Raises:
        ValueError: 유효하지 않은 인자값이 들어올 경우, 명시적인 오류 메시지와 함께 예외를 발생시킵니다.
    '''
    
    # --- 보너스 과제: 함수 내에서 인자값 유효성 검사 ---
    # 잘못된 값이 들어오면 계산을 시도하지 않고 즉시 ValueError를 발생(raise)시킵니다.
    if material not in DENSITY_MAP:
        raise ValueError
    
    if diameter <= 0:
        raise ValueError

    if thickness <= 0:
        raise ValueError
    
    if thickness == '':
        thickness = 1.0  # 입력이 없으면 기본값 1.0 사용
    else:
        try:
            thickness = float(thickness)
        except ValueError:
            raise ValueError
    
    # --- 계산 로직 ---
    # 1. 단위 통일: 계산의 일관성을 위해 모든 단위를 cm, g 기준으로 맞춥니다.
    # radius_cm = (diameter * 100) / 2
    
    # 2. 돔의 표면적(m²) 계산 (출력용)
    #area_m2 = 2 * math.pi * ((diameter / 2) ** 2)
    try: 
        area_m2 = math.pi * (diameter**2)

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
        mass_weight_kg = mass_kg * MARS_GRAVITY_RATIO
    except Exception:
        raise Exception

    return area_m2, mass_weight_kg
# --- 메인 프로그램 실행 부분 ---
def main():
    try:
        print("--- Mars 돔 구조물 설계 프로그램 ---")
        # 사용자로부터 재질, 지름, 두께를 순서대로 입력받습니다.
        try:
            diameter_input = input("돔의 지름(m)을 입력하세요: ").strip()
            diameter_input = float(diameter_input)
            if diameter_input <= 0:
                raise ValueError        
        except ValueError:
            raise ValueError

        material_input = input("재질을 입력하세요 (유리, 알루미늄, 탄소강): ").strip()
        if material_input not in DENSITY_MAP:
            raise ValueError
           
        try:
            thickness_input = input("돔의 두께(cm)를 입력하세요 (기본값: 1, Enter 입력 시): ").strip()
            if thickness_input == '':
                thickness_cm = 1.0  # 입력이 없으면 기본값 1.0 사용
            else:
                try:
                    thickness_cm = float(thickness_input)
                except ValueError:
                    raise ValueError
                if thickness_cm <= 0:
                    raise ValueError
        except ValueError:
            raise ValueError
    
    # --- try-except 문을 사용한 예외 처리 ---
    
        # 1. 핵심 계산 함수 호출
        #    잘못된 재질, 지름, 두께가 입력되면 이 함수가 ValueError를 발생시키고,
        #    아래 except 블록에서 처리됩니다.
        area, w = sphere_area(diameter_input, material_input, thickness_cm)
        # 4. 결과 출력
        print("\n[계산 결과]")
        print(f"재질 : {material_input}, 지름 : {diameter_input:g}, 두께 : {thickness_cm:g}, "
              f"면적 : {area:.3f}, 무게 : {w:.3f} kg")

    except ValueError as e:
        # 잘못된 입력에 대한 모든 오류를 여기서 처리합니다.
        print("Invalid input")

    except Exception as e:
        print(f"Processing error: {e}")

# 이 스크립트가 메인으로 실행될 때만 main() 함수를 호출합니다.
if __name__ == "__main__":
    main()