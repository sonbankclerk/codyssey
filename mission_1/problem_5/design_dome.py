import numpy as np

# 두 번째 컬럼(strength 값)만 읽기
arr1 = np.loadtxt('mars_base_main_parts-001.csv', delimiter=',', skiprows=1, usecols=1)
arr2 = np.loadtxt('mars_base_main_parts-002.csv', delimiter=',', skiprows=1, usecols=1)
arr3 = np.loadtxt('mars_base_main_parts-003.csv', delimiter=',', skiprows=1, usecols=1)

# 3개의 배열을 하나로 합치기
parts = np.concatenate([arr1, arr2, arr3])

# 각 항목의 값이 곧 평균값 (단일 값이므로)
mean_values = parts

# 평균값이 50보다 작은 값들을 찾기
parts_to_work_on = parts[mean_values < 50]

# CSV 파일로 저장 (1차원 배열을 2차원으로 변환해서 저장)
np.savetxt('parts_to_work_on.csv', parts_to_work_on.reshape(-1, 1), delimiter=',', fmt='%.0f')