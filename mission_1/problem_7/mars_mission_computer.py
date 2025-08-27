# mars_mission_computer.py
import random
import json
import time


class DummySensor:
    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None
        }

    def set_env(self):
        """랜덤 범위 내에서 센서 값들을 생성"""
        self.env_values["mars_base_internal_temperature"] = round(random.uniform(18, 30), 2)
        self.env_values["mars_base_external_temperature"] = round(random.uniform(0, 21), 2)
        self.env_values["mars_base_internal_humidity"] = round(random.uniform(50, 60), 2)
        self.env_values["mars_base_external_illuminance"] = round(random.uniform(500, 715), 2)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 4)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    def get_env(self):
        """현재 센서 값 반환"""
        return self.env_values


class MissionComputer:
    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None
        }
        # DummySensor 인스턴스화
        self.ds = DummySensor()

    def get_sensor_data(self):
        """센서 데이터를 5초마다 갱신하고 JSON 형태로 출력"""
        while True:
            # 센서 값 갱신
            self.ds.set_env()
            self.env_values = self.ds.get_env()

            # JSON 형태로 출력 (indent=4로 보기 좋게)
            print(json.dumps(self.env_values, ensure_ascii=False, indent=4))

            # 5초 대기
            time.sleep(5)


if __name__ == "__main__":
    # MissionComputer 인스턴스 생성
    RunComputer = MissionComputer()

    # 센서 데이터 지속적으로 출력
    RunComputer.get_sensor_data()
