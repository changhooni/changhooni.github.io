
'''
파이는 수학 내장함수 사용
area_m2 = math.pi * (diameter ** 2)
area_cm2 = area_m2 * 10000
volume_cm3 = area_cm2 * thickness
density = density_map[material]
mass_kg = density * volume_cm3 / 1000
mass_weight_kg = mass_kg * 0.38

print("Invalid input.")

print("Processing error.")

유리: 2.4 
알루미늄: 2.7
탄소강: 7.85

print(f"재질 : {재질값}, 지름 : {지름값}, 두께 : {두께값}, "면적 : {area:.3f}, 무게 : {w:.3f} kg")

                
def sphere_area(diameter: float, material: str, thickness: float=1) -> tuple[float, float]:
위 함수 무조건 사용

if __name__ == "__main__":
    main()

메인에서 처리
'''
import math

dem = {
    "유리": 2.4,
    "알루미늄": 2.7,
    "탄소강": 7.85
}

def sphere_area(diameter: float, material: str, thickness: float=1) -> tuple[float, float]:
    if material not in dem:
        raise ValueError
    if diameter <= 0:
        raise ValueError
    if thickness <= 0:
        raise ValueError

    if thickness == '':
        thickness = 1.0
    else:
        try:
            thickness = float(thickness)
        except:
            raise ValueError 
        
    try:
        area_m2 = math.pi * (diameter ** 2)
        area_cm2 = area_m2 * 10000
        volume_cm3 = area_cm2 * thickness
        density = dem[material]
        mass_kg = density * volume_cm3 / 1000
        mass_weight_kg = mass_kg * 0.38
        return area_m2, mass_weight_kg      
    except Exception:
        Exception


def main():
    try:
        try:
            diameter_input = input("돔의 지름(m)을 입력하세요: ").strip() 
            diameter = float(diameter_input)
            if diameter <= 0:
                raise ValueError
        except ValueError:
            raise ValueError
        
        material_input = input("재질을 입력하세요 (유리, 알루미늄, 탄소강): ").strip()
        if material_input not in dem:
            raise ValueError
        
        try:
            thickness_input = input("돔의 두께(cm)를 입력하세요 (기본값: 1, Enter 입력 시): ").strip()
            if thickness_input == '':
                thickness_cm = 1.0
            else:
                try:
                    thickness_cm = float(thickness_input)
                except ValueError:
                    raise ValueError
                if thickness_cm <= 0:
                    raise ValueError
        except ValueError:
            raise ValueError
        
        area, w = sphere_area(diameter, material_input, thickness_cm)
        print(f"재질 : {material_input}, 지름 : {diameter}, 두께 : {thickness_cm}, 면적 : {area:.3f}, 무게 : {w:.3f} kg")

    except ValueError:
        print("Invalid input.")
    except Exception:
        print("Processing error.")    

    
if __name__ == "__main__":
    main()

