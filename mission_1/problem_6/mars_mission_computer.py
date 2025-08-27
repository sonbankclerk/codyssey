# mars_mission_computer.py
import random


class DummySensor:
    def __init__(self):
        # 환경 값들을 저장할 딕셔너리
        self.env_values = {
            "mars_base_internal_temperature": None,     # 내부 온도
            "mars_base_external_temperature": None,     # 외부 온도
            "mars_base_internal_humidity": None,        # 내부 습도
            "mars_base_external_illuminance": None,     # 외부 광량
            "mars_base_internal_co2": None,             # 내부 CO2 농도
            "mars_base_internal_oxygen": None           # 내부 O2 농도
        }

    def set_env(self):
        """랜덤 범위 내에서 센서 값들을 생성"""
        self.env_values["mars_base_internal_temperature"] = round(random.uniform(18, 30), 2)
        self.env_values["mars_base_external_temperature"] = round(random.uniform(0, 21), 2)
        self.env_values["mars_base_internal_humidity"] = round(random.uniform(50, 60), 2)
        self.env_values["mars_base_external_illuminance"] = round(random.uniform(500, 715), 2)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 4)   # 소수 4자리까지
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    def get_env(self):
        """현재 센서 값들을 반환"""
        return self.env_values


if __name__ == "__main__":
    # 인스턴스 생성
    ds = DummySensor()

    # 환경값 세팅
    ds.set_env()

    # 환경값 출력
    print(ds.get_env())
