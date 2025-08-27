# cctv.py
# CCTV.zip 파일의 압축을 풀고, 이미지 속에서 사람을 찾아 보여주는 스크립트

import zipfile
import os
import glob
import cv2

def unzip_cctv_files():
    """
    'CCTV.zip' 파일이 있으면 'CCTV' 폴더에 압축을 해제합니다.
    """
    zip_filename = 'CCTV.zip'
    extract_folder = 'CCTV'

    if os.path.exists(extract_folder):
        print(f"'{extract_folder}' 폴더가 이미 존재합니다. 압축 해제를 건너뜁니다.")
        return True

    if not os.path.exists(zip_filename):
        print(f"'{zip_filename}'을 찾을 수 없습니다. 스크립트와 같은 위치에 파일을 두세요.")
        return False

    try:
        print(f"'{zip_filename}' 파일의 압축을 해제합니다...")
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
        print(f"✅ 압축 해제 완료. 파일들이 '{extract_folder}' 폴더에 저장되었습니다.")
        return True
    except Exception as e:
        print(f"[오류] 압축 해제 중 문제가 발생했습니다: {e}")
        return False

def find_people_in_cctv():
    """
    'CCTV' 폴더의 이미지를 순차적으로 검색하여 사람이 인식되면 화면에 출력합니다.
    """
    image_folder = 'CCTV'
    
    # 이미지 파일 목록 가져오기 (jpg, png 등, 대소문자 구분 없이)
    image_files = glob.glob(os.path.join(image_folder, '*.[jJ][pP][gG]')) + \
                  glob.glob(os.path.join(image_folder, '*.[pP][nN][gG]'))
    image_files.sort()

    if not image_files:
        print(f"'{image_folder}' 폴더에서 이미지를 찾을 수 없습니다.")
        return

    # OpenCV에 내장된 HOG 기술을 이용한 보행자 탐지기 초기화
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    window_name = 'CCTV Person Detector'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    print("\n--- CCTV 사람 탐지기 ---")
    print("사람이 탐지되면 이미지가 표시됩니다.")
    print("Enter : 다음 탐지된 사진으로 이동")
    print("ESC : 종료")
    print("-------------------------")
    print("탐색을 시작합니다...")

    for image_path in image_files:
        image = cv2.imread(image_path)
        if image is None:
            print(f"이미지 파일을 읽을 수 없습니다: {os.path.basename(image_path)}")
            continue

        # 사람 탐지 (detectMultiScale: 이미지에서 여러 크기의 객체 탐지)
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

        # 사람이 한 명이라도 탐지되면
        if len(rects) > 0:
            print(f"-> 사람이 탐지되었습니다: {os.path.basename(image_path)}")
            
            # 탐지된 사람 주위에 사각형 그리기
            for (x, y, w, h) in rects:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow(window_name, image)

            # Enter 또는 ESC 키를 누를 때까지 대기
            while True:
                # waitKeyEx()를 사용하여 Enter, ESC 등 특수 키 입력을 받음
                key = cv2.waitKeyEx(0)
                
                if key == 13:  # Enter 키
                    break
                elif key == 27: # ESC 키
                    cv2.destroyAllWindows()
                    print("사용자에 의해 탐색이 중단되었습니다.")
                    return
            
    cv2.destroyAllWindows()
    print("\n모든 사진의 검색이 끝났습니다.")

if __name__ == '__main__':
    if unzip_cctv_files():
        find_people_in_cctv()
