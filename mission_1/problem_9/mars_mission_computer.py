# mars_mission_computer.py
import random
import json
import time
import platform
import psutil
import threading
import multiprocessing


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
        self.ds = DummySensor()

    def get_sensor_data(self):
        """센서 데이터를 5초마다 갱신하고 JSON 형태로 출력"""
        while True:
            self.ds.set_env()
            self.env_values = self.ds.get_env()
            print("\n=== Sensor Data ===")
            print(json.dumps(self.env_values, ensure_ascii=False, indent=4))
            time.sleep(5)

    def get_mission_computer_info(self):
        """20초마다 시스템 정보 출력"""
        while True:
            info = {
                "Operating System": platform.system(),
                "OS Version": platform.version(),
                "CPU Type": platform.processor(),
                "CPU Cores": psutil.cpu_count(logical=True),
                "Memory Size (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2)
            }
            print("\n=== Mission Computer Info ===")
            print(json.dumps(info, ensure_ascii=False, indent=4))
            time.sleep(20)

    def get_mission_computer_load(self):
        """20초마다 시스템 부하 출력"""
        while True:
            load = {
                "CPU Usage (%)": psutil.cpu_percent(interval=1),
                "Memory Usage (%)": psutil.virtual_memory().percent
            }
            print("\n=== Mission Computer Load ===")
            print(json.dumps(load, ensure_ascii=False, indent=4))
            time.sleep(20)


# ---------------------------
# 멀티쓰레드 실행
# ---------------------------
def run_with_threads():
    runComputer = MissionComputer()

    t1 = threading.Thread(target=runComputer.get_mission_computer_info)
    t2 = threading.Thread(target=runComputer.get_mission_computer_load)
    t3 = threading.Thread(target=runComputer.get_sensor_data)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


# ---------------------------
# 멀티프로세스 실행
# ---------------------------
def run_with_processes():
    runComputer1 = MissionComputer()
    runComputer2 = MissionComputer()
    runComputer3 = MissionComputer()

    p1 = multiprocessing.Process(target=runComputer1.get_mission_computer_info)
    p2 = multiprocessing.Process(target=runComputer2.get_mission_computer_load)
    p3 = multiprocessing.Process(target=runComputer3.get_sensor_data)

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()


if __name__ == "__main__":
    print("=== 멀티쓰레드 실행 ===")
    # run_with_threads()

    print("=== 멀티프로세스 실행 ===")
    run_with_processes()
