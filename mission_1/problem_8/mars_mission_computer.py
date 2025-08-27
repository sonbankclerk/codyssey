# mars_mission_computer.py
import random
import json
import time
import platform
import psutil


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

            # JSON 형태로 출력
            print(json.dumps(self.env_values, ensure_ascii=False, indent=4))

            # 5초 대기
            time.sleep(5)

    def get_mission_computer_info(self):
        """미션 컴퓨터의 시스템 정보 JSON 출력"""
        info = {
            "Operating System": platform.system(),
            "OS Version": platform.version(),
            "CPU Type": platform.processor(),
            "CPU Cores": psutil.cpu_count(logical=True),
            "Memory Size (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2)
        }
        print(json.dumps(info, ensure_ascii=False, indent=4))
        return info

    def get_mission_computer_load(self):
        """미션 컴퓨터의 부하 정보 JSON 출력"""
        load = {
            "CPU Usage (%)": psutil.cpu_percent(interval=1),
            "Memory Usage (%)": psutil.virtual_memory().percent
        }
        print(json.dumps(load, ensure_ascii=False, indent=4))
        return load


if __name__ == "__main__":
    # MissionComputer 인스턴스 생성
    runComputer = MissionComputer()

    # 시스템 정보 출력
    print("=== Mission Computer Info ===")
    runComputer.get_mission_computer_info()

    # 부하 정보 출력
    print("=== Mission Computer Load ===")
    runComputer.get_mission_computer_load()
