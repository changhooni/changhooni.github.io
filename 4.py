
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

print(f"재질 : {재질값}, 지름 : {지름값}, 두께 : {두께값}, "
                f"면적 : {area:.3f}, 무게 : {w:.3f} kg")

                
def sphere_area(diameter: float, material: str, thickness: float=1) -> tuple[float, float]:
위 함수 무조건 사용

if __name__ == "__main__":
    main()

메인에서 처리
'''
