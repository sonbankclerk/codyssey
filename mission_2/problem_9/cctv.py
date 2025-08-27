# cctv.py
# CCTV.zip 파일의 압축을 풀고, 내부 이미지들을 보여주는 뷰어 스크립트

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

    # 압축 해제할 폴더가 이미 있는지 확인
    if os.path.exists(extract_folder):
        print(f"'{extract_folder}' 폴더가 이미 존재합니다. 압축 해제를 건너뜁니다.")
        return True

    # ZIP 파일이 있는지 확인
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

def show_cctv_images():
    """
    'CCTV' 폴더의 이미지들을 창에 띄우고, 키보드로 제어합니다.
    """
    image_folder = 'CCTV'
    
    # 이미지 파일 목록 가져오기 (jpg, png 등)
    image_files = glob.glob(os.path.join(image_folder, '*.[jJ][pP][gG]')) + \
                  glob.glob(os.path.join(image_folder, '*.[pP][nN][gG]'))
    
    # 파일 이름순으로 정렬
    image_files.sort()

    if not image_files:
        print(f"'{image_folder}' 폴더에서 이미지를 찾을 수 없습니다.")
        return

    current_index = 0
    window_name = 'CCTV Viewer'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL) # 창 크기 조절 가능하도록 설정

    print("\n--- CCTV 뷰어 ---")
    print("→ : 다음 사진")
    print("← : 이전 사진")
    print("ESC : 종료")
    print("-----------------")

    while True:
        # 현재 인덱스의 이미지 읽기
        image_path = image_files[current_index]
        image = cv2.imread(image_path)

        if image is None:
            print(f"이미지 파일을 불러올 수 없습니다: {image_path}")
            # 다음 이미지로 자동 이동
            current_index = (current_index + 1) % len(image_files)
            continue
        
        # 창에 이미지 파일 경로 표시
        cv2.putText(image, os.path.basename(image_path), (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow(window_name, image)

        # 키보드 입력 대기 (waitKeyEx로 특수키 입력 받기)
        key = cv2.waitKeyEx(0)

        if key == 27: # ESC 키
            break
        elif key == 2555904: # 오른쪽 화살표 키
            current_index = (current_index + 1) % len(image_files)
        elif key == 2424832: # 왼쪽 화살표 키
            current_index = (current_index - 1 + len(image_files)) % len(image_files)

    # 모든 창 닫기
    cv2.destroyAllWindows()
    print("CCTV 뷰어를 종료합니다.")


if __name__ == '__main__':
    # 1. CCTV 파일 압축 해제
    if unzip_cctv_files():
        # 2. 이미지 뷰어 실행
        show_cctv_images()
