import os
from calculator import sphere_area  # 계산 함수 임포트

def get_material():
    while True:
        material = input("재질을 입력하세요 (유리, 알루미늄, 탄소강, 종료: 'exit'): ") or '유리'
        if material == 'exit':
            return None  # 종료
        if material not in ['유리', '알루미늄', '탄소강']:
            print("잘못된 재질입니다. 유리, 알루미늄, 탄소강 중에서 선택하세요.")
        else:
            return material


def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("양의 실수를 입력해주세요. 다시 시도해주세요.")
            else:
                return value
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")


def calculate_area_and_weight():
    # 재질 입력
    material = get_material()
    if material is None:
        return False  # 종료

    # 지름 입력
    diameter = get_positive_float("지름을 입력하세요 (m): ")

    # 두께 입력 (기본값: 1cm)
    thickness = get_positive_float("두께를 입력하세요 (cm, 기본값 1cm): ") or 1

    # 계산
    area, mars_weight = sphere_area(diameter, material, thickness)

    # 결과 출력 (소수점 3자리까지)
    print(f'재질 =⇒ {material}, 지름 =⇒ {diameter}m, 두께 =⇒ {thickness}cm, 면적 =⇒ {area}㎡, 무게 =⇒ {mars_weight:.3f}g')

    return True  # 계속 계산할지 묻기


def main():
    print("--- 반구 돔 계산기 ---")
    while True:
        # 반복적으로 계산을 실행하고 결과를 출력하는 함수 호출
        continue_calculating = calculate_area_and_weight()

        if not continue_calculating:
            print("프로그램을 종료합니다.")
            break  # 종료

        # 다시 계산할지 묻기
        repeat = input("\n다시 계산하시겠습니까? (y/n): ").strip().lower()
        if repeat != 'y':
            print("프로그램을 종료합니다.")
            break  # 종료


if __name__ == "__main__":
    main()
