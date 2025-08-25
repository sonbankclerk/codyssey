import math

# 밀도 데이터 (g/cm³)
densities = {
    '유리': 2.4,
    '알루미늄': 2.7,
    '탄소강': 7.85
}

# 화성의 중력 (지구의 중력에 비해 약 0.38배)
gravity_factor = 0.38

def sphere_area(diameter, material='유리', thickness=1):
    radius = diameter / 2

    # 면적 (반구의 표면적)
    area = round(3 * math.pi * (radius ** 2), 3)

    # 부피 (반구의 부피)
    volume = round((2 / 3) * math.pi * (radius ** 3), 3)

    # 밀도 가져오기
    density = densities.get(material, 2.4)  # 기본값은 유리

    # 무게 계산 (g)
    weight = density * volume

    # 화성 중력을 반영한 무게 계산 (g)
    marsWeight = weight * gravity_factor

    return area, marsWeight  # 면적과 무게 반환
